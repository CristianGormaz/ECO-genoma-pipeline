from pathlib import Path


DOC = Path("docs/research/eco-vacuum-state-demo-traceability.md")
BASE_DOC = Path("docs/research/eco-vacio-cuantico-patrones-minimos.md")
SCRIPT = Path("scripts/run_eco_vacuum_state_demo.py")


def test_vacuum_state_traceability_files_exist():
    assert DOC.exists()
    assert BASE_DOC.exists()
    assert SCRIPT.exists()


def test_vacuum_state_traceability_declares_links_and_limits():
    text = DOC.read_text(encoding="utf-8")

    required = [
        "Estado: experimental",
        "Clasificación: permitido",
        "docs/research/eco-vacio-cuantico-patrones-minimos.md",
        "scripts/run_eco_vacuum_state_demo.py",
        "results/eco_vacuum_state_demo.json",
        "results/eco_vacuum_state_demo.md",
        "estado_base",
        "ausencia",
        "fluctuacion",
        "frontera",
        "medicion",
        "No usa datos sensibles",
        "no entrena modelos",
        "no modifica baseline",
        "no recalibra umbrales",
        "no afirma aplicaciones físicas reales",
    ]

    for phrase in required:
        assert phrase in text
