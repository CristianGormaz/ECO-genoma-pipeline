from pathlib import Path


TECHNICAL = Path("docs/operations/eco-technical-blueprint.md")
OPERATIONAL = Path("docs/operations/eco-operational-blueprint.md")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_technical_blueprint_contract() -> None:
    assert TECHNICAL.exists()
    text = _read(TECHNICAL)

    required_tokens = [
        "E.C.O. — Plano Técnico",
        "Entérico Codificador Orgánico",
        "sistema bioinspirado de digestión de información",
        "Sistema Nervioso Entérico",
        "Ingesta",
        "Fragmentación",
        "Filtrado",
        "Transformación",
        "Evaluación",
        "Absorción",
        "Retroalimentación",
        "Descarte",
        "Plexo de Auerbach",
        "Plexo de Meissner",
        "Sistema inmune intestinal",
        "Eje intestino-cerebro",
        "no modela conciencia",
        "no habilita datos reales",
        "no entrenar modelos",
        "no modificar baseline",
        "no recalibrar umbrales",
        "plano operativo",
    ]

    for token in required_tokens:
        assert token in text


def test_operational_blueprint_contract() -> None:
    assert OPERATIONAL.exists()
    text = _read(OPERATIONAL)

    required_tokens = [
        "E.C.O. — Plano Operativo",
        "entrar",
        "entender",
        "avanzar",
        "pausar",
        "validar",
        "no romper",
        "no trabajar directo en main",
        "git status --short",
        "git rev-list --left-right --count HEAD...origin/main",
        "make eco-status",
        "python -m pytest -q",
        "make eco-check-clean",
        "(END)",
        "Ctrl+C",
        "árbol limpio",
        "HEAD = origin/main",
        "sin PR abiertos",
        "plano técnico",
    ]

    for token in required_tokens:
        assert token in text


def test_blueprints_have_no_executable_code_blocks() -> None:
    forbidden_tokens = [
        "```python",
        "```bash",
        "```sh",
        "```sql",
    ]

    for path in (TECHNICAL, OPERATIONAL):
        text = _read(path)
        for token in forbidden_tokens:
            assert token not in text


def test_blueprints_do_not_enable_real_data_processing_or_false_agency() -> None:
    combined = "\n".join([_read(TECHNICAL), _read(OPERATIONAL)])

    forbidden_claims = [
        "E.C.O. tiene conciencia",
        "E.C.O. posee conciencia",
        "E.C.O. tiene autonomía real",
        "E.C.O. posee autonomía real",
        "E.C.O. tiene libre albedrío real",
        "E.C.O. posee libre albedrío real",
        "instrucciones para procesar datos reales",
        "debe procesar datos reales",
        "puede procesar datos reales",
        "debe abrir datos reales",
        "puede abrir datos reales",
        "debe descargar datos reales",
        "puede descargar datos reales",
    ]

    for token in forbidden_claims:
        assert token not in combined

    required_boundaries = [
        "no procesar datos reales en este sprint",
        "no afirma autonomía real",
        "no afirma libre albedrío real",
        "no abrir datos reales",
        "no entrenar modelos",
        "no modificar baseline",
        "no recalibrar umbrales",
    ]

    for token in required_boundaries:
        assert token in combined
