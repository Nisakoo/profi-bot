from bot.constants.messages import *


def start_message() -> str:
    return START_MESSAGE

def start_prof_test_text() -> str:
    return START_PROF_TEST_TEXT

def start_prof_test_message(question: int, questions_count: int, question_content: str) -> str:
    return START_PROF_TEST_MESSAGE.format(
        question=question,
        questions_count=questions_count,
        question_content=question_content
    )

def prof_test_question_message(question: int, questions_count: int, question_content: str) -> str:
    return PROF_TEST_QUESTION_MESSAGE.format(
        question=question,
        questions_count=questions_count,
        question_content=question_content
    )

def prof_test_result_message(result_content: str) -> str:
    return PROF_TEST_RESULT_MESSAGE.format(
        result_content=result_content
    )

def stop_prof_test_message() -> str:
    return STOP_PROF_TEST_MESSAGE

def error_occur_message() -> str:
    return ERROR_OCCUR_MESSAGE