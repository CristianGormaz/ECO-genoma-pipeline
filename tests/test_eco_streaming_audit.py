from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_eco_streaming_audit.py"


def run_audit(tmp_path: Path) -> tuple[Path, Path, subprocess.CompletedProcess[str]]:
    output_json = tmp_path / "eco_streaming_audit.json"
    output_md = tmp_path / "eco_streaming_audit.md"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--output-json", str(output_json), "--output-md", str(output_md)],
        capture_output=True,
        text=True,
        check=False,
        cwd=ROOT,
    )
    return output_json, output_md, result


def file_digests() -> dict[str, str]:
    digests: dict[str, str] = {}
    for base in ("src", "scripts"):
        for path in sorted((ROOT / base).rglob("*.py")):
            digests[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return digests


def test_streaming_audit_generates_json_and_markdown(tmp_path: Path):
    output_json, output_md, result = run_audit(tmp_path)
    assert result.returncode == 0
    assert output_json.exists()
    assert output_md.exists()

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    markdown = output_md.read_text(encoding="utf-8")

    assert payload["summary"]["schema_version"] == "eco_massification_readiness_audit_v1"
    assert payload["summary"]["touches_pipeline_semantics"] is False
    assert payload["findings"]
    assert "# E.C.O. massification readiness audit" in markdown


def test_streaming_audit_detects_productive_read_text(tmp_path: Path):
    output_json, _, _ = run_audit(tmp_path)
    payload = json.loads(output_json.read_text(encoding="utf-8"))

    assert any(
        finding["rule_id"] == "read_text_full_file_ingest"
        and finding["severity"] == "critical"
        and finding["path"] == "src/eco_core/ingestion.py"
        for finding in payload["findings"]
    )


def test_streaming_audit_classifies_tests_as_false_positive(tmp_path: Path):
    output_json, _, _ = run_audit(tmp_path)
    payload = json.loads(output_json.read_text(encoding="utf-8"))

    assert any(
        finding["severity"] == "false_positive"
        and "tests/" in finding["path"]
        and "tests/" in finding["evidence"]
        for finding in payload["findings"]
    )


def test_streaming_audit_detects_processed_packets_without_policy(tmp_path: Path):
    output_json, _, _ = run_audit(tmp_path)
    payload = json.loads(output_json.read_text(encoding="utf-8"))

    assert any(
        finding["rule_id"] == "processed_packets_without_memory_policy"
        and finding["severity"] == "high"
        and finding["path"] == "src/eco_core/enteric_orchestrator.py"
        for finding in payload["findings"]
    )


def test_streaming_audit_warns_no_refactor_and_does_not_modify_code(tmp_path: Path):
    before = file_digests()
    output_json, output_md, result = run_audit(tmp_path)
    after = file_digests()

    assert result.returncode == 0
    assert before == after

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    markdown = output_md.read_text(encoding="utf-8").lower()

    assert "no refactor todavia" in payload["summary"]["baseline_gate"].lower()
    assert "no refactor todavia" in markdown
