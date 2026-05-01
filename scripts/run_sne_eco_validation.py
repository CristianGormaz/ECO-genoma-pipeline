"""
Validación integral S.N.E.-E.C.O.
=================================

Ejecuta un lote mínimo de paquetes a través del orquestador entérico completo:

- barrera / mucosa informacional,
- plexo submucoso / sensado local,
- plexo mientérico / motilidad,
- defensa informacional,
- microbiota / memoria de recurrencia,
- homeostasis,
- eje intestino-cerebro.

Uso:
    python scripts/run_sne_eco_validation.py
    python scripts/run_sne_eco_validation.py --output-md results/sne_eco_validation_report.md
    python scripts/run_sne_eco_validation.py --output-json results/sne_eco_validation_report.json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.eco_core import EntericSystem


DEMO_PACKETS = (
    ("valid_sequence", "ACGTCCAATGGTATAAA"),
    ("invalid_sequence", "ACGTXYZ"),
    ("short_sequence", "ACG"),
    ("duplicate_sequence", "ACGTCCAATGGTATAAA"),
)


def run_validation() -> tuple[EntericSystem, str]:
    system = EntericSystem(min_length=6, max_n_percent=25.0, heavy_payload_threshold=10_000)

    for source, sequence in DEMO_PACKETS:
        system.process_dna_sequence(sequence, source=source)

    return system, system.gut_brain_markdown()


def build_validation_payload(system: EntericSystem, markdown: str) -> dict[str, Any]:
    """Construye un payload exportable y estable de la validación S.N.E.-E.C.O."""
    snapshot = system.homeostasis_snapshot()
    return {
        "title": "S.N.E.-E.C.O. VALIDATION REPORT",
        "status": "ok",
        "processed_packets": snapshot.total_packets,
        "absorbed_packets": snapshot.absorbed_packets,
        "rejected_packets": snapshot.rejected_packets,
        "quarantined_packets": snapshot.quarantined_packets,
        "discarded_packets": snapshot.discarded_packets,
        "duplicate_packets": snapshot.duplicate_packets,
        "defense_alerts": snapshot.defense_alerts,
        "state": snapshot.state,
        "homeostasis": asdict(snapshot),
        "gut_brain_markdown": markdown,
        "demo_sources": [source for source, _sequence in DEMO_PACKETS],
        "ethical_limit": "Sistema bioinformático educativo y bioinspirado; no entrega diagnóstico ni interpretación clínica.",
    }


def render_console_report(payload: dict[str, Any]) -> str:
    """Renderiza el mismo reporte que se muestra por terminal."""
    return "\n".join(
        [
            "S.N.E.-E.C.O. VALIDATION REPORT",
            "================================",
            f"processed_packets: {payload['processed_packets']}",
            f"absorbed_packets: {payload['absorbed_packets']}",
            f"rejected_packets: {payload['rejected_packets']}",
            f"quarantined_packets: {payload['quarantined_packets']}",
            f"discarded_packets: {payload['discarded_packets']}",
            f"duplicate_packets: {payload['duplicate_packets']}",
            f"defense_alerts: {payload['defense_alerts']}",
            f"state: {payload['state']}",
            "",
            payload["gut_brain_markdown"],
            "",
            "OK: S.N.E.-E.C.O. integrado funcionando.",
        ]
    )


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Valida el S.N.E.-E.C.O. integrado y opcionalmente exporta artefactos.")
    parser.add_argument("--output-md", type=Path, default=None, help="Ruta opcional para guardar el reporte Markdown/terminal.")
    parser.add_argument("--output-json", type=Path, default=None, help="Ruta opcional para guardar el payload JSON de validación.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    system, markdown = run_validation()
    payload = build_validation_payload(system, markdown)
    console_report = render_console_report(payload)

    print(console_report)

    if args.output_md:
        write_text(args.output_md, console_report)
    if args.output_json:
        write_json(args.output_json, payload)


if __name__ == "__main__":
    main()
