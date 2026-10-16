"""개발 공부 도우미 — git · 터미널 · 파이썬을 쉬운 말로 설명한다.

- /study 로 공부 모드, /lunchmode 로 점심 모드. 모드는 대화방(chat_id)마다 따로 기억한다
- 질문에 답한 뒤 "응용"이라고 하면 응용버전을 알려 준다 (대화방마다 마지막 질문·답을 기억)
- 기억은 메모리에만 저장하므로 서버를 다시 켜면 사라진다
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
    "- 응용버전은 사용자가 따로 요청할 때만 알려 준다. 먼저 꺼내지 않는다.\n"
    "- 확실하지 않은 내용은 지어내지 않고 모른다고 말한다."
)

APPLY_SYSTEM_PROMPT = (
    "너는 개발을 막 배우기 시작한 입문자를 돕는 공부 도우미 봇이다. 한국어로 답한다.\n"
    "사용자가 방금 한 질문과 네가 한 답을 아래에 준다. 그 내용의 응용버전을 알려 준다.\n"
    "규칙:\n"
    "- 방금 설명한 것을 조금 더 써먹는 방법(옵션, 비슷한 명령어, 실생활 예시 등)을 1~2개 알려 준다.\n"
    "- 개발 공부 1주차 학생이 이해할 수 있게 최대한 쉬운 말로 설명한다.\n"
    "- 처음 나오는 용어는 한 줄로 풀어서 설명한다.\n"
    "- 따라 칠 수 있는 예시 명령어나 코드를 함께 보여 준다.\n"
    "- 확실하지 않은 내용은 지어내지 않고 모른다고 말한다."
)

APPLY_WORD = "응용"
ASK_APPLY = f"\n\n응용버전을 원하시면 '{APPLY_WORD}'이라고 말해주세요."
NO_QUESTION = "먼저 git, 터미널, 파이썬 질문을 해주세요. 그 다음에 '응용'이라고 하면 응용버전을 알려드려요."

modes = {}  # {chat_id: "study" 또는 "lunch"}
last = {}   # {chat_id: (마지막 질문, 마지막 답)}


def set_mode(chat_id, mode):
    """대화방(chat_id)의 모드를 "study" 또는 "lunch"로 바꾼다."""
    modes[chat_id] = mode


def get_mode(chat_id):
    """대화방의 지금 모드. 정한 적이 없으면 "lunch"."""
    return modes.get(chat_id, "lunch")


def study_answer(chat_id, text):
    """공부 모드에서 받은 글자(text)에 답한다.

    - text가 "응용"이면: 이 대화방의 마지막 질문·답을 바탕으로 응용버전을 알려 준다 (없으면 NO_QUESTION)
    - 아니면: 질문으로 보고 답한 뒤 "응용이라고 말해주세요" 안내를 덧붙인다. 질문과 답은 기억해 둔다
    """
    if text.strip() == APPLY_WORD:
        if chat_id not in last:
            return NO_QUESTION
        question, answer = last[chat_id]
        return ai.ask_ai(APPLY_SYSTEM_PROMPT, f"사용자의 질문: {question}\n네가 한 답: {answer}")

    answer = ai.ask_ai(STUDY_SYSTEM_PROMPT, text)
    last[chat_id] = (text, answer)
    return answer + ASK_APPLY
