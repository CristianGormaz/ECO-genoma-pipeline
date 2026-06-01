from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_public_source_url_guard_registered_in_capabilities_map():
    content = _read("docs/operations/eco-current-capabilities-map.md")

    required_tokens = [
        "public-source-url-admission-guard",
        "scripts/eco_public_source_guard.py",
        "URLs públicas externas",
        "esquema",
        "dominio",
        "redirecciones",
        "--allow-custom-url",
        "no equivale a `real-biological-data-admission-gate`",
        "no autoriza procesamiento de datos reales",
        "no habilita entrenamiento",
        "no habilita diagnóstico",
        "no habilita interpretación clínica",
        "no modifica baseline",
        "no recalibra umbrales",
        "revisión humana",
    ]

    for token in required_tokens:
        assert token in content


def test_public_source_url_guard_registered_in_operational_panel_index():
    content = _read("docs/operations/eco-operational-panel-index.md")

    required_tokens = [
        "Public Source URL Admission Guard",
        "scripts/eco_public_source_guard.py",
        "tests/test_eco_public_source_url_admission_guard.py",
        "compuerta de seguridad operacional",
        "fuentes públicas allowlisted",
        "--allow-custom-url",
        "No equivale a `real-biological-data-admission-gate`",
        "protege la fuente de descarga",
        "no autoriza procesamiento de datos reales",
        "no habilita entrenamiento",
        "no habilita diagnóstico",
        "no habilita interpretación clínica",
        "no modifica baseline",
        "no recalibra umbrales",
        "revisión humana",
    ]

    for token in required_tokens:
        assert token in content
