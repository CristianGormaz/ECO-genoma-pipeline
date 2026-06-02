from pathlib import Path


TECHNICAL = Path("docs/operations/eco-technical-blueprint.md")
OPERATIONAL = Path("docs/operations/eco-operational-blueprint.md")
PROJECT_MAP = Path("docs/operations/project-map.md")
CAPABILITIES_MAP = Path("docs/operations/eco-current-capabilities-map.md")
PANEL_INDEX = Path("docs/operations/eco-operational-panel-index.md")


def _read_lower(path: Path) -> str:
    return path.read_text(encoding="utf-8").lower()


def test_blueprint_registry_files_exist() -> None:
    for path in (
        TECHNICAL,
        OPERATIONAL,
        PROJECT_MAP,
        CAPABILITIES_MAP,
        PANEL_INDEX,
    ):
        assert path.exists(), f"Missing expected blueprint registry file: {path}"


def test_project_map_registers_dual_blueprints() -> None:
    text = _read_lower(PROJECT_MAP)

    required_tokens = [
        "eco-technical-blueprint.md",
        "eco-operational-blueprint.md",
        "plano técnico",
        "plano operativo",
        "documentos de orientación",
        "no son ejecutables",
        "no habilitan datos reales",
        "no reemplazan tests",
        "reportes",
        "dashboard",
        "validaciones reales",
    ]

    for token in required_tokens:
        assert token in text


def test_current_capabilities_map_registers_dual_blueprints() -> None:
    text = _read_lower(CAPABILITIES_MAP)

    required_tokens = [
        "eco-technical-blueprint.md",
        "eco-operational-blueprint.md",
        "planos oficiales de orientación",
        "cómo está construido",
        "entrar, entender, avanzar, pausar, validar",
        "no habilitan datos reales",
        "no entrenan modelos",
        "no modifican baseline",
        "no recalibran umbrales",
        "no hacen afirmaciones biomédicas aplicadas",
    ]

    for token in required_tokens:
        assert token in text


def test_operational_panel_index_registers_dual_blueprints() -> None:
    text = _read_lower(PANEL_INDEX)

    required_tokens = [
        "eco-technical-blueprint.md",
        "eco-operational-blueprint.md",
        "plano técnico",
        "plano operativo",
        "entrar",
        "avanzar",
        "pausar",
        "validar",
        "recuperar",
        "cerrar",
        "no reemplazan comandos reales",
        "validaciones reales",
    ]

    for token in required_tokens:
        assert token in text


def test_snapshot_count_wording_is_not_rigid() -> None:
    capabilities = CAPABILITIES_MAP.read_text(encoding="utf-8")
    panel = _read_lower(PANEL_INDEX)

    assert "588 passed" not in capabilities
    assert "pytest passing" in capabilities.lower()
    assert "588 passed" not in panel
    assert "no usar conteo rígido como criterio de aceptación" in panel


def test_blueprint_registration_does_not_present_blueprints_as_scripts_or_gates() -> None:
    combined = "\n".join(
        [
            _read_lower(PROJECT_MAP),
            _read_lower(CAPABILITIES_MAP),
            _read_lower(PANEL_INDEX),
        ]
    )

    required_boundaries = [
        "no son scripts",
        "no son compuertas funcionales",
        "no habilitan datos reales",
    ]

    for token in required_boundaries:
        assert token in combined


def test_blueprint_registration_preserves_false_agency_boundaries() -> None:
    combined = "\n".join(
        [
            _read_lower(PROJECT_MAP),
            _read_lower(CAPABILITIES_MAP),
            _read_lower(PANEL_INDEX),
        ]
    )

    forbidden_claims = [
        "e.c.o. tiene conciencia",
        "e.c.o. posee conciencia",
        "e.c.o. tiene autonomía real",
        "e.c.o. posee autonomía real",
        "e.c.o. tiene libre albedrío real",
        "e.c.o. posee libre albedrío real",
    ]

    for token in forbidden_claims:
        assert token not in combined

    required_limits = [
        "no afirman conciencia",
        "no afirman autonomía real",
        "no afirman libre albedrío real",
    ]

    for token in required_limits:
        assert token in combined
