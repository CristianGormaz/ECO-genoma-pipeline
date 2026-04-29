"""
Módulo de absorción SNE-E.C.O.
=============================

Representa la conversión de datos validados en nutrientes informacionales:
features, métricas simples y señales útiles para análisis posteriores.
"""

from __future__ import annotations

from typing import Dict

from .filtering import normalize_dna_sequence
from .flow import EcoPacket, route_packet


def gc_percent(sequence: str) -> float:
    """Calcula porcentaje GC ignorando N como base no informativa."""
    informative = [base for base in sequence if base in "ACGT"]
    if not informative:
        return 0.0
    gc_count = sum(1 for base in informative if base in "GC")
    return round((gc_count / len(informative)) * 100, 4)


def n_percent(sequence: str) -> float:
    """Calcula porcentaje de bases ambiguas N."""
    if not sequence:
        return 0.0
    return round((sequence.count("N") / len(sequence)) * 100, 4)


def absorb_sequence_features(sequence: str) -> Dict[str, float | int]:
    """Extrae nutrientes informacionales básicos desde una secuencia de ADN."""
    normalized = normalize_dna_sequence(sequence)
    return {
        "length": len(normalized),
        "gc_percent": gc_percent(normalized),
        "n_percent": n_percent(normalized),
        "a_count": normalized.count("A"),
        "c_count": normalized.count("C"),
        "g_count": normalized.count("G"),
        "t_count": normalized.count("T"),
        "n_count": normalized.count("N"),
    }


def absorb_dna_packet(packet: EcoPacket) -> EcoPacket:
    """Agrega features básicas de ADN al metadata del paquete."""
    if not isinstance(packet.payload, str):
        return route_packet(packet, stage="absorption", status="rejected", message="No se pudo absorber: payload no textual.")

    packet.metadata["absorbed_features"] = absorb_sequence_features(packet.payload)
    return route_packet(packet, stage="absorption", message="Features básicas absorbidas como conocimiento útil.")
