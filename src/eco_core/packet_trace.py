"""
Trazabilidad digestiva S.N.E.-E.C.O.
===================================

Convierte un EcoPacket procesado en una ruta digestiva resumida y exportable.

La traza no cambia el flujo del pipeline: solo lee `history` y `metadata` para
explicar por dónde pasó cada paquete, qué decisión recibió y cuál fue su estado
final dentro del intestino informacional.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable

from .flow import EcoPacket


@dataclass(frozen=True)
class PacketTrace:
    """Ruta digestiva resumida de un paquete E.C.O."""

    packet_id: str
    source: str
    packet_type: str
    payload_type: str
    payload_length: int
    stage_count: int
    stages: tuple[str, ...]
    final_stage: str
    final_status: str
    barrier_status: str
    barrier_permeability: float
    motility_action: str
    motility_route: str
    defense_category: str
    defense_severity: str
    final_decision: str
    absorbed: bool
    quarantined: bool
    discarded: bool
    rejected: bool
    microbiota_seen_count: int

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["stages"] = list(self.stages)
        return data


def _payload_length(payload: Any) -> int:
    if isinstance(payload, str):
        return len(payload.strip())
    try:
        return len(payload)  # type: ignore[arg-type]
    except TypeError:
        return 0


def _has_status(packet: EcoPacket, status: str) -> bool:
    return any(log.status == status for log in packet.history)


def build_packet_trace(packet: EcoPacket) -> PacketTrace:
    """Construye una traza digestiva para un EcoPacket ya procesado."""
    barrier = packet.metadata.get("enteric_barrier_result", {})
    motility = packet.metadata.get("myenteric_motility_decision", {})
    defense = packet.metadata.get("enteric_defense_signal", {})
    decision = packet.metadata.get("enteric_decision", {})
    stages = tuple(log.stage for log in packet.history)
    final_log = packet.history[-1] if packet.history else None

    return PacketTrace(
        packet_id=packet.packet_id,
        source=packet.source,
        packet_type=packet.packet_type,
        payload_type=type(packet.payload).__name__,
        payload_length=_payload_length(packet.payload),
        stage_count=len(packet.history),
        stages=stages,
        final_stage=final_log.stage if final_log else "unknown",
        final_status=final_log.status if final_log else "unknown",
        barrier_status=str(barrier.get("status", "unknown")),
        barrier_permeability=float(barrier.get("permeability", 0.0)),
        motility_action=str(motility.get("action", "unknown")),
        motility_route=str(motility.get("route", "unknown")),
        defense_category=str(defense.get("category", "unknown")),
        defense_severity=str(defense.get("severity", "unknown")),
        final_decision=str(decision.get("action", "unknown")),
        absorbed="absorbed_features" in packet.metadata,
        quarantined=_has_status(packet, "quarantined"),
        discarded=_has_status(packet, "discarded"),
        rejected=_has_status(packet, "rejected"),
        microbiota_seen_count=int(packet.metadata.get("microbiome_seen_count", 0)),
    )


def build_packet_traces(packets: Iterable[EcoPacket]) -> list[PacketTrace]:
    """Construye trazas para un conjunto de paquetes procesados."""
    return [build_packet_trace(packet) for packet in packets]


def traces_to_markdown(traces: Iterable[PacketTrace]) -> str:
    """Renderiza las trazas digestivas como Markdown simple para portafolio."""
    trace_list = list(traces)
    lines = [
        "# Ruta digestiva S.N.E.-E.C.O.",
        "",
        "Resumen de tránsito por paquete dentro del intestino informacional E.C.O.",
        "",
        f"Paquetes trazados: {len(trace_list)}",
        "",
        "| source | final_decision | barrier | motility | defense | final_status | seen |",
        "|---|---|---|---|---|---|---|",
    ]
    for trace in trace_list:
        lines.append(
            "| "
            f"{trace.source} | "
            f"{trace.final_decision} | "
            f"{trace.barrier_status} | "
            f"{trace.motility_action} | "
            f"{trace.defense_category}/{trace.defense_severity} | "
            f"{trace.final_status} | "
            f"{trace.microbiota_seen_count} |"
        )

    lines.extend(
        [
            "",
            "## Lectura",
            "",
            "Cada fila resume si el paquete fue absorbido, retenido, descartado o marcado por recurrencia.",
            "La traza es una salida técnica de observabilidad; no representa diagnóstico ni conclusión clínica.",
        ]
    )
    return "\n".join(lines)
