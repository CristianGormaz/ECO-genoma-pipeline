from pathlib import Path

DOC = Path("docs/operations/terminal-stop-guide.md")


def test_terminal_stop_guide_exists():
    assert DOC.exists()


def test_terminal_stop_guide_declares_safe_stop_rules():
    text = DOC.read_text(encoding="utf-8")

    required = [
        "Señal verde",
        "Señal amarilla",
        "Señal roja",
        "git status muestra árbol limpio",
        "pytest termina con passed",
        "No hagas commit ni merge",
        "no ejecuta entrenamiento",
        "no cambia baseline",
        "no recalibra umbrales",
    ]

    for phrase in required:
        assert phrase in text
