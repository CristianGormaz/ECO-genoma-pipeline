from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_TOP_LEVEL = {"title", "scope", "trace", "summary", "limits"}
REQUIRED_TRACE_KEYS = {"tick", "nutrient", "signal", "waste", "stability", "action"}
ALLOWED_ACTIONS = {"digest", "rest"}


EXPECTED_SUMMARY = {
    "classification": "allowed",
    "data_policy": "synthetic_only",
    "training": False,
    "sensitive_data": False,
    "baseline_changed": False,
    "threshold_recalibrated": False,
}


def validate_payload(data: dict) -> list[str]:
    errors: list[str] = []

    missing_top_level = REQUIRED_TOP_LEVEL - set(data)
    if missing_top_level:
        errors.append("missing top-level keys: " + ", ".join(sorted(missing_top_level)))

    trace = data.get("trace")
    summary = data.get("summary")
    limits = data.get("limits")

    if not isinstance(trace, list) or not trace:
        errors.append("trace must be a non-empty list")

    if not isinstance(summary, dict):
        errors.append("summary must be a dictionary")
    else:
        for key, expected in EXPECTED_SUMMARY.items():
            if summary.get(key) != expected:
                errors.append(f"summary.{key} must be {expected!r}")

        if isinstance(trace, list) and trace:
            if summary.get("ticks") != len(trace):
                errors.append("summary.ticks must match trace length")
            if summary.get("final_state") != trace[-1]:
                errors.append("summary.final_state must match last trace item")

    if not isinstance(limits, list) or not limits:
        errors.append("limits must be a non-empty list")

    if isinstance(trace, list):
        for index, item in enumerate(trace, start=1):
            if not isinstance(item, dict):
                errors.append(f"trace item {index} must be a dictionary")
                continue

            missing_trace_keys = REQUIRED_TRACE_KEYS - set(item)
            if missing_trace_keys:
                errors.append(f"trace item {index} missing keys: " + ", ".join(sorted(missing_trace_keys)))

            if not isinstance(item.get("tick"), int) or item.get("tick", 0) < 1:
                errors.append(f"trace item {index} tick must be an integer >= 1")

            for key in ["nutrient", "signal", "waste", "stability"]:
                if not isinstance(item.get(key), int) or item.get(key, -1) < 0:
                    errors.append(f"trace item {index} {key} must be a non-negative integer")

            if item.get("action") not in ALLOWED_ACTIONS:
                errors.append(f"trace item {index} action must be one of: digest, rest")

    return errors


def validate_file(path: Path) -> list[str]:
    if not path.exists():
        return ["file does not exist: " + str(path)]

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return ["payload must be a JSON object"]

    return validate_payload(data)


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    path = Path(args[0]) if args else Path("results/eco_minimal_simulation_demo.json")

    errors = validate_file(path)
    if errors:
        print("# E.C.O. synthetic contract validation")
        print("Estado: failed")
        for error in errors:
            print("- " + error)
        return 1

    print("# E.C.O. synthetic contract validation")
    print("Estado: passed")
    print("Archivo validado: " + str(path))
    print("Límite: datos sintéticos; sin entrenamiento; sin datos sensibles; sin recalibración.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
