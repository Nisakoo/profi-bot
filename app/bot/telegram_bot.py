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


class TelegramBot(BaseBot):
    def __init__(self, token: str, neural_network: BaseNeuralNetwork, db: BaseDataBase) -> None:
        super().__init__(token, neural_network, db)

        self._create_app()
        self._add_handlers()

    def run(self) -> None:
        self._app.run_polling()

    def _create_app(self) -> None:
        self._app = ApplicationBuilder().token(self._token).build()

    def _add_handlers(self) -> None:
        self._app.add_handler(CommandHandler(["start", "hello", "help"], self._start))

    async def _start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.effective_user.send_message("Hello, World!")