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
        if line and not line.startswith("\t") and not line.startswith(" "):
            end = index
            break
    return "\n".join(lines[start:end])


def test_eco_check_runs_operational_state_examples_report():
    makefile = Path("Makefile").read_text(encoding="utf-8")
    eco_check = _make_target_block(makefile, "eco-check")

    assert "$(MAKE) eco-validate-operational-state-examples" in eco_check
    assert "$(MAKE) eco-operational-state-examples-report" in eco_check
    assert eco_check.index("eco-validate-operational-state-examples") < eco_check.index("eco-operational-state-examples-report")
    assert "eco-operational-state-examples-report:" in makefile
    assert "rm -f results/eco_operational_state_examples_report.json" in makefile
    assert "rm -f results/eco_operational_state_examples_report.md" in makefile
