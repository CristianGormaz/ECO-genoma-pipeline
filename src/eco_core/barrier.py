"""
Barrera informacional E.C.O.
===========================

Capa inspirada en la mucosa intestinal: permite, limita o rechaza
la entrada de paquetes antes de que el sistema los absorba.

No diagnostica. No interpreta clínicamente. Solo valida condiciones
mínimas de entrada para el pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BarrierResult:
    allowed: bool
    status: str
    reason: str
    permeability: float


def evaluate_barrier(
    *,
    is_text: bool,
    is_empty: bool,
    invalid_characters: list[str],
    length: int,
    min_length: int,
    n_percent: float,
    max_n_percent: float,
) -> BarrierResult:
    """Evalúa si un paquete puede cruzar la barrera informacional."""

    if not is_text:
        return BarrierResult(
            allowed=False,
            status="rejected",
            reason="Payload no textual: la barrera informacional no puede validarlo.",
            permeability=0.0,
        )

    if is_empty:
        return BarrierResult(
            allowed=False,
            status="rejected",
            reason="Secuencia vacía: no contiene nutriente informacional.",
            permeability=0.0,
        )

    if invalid_characters:
        invalid = ", ".join(invalid_characters)
        return BarrierResult(
            allowed=False,
            status="rejected",
            reason=f"Secuencia con caracteres no válidos: {invalid}.",
            permeability=0.05,
        )

    if length < min_length:
        return BarrierResult(
            allowed=True,
            status="quarantined",
            reason="Secuencia demasiado corta: cruza parcialmente hacia cuarentena.",
            permeability=0.35,
        )

    if n_percent > max_n_percent:
        return BarrierResult(
            allowed=True,
            status="quarantined",
            reason="Secuencia con exceso de bases ambiguas N: cruza parcialmente hacia cuarentena.",
            permeability=0.45,
        )

    return BarrierResult(
        allowed=True,
        status="ok",
        reason="Secuencia apta para cruzar la barrera informacional.",
        permeability=0.95,
    )
