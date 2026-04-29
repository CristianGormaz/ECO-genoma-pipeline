#!/usr/bin/env python3
"""
Revisión humana del reporte integrado E.C.O.
===========================================

Lee el JSON generado por scripts/run_eco_demo_pipeline.py y muestra una
bitácora digestiva resumida para lectura humana.

Uso recomendado desde la raíz del repositorio:

    python3 scripts/review_eco_demo_report.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = PROJECT_ROOT / "results" / "eco_demo_pipeline_report.json"


def load_report(path: Path) -> Dict[str, Any]:
    """Carga el reporte JSON integrado de E.C.O."""
    if not path.exists():
        raise FileNotFoundError(
            f"No existe el reporte: {path}. Ejecuta primero: make demo"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def get_motif_names(sequence_entry: Dict[str, Any]) -> List[str]:
    """Extrae nombres de motivos desde una entrada de secuencia."""
    motif_report = sequence_entry.get("motif_report") or {}
    hits = motif_report.get("hits") or []
    return [hit.get("motif_name", "motivo_desconocido") for hit in hits]


def print_report_review(report: Dict[str, Any]) -> None:
    """Imprime una revisión legible del reporte integrado."""
    summary = report["summary"]
    feedback = summary["feedback"]

    print("E.C.O. REPORT REVIEW")
    print("====================")
    print(f"Pipeline: {report['pipeline']}")
    print(f"BED: {report['inputs']['bed']}")
    print(f"Referencia: {report['inputs']['reference']}")
    print(f"FASTA generado: {report['outputs']['fasta']}")
    print(f"JSON revisado: {report['outputs']['json']}")

    print("\nResumen digestivo")
    print("-----------------")
    print(f"Regiones procesadas: {summary['regions_processed']}")
    print(f"Motivos encontrados: {summary['total_motif_hits']}")
    print(f"Paquetes aceptados: {feedback['accepted_packets']}")
    print(f"Paquetes rechazados: {feedback['rejected_packets']}")
    print(f"Paquetes absorbidos: {feedback['absorbed_packets']}")
    print(f"Tasa de rechazo: {feedback['rejection_rate']}%")
    print(f"Tasa de absorción: {feedback['absorbed_rate']}%")

    notes = feedback.get("notes") or []
    if notes:
        print("Notas del sistema:")
        for note in notes:
            print(f"  - {note}")
    else:
        print("Notas del sistema: sin alertas.")

    print("\nDetalle por región")
    print("------------------")
    for index, entry in enumerate(report["sequences"], start=1):
        metadata = entry.get("metadata", {})
        features = metadata.get("absorbed_features", {})
        motif_names = get_motif_names(entry)
        history_status = " -> ".join(
            f"{item['stage']}:{item['status']}" for item in entry.get("history", [])
        )

        print(f"{index}. {entry['sequence_id']}")
        print(f"   Historial: {history_status}")
        print(f"   Longitud: {features.get('length', 'n/a')} bp")
        print(f"   GC: {features.get('gc_percent', 'n/a')}%")
        print(f"   N ambiguas: {features.get('n_percent', 'n/a')}%")
        print(f"   Motivos: {', '.join(motif_names) if motif_names else 'sin motivos'}")

    print("\nLectura final")
    print("-------------")
    if feedback["rejected_packets"] == 0 and feedback["absorbed_packets"] == summary["regions_processed"]:
        print("OK: el reporte muestra digestión informacional completa y sin rechazos.")
    else:
        print("REVISAR: el reporte muestra rechazos o absorción incompleta.")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Revisa en formato humano el JSON integrado generado por la demo E.C.O."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_REPORT,
        help="Ruta al JSON integrado. Por defecto usa results/eco_demo_pipeline_report.json.",
    )
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    try:
        report = load_report(args.input)
        print_report_review(report)
        feedback = report["summary"]["feedback"]
        return 0 if feedback["rejected_packets"] == 0 else 1
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
