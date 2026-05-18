from pathlib import Path


DOC_PATH = Path("docs/operations/eco-agentic-scaffold-protocol.md")


def test_agentic_scaffold_protocol_exists() -> None:
    assert DOC_PATH.exists(), "Debe existir el protocolo de agentic scaffold"


def test_agentic_scaffold_protocol_contract() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")
    lower_text = text.lower()

    assert (
        "autodesarrollo asistido" in lower_text
        or "autodesarrollo gobernado" in lower_text
    )
    assert "agente generativo" in lower_text
    assert "plantilla" in lower_text
    assert "principios admitidos" in lower_text
    assert "revisión humana" in lower_text or "revision humana" in lower_text
    assert "LAOS Governance Gate" in text

    for item in ["pausar", "avanzar con control"]:
        assert item in lower_text
    assert "revisión humana" in lower_text or "revision humana" in lower_text

    assert "nuevas funciones" in lower_text or "modulos candidatos" in lower_text

    no_real_autonomy = (
        "no implica autonomia real" in lower_text
        or "no implica autonomía real" in lower_text
        or "sin autonomia real" in lower_text
        or "sin autonomía real" in lower_text
    )
    assert no_real_autonomy
    assert "conciencia" in lower_text
    assert "libre albedrio real" in lower_text or "libre albedrío real" in lower_text

    required_limits = [
        "sin datos reales",
        "sin entrenamiento",
        "sin modificacion de baseline",
        "sin recalibracion de umbrales",
        "sin afirmaciones biomedicas aplicadas",
        "sin autonomia real",
        "sin conciencia",
        "sin libre albedrio real",
    ]
    for item in required_limits:
        assert item in lower_text
