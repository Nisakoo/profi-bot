from functools import wraps

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


def typing_status(func):

    @wraps(func)
    async def inner(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.effective_chat.send_action(ChatAction.TYPING)
        return await func(self, update, context)
    
    return inner

def send_user_error_message(func):

    @wraps(func)
    async def inner(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            return await func(self, update, context)
        except Exception as e:
            print(e)
            await update.effective_chat.send_message(error_occur_message())

    return inner