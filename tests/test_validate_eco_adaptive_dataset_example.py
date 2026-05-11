import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_eco_adaptive_dataset_example.py"


def test_adaptive_dataset_example_validator_passes():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Estado: passed" in completed.stdout
    assert "Registros sintéticos: 2" in completed.stdout
    assert "sin datos reales" in completed.stdout
    assert "sin entrenamiento" in completed.stdout


def test_adaptive_dataset_example_validator_declares_limits():
    content = SCRIPT.read_text(encoding="utf-8")

    required_tokens = [
        "no_real_data",
        "no_sensitive_data",
        "no_private_genetic_data",
        "no_training",
        "no_baseline_change",
        "no_threshold_recalibration",
        "no_biomedical_claims",
    ]

    for token in required_tokens:
        assert token in content
