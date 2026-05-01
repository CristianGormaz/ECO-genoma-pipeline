"""
Exporta diagnóstico de cobertura adaptativa E.C.O.
=================================================

Analiza cobertura de rutas digestivas del dataset extendido y relaciona el
resultado con la evaluación holdout del baseline adaptativo.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.eco_core import (
    build_adaptive_state_rows,
    build_coverage_diagnostics,
    coverage_report_to_markdown,
    evaluate_state_transition_holdout,
    get_transition_packets,
)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Exporta diagnóstico de cobertura adaptativa E.C.O.")
    parser.add_argument("--extended", action="store_true", help="Usa escenarios sintéticos extendidos.")
    parser.add_argument("--output-json", type=Path, default=None, help="Ruta opcional para guardar JSON.")
    parser.add_argument("--output-md", type=Path, default=None, help="Ruta opcional para guardar Markdown.")
    return parser.parse_args()


def build_payload(*, extended: bool = False) -> tuple[dict[str, object], str]:
    rows = build_adaptive_state_rows(get_transition_packets(extended=extended))
    evaluation = evaluate_state_transition_holdout(rows)
    diagnostics = build_coverage_diagnostics(rows, evaluation=evaluation)
    payload = diagnostics.to_dict()
    payload["scenario_set"] = "extended" if extended else "default"
    payload["accuracy_holdout"] = evaluation.accuracy_holdout
    payload["macro_f1_holdout"] = evaluation.macro_f1_holdout
    markdown = coverage_report_to_markdown(diagnostics)
    return payload, markdown


def main() -> None:
    args = parse_args()
    payload, markdown = build_payload(extended=args.extended)

    print(markdown)
    print("")
    print("OK: diagnóstico de cobertura adaptativa E.C.O. generado.")

    if args.output_json:
        write_json(args.output_json, payload)
    if args.output_md:
        write_text(args.output_md, markdown)


if __name__ == "__main__":
    main()
