import importlib.util
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_eco_adaptive_dataset_example.py"


def _load_validator_module():
    spec = importlib.util.spec_from_file_location(
        "validate_eco_adaptive_dataset_example", SCRIPT
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
        "synthetic_only",
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



def test_adaptive_dataset_example_validator_rejects_empty_json_payload(tmp_path, capsys):
    module = _load_validator_module()
    module.JSON_DOC = tmp_path / "example.json"
    module.MD_DOC = tmp_path / "example.md"

    module.JSON_DOC.write_text("{}", encoding="utf-8")
    module.MD_DOC.write_text(
        "\n".join(module.REQUIRED_MARKDOWN_TOKENS),
        encoding="utf-8",
    )

    exit_code = module.main()
    output = capsys.readouterr().out

    assert exit_code == 1
    assert "Estado: failed" in output
    assert "classification must be permitido" in output
    assert "records must be a non-empty list" in output


def test_adaptive_dataset_example_validator_rejects_non_object_json_root(tmp_path, capsys):
    module = _load_validator_module()
    module.JSON_DOC = tmp_path / "example.json"
    module.MD_DOC = tmp_path / "example.md"

    module.JSON_DOC.write_text("[]", encoding="utf-8")
    module.MD_DOC.write_text(
        "\n".join(module.REQUIRED_MARKDOWN_TOKENS),
        encoding="utf-8",
    )

    exit_code = module.main()
    output = capsys.readouterr().out

    assert exit_code == 1
    assert "Estado: failed" in output
    assert "payload must be an object" in output


def test_adaptive_dataset_example_validator_enforces_limits_behavior():
    module = _load_validator_module()

    for limit_name in module.REQUIRED_LIMITS:
        payload = {
            "classification": "permitido",
            "scope": "synthetic_documental_example",
            "contract": "docs/architecture/eco-adaptive-dataset-contract.md",
            "limits": {key: True for key in module.REQUIRED_LIMITS},
            "records": [
                {
                    "record_id": "eco-synth-adaptive-001",
                    "source_type": "synthetic",
                    "adaptive_state": "candidate",
                    "signal_family": "demo",
                    "evidence_level": "synthetic",
                    "risk_flag": "none",
                    "review_status": "candidate",
                    "notes": "synthetic example only",
                }
            ],
        }

        payload["limits"][limit_name] = False
        errors = []

        module.validate_payload(payload, errors)

        assert f"limit must be true: {limit_name}" in errors


def test_adaptive_dataset_example_validator_enforces_markdown_responsible_tokens(tmp_path):
    module = _load_validator_module()
    module.MD_DOC = tmp_path / "example.md"

    omitted = "No contiene datos personales."
    module.MD_DOC.write_text(
        "\n".join(
            token for token in module.REQUIRED_MARKDOWN_TOKENS
            if token != omitted
        ),
        encoding="utf-8",
    )

    errors = []
    module.validate_markdown(errors)

    assert f"Markdown guide missing token: {omitted}" in errors
