from pathlib import Path


WORKFLOW = Path(".github/workflows/eco-check.yml")


def test_eco_check_workflow_exists():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "E.C.O. operational check" in text
    assert "pull_request:" in text
    assert "push:" in text
    assert "branches:" in text
    assert "- main" in text


def test_eco_check_workflow_runs_check_clean_command():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "make eco-check-clean" in text
    assert "run: make eco-check-clean" in text
