"""
Homeostasis entérica E.C.O.
==========================

Capa inspirada en la homeostasis intestinal: resume el equilibrio del flujo
informacional después de absorción, cuarentena, descarte, rechazo, defensa y
recurrencia.

No diagnostica. No interpreta clínicamente. Solo convierte eventos técnicos
del pipeline en un estado operativo trazable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .flow import EcoPacket


@dataclass(frozen=True)
class HomeostasisSnapshot:
    """Instantánea del equilibrio operativo del intestino informacional."""

    total_packets: int
    absorbed_packets: int
    quarantined_packets: int
    discarded_packets: int
    rejected_packets: int
    duplicate_packets: int
    defense_alerts: int
    absorption_ratio: float
    immune_load: float
    quarantine_ratio: float
    recurrence_ratio: float
    state: str
    notes: tuple[str, ...]

    @property
    def needs_attention(self) -> bool:
        """Indica si el sistema requiere revisión humana o ajuste técnico."""
        return self.state in {"attention", "overload"}


def safe_ratio(part: int, total: int) -> float:
    """Calcula una proporción estable cuando el total puede ser cero."""
    if total <= 0:
        return 0.0
    return round(part / total, 4)


def build_homeostasis_snapshot(packets: Sequence[EcoPacket] | Iterable[EcoPacket]) -> HomeostasisSnapshot:
    """Construye un resumen homeostático desde paquetes procesados."""
    packet_list = list(packets)
    total = len(packet_list)

    absorbed = sum(1 for packet in packet_list if "absorbed_features" in packet.metadata)
    quarantined = sum(_has_status(packet, "quarantined") for packet in packet_list)
    discarded = sum(_has_status(packet, "discarded") for packet in packet_list)
    rejected = sum(_has_status(packet, "rejected") for packet in packet_list)
    duplicates = sum(
        1
        for packet in packet_list
        if packet.metadata.get("enteric_decision", {}).get("action") == "discard_duplicate"
    )
    defense_alerts = sum(_has_defense_alert(packet) for packet in packet_list)

    absorption_ratio = safe_ratio(absorbed, total)
    immune_load = safe_ratio(rejected + defense_alerts, total)
    quarantine_ratio = safe_ratio(quarantined, total)
    recurrence_ratio = safe_ratio(duplicates, total)

    notes: list[str] = []
    if total == 0:
        return HomeostasisSnapshot(
            total_packets=0,
            absorbed_packets=0,
            quarantined_packets=0,
            discarded_packets=0,
            rejected_packets=0,
            duplicate_packets=0,
            defense_alerts=0,
            absorption_ratio=0.0,
            immune_load=0.0,
            quarantine_ratio=0.0,
            recurrence_ratio=0.0,
            state="idle",
            notes=("Sin paquetes procesados.",),
        )

    if immune_load > 0.6:
        notes.append("Sobrecarga defensiva: revisar calidad de entrada y reglas de rechazo.")
    elif immune_load > 0.4:
        notes.append("Alta respuesta inmune: revisar calidad de entrada.")

    if quarantine_ratio > 0.3:
        notes.append("Cuarentena elevada: revisar longitud mínima o ambigüedad de secuencias.")

    if recurrence_ratio > 0:
        notes.append("Recurrencia detectada: la microbiota informacional identificó repetición.")

    if absorption_ratio >= 0.7 and not notes:
        notes.append("Homeostasis estable: flujo informacional dentro de rangos esperados.")

    if not notes:
        notes.append("Homeostasis en observación: flujo procesado sin alertas críticas.")

    state = _classify_state(
        immune_load=immune_load,
        quarantine_ratio=quarantine_ratio,
        absorption_ratio=absorption_ratio,
    )

    return HomeostasisSnapshot(
        total_packets=total,
        absorbed_packets=absorbed,
        quarantined_packets=quarantined,
        discarded_packets=discarded,
        rejected_packets=rejected,
        duplicate_packets=duplicates,
        defense_alerts=defense_alerts,
        absorption_ratio=absorption_ratio,
        immune_load=immune_load,
        quarantine_ratio=quarantine_ratio,
        recurrence_ratio=recurrence_ratio,
        state=state,
        notes=tuple(notes),
    )


def _classify_state(*, immune_load: float, quarantine_ratio: float, absorption_ratio: float) -> str:
    if immune_load > 0.6:
        return "overload"
    if immune_load > 0.4 or quarantine_ratio > 0.3:
        return "attention"
    if absorption_ratio >= 0.7:
        return "stable"
    return "watch"


def _has_status(packet: EcoPacket, status: str) -> bool:
    return any(log.status == status for log in packet.history)


def _has_defense_alert(packet: EcoPacket) -> bool:
    signal = packet.metadata.get("enteric_defense_signal", {})
    return signal.get("severity") in {"warning", "critical"}
