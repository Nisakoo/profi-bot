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

from bot.constants.bot_messages import *
from bot.constants.telegram.callback_data import *


START_KEYBOARD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(
            start_prof_test_text(),
            callback_data=START_PROF_TEST_CD
        )]
    ]
)