import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_adaptive_dataset_readiness_gate_outputs_passed_report():
    result = subprocess.run(
        ["python3", "scripts/run_eco_adaptive_dataset_readiness_gate.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "Estado: passed" in result.stdout

    output_json = ROOT / "results" / "eco_adaptive_dataset_readiness_gate.json"
    output_md = ROOT / "results" / "eco_adaptive_dataset_readiness_gate.md"

    assert output_json.exists()
    assert output_md.exists()

    data = json.loads(output_json.read_text(encoding="utf-8"))

    assert data["status"] == "passed"
    assert data["classification"] == "permitted"
    assert data["ready_for_operational_review"] is True
    assert data["missing_files"] == []

    required_paths = {item["path"] for item in data["required_files"]}

    assert "docs/architecture/eco-adaptive-dataset-contract.md" in required_paths
    assert "docs/operations/eco-adaptive-dataset-index.md" in required_paths
    assert "scripts/run_eco_adaptive_dataset_report.py" in required_paths


def test_adaptive_dataset_readiness_gate_declares_responsible_limits():
    output_json = ROOT / "results" / "eco_adaptive_dataset_readiness_gate.json"

    subprocess.run(
        ["python3", "scripts/run_eco_adaptive_dataset_readiness_gate.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    data = json.loads(output_json.read_text(encoding="utf-8"))
    limits = set(data["responsible_limits"])

    assert "sin datos reales" in limits
    assert "sin datos sensibles" in limits
    assert "sin datos genéticos privados" in limits
    assert "sin entrenamiento" in limits
    assert "sin modificación de baseline" in limits
    assert "sin recalibración de umbrales" in limits
    assert "sin afirmaciones biomédicas aplicadas" in limits


def test_adaptive_dataset_readiness_gate_markdown_is_operational():
    subprocess.run(
        ["python3", "scripts/run_eco_adaptive_dataset_readiness_gate.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    output_md = ROOT / "results" / "eco_adaptive_dataset_readiness_gate.md"
    text = output_md.read_text(encoding="utf-8")

    assert "# E.C.O. adaptive dataset readiness gate" in text
    assert "## Archivos requeridos" in text
    assert "## Límites responsables" in text
    assert "No usar para entrenamiento." in text
