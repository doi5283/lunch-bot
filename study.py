"""개발 공부 도우미 — git · 터미널 · 파이썬을 쉬운 말로 설명한다.

- /study 로 공부 모드, /lunchmode 로 점심 모드. 모드는 대화방(chat_id)마다 따로 기억한다
- 모드는 메모리에만 저장하므로 서버를 다시 켜면 점심 모드로 돌아간다
- 확인: uv run pytest tests/test_study.py
"""

import ai

STUDY_SYSTEM_PROMPT = (
    "너는 개발을 막 배우기 시작한 입문자를 돕는 공부 도우미 봇이다. 한국어로 답한다.\n"
    "규칙:\n"
    "- git, 터미널(명령어), 파이썬에 대한 질문에만 답한다. 다른 주제는 "
    "\"저는 git, 터미널, 파이썬만 도와드려요\"라고 정중히 말한다.\n"
    "- 개발 공부 1주차 학생이 이해할 수 있게 최대한 쉬운 말로 설명한다.\n"
    "- 처음 나오는 용어는 한 줄로 풀어서 설명한다.\n"
    "- 짧게 답하고, 따라 칠 수 있는 예시 명령어나 코드를 하나 보여 준다.\n"
    "- 확실하지 않은 내용은 지어내지 않고 모른다고 말한다."
)

modes = {}  # {chat_id: "study" 또는 "lunch"}


def set_mode(chat_id, mode):
    """대화방(chat_id)의 모드를 "study" 또는 "lunch"로 바꾼다."""
    modes[chat_id] = mode


def get_mode(chat_id):
    """대화방의 지금 모드. 정한 적이 없으면 "lunch"."""
    return modes.get(chat_id, "lunch")


def study_answer(question):
    """공부 질문을 공부 도우미 지침과 함께 AI에게 묻고 답 글자를 돌려준다."""
    return ai.ask_ai(STUDY_SYSTEM_PROMPT, question)
