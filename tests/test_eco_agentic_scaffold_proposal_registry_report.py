import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/run_eco_agentic_scaffold_proposal_registry_report.py")
MAKEFILE = Path("Makefile")
CLEANER = Path("scripts/clean_eco_results.py")
JSON_OUTPUT = Path("results/eco_agentic_scaffold_proposal_registry_report.json")
MD_OUTPUT = Path("results/eco_agentic_scaffold_proposal_registry_report.md")
SOURCE = "docs/operations/eco-agentic-scaffold-proposal-registry.md"


def test_script_and_makefile_target_exist():
    assert SCRIPT.exists()

    makefile_text = MAKEFILE.read_text(encoding="utf-8")
    assert ".PHONY: eco-agentic-scaffold-proposal-registry-report" in makefile_text
    assert "eco-agentic-scaffold-proposal-registry-report:" in makefile_text
    assert str(SCRIPT) in makefile_text


def test_registry_report_command_generates_json_and_markdown():
    result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)

    assert result.returncode == 0, result.stdout + result.stderr
    assert JSON_OUTPUT.exists()
    assert MD_OUTPUT.exists()

    payload = json.loads(JSON_OUTPUT.read_text(encoding="utf-8"))
    assert payload["status"] == "passed"
    assert payload["classification"] == "permitted"
    assert payload["source"] == SOURCE
    assert payload["proposal_count"] >= 1
    assert payload["human_review_required"] is True
    assert payload["final_human_decision_required"] is True

    proposal_ids = [proposal["proposal_id"] for proposal in payload["proposals"]]
    assert "ASC-PROP-001" in proposal_ids or proposal_ids[0]

    markdown = MD_OUTPUT.read_text(encoding="utf-8").lower()
    assert "agentic scaffold proposal registry report" in markdown
    assert "passed" in markdown
    assert "asc-prop-001" in markdown
    assert "revisión humana" in markdown or "human review" in markdown
    assert "decisión final humana" in markdown or "final human decision" in markdown


def test_cleaner_registers_and_cleans_registry_report_artifacts():
    cleaner_text = CLEANER.read_text(encoding="utf-8")
    assert str(JSON_OUTPUT) in cleaner_text
    assert str(MD_OUTPUT) in cleaner_text

    JSON_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUTPUT.write_text("temporary registry report json", encoding="utf-8")
    MD_OUTPUT.write_text("temporary registry report md", encoding="utf-8")

    result = subprocess.run([sys.executable, str(CLEANER)], capture_output=True, text=True, check=False)

    assert result.returncode == 0, result.stdout + result.stderr
    assert not JSON_OUTPUT.exists()
    assert not MD_OUTPUT.exists()
