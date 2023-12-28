from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from bot.bot_messages import *
from bot.telegram.callback_data import *


def get_question_feedback_keyboard(id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    good_feedback_message(),
                    callback_data=QUESTION_GOOD_FEEDBACk_CD.format(id=id)
                ),
                InlineKeyboardButton(
                    bad_feedback_message(),
                    callback_data=QUESTION_BAD_FEEDBACk_CD.format(id=id)
                )
            ]
        ]
    )


def get_reuslt_feedback_keyboard(id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    good_feedback_message(),
                    callback_data=RESULT_GOOD_FEEDBACk_CD.format(id=id)
                ),
                InlineKeyboardButton(
                    bad_feedback_message(),
                    callback_data=RESULT_BAD_FEEDBACk_CD.format(id=id)
                )
            ]
        ]
    )