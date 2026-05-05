from pathlib import Path


DOC = Path("docs/research/eco-research-index.md")


def test_eco_research_index_exists():
    assert DOC.exists()


def test_eco_research_index_links_core_pieces_and_limits():
    text = DOC.read_text(encoding="utf-8")

    required = [
        "Estado: experimental",
        "Clasificación: permitido",
        "eco-vacio-cuantico-patrones-minimos.md",
        "run_eco_vacuum_state_demo.py",
        "eco-vacuum-state-demo-traceability.md",
        "make eco-vacuum-state-demo",
        "README.md",
        "No miden el vacío cuántico real",
        "no usan datos sensibles",
        "no entrenan modelos",
        "no modifican baseline",
        "no recalibran umbrales",
    ]

    for phrase in required:
        assert phrase in text
