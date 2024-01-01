import html
import json
import traceback
from functools import wraps
from collections.abc import Callable

from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update
)

from telegram.constants import ChatAction, ParseMode

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from db.base_database import BaseDataBase
from bot.base_bot import BaseBot

from bot.bot_messages import *
from bot.telegram.keyboards import *
from bot.telegram.callback_data import *

from tests.base_test import BaseTest


class TelegramBot(BaseBot):
    def __init__(self, token: str, tests: list[BaseTest], db: BaseDataBase, **kwargs) -> None:
        super().__init__(token, tests, db, **kwargs)

        self._tests_menu = get_tests_menu(self._tests)
        self._admin_id = kwargs["admin_id"]

        self._create_app()
        self._add_handlers()

    def run(self) -> None:
        self._app.run_polling()

    def _create_app(self) -> None:
        self._app = ApplicationBuilder().token(self._token).build()

        self._app.bot_data["db"] = self._db
        self._app.bot_data["tests_menu"] = self._tests_menu
        self._app.bot_data["admin_id"] = self._admin_id

    def _add_handlers(self) -> None:
        self._app.add_handler(CommandHandler(["start", "hello", "help", "about"], self._start))
        self._app.add_handler(CallbackQueryHandler(
            self._feedback_callback,
            pattern=CALLBACK_DATA_PATTERN
        ))

        for test in self._tests:
            self._app.add_handlers(
                [
                    CommandHandler(test.short_name, self._show_test_description(test)),
                    CallbackQueryHandler(self._show_test_description(test), pattern=f"^{test.short_name}$")
                ]
            )
            self._app.add_handler(
                ConversationHandler(
                    entry_points=[
                        CallbackQueryHandler(self._start_test(test), pattern=f"^start_{test.short_name}$")
                    ],
                    states={
                        1: [
                            MessageHandler(filters.TEXT & ~filters.COMMAND, self._test_message_handler(test))
                        ]
                    },
                    fallbacks=[
                        CommandHandler("stop", self._stop_test(test)),
                        CommandHandler("restart", self._restart_test(test))
                    ]
                )
            )
        self._app.add_error_handler(self._error_handler)

    @staticmethod
    def typing_status(func):
        """ Ставит статус "печатает...". """

        @wraps(func)
        async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.effective_chat.send_action(ChatAction.TYPING)
            return await func(update, context)
        
        return inner
    
    @staticmethod
    def write_event(base_event: str, test: BaseTest=None):
        """ Записывает события в базу данных. """

        def decorator(func):

            @wraps(func)
            async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE):
                nonlocal base_event

                event = base_event

                if not (test is None):
                    event = base_event + "_" + test.short_name

                await context.bot_data.get("db").insert(
                    user_id=update.effective_user.id,
                    event=event,
                    message=""
                )

                return await func(update, context)
        
            return inner
        return decorator
    
    @staticmethod
    def save_test_data(test: BaseTest):
        """ Сохраняет ответы пользователя в базу данных """

        def decorator(func):

            @wraps(func)
            async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
                if test.save_data:
                    await context.bot_data.get("db").insert(
                        user_id=update.effective_user.id,
                        event=f"{test.short_name}_user_answer",
                        message=update.effective_message.text
                    )

                return await func(update, context)

            return inner
        return decorator
    
    @staticmethod
    @typing_status
    async def _error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.effective_user.send_message(error_occur_message())

        # traceback.format_exception returns the usual python message about an exception, but as a
        # list of strings rather than a single string, so we have to join them together.
        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
        tb_string = "".join(tb_list)

        # Build the message with some markup and additional information about what happened.
        # You might need to add some logic to deal with messages longer than the 4096 character limit.
        update_str = update.to_dict() if isinstance(update, Update) else str(update)
        message = (
            "Произошла ошибка:\n"
            f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
            "</pre>\n\n"
            f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
            f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
            f"<pre>{html.escape(tb_string)}</pre>"
        )

        await context.bot.send_message(
            chat_id=context.bot_data.get("admin_id"), text=message, parse_mode=ParseMode.HTML
        )

    @staticmethod
    @typing_status
    @write_event("send_start_msg")
    async def _start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """ Обработчик команд: start, hello, help, about """
        await update.effective_user.send_message(
            start_message(),
            reply_markup=context.bot_data.get("tests_menu")
        )

    @staticmethod
    @typing_status
    async def _feedback_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """ Записывает отзыв пользователя на сообщение бота в базу данных. """
        query = update.callback_query

        await query.answer()
        await query.edit_message_reply_markup(None)
        await update.effective_user.send_message(feedback_thanks_message())

        await context.bot_data.get("db").insert(
            user_id=update.effective_user.id,
            event=query.data,
            message=query.message.text
        )

    @staticmethod
    def _show_test_description(test: BaseTest) -> Callable:
        """ Отображает описание теста. """

        @TelegramBot.typing_status
        @TelegramBot.write_event("show_test_desc", test)
        async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            user = update.effective_user

            if not (update.callback_query is None):
                await update.callback_query.answer()

            await user.send_message(
                test.description,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Начать", callback_data=f"start_{test.short_name}")]
                    ]
                )
            )
        
        return inner

    @staticmethod
    def _start_test(test: BaseTest) -> Callable:
        """ Обработчик entry_points. """

        question_feedback_keyboard = None

        if test.feedback:
            question_feedback_keyboard = get_question_feedback_keyboard(test.short_name)

        @TelegramBot.typing_status
        @TelegramBot.write_event("start_test", test)
        async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
            user = update.effective_user

            if not (update.callback_query is None):
                await update.callback_query.answer()

            test.start_test(user_id=user.id)

            await user.send_message(await test.next_question(
                user_id=user.id,
                message=""
            ), reply_markup=question_feedback_keyboard)

            return 1
        
        return inner
    
    @staticmethod
    def _end_test(test: BaseTest, user_id: int) -> int:
        """ Корректно завершает тест. """
        test.end_test(user_id=user_id)
        return ConversationHandler.END
    
    @staticmethod
    def _test_message_handler(test: BaseTest) -> Callable:
        """ Обрабатывает переход к следующему вопросу. """

        question_feedback_keyboard = None

        if test.feedback:
            question_feedback_keyboard = get_question_feedback_keyboard(test.short_name)

        @TelegramBot.typing_status
        @TelegramBot.write_event("user_message", test)
        @TelegramBot.save_test_data(test)
        async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
            user = update.effective_user

            if test.is_ended(user_id=user.id):
                await TelegramBot._show_test_result(test)(update, context)
                return TelegramBot._end_test(test, user.id)

            await user.send_message(
                await test.next_question(user_id=user.id, message=update.effective_message.text),
                reply_markup=question_feedback_keyboard
            )

            return 1
        
        return inner
    
    @staticmethod
    def _show_test_result(test: BaseTest) -> Callable:
        
        result_feedback_keyboard = None

        if test.feedback:
            result_feedback_keyboard = get_reuslt_feedback_keyboard(test.short_name)

        @TelegramBot.write_event("show_result", test)
        async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user = update.effective_user
            await user.send_message(
                await test.show_result(user_id=user.id, message=update.effective_message.text),
                reply_markup=result_feedback_keyboard
            )

        return inner
    
    @staticmethod
    def _stop_test(test: BaseTest) -> Callable:
        """ Обрабочтик /stop. """

        @TelegramBot.typing_status
        @TelegramBot.write_event("stop_test", test)
        async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
            await update.effective_user.send_message(stop_prof_test_message(test.short_name))
            return TelegramBot._end_test(test, update.effective_user.id)
        
        return inner
    
    @staticmethod
    def _restart_test(test: BaseTest) -> Callable:
        """ Обрабочтик /stop. """

        @TelegramBot.typing_status
        @TelegramBot.write_event("restart_test", test)
        async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
            TelegramBot._end_test(test, update.effective_user.id)
            return await TelegramBot._start_test(test)(update, context)
        
        return inner