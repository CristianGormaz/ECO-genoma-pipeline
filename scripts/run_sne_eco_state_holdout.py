"""
Exporta evaluación holdout del baseline adaptativo E.C.O.
=========================================================

Genera una evaluación mínima con separación entrenamiento/prueba para evitar
confundir funcionamiento con generalización.
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
    DEFAULT_TRANSITION_PACKETS,
    build_adaptive_state_rows,
    evaluate_state_transition_holdout,
    holdout_report_to_markdown,
)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Exporta evaluación holdout E.C.O. v0.")
    parser.add_argument("--output-json", type=Path, default=None, help="Ruta opcional para guardar JSON.")
    parser.add_argument("--output-md", type=Path, default=None, help="Ruta opcional para guardar Markdown.")
    return parser.parse_args()


def build_payload() -> tuple[dict[str, object], str]:
    rows = build_adaptive_state_rows(DEFAULT_TRANSITION_PACKETS)
    evaluation = evaluate_state_transition_holdout(rows)
    payload = evaluation.to_dict()
    markdown = holdout_report_to_markdown(evaluation)
    return payload, markdown


def main() -> None:
    args = parse_args()
    payload, markdown = build_payload()

    print(markdown)
    print("")
    print("OK: evaluación holdout adaptativa E.C.O. v0 generada.")

    if args.output_json:
        write_json(args.output_json, payload)
    if args.output_md:
        write_text(args.output_md, markdown)


if __name__ == "__main__":
    main()
