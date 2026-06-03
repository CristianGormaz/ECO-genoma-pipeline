import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/run_eco_operational_gauntlet.py")
JSON_OUTPUT = Path("results/eco_operational_gauntlet.json")
MD_OUTPUT = Path("results/eco_operational_gauntlet.md")

REQUIRED_CHECKS = {
    "classifier_exact_tie_confidence",
    "classifier_raw_distance_prediction",
    "motif_rejects_plain_text_fasta",
    "homeostasis_public_paths_consistent",
    "readiness_report_does_not_claim_live_green",
    "eco_status_green_requires_clean_main_synced",
    "governed_admission_blocks_on_relevant_gates",
    "responsible_limits_not_tautological",
}


def test_eco_operational_gauntlet_script_runs_and_writes_outputs():
    assert SCRIPT.exists()

    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert JSON_OUTPUT.exists()
    assert MD_OUTPUT.exists()

    payload = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
    markdown = MD_OUTPUT.read_text(encoding="utf-8")

    assert payload["title"] == "E.C.O. Operational Gauntlet v1"
    assert payload["status"] == "passed"
    assert payload["classification"] == "synthetic_operational_gauntlet"
    assert len(payload["checks"]) >= 8

    check_names = {item["name"] for item in payload["checks"]}
    assert REQUIRED_CHECKS.issubset(check_names)
    assert all(item["status"] == "passed" for item in payload["checks"])

    limits = set(payload["limits"])
    assert "sin datos reales" in limits
    assert "sin entrenamiento" in limits
    assert "sin baseline" in limits
    assert "sin recalibración" in limits
    assert "sin afirmaciones biomédicas aplicadas" in limits

    assert "E.C.O. Operational Gauntlet v1" in markdown
    assert "Estado global" in markdown
    assert "## Checks" in markdown
    assert "## Límites responsables" in markdown
    assert "sin datos reales" in markdown
    assert "sin entrenamiento" in markdown
    assert "sin baseline" in markdown
    assert "sin recalibración" in markdown
