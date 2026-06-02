import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAKEFILE = ROOT / "Makefile"
SCRIPT = "scripts/run_eco_real_biological_data_admission_dry_run.py"
DOC = ROOT / "docs" / "operations" / "eco-real-biological-data-admission-dry-run.md"
PANEL_INDEX = ROOT / "docs" / "operations" / "eco-operational-panel-index.md"
CAPABILITIES_MAP = ROOT / "docs" / "operations" / "eco-current-capabilities-map.md"
PROJECT_MAP = ROOT / "docs" / "operations" / "project-map.md"
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


def test_eco_check_references_real_biological_data_admission_dry_run() -> None:
    text = MAKEFILE.read_text(encoding="utf-8")
    eco_check = _make_target_block("eco-check")
    dry_run = _make_target_block("eco-real-biological-data-admission-dry-run")

    assert "eco-real-biological-data-admission-dry-run:" in text
    assert "eco-check:" in text
    assert "$(MAKE) eco-real-biological-data-admission-dry-run" in eco_check
    assert "$(MAKE) eco-validate-real-data-source-manifest" in eco_check
    assert eco_check.index("eco-validate-real-data-source-manifest") < eco_check.index(
        "eco-real-biological-data-admission-dry-run"
    )
    assert SCRIPT in dry_run


def test_dry_run_docs_register_eco_check_integration() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in (DOC, PANEL_INDEX, CAPABILITIES_MAP, PROJECT_MAP)
    )

    required_tokens = [
        "make eco-real-biological-data-admission-dry-run",
        "make eco-check",
        "manifiestos descriptivos",
        "evidencia auditable",
        "no lee datos reales",
        "no descarga datos reales",
        "no aprueba admisión real",
        "revisión humana",
        "no datasets",
        "sin entrenamiento",
        "baseline",
        "umbrales",
        "afirmaciones biomédicas aplicadas",
    ]

    for token in required_tokens:
        assert token in combined


def test_dry_run_target_still_runs_and_artifacts_are_cleanable() -> None:
    result = _run(["make", "eco-real-biological-data-admission-dry-run"])

    assert result.returncode == 0, result.stdout + result.stderr
    assert OUTPUT_JSON.exists()
    assert OUTPUT_MD.exists()

    payload = json.loads(OUTPUT_JSON.read_text(encoding="utf-8"))
    assert payload["gate_id"] == "eco_real_biological_data_admission_dry_run_v1"
    assert payload["processed_real_data"] is False
    assert payload["downloaded_real_data"] is False
    assert payload["read_real_data_files"] is False
    assert payload["trained_model"] is False
    assert payload["modified_baseline"] is False
    assert payload["recalibrated_thresholds"] is False
    assert payload["makes_applied_biomedical_claims"] is False

    clean = _run(["make", "eco-clean-results"])

    assert clean.returncode == 0, clean.stdout + clean.stderr
    assert not OUTPUT_JSON.exists()
    assert not OUTPUT_MD.exists()


def test_eco_check_registration_does_not_execute_recursive_pytest_in_contract() -> None:
    test_text = Path(__file__).read_text(encoding="utf-8")
    forbidden = '["make", ' + '"eco-check"]'

    assert forbidden not in test_text
