from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAKEFILE = ROOT / "Makefile"


def _target_block(name: str) -> str:
    lines = MAKEFILE.read_text(encoding="utf-8").splitlines()
    start = None

    for index, line in enumerate(lines):
        if line.startswith(f"{name}:"):
            start = index
            break

    assert start is not None, f"target not found: {name}"

    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line and not line.startswith((" ", "\t", "#")) and ":" in line:
            end = index
            break

    return "\n".join(lines[start:end])


def test_eco_check_runs_adaptive_dataset_example_validator():
    block = _target_block("eco-check")

    assert "make eco-validate-adaptive-dataset-example" in block


def test_adaptive_dataset_validator_target_still_exists():
    block = _target_block("eco-validate-adaptive-dataset-example")

    assert "scripts/validate_eco_adaptive_dataset_example.py" in block
