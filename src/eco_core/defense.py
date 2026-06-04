"""
Defensa informacional E.C.O.
===========================

Capa inspirada en la respuesta defensiva del ecosistema intestinal.
Su función es clasificar señales de riesgo técnico del pipeline: invalidez,
ambigüedad, redundancia o tránsito detenido.

No diagnostica. No interpreta clínicamente. Solo entrega una señal defensiva
para mantener trazabilidad, seguridad técnica y calidad de entrada.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from .barrier import BarrierResult
from .motility import MotilityDecision
from .sensor_local import SensoryProfile

DefenseCategory = Literal[
    "none",
    "invalid_payload",
    "ambiguous_payload",
    "redundant_payload",
    "retained_payload",
]

DefenseSeverity = Literal["none", "low", "medium", "high"]


@dataclass(frozen=True)
class DefenseSignal:
    """Señal defensiva técnica del S.N.E.-E.C.O."""

    category: DefenseCategory
    severity: DefenseSeverity
    should_alert: bool
    reason: str
    recommended_action: str
    internal_logs: tuple[str, ...] = field(default_factory=tuple)


def evaluate_defense(
    sensory_profile: SensoryProfile,
    barrier_result: BarrierResult,
    motility_decision: MotilityDecision,
) -> DefenseSignal:
    """Evalúa una señal defensiva a partir del sensado, barrera y motilidad."""
    logs = []

    if motility_decision.action == "immune_discard":
        reason = barrier_result.reason
        return DefenseSignal(
            category="invalid_payload",
            severity="high",
            should_alert=True,
            reason=reason,
            recommended_action="discard",
            internal_logs=(reason,),
        )
    logs.append("Chequeo de motilidad: no se requiere descarte inmune.")

    if sensory_profile.is_duplicate or motility_decision.action == "discard_duplicate":
        reason = "Payload recurrente: la memoria evita absorber redundancia como conocimiento nuevo."
        return DefenseSignal(
            category="redundant_payload",
            severity="low",
            should_alert=False,
            reason=reason,
            recommended_action="discard_duplicate",
            internal_logs=tuple(logs + [reason]),
        )
    logs.append("Chequeo de microbiota: secuencia no redundante.")

    if barrier_result.status == "quarantined":
        category: DefenseCategory = "ambiguous_payload" if sensory_profile.n_percent > 0 else "retained_payload"
        reason = barrier_result.reason
        return DefenseSignal(
            category=category,
            severity="medium",
            should_alert=True,
            reason=reason,
            recommended_action="quarantine",
            internal_logs=tuple(logs + [reason]),
        )
    logs.append("Chequeo de barrera: no hay retención en cuarentena.")

    reason = "Sin señal defensiva relevante: flujo informacional estable."
    return DefenseSignal(
        category="none",
        severity="none",
        should_alert=False,
        reason=reason,
        recommended_action="continue",
        internal_logs=tuple(logs + [reason]),
    )
