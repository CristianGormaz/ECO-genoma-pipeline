from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "docs" / "operations" / "eco-real-biological-data-maturity-manual.md"
PROJECT_MAP = ROOT / "docs" / "operations" / "project-map.md"
CAPABILITIES_MAP = ROOT / "docs" / "operations" / "eco-current-capabilities-map.md"
OPERATIONAL_INDEX = ROOT / "docs" / "operations" / "eco-operational-panel-index.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_real_biological_data_maturity_manual_is_registered_in_operational_maps() -> None:
    assert MANUAL.exists()

    project_map = _read(PROJECT_MAP)
    capabilities_map = _read(CAPABILITIES_MAP)
    operational_index = _read(OPERATIONAL_INDEX)
    combined = "\n".join([project_map, capabilities_map, operational_index])

    assert "docs/operations/eco-real-biological-data-maturity-manual.md" in project_map
    assert "docs/operations/eco-real-biological-data-maturity-manual.md" in capabilities_map
    assert "docs/operations/eco-real-biological-data-maturity-manual.md" in operational_index
    assert "Manual de Madurez para Datos Reales Biológicos" in combined


def test_real_biological_data_maturity_manual_registration_preserves_boundary_language() -> None:
    combined = "\n".join(
        [
            _read(PROJECT_MAP),
            _read(CAPABILITIES_MAP),
            _read(OPERATIONAL_INDEX),
        ]
    )

    required_tokens = [
        "capacidad documental de frontera",
        "no habilita uso de datos reales",
        "no autoriza procesamiento de datos reales",
        "no aprueba procesamiento de datos reales por sí mismo",
        "condiciones futuras de madurez",
        "revisión humana",
        "evidencia auditable",
        "rollback",
        "schema o dry-run gate",
        "no datos reales",
        "no es una compuerta funcional activa",
    ]

    for token in required_tokens:
        assert token in combined
