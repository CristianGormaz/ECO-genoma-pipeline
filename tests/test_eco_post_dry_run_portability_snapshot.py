import re
from pathlib import Path


SNAPSHOT = Path("docs/operations/eco-post-dry-run-portability-snapshot.md")


def _content() -> str:
    assert SNAPSHOT.exists(), "Debe existir el snapshot post dry-run y portabilidad"
    return SNAPSHOT.read_text(encoding="utf-8")


def test_post_dry_run_portability_snapshot_exists_and_mentions_progress():
    text = _content()

    required_tokens = [
        "Snapshot Operativo Post Dry-Run y Portabilidad",
        "Real Biological Data Admission Dry-Run Gate",
        "make eco-real-biological-data-admission-dry-run",
        "make eco-check",
        "make eco-check-clean",
        "pytest passing",
        "dashboard sintético",
        "advance",
        "baseline ML S.N.E.-E.C.O.",
        "reproducible",
        "data/training",
        "training readiness",
        "revisión humana",
        "$(PY)",
    ]

    for token in required_tokens:
        assert token in text


def test_post_dry_run_portability_snapshot_preserves_responsible_limits():
    text = _content().lower()

    required_limits = [
        "sin datos reales",
        "sin descarga de datos reales",
        "sin lectura de datos reales",
        "sin entrenamiento",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin diagnóstico",
        "sin interpretación biomédica aplicada",
        "sin conciencia",
        "sin libre albedrío real",
        "sin autonomía real",
    ]

    for token in required_limits:
        assert token in text


def test_post_dry_run_portability_snapshot_declares_what_progress_does_not_mean():
    text = _content().lower()

    required_boundaries = [
        "no significa admisión real",
        "entrenamiento esté permitido",
        "accuracy del baseline sea desempeño real",
        "no reemplaza revisión humana",
    ]

    assert "no significa" in text
    for token in required_boundaries:
        assert token in text


def test_post_dry_run_portability_snapshot_has_no_executable_blocks_or_real_data_instructions():
    text = _content()
    lowered = text.lower()

    prohibited_fences = [
        "```python",
        "```bash",
        "```sh",
        "```sql",
    ]
    prohibited_real_data_instructions = [
        "descargue datos reales",
        "descargar datos reales desde",
        "lea datos reales",
        "leer datos reales desde",
        "procesar datos reales con",
        "procesa datos reales con",
        "entrenar con datos reales",
    ]
    prohibited_concrete_real_datasets = [
        "ncbi",
        "sra",
        "ena",
        "dbgap",
        "clinvar",
        "1000 genomes",
    ]

    for token in prohibited_fences:
        assert token not in lowered
    for token in prohibited_real_data_instructions:
        assert token not in lowered
    for token in prohibited_concrete_real_datasets:
        assert re.search(rf"\b{re.escape(token)}\b", lowered) is None
