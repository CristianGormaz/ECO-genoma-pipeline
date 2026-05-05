import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/run_eco_vacuum_state_demo.py")


def test_eco_vacuum_state_demo_generates_outputs(tmp_path):
    output_dir = tmp_path / "results"

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--output-dir", str(output_dir)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "OK: demo E.C.O. vacuum state generada." in result.stdout

    json_path = output_dir / "eco_vacuum_state_demo.json"
    md_path = output_dir / "eco_vacuum_state_demo.md"

    assert json_path.exists()
    assert md_path.exists()

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    md = md_path.read_text(encoding="utf-8")

    assert payload["status"] == "experimental"
    assert payload["classification"] == "permitted"
    assert payload["not_physical_measurement"] is True
    assert payload["sensitive_data_used"] is False
    assert payload["training_executed"] is False
    assert payload["baseline_modified"] is False
    assert payload["thresholds_recalibrated"] is False

    assert payload["summary"]["total_steps"] == 6
    assert payload["summary"]["observable_events"] >= 1

    for required in [
        "estado_base",
        "ausencia",
        "fluctuacion",
        "frontera",
        "medicion",
        "evento",
    ]:
        assert required in payload["controlled_vocabulary"]

    assert "No mide el vacío cuántico real" in md
    assert "no usa datos sensibles" in md
