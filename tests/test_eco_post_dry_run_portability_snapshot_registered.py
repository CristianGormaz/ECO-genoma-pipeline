from pathlib import Path


SNAPSHOT = Path("docs/operations/eco-post-dry-run-portability-snapshot.md")
PROJECT_MAP = Path("docs/operations/project-map.md")
CAPABILITIES_MAP = Path("docs/operations/eco-current-capabilities-map.md")
PANEL_INDEX = Path("docs/operations/eco-operational-panel-index.md")


def _read(path: Path) -> str:
    assert path.exists(), f"Debe existir {path}"
    return path.read_text(encoding="utf-8")


def test_post_dry_run_portability_snapshot_exists():
    assert SNAPSHOT.exists()


def test_project_map_registers_post_dry_run_portability_snapshot():
    content = _read(PROJECT_MAP)
    lowered = content.lower()

    required_tokens = [
        "eco-post-dry-run-portability-snapshot.md",
        "Snapshot operativo post dry-run y portabilidad",
        "dry-run gate",
        "make eco-check",
        "baseline ML reproducible",
        "training readiness seguro",
        "Makefile portable",
        "no habilita datos reales",
        "no autoriza entrenamiento",
        "no reemplaza tests, dashboard ni revisión humana",
    ]

    for token in required_tokens:
        assert token in content

    assert "documental" in lowered
    assert "no ejecutable" in lowered


def test_current_capabilities_map_registers_post_dry_run_portability_snapshot():
    content = _read(CAPABILITIES_MAP)

    required_tokens = [
        "eco-post-dry-run-portability-snapshot.md",
        "Snapshot Operativo Post Dry-Run y Portabilidad",
        "dry-run gate",
        "make eco-real-biological-data-admission-dry-run",
        "make eco-check",
        "baseline ML S.N.E.-E.C.O.",
        "training readiness",
        "revisión humana",
        "$(PY)",
        "pytest passing",
    ]

    for token in required_tokens:
        assert token in content


def test_operational_panel_index_registers_post_dry_run_portability_snapshot():
    content = _read(PANEL_INDEX)

    required_tokens = [
        "eco-post-dry-run-portability-snapshot.md",
        "Snapshot Post Dry-Run y Portabilidad",
        "cierre del bloque #256–#261",
        "no autoriza datos reales",
        "no autoriza entrenamiento",
    ]

    for token in required_tokens:
        assert token in content


def test_snapshot_registration_preserves_responsible_limits():
    combined = "\n".join(
        _read(path).lower()
        for path in [PROJECT_MAP, CAPABILITIES_MAP, PANEL_INDEX]
    )

    required_limits = [
        "sin datos reales",
        "sin entrenamiento",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin diagnóstico",
        "sin interpretación biomédica aplicada",
    ]

    for token in required_limits:
        assert token in combined


def test_snapshot_registration_does_not_require_datasets():
    content = "\n".join(_read(path).lower() for path in [PROJECT_MAP, CAPABILITIES_MAP, PANEL_INDEX])

    prohibited_tokens = [
        "crear dataset",
        "crear datasets",
        "versionar dataset",
        "versionar datasets",
        "agregar datos reales",
    ]

    for token in prohibited_tokens:
        assert token not in content
