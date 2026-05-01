#!/usr/bin/env python3
"""
Demo ejecutable del Sistema Entérico Integrado E.C.O.
====================================================

Muestra la capa `EntericSystem` como una pieza presentable del pipeline:

1. Una secuencia válida se absorbe.
2. Una secuencia inválida se rechaza y descarta.
3. Una secuencia corta queda en cuarentena.
4. Una secuencia duplicada activa memoria microbiota y se descarta.
5. El sistema reporta homeostasis del flujo completo.

Uso recomendado desde la raíz del repositorio:

    python3 scripts/run_eco_enteric_demo.py
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.eco_core import EntericSystem  # noqa: E402
from src.eco_core.flow import EcoPacket  # noqa: E402


def print_section(title: str) -> None:
    """Imprime una sección legible para revisión en terminal."""
    print(f"\n{title}")
    print("-" * len(title))


def compact_history(packet: EcoPacket) -> str:
    """Devuelve una traza breve etapa:estado para UX de terminal."""
    return " -> ".join(f"{log.stage}:{log.status}" for log in packet.history)


def print_packet_summary(label: str, packet: EcoPacket) -> None:
    """Muestra la lectura humana de un paquete procesado por EntericSystem."""
    decision = packet.metadata.get("enteric_decision", {})
    sensory = packet.metadata.get("enteric_sensory_profile", {})
    features = packet.metadata.get("absorbed_features")

    print_section(label)
    print(f"Origen: {packet.source}")
    print(f"Payload: {packet.payload}")
    print(f"Acción: {decision.get('action')}")
    print(f"Ruta: {decision.get('route')}")
    print(f"Motivo: {decision.get('reason')}")
    print(f"Confianza local: {decision.get('confidence')}")
    print(f"Longitud detectada: {sensory.get('length')}")
    print(f"N ambiguas: {sensory.get('n_percent')}%")
    print(f"Duplicado: {sensory.get('is_duplicate')}")
    print(f"Historial: {compact_history(packet)}")

    if features:
        print("Nutrientes informacionales:")
        print(f"  - length: {features['length']}")
        print(f"  - gc_percent: {features['gc_percent']}")
        print(f"  - n_percent: {features['n_percent']}")

    if "quarantine_reason" in packet.metadata:
        print(f"Cuarentena: {packet.metadata['quarantine_reason']}")
    if "discard_reason" in packet.metadata:
        print(f"Descarte: {packet.metadata['discard_reason']}")


def run_demo() -> int:
    """Ejecuta una demostración mínima del reflejo entérico E.C.O."""
    print("E.C.O. ENTERIC SYSTEM REPORT")
    print("============================")
    print("Objetivo: probar sensado, reflejo local, absorción, cuarentena, descarte, microbiota y homeostasis.")

    system = EntericSystem(min_length=6, max_n_percent=25.0)

    packets = [
        system.process_dna_sequence("ACGTCCAATGGTATAAA", source="enteric_valid_sequence"),
        system.process_dna_sequence("ACGTXYZ", source="enteric_invalid_sequence"),
        system.process_dna_sequence("ACG", source="enteric_short_sequence"),
        system.process_dna_sequence("ACGTCCAATGGTATAAA", source="enteric_duplicate_sequence"),
    ]

    labels = [
        "Secuencia válida",
        "Secuencia inválida",
        "Secuencia en cuarentena",
        "Secuencia duplicada",
    ]

    for label, packet in zip(labels, packets):
        print_packet_summary(label, packet)

    homeostasis = system.homeostasis_report()

    print_section("Homeostasis entérica")
    print(f"Paquetes procesados: {homeostasis.total_packets}")
    print(f"Absorbidos: {homeostasis.absorbed_packets}")
    print(f"Cuarentena: {homeostasis.quarantined_packets}")
    print(f"Descartados: {homeostasis.discarded_packets}")
    print(f"Rechazados: {homeostasis.rejected_packets}")
    print(f"Duplicados: {homeostasis.duplicate_packets}")
    print(f"Estado: {homeostasis.state}")
    print("Notas:")
    for note in homeostasis.notes:
        print(f"  - {note}")

    expected_actions = [
        "absorb",
        "reject",
        "quarantine",
        "discard_duplicate",
    ]
    actual_actions = [packet.metadata.get("enteric_decision", {}).get("action") for packet in packets]

    print_section("Estado final")
    if actual_actions == expected_actions and homeostasis.total_packets == 4:
        print("OK: sistema entérico integrado funcionando.")
        return 0

    print("REVISAR: la demo entérica no produjo las rutas esperadas.")
    print(f"Rutas esperadas: {expected_actions}")
    print(f"Rutas obtenidas: {actual_actions}")
    return 1


if __name__ == "__main__":
    raise SystemExit(run_demo())
