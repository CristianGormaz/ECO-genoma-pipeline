"""
Módulo de descarte SNE-E.C.O.
============================

Representa la excreción informacional: registrar por qué un dato no se absorbe
y evitar acumulación de basura dentro del sistema.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .flow import EcoPacket, route_packet, utc_now_iso


@dataclass(frozen=True)
class EcoDiscardRecord:
    """Registro de descarte controlado."""

    packet_id: str
    source: str
    reason: str
    timestamp: str = field(default_factory=utc_now_iso)


def discard_packet(packet: EcoPacket, reason: str) -> EcoDiscardRecord:
    """Marca un paquete como descartado y devuelve un registro auditable."""
    packet.metadata["discard_reason"] = reason
    route_packet(packet, stage="discard", status="discarded", message=reason)
    return EcoDiscardRecord(packet_id=packet.packet_id, source=packet.source, reason=reason)
