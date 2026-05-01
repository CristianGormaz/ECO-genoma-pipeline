#!/usr/bin/env python3
"""
Reporte exportable del Sistema Entérico Integrado E.C.O.
=======================================================

Genera un reporte JSON y Markdown desde la capa EntericSystem.

A diferencia de run_eco_enteric_demo.py, que está optimizado para lectura en
terminal, este script deja evidencia persistente en results/ para portafolio,
auditoría técnica y documentación de arquitectura.

Uso recomendado desde la raíz del repositorio:

    python3 scripts/run_eco_enteric_report.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.eco_core import EntericSystem  # noqa: E402
from src.eco_core.flow import EcoPacket  # noqa: E402


def packet_to_record(label: str, packet: EcoPacket) -> Dict[str, Any]:
    """Convierte un paquete E.C.O. procesado en registro serializable."""
    decision = packet.metadata.get("enteric_decision", {})
    sensory = packet.metadata.get("enteric_sensory_profile", {})
    features = packet.metadata.get("absorbed_features", {})

    return {
        "label": label,
        "packet_id": packet.packet_id,
        "source": packet.source,
        "payload": packet.payload,
        "decision": decision,
        "sensory_profile": {
            "length": sensory.get("length"),
            "gc_percent": sensory.get("gc_percent"),
            "n_percent": sensory.get("n_percent"),
            "invalid_characters": sensory.get("invalid_characters", []),
            "is_duplicate": sensory.get("is_duplicate"),
            "is_heavy": sensory.get("is_heavy"),
        },
        "absorbed_features": features,
        "quarantine_reason": packet.metadata.get("quarantine_reason"),
        "discard_reason": packet.metadata.get("discard_reason"),
        "history": [
            {
                "stage": log.stage,
                "status": log.status,
                "message": log.message,
                "timestamp": log.timestamp,
            }
            for log in packet.history
        ],
    }


def build_report() -> Dict[str, Any]:
    """Ejecuta una corrida entérica demostrativa y devuelve reporte estructurado."""
    system = EntericSystem(min_length=6, max_n_percent=25.0)

    examples = [
        ("Secuencia válida", "ACGTCCAATGGTATAAA", "enteric_valid_sequence"),
        ("Secuencia inválida", "ACGTXYZ", "enteric_invalid_sequence"),
        ("Secuencia en cuarentena", "ACG", "enteric_short_sequence"),
        ("Secuencia duplicada", "ACGTCCAATGGTATAAA", "enteric_duplicate_sequence"),
    ]

    records: List[Dict[str, Any]] = []
    for label, sequence, source in examples:
        packet = system.process_dna_sequence(sequence, source=source)
        records.append(packet_to_record(label, packet))

    homeostasis = system.homeostasis_report()

    return {
        "title": "E.C.O. Enteric System Report",
        "purpose": "Validar sensado, reflejo local, absorción, cuarentena, descarte, microbiota y homeostasis.",
        "architecture_layer": "src.eco_core.enteric_system.EntericSystem",
        "records": records,
        "homeostasis": {
            "total_packets": homeostasis.total_packets,
            "absorbed_packets": homeostasis.absorbed_packets,
            "quarantined_packets": homeostasis.quarantined_packets,
            "discarded_packets": homeostasis.discarded_packets,
            "rejected_packets": homeostasis.rejected_packets,
            "duplicate_packets": homeostasis.duplicate_packets,
            "state": homeostasis.state,
            "notes": homeostasis.notes,
        },
        "expected_actions": ["absorb", "reject", "quarantine", "discard_duplicate"],
        "actual_actions": [record["decision"].get("action") for record in records],
    }


def report_to_markdown(report: Dict[str, Any]) -> str:
    """Convierte el reporte JSON en Markdown legible para portafolio."""
    lines: List[str] = []
    lines.append("# E.C.O. Enteric System Report")
    lines.append("")
    lines.append(f"**Propósito:** {report['purpose']}")
    lines.append("")
    lines.append(f"**Capa técnica:** `{report['architecture_layer']}`")
    lines.append("")
    lines.append("## Resumen homeostático")
    lines.append("")
    homeostasis = report["homeostasis"]
    lines.append(f"- Paquetes procesados: {homeostasis['total_packets']}")
    lines.append(f"- Absorbidos: {homeostasis['absorbed_packets']}")
    lines.append(f"- Cuarentena: {homeostasis['quarantined_packets']}")
    lines.append(f"- Descartados: {homeostasis['discarded_packets']}")
    lines.append(f"- Rechazados: {homeostasis['rejected_packets']}")
    lines.append(f"- Duplicados: {homeostasis['duplicate_packets']}")
    lines.append(f"- Estado: `{homeostasis['state']}`")
    lines.append("")
    lines.append("### Notas")
    lines.append("")
    for note in homeostasis["notes"]:
        lines.append(f"- {note}")
    lines.append("")
    lines.append("## Paquetes evaluados")
    lines.append("")

    for record in report["records"]:
        decision = record["decision"]
        sensory = record["sensory_profile"]
        lines.append(f"### {record['label']}")
        lines.append("")
        lines.append(f"- Origen: `{record['source']}`")
        lines.append(f"- Payload: `{record['payload']}`")
        lines.append(f"- Acción: `{decision.get('action')}`")
        lines.append(f"- Ruta: `{decision.get('route')}`")
        lines.append(f"- Motivo: {decision.get('reason')}")
        lines.append(f"- Confianza local: {decision.get('confidence')}")
        lines.append(f"- Longitud detectada: {sensory.get('length')}")
        lines.append(f"- GC%: {sensory.get('gc_percent')}")
        lines.append(f"- N%: {sensory.get('n_percent')}")
        lines.append(f"- Duplicado: {sensory.get('is_duplicate')}")
        if record.get("absorbed_features"):
            lines.append("- Nutrientes informacionales: presentes")
        if record.get("quarantine_reason"):
            lines.append(f"- Cuarentena: {record['quarantine_reason']}")
        if record.get("discard_reason"):
            lines.append(f"- Descarte: {record['discard_reason']}")
        lines.append("")
        lines.append("Historial:")
        lines.append("")
        for step in record["history"]:
            lines.append(f"- `{step['stage']}` → `{step['status']}`: {step['message']}")
        lines.append("")

    lines.append("## Lectura arquitectónica")
    lines.append("")
    lines.append(
        "La capa entérica demuestra que E.C.O. puede tomar microdecisiones locales "
        "antes de absorber información. Esto permite distinguir datos útiles, "
        "datos inválidos, datos insuficientes y redundancia informacional sin "
        "tratar todas las entradas como equivalentes."
    )
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera reporte exportable del sistema entérico E.C.O.")
    parser.add_argument("--output-json", default="results/eco_enteric_system_report.json")
    parser.add_argument("--output-md", default="results/eco_enteric_system_report.md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report()

    output_json = PROJECT_ROOT / args.output_json
    output_md = PROJECT_ROOT / args.output_md
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)

    output_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    output_md.write_text(report_to_markdown(report), encoding="utf-8")

    if report["actual_actions"] != report["expected_actions"]:
        print("REVISAR: el reporte entérico no produjo las acciones esperadas.")
        print(f"JSON: {output_json}")
        print(f"Markdown: {output_md}")
        return 1

    print("OK: reporte entérico exportable generado.")
    print(f"JSON: {output_json.relative_to(PROJECT_ROOT)}")
    print(f"Markdown: {output_md.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
