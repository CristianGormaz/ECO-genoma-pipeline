from pathlib import Path


SNAPSHOT = Path("docs/operations/eco-operational-state-snapshot.md")


def test_operational_state_snapshot_declares_current_green_state():
    assert SNAPSHOT.exists(), "Debe existir el snapshot operativo E.C.O."

    content = SNAPSHOT.read_text(encoding="utf-8")

    required_tokens = [
        "Estado: green",
        "Rama estable: `main`",
        "Último commit estable: `3d8592c`",
        "HEAD = origin/main",
        "PR abiertos: ninguno",
        "Dashboard sintético operativo: 8 componentes",
        "Suite local validada: 588 tests passing",
        "Relación local/remoto esperada: `0 0`",
        "public-source-url-admission-guard",
    ]

    for token in required_tokens:
        assert token in content


def test_operational_state_snapshot_preserves_responsible_limits():
    content = SNAPSHOT.read_text(encoding="utf-8")

    required_tokens = [
        "No ingiere datos reales",
        "No habilita entrenamiento",
        "No modifica baseline",
        "No recalibra umbrales",
        "No produce afirmaciones biomédicas aplicadas",
        "no reemplaza una compuerta completa de admisión de datos reales biológicos",
    ]

    for token in required_tokens:
        assert token in content
