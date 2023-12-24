from telegram import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update
)

from telegram.constants import ChatAction

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from neural_network.base_neural_network import BaseNeuralNetwork
from db.base_database import BaseDataBase
from bot.base_bot import BaseBot

from bot.telegram.decorators import *
from bot.constants.bot_messages import *
from bot.constants.telegram.keyboards import *
from bot.constants.telegram.callback_data import *
from bot.constants.telegram.conversation import *

from cache_storage.cache_storage import CacheStorage


class TelegramBot(BaseBot):
    def __init__(self, token: str, neural_network: BaseNeuralNetwork, db: BaseDataBase) -> None:
        super().__init__(token, neural_network, db)

        self._create_app()
        self._add_handlers()

        self._data = CacheStorage()

    def run(self) -> None:
        self._app.run_polling()

    def _create_app(self) -> None:
        self._app = ApplicationBuilder().token(self._token).build()

    def _add_handlers(self) -> None:
        prof_test_conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler("test", self._start_prof_test),
                CallbackQueryHandler(
                    self._start_prof_test_callback,
                    pattern=f"^{START_PROF_TEST_CD}$"
                )
            ],
            states={
                QUESTION_STATE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self._prof_test_question)
                ]
            },
            fallbacks=[
                CommandHandler("stop", self._prof_test_stop),
                CommandHandler("restart", self._prof_test_restart)
            ]
        )

        self._app.add_handler(CommandHandler(["start", "hello", "help", "about"], self._start))
        self._app.add_handler(CallbackQueryHandler(
            self._feedback_callback,
            pattern="|".join([
                QUESTION_GOOD_FEEDBACk_CD,
                QUESTION_BAD_FEEDBACk_CD,
                RESULT_GOOD_FEEDBACk_CD,
                RESULT_BAD_FEEDBACk_CD
            ])
        ))
        self._app.add_handler(prof_test_conv_handler)

    @typing_status
    @send_user_error_message
    async def _feedback_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """ Записывает отзыв пользователя на сообщение бота в базу данных. """
        query = update.callback_query

        await query.answer()
        await query.edit_message_reply_markup(None)
        await update.effective_user.send_message(feedback_thanks_message())

        await self._db.insert(
            user_id=update.effective_user.id,
            event=query.data,
            message=query.message.text
        )

    @typing_status
    @send_user_error_message
    @write_event_to_db("start_test")
    async def _start_prof_test(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """ Начало профориентационного теста. """
        user = update.effective_user
        
        self._data.create(user.id)
        response = await self._neural_network.ask_question(self._data.get_messages(user.id))
        self._data.add_message(user.id, self._neural_network.agent_msg(response))

        await user.send_message(start_prof_test_message(
            self._data.get_question_number(user.id),
            QUESTIONS_COUNT,
            response,
        ), reply_markup=QUESTION_FEEDBACK_KEYBOARD)
        self._data.next_question(user.id)

        return QUESTION_STATE

    @send_user_error_message
    async def _start_prof_test_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """ Обработчик кнопки начала профориентационного теста. """
        await update.callback_query.answer()
        return await self._start_prof_test(update, context)
    
    @typing_status
    @send_user_error_message
    @write_event_to_db("ask_question")
    async def _prof_test_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """ Обработчик ответов пользователя во время профориентационного теста. """
        user = update.effective_user
        user_answer = update.effective_message.text

        self._data.add_message(user.id, self._neural_network.user_msg(user_answer))

        if self._data.get_question_number(user.id) > QUESTIONS_COUNT:
            return await self._prof_test_result(update, context)
        
        response = await self._neural_network.ask_question(self._data.get_messages(user.id))
        self._data.add_message(user.id, self._neural_network.agent_msg(response))

        await user.send_message(prof_test_question_message(
            self._data.get_question_number(user.id),
            QUESTIONS_COUNT,
            response
        ), reply_markup=QUESTION_FEEDBACK_KEYBOARD)
        self._data.next_question(user.id)

        return QUESTION_STATE
    
    @typing_status
    @send_user_error_message
    @write_event_to_db("stop_test")
    async def _prof_test_stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """ Обработчик команды /stop - останавливает профориентационный тест. """
        await update.effective_user.send_message(stop_prof_test_message())
        return await self._prof_test_end(update, context)
    
    @send_user_error_message
    @write_event_to_db("restart_test")
    async def _prof_test_restart(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """ Обработчик команды /restart - перезапускает профориентационный тест. """
        await self._prof_test_end(update, context)
        return await self._start_prof_test(update, context)
    
    @typing_status
    @send_user_error_message
    @write_event_to_db("show_test_result")
    async def _prof_test_result(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """ Вывод результат профориентационного теста. """
        user = update.effective_user

        response = await self._neural_network.ask_result(self._data.get_messages(user.id))
        await user.send_message(
            prof_test_result_message(response),
            reply_markup=RESULT_FEEDBACK_KEYBOARD
        )

        return await self._prof_test_end(update, context)
    
    @send_user_error_message
    async def _prof_test_end(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """ Метод для правильного завершения профориентационно теста. """
        del self._data[update.effective_user.id]
        return ConversationHandler.END

    @typing_status
    @send_user_error_message
    @write_event_to_db("show_start_message")
    async def _start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """ Обработчик команд: start, hello, help """
        await update.effective_user.send_message(
            start_message(),
            reply_markup=START_KEYBOARD
        )