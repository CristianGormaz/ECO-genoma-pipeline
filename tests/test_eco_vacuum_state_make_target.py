import json
import subprocess
import shutil
import sys
from pathlib import Path


MAKEFILE = Path("Makefile")


def test_eco_vacuum_state_make_target_is_declared():
    text = MAKEFILE.read_text(encoding="utf-8")

    assert ".PHONY: eco-vacuum-state-demo" in text
    assert "eco-vacuum-state-demo:" in text
    assert "scripts/run_eco_vacuum_state_demo.py" in text
    assert "ECO_VACUUM_OUTPUT_DIR" in text


def test_eco_vacuum_state_make_target_generates_outputs(tmp_path):
    command = (
        [
            "make",
            "eco-vacuum-state-demo",
            f"PYTHON={sys.executable}",
            f"ECO_VACUUM_OUTPUT_DIR={tmp_path}",
        ]
        if shutil.which("make")
        else [
            sys.executable,
            "scripts/run_eco_vacuum_state_demo.py",
            "--output-dir",
            str(tmp_path),
        ]
    )
    result = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr + result.stdout

    json_path = tmp_path / "eco_vacuum_state_demo.json"
    md_path = tmp_path / "eco_vacuum_state_demo.md"

    assert json_path.exists()
    assert md_path.exists()

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["status"] == "experimental"
    assert payload["classification"] == "permitted"
    assert payload["not_physical_measurement"] is True
    assert payload["training_executed"] is False
