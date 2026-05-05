from pathlib import Path

DOC = Path("docs/research/eco-vacio-cuantico-patrones-minimos.md")


def test_eco_vacio_cuantico_doc_exists():
    assert DOC.exists()


def test_eco_vacio_cuantico_declares_responsible_limits():
    text = DOC.read_text(encoding="utf-8")

    required = [
        "Estado: experimental",
        "Clasificación: permitido",
        "E.C.O. no modela moléculas del vacío",
        "estado base",
        "ausencia",
        "fluctuacion",
        "frontera",
        "medicion",
        "No se afirma que E.C.O. mida el vacío cuántico",
        "No se entrena con datos sensibles",
        "No se modifica baseline estable",
    ]

    for phrase in required:
        assert phrase in text
