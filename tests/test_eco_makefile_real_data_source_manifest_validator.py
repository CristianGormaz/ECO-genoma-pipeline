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
        if lines[index] and not lines[index].startswith("\t") and not lines[index].startswith("#"):
            end = index
            break
    return "\n".join(lines[start:end])


def test_eco_check_runs_real_data_source_manifest_validator():
    root = Path(__file__).resolve().parents[1]
    makefile = (root / "Makefile").read_text(encoding="utf-8")
    eco_check = _make_target_block(makefile, "eco-check")
    validator = _make_target_block(makefile, "eco-validate-real-data-source-manifest")
    assert "$(MAKE) eco-validate-real-data-source-manifest" in eco_check
    assert "validate_eco_real_data_source_manifest" in validator
