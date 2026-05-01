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

from dataclasses import dataclass
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


def evaluate_defense(
    sensory_profile: SensoryProfile,
    barrier_result: BarrierResult,
    motility_decision: MotilityDecision,
) -> DefenseSignal:
    """Evalúa una señal defensiva a partir del sensado, barrera y motilidad."""

    if motility_decision.action == "immune_discard":
        return DefenseSignal(
            category="invalid_payload",
            severity="high",
            should_alert=True,
            reason=barrier_result.reason,
            recommended_action="discard",
        )

    if sensory_profile.is_duplicate or motility_decision.action == "discard_duplicate":
        return DefenseSignal(
            category="redundant_payload",
            severity="low",
            should_alert=False,
            reason="Payload recurrente: la memoria evita absorber redundancia como conocimiento nuevo.",
            recommended_action="discard_duplicate",
        )

    if barrier_result.status == "quarantined":
        category: DefenseCategory = "ambiguous_payload" if sensory_profile.n_percent > 0 else "retained_payload"
        return DefenseSignal(
            category=category,
            severity="medium",
            should_alert=True,
            reason=barrier_result.reason,
            recommended_action="quarantine",
        )

    return DefenseSignal(
        category="none",
        severity="none",
        should_alert=False,
        reason="Sin señal defensiva relevante: flujo informacional estable.",
        recommended_action="continue",
    )
