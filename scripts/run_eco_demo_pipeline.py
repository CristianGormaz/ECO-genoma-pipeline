#!/usr/bin/env python3
"""
Demo integrada del pipeline E.C.O.
=================================

Ejecuta el primer recorrido completo del metabolismo informacional:

BED -> FASTA -> eco_core -> análisis de motivos -> reporte integrado

Uso recomendado desde la raíz del repositorio:

    python3 scripts/run_eco_demo_pipeline.py
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
import sys
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from eco_bed_to_fasta import bed_to_fasta, format_fasta, parse_bed, parse_fasta  # noqa: E402
from eco_motif_analysis import scan_sequence  # noqa: E402
from src.eco_core import absorb_sequence_features, build_feedback_summary, discard_packet, ingest_text  # noqa: E402
from src.eco_core.filtering import filter_dna_packet, has_rejection  # noqa: E402
from src.eco_core.flow import EcoPacket  # noqa: E402


def packet_history_as_dict(packet: EcoPacket) -> List[Dict[str, Any]]:
    """Devuelve el historial de un paquete como estructura serializable."""
    return [asdict(log) for log in packet.history]


def absorb_packet(packet: EcoPacket) -> EcoPacket:
    """Absorbe features genómicas si el paquete no fue rechazado."""
    if has_rejection(packet):
        return packet

    packet.metadata["absorbed_features"] = absorb_sequence_features(packet.payload)
    packet.log(
        stage="absorption",
        status="ok",
        message="Features genómicas básicas absorbidas como nutrientes informacionales.",
    )
    return packet


def build_sequence_entry(record_id: str, sequence: str) -> tuple[EcoPacket, Dict[str, Any]]:
    """Procesa una secuencia por eco_core y análisis de motivos."""
    packet = ingest_text(sequence, source=record_id, packet_type="dna")
    packet = filter_dna_packet(packet)
    packet = absorb_packet(packet)

    motif_report = None
    if has_rejection(packet):
        discard = discard_packet(packet, reason="Secuencia descartada por filtro de calidad.")
        packet.metadata["discard_record"] = asdict(discard)
    else:
        motif_report = scan_sequence(packet.payload, sequence_id=record_id)
        packet.metadata["motif_hits"] = len(motif_report.hits)

    entry: Dict[str, Any] = {
        "sequence_id": record_id,
        "packet_id": packet.packet_id,
        "history": packet_history_as_dict(packet),
        "metadata": packet.metadata,
        "motif_report": asdict(motif_report) if motif_report else None,
    }
    return packet, entry


def run_demo_pipeline(
    bed_path: Path,
    reference_path: Path,
    output_fasta: Path,
    output_json: Path,
) -> Dict[str, Any]:
    """Ejecuta BED -> FASTA -> eco_core -> motivos -> JSON integrado."""
    reference = parse_fasta(reference_path)
    regions = parse_bed(bed_path)
    fasta_records = bed_to_fasta(reference, regions)

    output_fasta.parent.mkdir(parents=True, exist_ok=True)
    output_fasta.write_text(format_fasta(fasta_records), encoding="utf-8")

    packets: List[EcoPacket] = []
    sequence_entries: List[Dict[str, Any]] = []
    for record in fasta_records:
        packet, entry = build_sequence_entry(record.sequence_id, record.sequence)
        packets.append(packet)
        sequence_entries.append(entry)

    feedback = build_feedback_summary(packets)
    total_motif_hits = sum(entry["metadata"].get("motif_hits", 0) for entry in sequence_entries)

    report: Dict[str, Any] = {
        "pipeline": "BED -> FASTA -> eco_core -> motif_analysis -> integrated_report",
        "inputs": {
            "bed": str(bed_path),
            "reference": str(reference_path),
        },
        "outputs": {
            "fasta": str(output_fasta),
            "json": str(output_json),
        },
        "summary": {
            "regions_processed": len(fasta_records),
            "total_motif_hits": total_motif_hits,
            "feedback": asdict(feedback),
        },
        "sequences": sequence_entries,
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def print_demo_summary(report: Dict[str, Any]) -> None:
    """Imprime una salida humana breve para UX de terminal."""
    feedback = report["summary"]["feedback"]

    print("E.C.O. DEMO PIPELINE REPORT")
    print("===========================")
    print("Flujo: BED -> FASTA -> eco_core -> análisis de motivos -> reporte integrado")
    print(f"Regiones procesadas: {report['summary']['regions_processed']}")
    print(f"Motivos encontrados: {report['summary']['total_motif_hits']}")
    print(f"Aceptados: {feedback['accepted_packets']}")
    print(f"Rechazados: {feedback['rejected_packets']}")
    print(f"Absorbidos: {feedback['absorbed_packets']}")
    print(f"Tasa de rechazo: {feedback['rejection_rate']}%")
    print(f"FASTA generado: {report['outputs']['fasta']}")
    print(f"Reporte JSON: {report['outputs']['json']}")

    if feedback["rejected_packets"] == 0 and feedback["absorbed_packets"] == report["summary"]["regions_processed"]:
        print("Estado: OK, intestino informacional demo funcionando.")
    else:
        print("Estado: REVISAR, el flujo demo produjo rechazos o absorción incompleta.")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ejecuta una demo integrada BED -> FASTA -> eco_core -> análisis de motivos."
    )
    parser.add_argument(
        "--bed",
        type=Path,
        default=PROJECT_ROOT / "examples" / "demo_regions.bed",
        help="Archivo BED de entrada. Por defecto usa examples/demo_regions.bed.",
    )
    parser.add_argument(
        "--reference",
        type=Path,
        default=PROJECT_ROOT / "examples" / "tiny_reference.fa",
        help="FASTA de referencia. Por defecto usa examples/tiny_reference.fa.",
    )
    parser.add_argument(
        "--output-fasta",
        type=Path,
        default=PROJECT_ROOT / "results" / "eco_demo_pipeline.fa",
        help="Ruta para guardar FASTA intermedio generado.",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=PROJECT_ROOT / "results" / "eco_demo_pipeline_report.json",
        help="Ruta para guardar reporte JSON integrado.",
    )
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    try:
        report = run_demo_pipeline(
            bed_path=args.bed,
            reference_path=args.reference,
            output_fasta=args.output_fasta,
            output_json=args.output_json,
        )
        print_demo_summary(report)
        feedback = report["summary"]["feedback"]
        return 0 if feedback["rejected_packets"] == 0 else 1
    except (FileNotFoundError, ValueError) as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
