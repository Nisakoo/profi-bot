from bot.raw_messages import *


def start_message() -> str:
    return START_MESSAGE

def stop_prof_test_message(test_short_name: str) -> str:
    return STOP_PROF_TEST_MESSAGE.format(test_short_name=test_short_name)

def good_feedback_message() -> str:
    return GOOD_FEEDBACK_MESSAGE

def bad_feedback_message() -> str:
    return BAD_FEEDBACK_MESSAGE

def feedback_thanks_message() -> str:
    return FEEDBACK_THANKS_MESSAGE

def error_occur_message() -> str:
    return ERROR_OCCUR_MESSAGE