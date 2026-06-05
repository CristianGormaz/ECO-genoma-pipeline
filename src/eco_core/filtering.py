"""
Módulo de filtrado SNE-E.C.O.
============================

Representa el filtro gástrico y el sistema inmune inicial: valida calidad
mínima antes de permitir que el dato avance hacia absorción.
"""

from __future__ import annotations

from typing import Iterable, List, Sequence

from .flow import EcoPacket, route_packet
from .validation.dna_validation import (
    DNA_ALPHABET,
    normalize_dna_sequence as shared_normalize_dna_sequence,
    validate_dna_sequence as shared_validate_dna_sequence,
)


def normalize_dna_sequence(sequence: str) -> str:
    """Normaliza una secuencia de ADN eliminando espacios y usando mayúsculas."""
    return shared_normalize_dna_sequence(sequence)


def validate_dna_sequence(sequence: str, allow_n: bool = True) -> List[str]:
    """Valida una secuencia de ADN y devuelve una lista de problemas.

    No lanza excepción por diseño: funciona como filtro diagnóstico para que
    el flujo decida si absorbe, descarta o deriva a revisión.
    """
    return list(shared_validate_dna_sequence(sequence, allow_n=allow_n).issues)


def validate_packet_payload(packet: EcoPacket, required_types: Sequence[type] = (str,)) -> EcoPacket:
    """Valida que el payload tenga un tipo esperado y registra el resultado."""
    if not isinstance(packet.payload, tuple(required_types)):
        packet.metadata["filter_issues"] = [
            f"Payload con tipo no esperado: {type(packet.payload).__name__}"
        ]
        return route_packet(
            packet,
            stage="filtering",
            status="rejected",
            message="Payload rechazado por tipo no válido.",
            plexus="mucosa_epithelial",
        )

    packet.metadata["filter_issues"] = []
    return route_packet(
        packet,
        stage="filtering",
        message="Payload aceptado por filtro básico.",
        plexus="mucosa_epithelial",
    )


def filter_dna_packet(packet: EcoPacket, allow_n: bool = True) -> EcoPacket:
    """Valida un paquete cuyo payload es una secuencia de ADN."""
    if not isinstance(packet.payload, str):
        packet.metadata["filter_issues"] = ["El payload no es texto."]
        return route_packet(
            packet,
            stage="filtering",
            status="rejected",
            message="Secuencia rechazada: payload no textual.",
            plexus="mucosa_epithelial",
        )

    sequence = normalize_dna_sequence(packet.payload)
    issues = validate_dna_sequence(sequence, allow_n=allow_n)
    packet.payload = sequence
    packet.metadata["filter_issues"] = issues

    if issues:
        return route_packet(
            packet,
            stage="filtering",
            status="rejected",
            message="Secuencia rechazada por problemas de calidad.",
            plexus="mucosa_epithelial",
        )

    return route_packet(
        packet,
        stage="filtering",
        message="Secuencia ADN validada correctamente.",
        plexus="mucosa_epithelial",
    )


def has_rejection(packet: EcoPacket) -> bool:
    """Indica si el paquete tiene al menos una etapa rechazada."""
    return any(log.status == "rejected" for log in packet.history)
