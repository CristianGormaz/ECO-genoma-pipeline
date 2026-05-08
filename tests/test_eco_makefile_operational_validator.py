from pathlib import Path


def _make_target_block(text: str, target: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == f"{target}:":
            start = index
            break
    assert start is not None

    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line and not line.startswith((" ", "\t")) and ":" in line:
            end = index
            break
    return "\n".join(lines[start:end])


def test_eco_check_runs_operational_state_examples_validator():
    root = Path(__file__).resolve().parents[1]
    makefile_text = (root / "Makefile").read_text(encoding="utf-8")
    eco_check_block = _make_target_block(makefile_text, "eco-check")

    assert "eco-validate-operational-state-examples" in makefile_text
    assert "eco-validate-operational-state-examples" in eco_check_block
