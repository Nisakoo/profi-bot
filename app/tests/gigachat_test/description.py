QUESTIONS_COUNT = 10
TEST_NAME = "Тест от GigaChat"
SHORT_NAME = "ai_test"
FEEDBACK = True
SAVE_DATA = False
TEST_DESCRIPTION = """Этот тест использует языковую модель GigaChat от Сбера. \
В ходе теста нейросеть задаст вам {questions_count} вопросов. \
Не бойтесь отвечать развернуто, а также не бойтесь отвечать «я не знаю».

Чтобы прервать тестирование напишите /stop, чтобы начать тест заново /restart"""

QUESTION_TEMPLATE = """{question}/{questions_count}. {question_content}"""
RESULT_TEMPLATE = """Тестирование завершено! \
Спасибо, что уделил мне время! Вот твой результат:

{result_content}

Согласен ли ты с результатом тестрирования?"""