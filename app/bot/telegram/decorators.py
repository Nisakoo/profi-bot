from functools import wraps

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from bot.bot_messages import *


def typing_status(func):
    """ Ставит статус "печатает...". """

    @wraps(func)
    async def inner(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.effective_chat.send_action(ChatAction.TYPING)
        return await func(self, update, context)
    
    return inner

def send_user_error_message(func):
    """ В случае ошибки во время выполнения, отправляет пользователю сообщение об ошибке. """

    @wraps(func)
    async def inner(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            return await func(self, update, context)
        except Exception as e:
            print(e)
            await update.effective_chat.send_message(error_occur_message())
            await self._prof_test_end(update, context)

    return inner

def write_event(event: str):
    """ Записывает события в базу данных. """

    def decorator(func):

        @wraps(func)
        async def inner(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            nonlocal event

            if type(self).__name__ == "TelegramTestAdapter":
                event = f"{self._test.short_name}_{event}"

            await self._db.insert(
                user_id=update.effective_user.id,
                event=event,
                message=""
            )
            return await func(self, update, context)
    
        return inner
    return decorator

def save_data(func):
    """ Сохраняет ответы пользователя в базу данных """

    @wraps(func)
    async def inner(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if self._save_data:
            await self._db.insert(
                user_id=update.effective_user.id,
                event=f"{self._test.short_name}_user_answer",
                message=update.effective_message.text
            )

        return await func(self, update, context)

    return inner