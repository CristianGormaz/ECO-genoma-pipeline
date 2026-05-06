import json
from pathlib import Path

MATRIX = Path("docs/architecture/eco-synthetic-signal-matrix.json")
GUIDE = Path("docs/operations/eco-synthetic-signal-matrix.md")


def test_signal_matrix_contract():
    payload = json.loads(MATRIX.read_text(encoding="utf-8"))
    assert payload["classification"] == "allowed"
    assert "datos sintéticos" in payload["limit"]
    assert "sin entrenamiento" in payload["limit"]
    assert "sin datos sensibles" in payload["limit"]
    assert len(payload["signals"]) == 4


def test_signal_matrix_mentions_all_registered_demo_names():
    payload = json.loads(MATRIX.read_text(encoding="utf-8"))
    names = " ".join(signal["demo"] for signal in payload["signals"])
    assert "minimal simulation" in names
    assert "signal balance" in names
    assert "waste pressure" in names
    assert "absorption threshold" in names


def test_signal_matrix_markdown_matches_json():
    payload = json.loads(MATRIX.read_text(encoding="utf-8"))
    guide = GUIDE.read_text(encoding="utf-8")
    for signal in payload["signals"]:
        assert signal["demo"] in guide
        assert signal["observed_pattern"] in guide
    assert "sin afirmaciones biomédicas aplicadas" in guide
