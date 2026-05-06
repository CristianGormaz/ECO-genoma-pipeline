from pathlib import Path


WORKFLOW = Path(".github/workflows/eco-check.yml")


def test_eco_check_workflow_exists():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "E.C.O. operational check" in text
    assert "pull_request:" in text
    assert "push:" in text
    assert "branches:" in text
    assert "- main" in text


def test_eco_check_workflow_runs_operational_check():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "actions/checkout@v4" in text
    assert "actions/setup-python@v5" in text
    assert "python-version:" in text
    assert "python -m pip install pytest" in text
    assert "make eco-check" in text
