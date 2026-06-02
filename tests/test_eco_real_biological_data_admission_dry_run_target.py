import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAKEFILE = ROOT / "Makefile"
SCRIPT = "scripts/run_eco_real_biological_data_admission_dry_run.py"
DOC = ROOT / "docs" / "operations" / "eco-real-biological-data-admission-dry-run.md"
PANEL_INDEX = ROOT / "docs" / "operations" / "eco-operational-panel-index.md"
OUTPUT_JSON = ROOT / "results" / "eco_real_biological_data_admission_dry_run_report.json"
OUTPUT_MD = ROOT / "results" / "eco_real_biological_data_admission_dry_run_report.md"


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)


def _make_target_block(target: str) -> str:
    lines = MAKEFILE.read_text(encoding="utf-8").splitlines()
    start = lines.index(f"{target}:")
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line and not line.startswith("\t") and not line.startswith(" "):
            end = index
            break
    return "\n".join(lines[start:end])


def test_makefile_registers_dry_run_admission_target() -> None:
    text = MAKEFILE.read_text(encoding="utf-8")
    block = _make_target_block("eco-real-biological-data-admission-dry-run")

    assert ".PHONY: eco-real-biological-data-admission-dry-run" in text
    assert "eco-real-biological-data-admission-dry-run:" in text
    assert SCRIPT in block
    assert "wget" not in block
    assert "curl" not in block


def test_dry_run_admission_target_generates_safe_reports() -> None:
    result = _run(["make", "eco-real-biological-data-admission-dry-run"])

    assert result.returncode == 0, result.stdout + result.stderr
    assert OUTPUT_JSON.exists()
    assert OUTPUT_MD.exists()

    payload = json.loads(OUTPUT_JSON.read_text(encoding="utf-8"))
    markdown = OUTPUT_MD.read_text(encoding="utf-8")
    markdown_lower = markdown.lower()

    assert payload["gate_id"] == "eco_real_biological_data_admission_dry_run_v1"
    assert payload["processed_real_data"] is False
    assert payload["downloaded_real_data"] is False
    assert payload["read_real_data_files"] is False
    assert payload["trained_model"] is False
    assert payload["modified_baseline"] is False
    assert payload["recalibrated_thresholds"] is False
    assert payload["makes_applied_biomedical_claims"] is False
    assert "E.C.O. Real Biological Data Admission Dry-Run Report" in markdown
    assert "no se procesaron datos reales" in markdown_lower
    assert "no habilita admisión real" in markdown_lower
    assert "revisión humana" in markdown_lower


def test_eco_clean_results_removes_dry_run_admission_reports() -> None:
    result = _run(["make", "eco-real-biological-data-admission-dry-run"])

    assert result.returncode == 0, result.stdout + result.stderr
    assert OUTPUT_JSON.exists()
    assert OUTPUT_MD.exists()

    clean = _run(["make", "eco-clean-results"])

    assert clean.returncode == 0, clean.stdout + clean.stderr
    assert not OUTPUT_JSON.exists()
    assert not OUTPUT_MD.exists()


def test_dry_run_admission_docs_and_panel_register_operational_command() -> None:
    doc = DOC.read_text(encoding="utf-8").lower()
    panel = PANEL_INDEX.read_text(encoding="utf-8").lower()

    required_doc_tokens = [
        "make eco-real-biological-data-admission-dry-run",
        "no lee datos reales",
        "no descarga datos reales",
        "no aprueba admisión real",
        "revisión humana",
    ]

    for token in required_doc_tokens:
        assert token in doc

    required_panel_tokens = [
        "make eco-real-biological-data-admission-dry-run",
        "manifiestos descriptivos",
        "no lee",
        "no descarga",
        "no procesa",
        "no interpreta datos reales",
        "no entrena modelos",
        "no modifica baseline",
        "no recalibra umbrales",
    ]

    for token in required_panel_tokens:
        assert token in panel
