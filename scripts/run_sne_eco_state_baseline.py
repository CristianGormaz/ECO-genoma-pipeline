"""
Exporta baseline adaptativo E.C.O. v0
====================================

Entrena/evalúa un baseline categórico mínimo sobre el dataset adaptativo
S.N.E.-E.C.O. y exporta reporte JSON/Markdown.
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
    baseline_report_to_markdown,
    build_adaptive_state_rows,
    evaluate_state_transition_baseline,
    get_transition_packets,
)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Exporta baseline adaptativo E.C.O. v0.")
    parser.add_argument("--extended", action="store_true", help="Usa escenarios sintéticos extendidos.")
    parser.add_argument("--output-json", type=Path, default=None, help="Ruta opcional para guardar JSON.")
    parser.add_argument("--output-md", type=Path, default=None, help="Ruta opcional para guardar Markdown.")
    return parser.parse_args()


def build_payload(*, extended: bool = False) -> tuple[dict[str, Any], str]:
    rows = build_adaptive_state_rows(get_transition_packets(extended=extended))
    report = evaluate_state_transition_baseline(rows)
    report["scenario_set"] = "extended" if extended else "default"
    markdown = baseline_report_to_markdown(report)
    return report, markdown


def main() -> None:
    args = parse_args()
    report, markdown = build_payload(extended=args.extended)

    print(markdown)
    print("")
    print("OK: baseline adaptativo E.C.O. v0 generado.")

    if args.output_json:
        write_json(args.output_json, report)
    if args.output_md:
        write_text(args.output_md, markdown)


if __name__ == "__main__":
    main()
