import json
import subprocess
import sys
from pathlib import Path

from src.eco_core import EntericSystem


ROOT = Path(__file__).resolve().parents[1]
VALIDATION_SCRIPT = ROOT / "scripts" / "run_sne_eco_validation.py"
ENTERIC_REPORT_SCRIPT = ROOT / "scripts" / "run_eco_enteric_report.py"
CANONICAL_FLOW = (
    ("valid_sequence", "ACGTCCAATGGTATAAA"),
    ("invalid_sequence", "ACGTXYZ"),
    ("short_sequence", "ACG"),
    ("duplicate_sequence", "ACGTCCAATGGTATAAA"),
)


def build_canonical_system() -> EntericSystem:
    system = EntericSystem(min_length=6, max_n_percent=25.0, heavy_payload_threshold=10_000)
    for source, sequence in CANONICAL_FLOW:
        system.process_dna_sequence(sequence, source=source)
    return system


def test_canonical_homeostasis_state_is_single_and_consistent():
    system = build_canonical_system()

    snapshot = system.homeostasis_snapshot()
    legacy_report = system.homeostasis_report()

    assert snapshot.state == "watch"
    assert legacy_report.state == snapshot.state
    assert legacy_report.total_packets == snapshot.total_packets
    assert legacy_report.absorbed_packets == snapshot.absorbed_packets
    assert legacy_report.quarantined_packets == snapshot.quarantined_packets
    assert legacy_report.discarded_packets == snapshot.discarded_packets
    assert legacy_report.rejected_packets == snapshot.rejected_packets
    assert legacy_report.duplicate_packets == snapshot.duplicate_packets
    assert legacy_report.notes == list(snapshot.notes)


def test_public_homeostasis_reports_do_not_diverge_for_canonical_flow(tmp_path: Path):
    validation_json = tmp_path / "sne_validation.json"
    validation_md = tmp_path / "sne_validation.md"
    enteric_json = tmp_path / "enteric_report.json"
    enteric_md = tmp_path / "enteric_report.md"

    validation_result = subprocess.run(
        [
            sys.executable,
            str(VALIDATION_SCRIPT),
            "--output-json",
            str(validation_json),
            "--output-md",
            str(validation_md),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    enteric_result = subprocess.run(
        [
            sys.executable,
            str(ENTERIC_REPORT_SCRIPT),
            "--output-json",
            str(enteric_json),
            "--output-md",
            str(enteric_md),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert validation_result.returncode == 0, validation_result.stderr
    assert enteric_result.returncode == 0, enteric_result.stderr

    validation_payload = json.loads(validation_json.read_text(encoding="utf-8"))
    enteric_payload = json.loads(enteric_json.read_text(encoding="utf-8"))

    assert validation_payload["state"] == "watch"
    assert validation_payload["homeostasis"]["state"] == "watch"
    assert enteric_payload["homeostasis"]["state"] == "watch"
    assert validation_payload["state"] == enteric_payload["homeostasis"]["state"]
