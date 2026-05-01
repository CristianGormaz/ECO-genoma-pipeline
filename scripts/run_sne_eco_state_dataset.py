"""
Exporta dataset adaptativo S.N.E.-E.C.O.
=======================================

Genera filas de transición entrenables:
packet_trace + homeostasis_before + homeostasis_after.

Uso:
    python scripts/run_sne_eco_state_dataset.py
    python scripts/run_sne_eco_state_dataset.py --extended --output-json results/sne_eco_state_dataset_extended.json --output-tsv results/sne_eco_state_dataset_extended.tsv
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.eco_core import adaptive_rows_to_markdown, build_adaptive_state_rows, get_transition_packets, rows_to_dicts


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Exporta dataset adaptativo de transiciones S.N.E.-E.C.O.")
    parser.add_argument("--extended", action="store_true", help="Usa escenarios sintéticos extendidos.")
    parser.add_argument("--output-json", type=Path, default=None, help="Ruta opcional para guardar JSON.")
    parser.add_argument("--output-tsv", type=Path, default=None, help="Ruta opcional para guardar TSV.")
    return parser.parse_args()


def build_payload(*, extended: bool = False) -> dict[str, Any]:
    packets = get_transition_packets(extended=extended)
    rows = build_adaptive_state_rows(packets)
    row_dicts = rows_to_dicts(rows)
    return {
        "title": "S.N.E.-E.C.O. ADAPTIVE STATE DATASET",
        "status": "ok",
        "scenario_set": "extended" if extended else "default",
        "row_count": len(row_dicts),
        "rows": row_dicts,
        "markdown": adaptive_rows_to_markdown(rows),
        "responsible_limit": "Dataset técnico/educativo; no modela conciencia humana ni uso clínico/forense.",
    }


def main() -> None:
    args = parse_args()
    payload = build_payload(extended=args.extended)

    print(payload["markdown"])
    print("")
    print("OK: dataset adaptativo S.N.E.-E.C.O. generado.")

    if args.output_json:
        write_json(args.output_json, payload)
    if args.output_tsv:
        write_tsv(args.output_tsv, payload["rows"])


if __name__ == "__main__":
    main()
