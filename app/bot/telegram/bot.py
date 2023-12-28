from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from db.base_database import BaseDataBase
from bot.base_bot import BaseBot

from bot.telegram.decorators import *
from bot.bot_messages import *
from bot.telegram.keyboards import *
from bot.telegram.callback_data import *

from bot.telegram.test_adapter import TelegramTestAdapter


class TelegramBot(BaseBot):
    def __init__(self, token: str, tests: list, db: BaseDataBase) -> None:
        super().__init__(token, tests, db)

        self._tests_menu = self._create_tests_menu()

        self._create_app()
        self._add_handlers()

    def run(self) -> None:
        self._app.run_polling()

    def _create_app(self) -> None:
        self._app = ApplicationBuilder().token(self._token).build()

    def _create_tests_menu(self) -> InlineKeyboardMarkup:
        """ Создает меню выбора тестов для прохождения. """
        return InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                    test["test"].name,
                    callback_data=test["test"].short_name
                )] for test in self._tests
            ]
        )

    def _add_handlers(self) -> None:
        self._app.add_handler(CommandHandler(["start", "hello", "help", "about"], self._start))
        self._app.add_handler(CallbackQueryHandler(
            self._feedback_callback,
            pattern=CALLBACK_DATA_PATTERN
        ))

        for test in self._tests:
            self._app.add_handler(
                TelegramTestAdapter(
                    test["test"], test["feedback"], test["save_data"], self._db
                ).get_handler()
            )

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
    @write_event("show_start_message")
    async def _start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """ Обработчик команд: start, hello, help, about """
        await update.effective_user.send_message(
            start_message(),
            reply_markup=self._tests_menu
        )