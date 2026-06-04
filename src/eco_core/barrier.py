"""
Barrera informacional E.C.O.
===========================

Capa inspirada en la mucosa intestinal: permite, limita o rechaza
la entrada de paquetes antes de que el sistema los absorba.

No diagnostica. No interpreta clínicamente. Solo valida condiciones
mínimas de entrada para el pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BarrierResult:
    allowed: bool
    status: str
    reason: str
    permeability: float
    internal_logs: tuple[str, ...] = field(default_factory=tuple)


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
    logs = []

    if not is_text:
        reason = "Payload no textual: la barrera informacional no puede validarlo."
        return BarrierResult(
            allowed=False,
            status="rejected",
            reason=reason,
            permeability=0.0,
            internal_logs=(reason,),
        )
    logs.append("Chequeo de tipo: texto detectado.")

    if is_empty:
        reason = "Secuencia vacía: no contiene nutriente informacional."
        return BarrierResult(
            allowed=False,
            status="rejected",
            reason=reason,
            permeability=0.0,
            internal_logs=tuple(logs + [reason]),
        )
    logs.append(f"Chequeo de contenido: longitud {length} detectada.")

    if invalid_characters:
        invalid = ", ".join(invalid_characters)
        reason = f"Secuencia con caracteres no válidos: {invalid}."
        return BarrierResult(
            allowed=False,
            status="rejected",
            reason=reason,
            permeability=0.05,
            internal_logs=tuple(logs + [reason]),
        )
    logs.append("Chequeo de alfabeto: caracteres válidos.")

    if length < min_length:
        reason = "Secuencia demasiado corta: cruza parcialmente hacia cuarentena."
        return BarrierResult(
            allowed=True,
            status="quarantined",
            reason=reason,
            permeability=0.35,
            internal_logs=tuple(logs + [reason]),
        )
    logs.append(f"Chequeo de longitud: {length} >= {min_length}.")

    if n_percent > max_n_percent:
        reason = "Secuencia con exceso de bases ambiguas N: cruza parcialmente hacia cuarentena."
        return BarrierResult(
            allowed=True,
            status="quarantined",
            reason=reason,
            permeability=0.45,
            internal_logs=tuple(logs + [reason]),
        )
    logs.append(f"Chequeo de calidad (N%): {n_percent}% <= {max_n_percent}%.")

    reason = "Secuencia apta para cruzar la barrera informacional."
    return BarrierResult(
        allowed=True,
        status="ok",
        reason=reason,
        permeability=0.95,
        internal_logs=tuple(logs + [reason]),
    )
