"""
Exporta trazabilidad digestiva S.N.E.-E.C.O.
==========================================

Genera una vista por paquete del tránsito interno del intestino informacional:
barrera, motilidad, defensa, decisión final, estado final y memoria microbiota.

Uso:
    python scripts/run_sne_eco_trace.py
    python scripts/run_sne_eco_trace.py --output-json results/sne_eco_packet_trace.json --output-md results/sne_eco_packet_trace.md
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

from src.eco_core import EntericSystem, build_packet_traces, traces_to_markdown


TRACE_PACKETS = (
    ("valid_sequence", "ACGTCCAATGGTATAAA"),
    ("invalid_sequence", "ACGTXYZ"),
    ("short_sequence", "ACG"),
    ("duplicate_sequence", "ACGTCCAATGGTATAAA"),
)


def run_trace_demo() -> tuple[EntericSystem, list[dict[str, Any]], str]:
    system = EntericSystem(min_length=6, max_n_percent=25.0, heavy_payload_threshold=10_000)
    for source, sequence in TRACE_PACKETS:
        system.process_dna_sequence(sequence, source=source)

    traces = build_packet_traces(system.processed_packets)
    trace_dicts = [trace.to_dict() for trace in traces]
    markdown = traces_to_markdown(traces)
    return system, trace_dicts, markdown


def build_trace_payload(system: EntericSystem, traces: list[dict[str, Any]], markdown: str) -> dict[str, Any]:
    snapshot = system.homeostasis_snapshot()
    return {
        "title": "S.N.E.-E.C.O. PACKET TRACE",
        "status": "ok",
        "processed_packets": snapshot.total_packets,
        "state": snapshot.state,
        "traces": traces,
        "markdown": markdown,
        "technical_limit": "Traza técnica de pipeline; no representa conclusión clínica ni interpretación personal.",
    }


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Exporta trazabilidad digestiva por paquete para S.N.E.-E.C.O.")
    parser.add_argument("--output-json", type=Path, default=None, help="Ruta opcional para guardar JSON de trazas.")
    parser.add_argument("--output-md", type=Path, default=None, help="Ruta opcional para guardar Markdown de trazas.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    system, traces, markdown = run_trace_demo()
    payload = build_trace_payload(system, traces, markdown)

    print(markdown)
    print("")
    print("OK: trazabilidad digestiva S.N.E.-E.C.O. generada.")

    if args.output_json:
        write_json(args.output_json, payload)
    if args.output_md:
        write_text(args.output_md, markdown)


if __name__ == "__main__":
    main()
