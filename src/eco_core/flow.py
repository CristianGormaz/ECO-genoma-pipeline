"""
Módulo de flujo SNE-E.C.O.
=========================

Representa el equivalente técnico del plexo de Auerbach: mueve el dato por
etapas, registra trazabilidad y evita que el procesamiento sea una caja negra.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4


def utc_now_iso() -> str:
    """Devuelve una marca temporal UTC en formato ISO-8601."""
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class EcoStageLog:
    """Registro de una etapa recorrida por un paquete E.C.O."""

    stage: str
    status: str
    message: str
    timestamp: str = field(default_factory=utc_now_iso)


@dataclass
class EcoPacket:
    """Unidad mínima de información que circula por el metabolismo E.C.O."""

    payload: Any
    source: str
    packet_type: str = "raw"
    packet_id: str = field(default_factory=lambda: str(uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)
    history: List[EcoStageLog] = field(default_factory=list)

    def log(self, stage: str, status: str, message: str) -> None:
        """Agrega un registro de trazabilidad al paquete."""
        self.history.append(EcoStageLog(stage=stage, status=status, message=message))


def route_packet(packet: EcoPacket, stage: str, message: str, status: str = "ok") -> EcoPacket:
    """Registra que un paquete avanzó por una etapa del pipeline."""
    packet.log(stage=stage, status=status, message=message)
    return packet
