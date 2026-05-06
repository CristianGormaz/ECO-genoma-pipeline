from pathlib import Path

GUIDE = Path("docs/operations/eco-synthetic-demo-decision-guide.md")


def test_decision_guide_exists_and_mentions_demos():
    text = GUIDE.read_text(encoding="utf-8")
    assert "minimal simulation" in text
    assert "signal balance" in text
    assert "waste pressure" in text
    assert "absorption threshold" in text


def test_decision_guide_keeps_responsible_limits():
    text = GUIDE.read_text(encoding="utf-8").lower()
    assert "datos sintéticos" in text
    assert "sin entrenamiento" in text
    assert "datos sensibles" in text
    assert "afirmaciones biomédicas aplicadas" in text
