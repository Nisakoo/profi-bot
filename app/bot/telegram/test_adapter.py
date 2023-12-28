from telegram import Update

from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from bot.telegram.decorators import *
from bot.bot_messages import *
from bot.telegram.keyboards import *

from tests.base_test import BaseTest
from db.base_database import BaseDataBase


class TelegramTestAdapter:
    def __init__(self, test: BaseTest, feedback: bool, save_data: bool, db: BaseDataBase) -> None:
        self._test = test
        self._feedback = feedback
        self._save_data = save_data
        self._db = db

        self._command = test.short_name
        self._callback_data = test.short_name

        self._QUESTION_STATE = 1
        self._QUESTION_FEEDBACK_KEYBOARD = get_question_feedback_keyboard(self._test.short_name)
        self._RESULT_FEEDBACK_KEYBOARD = get_reuslt_feedback_keyboard(self._test.short_name)

    def get_handler(self) -> ConversationHandler:
        """ Создает handler для Telegram для теста. """
        return ConversationHandler(
            entry_points=[
                CommandHandler(self._command, self._command_handler),
                CallbackQueryHandler(self._callback_handler, pattern=f"^{self._callback_data}$")
            ],
            states={
                self._QUESTION_STATE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self._message_handler)
                ]
            },
            fallbacks=[
                CommandHandler("stop", self._stop),
                CommandHandler("restart", self._restart)
            ]
        )
    
    @typing_status
    @send_user_error_message
    @write_event("start_test")
    async def _command_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """ Обработчик entry_points. """
        user = update.effective_user

        self._test.start_test(user_id=user.id)

        reply_markup = None

        if self._feedback:
            reply_markup = self._QUESTION_FEEDBACK_KEYBOARD

        await user.send_message(self._test.description)
        await user.send_message(await self._test.next_question(
            user_id=user.id,
            message=""
        ), reply_markup=reply_markup)

        return self._QUESTION_STATE

    @send_user_error_message
    async def _callback_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """ Обработчик entry_points. """
        await update.callback_query.answer()
        return await self._command_handler(update, context)
    
    @save_data
    @typing_status
    @send_user_error_message
    @write_event("user_message")
    async def _message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """ Обрабатывает переход к следующему вопросу. """
        user = update.effective_user

        if self._test.is_ended(user_id=user.id):
            return await self._show_result(update, context)
        
        reply_markup = None

        if self._feedback:
            reply_markup = self._QUESTION_FEEDBACK_KEYBOARD

        await user.send_message(
            await self._test.next_question(user_id=user.id, message=update.effective_message.text),
            reply_markup=reply_markup
        )

        return self._QUESTION_STATE

    @typing_status
    @send_user_error_message
    @write_event("show_result")
    async def _show_result(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """ Отображает результат теста. """
        user = update.effective_user
        reply_markup = None

        if self._feedback:
            reply_markup = self._RESULT_FEEDBACK_KEYBOARD

        await user.send_message(
            await self._test.show_result(user_id=user.id, message=update.effective_message.text),
            reply_markup=reply_markup
        )

        return await self._end_test(update, context)
    
    @typing_status
    @send_user_error_message
    @write_event("stop_test")
    async def _stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """ Останавливает тест. Результат не выводиться. """
        await update.effective_user.send_message(stop_prof_test_message(self._test.short_name))
        return await self._end_test(update, context)
    
    @send_user_error_message
    @write_event("restart_test")
    async def _restart(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """ Перезапуск теста. Результат не выводиться. """
        await self._end_test(update, context)
        return await self._command_handler(update, context)
    
    @send_user_error_message
    @write_event("end_test")
    async def _end_test(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """ Корректно завершает тест. """
        self._test.end_test(user_id=update.effective_user.id)
        return ConversationHandler.END
        