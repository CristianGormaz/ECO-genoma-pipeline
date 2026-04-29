"""
Módulo de retroalimentación SNE-E.C.O.
=====================================

Representa el eje intestino-cerebro del sistema: resume estado, errores,
rechazos y señales absorbidas para ajustar el proceso.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List

from .flow import EcoPacket


@dataclass(frozen=True)
class EcoFeedback:
    """Resumen de retroalimentación de un conjunto de paquetes E.C.O."""

    total_packets: int
    accepted_packets: int
    rejected_packets: int
    absorbed_packets: int
    rejection_rate: float
    absorbed_rate: float
    notes: List[str]


def build_feedback_summary(packets: Iterable[EcoPacket]) -> EcoFeedback:
    """Construye un resumen de feedback para evaluar el metabolismo E.C.O."""
    packet_list = list(packets)
    total = len(packet_list)
    rejected = sum(1 for packet in packet_list if any(log.status == "rejected" for log in packet.history))
    absorbed = sum(1 for packet in packet_list if "absorbed_features" in packet.metadata)
    accepted = total - rejected

    rejection_rate = round((rejected / total) * 100, 4) if total else 0.0
    absorbed_rate = round((absorbed / total) * 100, 4) if total else 0.0

    notes: List[str] = []
    if rejection_rate > 25:
        notes.append("Alta tasa de rechazo: revisar calidad de entrada o filtros.")
    if absorbed == 0 and total > 0:
        notes.append("No hubo absorción informacional: revisar etapa de features.")
    if total == 0:
        notes.append("No hay paquetes para evaluar.")

    return EcoFeedback(
        total_packets=total,
        accepted_packets=accepted,
        rejected_packets=rejected,
        absorbed_packets=absorbed,
        rejection_rate=rejection_rate,
        absorbed_rate=absorbed_rate,
        notes=notes,
    )


def packet_trace(packet: EcoPacket) -> Dict[str, object]:
    """Devuelve una traza serializable de un paquete individual."""
    return {
        "packet_id": packet.packet_id,
        "source": packet.source,
        "packet_type": packet.packet_type,
        "metadata": packet.metadata,
        "history": [log.__dict__ for log in packet.history],
    }
