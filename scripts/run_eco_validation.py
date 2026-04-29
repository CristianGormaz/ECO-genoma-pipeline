#!/usr/bin/env python3
"""
Validación oficial del metabolismo E.C.O.
========================================

Ejecuta una prueba mínima y legible de la arquitectura SNE-E.C.O.:

1. Ingesta de una secuencia válida.
2. Filtrado de calidad.
3. Absorción de features genómicas básicas.
4. Ingesta de una secuencia inválida.
5. Rechazo controlado.
6. Descarte auditable.
7. Feedback final del metabolismo informacional.

Uso recomendado desde la raíz del repositorio:

    python3 scripts/run_eco_validation.py
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.eco_core import (  # noqa: E402
    absorb_sequence_features,
    build_feedback_summary,
    discard_packet,
    ingest_text,
)
from src.eco_core.filtering import filter_dna_packet, has_rejection  # noqa: E402
from src.eco_core.flow import EcoPacket  # noqa: E402


def print_section(title: str) -> None:
    """Imprime una sección visual simple para mejorar lectura UX."""
    print(f"\n{title}")
    print("-" * len(title))


def print_packet_trace(packet: EcoPacket) -> None:
    """Muestra una traza breve y comprensible de un paquete E.C.O."""
    print(f"ID: {packet.packet_id}")
    print(f"Origen: {packet.source}")
    print(f"Tipo: {packet.packet_type}")
    print(f"Payload: {packet.payload}")
    print("Historial:")
    for log in packet.history:
        print(f"  - [{log.status}] {log.stage}: {log.message}")
    print("Metadata:")
    for key, value in packet.metadata.items():
        print(f"  - {key}: {value}")


def absorb_if_valid(packet: EcoPacket) -> EcoPacket:
    """Absorbe features solo si el paquete no fue rechazado."""
    if has_rejection(packet):
        return packet

    packet.metadata["absorbed_features"] = absorb_sequence_features(packet.payload)
    packet.log(
        stage="absorption",
        status="ok",
        message="Features genómicas básicas absorbidas como nutrientes informacionales.",
    )
    return packet


def run_validation() -> int:
    """Ejecuta la validación oficial del metabolismo mínimo E.C.O."""
    print("E.C.O. VALIDATION REPORT")
    print("========================")
    print("Objetivo: probar ingesta, filtro, absorción, descarte y feedback.")

    packets = []

    good_packet = ingest_text(
        "ACGTACGTCCAATNN",
        source="validation_good_sequence",
        packet_type="dna",
    )
    good_packet = filter_dna_packet(good_packet)
    good_packet = absorb_if_valid(good_packet)
    packets.append(good_packet)

    bad_packet = ingest_text(
        "ACGTXYZ",
        source="validation_bad_sequence",
        packet_type="dna",
    )
    bad_packet = filter_dna_packet(bad_packet)
    if has_rejection(bad_packet):
        discard_record = discard_packet(
            bad_packet,
            reason="Secuencia descartada por caracteres no válidos.",
        )
        bad_packet.metadata["discard_record"] = discard_record.__dict__
    packets.append(bad_packet)

    feedback = build_feedback_summary(packets)

    print_section("Paquete válido")
    print_packet_trace(good_packet)

    print_section("Paquete rechazado")
    print_packet_trace(bad_packet)

    print_section("Feedback final")
    print(f"Paquetes procesados: {feedback.total_packets}")
    print(f"Aceptados: {feedback.accepted_packets}")
    print(f"Rechazados: {feedback.rejected_packets}")
    print(f"Absorbidos: {feedback.absorbed_packets}")
    print(f"Tasa de rechazo: {feedback.rejection_rate}%")
    print(f"Tasa de absorción: {feedback.absorbed_rate}%")
    if feedback.notes:
        print("Notas:")
        for note in feedback.notes:
            print(f"  - {note}")
    else:
        print("Notas: sin alertas.")

    print_section("Estado")
    if feedback.total_packets == 2 and feedback.accepted_packets == 1 and feedback.rejected_packets == 1:
        print("OK: metabolismo informacional mínimo funcionando.")
        return 0

    print("REVISAR: el metabolismo informacional no produjo el balance esperado.")
    return 1


if __name__ == "__main__":
    raise SystemExit(run_validation())
