#!/usr/bin/env python3
"""Validate the E.C.O. adaptive dataset synthetic example.

This validator is intentionally structural and responsible-use oriented.
It does not ingest real data, train models, modify baselines, or recalibrate thresholds.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JSON_DOC = ROOT / "docs" / "architecture" / "eco-adaptive-dataset-example.json"
MD_DOC = ROOT / "docs" / "architecture" / "eco-adaptive-dataset-example.md"

REQUIRED_LIMITS = (
    "synthetic_only",
    "no_real_data",
    "no_sensitive_data",
    "no_private_genetic_data",
    "no_training",
    "no_baseline_change",
    "no_threshold_recalibration",
    "no_biomedical_claims",
)

REQUIRED_RECORD_KEYS = {
    "record_id",
    "source_type",
    "adaptive_state",
    "signal_family",
    "evidence_level",
    "risk_flag",
    "review_status",
    "notes",
}

ALLOWED_SOURCE_TYPES = {"synthetic", "documental", "mock"}
ALLOWED_REVIEW_STATUSES = {"draft", "review_needed", "candidate", "accepted", "blocked"}

REQUIRED_MARKDOWN_TOKENS = (
    "Ejemplo sintético de dataset adaptativo E.C.O.",
    "No contiene datos reales.",
    "No contiene datos sensibles.",
    "No contiene datos genéticos privados.",
    "No entrena modelos.",
    "No modifica baseline.",
    "No recalibra umbrales.",
    "No usar este ejemplo como fuente de entrenamiento",
)


def load_json(errors: list[str]) -> dict:
    if not JSON_DOC.exists():
        errors.append(f"missing JSON example: {JSON_DOC}")
        return {}

    try:
        return json.loads(JSON_DOC.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON: {exc}")
        return {}


def validate_payload(payload: dict, errors: list[str]) -> None:
    if payload.get("classification") != "permitido":
        errors.append("classification must be permitido")

    if payload.get("scope") != "synthetic_documental_example":
        errors.append("scope must be synthetic_documental_example")

    expected_contract = "docs/architecture/eco-adaptive-dataset-contract.md"
    if payload.get("contract") != expected_contract:
        errors.append(f"contract must be {expected_contract}")

    limits = payload.get("limits")
    if not isinstance(limits, dict):
        errors.append("limits must be an object")
        limits = {}

    for key in REQUIRED_LIMITS:
        if limits.get(key) is not True:
            errors.append(f"limit must be true: {key}")

    records = payload.get("records")
    if not isinstance(records, list) or not records:
        errors.append("records must be a non-empty list")
        return

    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            errors.append(f"record {index} must be an object")
            continue

        missing = REQUIRED_RECORD_KEYS - set(record)
        extra = set(record) - REQUIRED_RECORD_KEYS

        if missing:
            errors.append(f"record {index} missing keys: {sorted(missing)}")
        if extra:
            errors.append(f"record {index} has unexpected keys: {sorted(extra)}")

        record_id = record.get("record_id", "")
        if not isinstance(record_id, str) or not record_id.startswith("eco-synth-adaptive-"):
            errors.append(f"record {index} has invalid record_id")

        if record.get("source_type") not in ALLOWED_SOURCE_TYPES:
            errors.append(f"record {index} has invalid source_type")

        if record.get("review_status") not in ALLOWED_REVIEW_STATUSES:
            errors.append(f"record {index} has invalid review_status")

        notes = record.get("notes")
        if not isinstance(notes, str) or not notes.strip():
            errors.append(f"record {index} must include non-empty notes")


def validate_markdown(errors: list[str]) -> None:
    if not MD_DOC.exists():
        errors.append(f"missing Markdown guide: {MD_DOC}")
        return

    content = MD_DOC.read_text(encoding="utf-8")
    for token in REQUIRED_MARKDOWN_TOKENS:
        if token not in content:
            errors.append(f"Markdown guide missing token: {token}")


def main() -> int:
    errors: list[str] = []
    payload = load_json(errors)

    if payload:
        validate_payload(payload, errors)

    validate_markdown(errors)

    print("# E.C.O. adaptive dataset example validation")

    if errors:
        print("Estado: failed")
        for error in errors:
            print(f"- {error}")
        return 1

    records = payload.get("records", [])
    print("Estado: passed")
    print(f"JSON validado: {JSON_DOC.relative_to(ROOT)}")
    print(f"Markdown validado: {MD_DOC.relative_to(ROOT)}")
    print(f"Registros sintéticos: {len(records)}")
    print("Límite: ejemplo sintético documental; sin datos reales; sin entrenamiento; sin baseline; sin recalibración.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
