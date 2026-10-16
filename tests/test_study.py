import ai
import study


def setup_function():
    study.modes.clear()
    study.last.clear()


def test_기본_모드는_lunch():
    assert study.get_mode(111) == "lunch"


def test_모드를_바꾸면_기억한다():
    study.set_mode(111, "study")
    assert study.get_mode(111) == "study"
    study.set_mode(111, "lunch")
    assert study.get_mode(111) == "lunch"


def test_대화방마다_따로_기억한다():
    study.set_mode(111, "study")
    assert study.get_mode(222) == "lunch"


def test_질문에_답하고_응용_안내를_덧붙인다(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "fake")
    output = study.study_answer(111, "git commit이 뭐야?")
    assert output.startswith(ai.FAKE_ANSWER)
    assert "응용" in output


def test_질문할_때는_응용버전을_먼저_말하지_않는다():
    assert "응용버전은 사용자가 따로 요청할 때만" in study.STUDY_SYSTEM_PROMPT


def test_응용이라고_하면_마지막_질문으로_응용버전을_묻는다(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "fake")
    calls = []

    def fake_ask(system, user_text):
        calls.append((system, user_text))
        return "답"

    monkeypatch.setattr(ai, "ask_ai", fake_ask)
    study.study_answer(111, "git commit이 뭐야?")
    study.study_answer(111, "응용")
    system, user_text = calls[-1]
    assert system == study.APPLY_SYSTEM_PROMPT
    assert "git commit이 뭐야?" in user_text


def test_질문_전에_응용이라고_하면_먼저_질문하라고_한다():
    assert study.study_answer(111, "응용") == study.NO_QUESTION


def test_응용은_대화방마다_따로_기억한다(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "fake")
    study.study_answer(111, "git commit이 뭐야?")
    assert study.study_answer(222, "응용") == study.NO_QUESTION


def test_지침에_공부_주제가_들어_있다():
    for word in ("git", "터미널", "파이썬"):
        assert word in study.STUDY_SYSTEM_PROMPT
