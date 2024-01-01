from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from bot.bot_messages import *
from bot.telegram.callback_data import *
from tests.base_test import BaseTest


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

def get_tests_menu(tests: list[BaseTest]) -> InlineKeyboardMarkup:
    """ Создает меню выбора тестов для прохождения. """
    menu = list()

    for test in tests:
        menu.append([
            InlineKeyboardButton(test.name, callback_data=test.short_name)
        ])

    return InlineKeyboardMarkup(menu)