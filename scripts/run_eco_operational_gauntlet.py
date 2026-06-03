#!/usr/bin/env python3
"""E.C.O. Operational Gauntlet v1.

Batería sintética mínima para detectar regresiones en bordes operativos
corregidos recientemente. No usa datos reales, no descarga dependencias, no
entrena modelos y no modifica baseline ni recalibra umbrales.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from typing import Callable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from src.eco_core import EntericSystem
from src.eco_motif_analysis import parse_fasta
from src.eco_sequence_classifier import LabeledSequence, confidence_from_distances, prediction_from_features

RESULTS_DIR = PROJECT_ROOT / "results"
JSON_OUTPUT = RESULTS_DIR / "eco_operational_gauntlet.json"
MD_OUTPUT = RESULTS_DIR / "eco_operational_gauntlet.md"

LIMITS = [
    "sin datos reales",
    "sin entrenamiento",
    "sin baseline",
    "sin recalibración",
    "sin afirmaciones biomédicas aplicadas",
]
CHECK_LIMIT = (
    "prueba sintética interna; sin datos reales; sin entrenamiento; "
    "sin baseline; sin recalibración; sin afirmaciones biomédicas aplicadas"
)

CANONICAL_FLOW = (
    ("valid_sequence", "ACGTCCAATGGTATAAA"),
    ("invalid_sequence", "ACGTXYZ"),
    ("short_sequence", "ACG"),
    ("duplicate_sequence", "ACGTCCAATGGTATAAA"),
)


def load_script_module(module_name: str, script_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise ImportError(f"No se pudo cargar el módulo desde {script_path}")
    spec.loader.exec_module(module)
    return module


def build_canonical_system() -> EntericSystem:
    system = EntericSystem(min_length=6, max_n_percent=25.0, heavy_payload_threshold=10_000)
    for source, sequence in CANONICAL_FLOW:
        system.process_dna_sequence(sequence, source=source)
    return system


def build_gate_states(
    *,
    source_admission_decision_summary: str = "passed",
    sensitive_intake_gate: str = "passed",
    governed_ml_evaluation_gate: str = "passed",
) -> list[dict]:
    return [
        {
            "id": "source_admission_decision_summary",
            "state": source_admission_decision_summary,
            "output": "results/source.json",
            "signals": {},
        },
        {
            "id": "sensitive_intake_gate",
            "state": sensitive_intake_gate,
            "output": "results/intake.json",
            "signals": {},
        },
        {
            "id": "governed_ml_evaluation_gate",
            "state": governed_ml_evaluation_gate,
            "output": "results/ml.json",
            "signals": {},
        },
    ]


def classifier_exact_tie_confidence() -> str:
    confidence = confidence_from_distances({"regulatory": 0.0, "non_regulatory": 0.0})
    assert confidence == 0.0
    return f"confidence={confidence}"


def classifier_raw_distance_prediction() -> str:
    record = LabeledSequence(sequence_id="seq_tie_margin", sequence="A", label="regulatory")
    features = {"axis": 0.0}
    centroids = {
        "non_regulatory": {"axis": 0.000049},
        "regulatory": {"axis": 0.000041},
    }
    prediction = prediction_from_features(record, features, centroids)
    assert prediction.predicted_label == "regulatory"
    assert prediction.confidence == 0.1633
    assert prediction.distances == {"non_regulatory": 0.0, "regulatory": 0.0}
    return (
        f"predicted_label={prediction.predicted_label}, "
        f"confidence={prediction.confidence}, distances={prediction.distances}"
    )


def motif_rejects_plain_text_fasta() -> str:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".fa", delete=False) as handle:
        handle.write("ACGT\nTATAAA\n")
        temp_path = Path(handle.name)
    try:
        try:
            parse_fasta(temp_path)
        except ValueError as exc:
            assert "cabecera '>'" in str(exc)
            return str(exc)
        raise AssertionError("parse_fasta aceptó contenido plano sin cabecera FASTA.")
    finally:
        temp_path.unlink(missing_ok=True)


def homeostasis_public_paths_consistent() -> str:
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
    return f"state={snapshot.state}, total_packets={snapshot.total_packets}"


def readiness_report_does_not_claim_live_green() -> str:
    module = load_script_module(
        "run_eco_readiness_report",
        PROJECT_ROOT / "scripts" / "run_eco_readiness_report.py",
    )
    report = module.build_report()
    required_terms = [
        "readiness report sintético",
        "no verifica el estado actual de git",
        "no ejecuta pytest",
        "no debe interpretarse como prueba de que el repo está green",
        "ejecutar make eco-status",
        "ejecutar pytest",
        "ejecutar make eco-check-clean",
    ]
    for term in required_terms:
        assert term in report
    assert "eco-status green" not in report
    assert "pytest passing" not in report
    return "readiness report marcado como sintético/no live"


def eco_status_green_requires_clean_main_synced() -> str:
    module = load_script_module(
        "run_eco_status",
        PROJECT_ROOT / "scripts" / "run_eco_status.py",
    )
    assert module.compute_operational_state(clean=True, on_main=True, synced=True) == "green"
    assert module.compute_operational_state(clean=True, on_main=False, synced=True) == "attention"
    assert module.compute_operational_state(clean=True, on_main=True, synced=False) == "attention"
    assert module.compute_operational_state(clean=False, on_main=True, synced=True) == "attention"
    assert module.is_synced_with_origin_main(head="abc123", origin_main="abc123") is True
    assert module.is_synced_with_origin_main(head="abc123", origin_main="def456") is False
    return "green solo para clean && on_main && synced"


def governed_admission_blocks_on_relevant_gates() -> str:
    module = load_script_module(
        "run_eco_governed_experimental_cycle",
        PROJECT_ROOT / "scripts" / "run_eco_governed_experimental_cycle.py",
    )
    scenarios = [
        ("source_admission_decision_summary", build_gate_states(source_admission_decision_summary="blocked")),
        ("governed_ml_evaluation_gate", build_gate_states(governed_ml_evaluation_gate="blocked")),
        ("intake_gate", build_gate_states(sensitive_intake_gate="blocked")),
    ]
    degraded = []
    happy_path = module.build_governed_admission(
        gates=build_gate_states(),
        maturity_score={"state": "passed", "output": "results/maturity.json"},
        rollback_visibility={"status": "passed", "output": "results/rollback.json"},
    )
    assert happy_path["status"] == "passed"
    for check_id, gates in scenarios:
        report = module.build_governed_admission(
            gates=gates,
            maturity_score={"state": "passed", "output": "results/maturity.json"},
            rollback_visibility={"status": "passed", "output": "results/rollback.json"},
        )
        checks = {item["id"]: item["state"] for item in report["checks"]}
        assert report["status"] == "blocked"
        assert checks[check_id] == "blocked"
        degraded.append(f"{check_id}={report['status']}")
    return ", ".join(degraded)


def responsible_limits_not_tautological() -> str:
    module = load_script_module(
        "run_eco_governed_experimental_cycle",
        PROJECT_ROOT / "scripts" / "run_eco_governed_experimental_cycle.py",
    )
    original_limits = list(module.RESPONSIBLE_LIMITS)
    try:
        module.RESPONSIBLE_LIMITS = []
        report = module.build_governed_admission(
            gates=build_gate_states(),
            maturity_score={"state": "passed", "output": "results/maturity.json"},
            rollback_visibility={"status": "passed", "output": "results/rollback.json"},
        )
    finally:
        module.RESPONSIBLE_LIMITS = original_limits
    responsible_limits = next(item for item in report["checks"] if item["id"] == "responsible_limits")
    assert responsible_limits["state"] == "missing"
    assert "no es un gate operativo ejecutado" in responsible_limits["explanation"]
    assert report["status"] == "attention"
    return f"responsible_limits={responsible_limits['state']}"


def run_check(name: str, fn: Callable[[], str]) -> dict[str, str]:
    try:
        evidence = fn()
        status = "passed"
    except Exception as exc:  # pragma: no cover - exercised through script integration
        evidence = f"{type(exc).__name__}: {exc}"
        status = "failed"
    return {
        "name": name,
        "status": status,
        "evidence": evidence,
        "limit": CHECK_LIMIT,
    }


def build_payload() -> dict[str, object]:
    checks = [
        run_check("classifier_exact_tie_confidence", classifier_exact_tie_confidence),
        run_check("classifier_raw_distance_prediction", classifier_raw_distance_prediction),
        run_check("motif_rejects_plain_text_fasta", motif_rejects_plain_text_fasta),
        run_check("homeostasis_public_paths_consistent", homeostasis_public_paths_consistent),
        run_check("readiness_report_does_not_claim_live_green", readiness_report_does_not_claim_live_green),
        run_check("eco_status_green_requires_clean_main_synced", eco_status_green_requires_clean_main_synced),
        run_check("governed_admission_blocks_on_relevant_gates", governed_admission_blocks_on_relevant_gates),
        run_check("responsible_limits_not_tautological", responsible_limits_not_tautological),
    ]
    status = "passed" if all(check["status"] == "passed" for check in checks) else "failed"
    return {
        "title": "E.C.O. Operational Gauntlet v1",
        "status": status,
        "classification": "synthetic_operational_gauntlet",
        "checks": checks,
        "limits": LIMITS,
    }


def to_markdown(payload: dict[str, object]) -> str:
    lines = [
        "# E.C.O. Operational Gauntlet v1",
        "",
        f"Estado global: `{payload['status']}`",
        f"Clasificación: `{payload['classification']}`",
        "",
        "## Checks",
        "",
        "| Check | Estado | Evidencia |",
        "|---|---|---|",
    ]
    for check in payload["checks"]:
        lines.append(f"| `{check['name']}` | `{check['status']}` | {check['evidence']} |")
    lines.extend(["", "## Límites responsables", ""])
    for limit in payload["limits"]:
        lines.append(f"- {limit}")
    lines.append("")
    return "\n".join(lines)


def write_outputs(payload: dict[str, object]) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    MD_OUTPUT.write_text(to_markdown(payload), encoding="utf-8")


def print_summary(payload: dict[str, object]) -> None:
    print("E.C.O. Operational Gauntlet v1")
    print("==============================")
    print(f"Estado: {payload['status']}")
    for check in payload["checks"]:
        print(f"- {check['name']}: {check['status']} | {check['evidence']}")
    print(f"JSON: {JSON_OUTPUT}")
    print(f"Markdown: {MD_OUTPUT}")


def main() -> int:
    payload = build_payload()
    write_outputs(payload)
    print_summary(payload)
    return 0 if payload["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
