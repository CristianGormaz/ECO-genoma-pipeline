from pathlib import Path


def test_eco_sprint_release_checklist_content() -> None:
    doc_path = Path("docs/operations/eco-sprint-release-checklist.md")
    assert doc_path.exists(), "Debe existir el documento de checklist de release de sprint"

    content = doc_path.read_text(encoding="utf-8").lower()

    required_phrases = [
        "antes de abrir pr",
        "antes de mergear",
        "después de mergear",
        "limpieza de ramas",
        "make eco-status",
        "python3 -m pytest -q",
        "make eco-check-clean",
        "git status --short",
        "git rev-list --left-right --count head...origin/main",
        "head = origin/main",
        "árbol limpio",
        "no pr pendiente",
        "sin datos reales",
        "sin entrenamiento",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin afirmaciones biomédicas aplicadas",
    ]

    for phrase in required_phrases:
        assert phrase in content, f"Falta la mención obligatoria: {phrase}"
