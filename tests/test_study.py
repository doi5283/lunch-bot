import ai
import study


def setup_function():
    study.modes.clear()


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


def test_fake_모드에서_고정_답을_돌려준다(monkeypatch):
    monkeypatch.setenv("AI_PROVIDER", "fake")
    assert study.study_answer("git commit이 뭐야?") == ai.FAKE_ANSWER


def test_지침에_공부_주제가_들어_있다():
    for word in ("git", "터미널", "파이썬"):
        assert word in study.STUDY_SYSTEM_PROMPT
