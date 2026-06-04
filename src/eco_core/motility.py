"""
Motilidad mientérica E.C.O.
==========================

Capa inspirada en el plexo mientérico del sistema nervioso entérico.
Su función es decidir el movimiento operativo del paquete después del sensado
local: avanzar, quedar en cuarentena, procesarse por lote, descartarse o
activarse como respuesta inmune informacional.

No diagnostica. No interpreta clínicamente. Solo traduce señales técnicas del
payload en rutas de flujo trazables para el pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from .barrier import BarrierResult
from .sensor_local import SensoryProfile

MotilityAction = Literal[
    "advance",
    "quarantine",
    "batch_advance",
    "discard_duplicate",
    "immune_discard",
]


@dataclass(frozen=True)
class MotilityDecision:
    """Decisión de movimiento producida por el plexo mientérico digital."""

    action: MotilityAction
    status: str
    route: str
    reason: str
    transit_score: float
    internal_logs: tuple[str, ...] = field(default_factory=tuple)

    @property
    def can_continue(self) -> bool:
        """Indica si el paquete puede seguir hacia absorción o procesamiento posterior."""
        return self.action in {"advance", "batch_advance"}


def decide_motility(
    sensory_profile: SensoryProfile,
    barrier_result: BarrierResult,
) -> MotilityDecision:
    """Decide cómo se debe mover un paquete dentro del intestino informacional."""
    logs = []

    if not barrier_result.allowed and barrier_result.status == "rejected":
        reason = barrier_result.reason
        return MotilityDecision(
            action="immune_discard",
            status="rejected",
            route="immune_discard",
            reason=reason,
            transit_score=0.0,
            internal_logs=(reason,),
        )
    logs.append("Chequeo de barrera: acceso permitido por la mucosa.")

    if sensory_profile.is_duplicate:
        reason = "Secuencia duplicada: se evita mover redundancia hacia absorción."
        return MotilityDecision(
            action="discard_duplicate",
            status="discarded",
            route="controlled_discard",
            reason=reason,
            transit_score=0.1,
            internal_logs=tuple(logs + [reason]),
        )
    logs.append("Chequeo de redundancia: secuencia nueva en microbiota.")

    if barrier_result.status == "quarantined":
        reason = barrier_result.reason
        return MotilityDecision(
            action="quarantine",
            status="quarantined",
            route="quarantine",
            reason=reason,
            transit_score=barrier_result.permeability,
            internal_logs=tuple(logs + [reason]),
        )
    logs.append("Chequeo de permeabilidad: tránsito fluido detectado.")

    if sensory_profile.is_heavy:
        reason = "Payload grande: avanza con tránsito lento y procesamiento por lote."
        return MotilityDecision(
            action="batch_advance",
            status="batched",
            route="myenteric_batch_flow",
            reason=reason,
            transit_score=0.65,
            internal_logs=tuple(logs + [reason]),
        )
    logs.append("Chequeo de carga: payload ligero manejable en tiempo real.")

    reason = "Payload apto para avanzar hacia absorción informacional."
    return MotilityDecision(
        action="advance",
        status="ok",
        route="submucosal_absorption",
        reason=reason,
        transit_score=min(1.0, barrier_result.permeability),
        internal_logs=tuple(logs + [reason]),
    )
