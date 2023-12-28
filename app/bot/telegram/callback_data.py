import re


RESULT_GOOD_FEEDBACk_CD = "{id}_result_good_feedback"
RESULT_BAD_FEEDBACk_CD = "{id}_result_bad_feedback"

QUESTION_GOOD_FEEDBACk_CD = "{id}_question_good_feedback"
QUESTION_BAD_FEEDBACk_CD = "{id}_question_bad_feedback"

CALLBACK_DATA_PATTERN = re.compile(r".+feedback$")