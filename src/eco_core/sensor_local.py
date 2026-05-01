"""
Sensor local submucoso E.C.O.
=============================

Capa inspirada en el plexo submucoso del sistema nervioso entérico.
Su función es generar un perfil sensorial del dato antes de que el sistema
decida si debe avanzar, quedar en cuarentena, procesarse por lote o descartarse.

No diagnostica. No interpreta clínicamente. Solo mide señales técnicas del
payload para apoyar decisiones trazables del pipeline.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Collection

from .absorption import gc_percent, n_percent
from .filtering import DNA_ALPHABET, normalize_dna_sequence, validate_dna_sequence
from .flow import EcoPacket


@dataclass(frozen=True)
class SensoryProfile:
    """Perfil sensorial mínimo producido por el plexo submucoso digital."""

    packet_id: str | None
    source: str
    packet_type: str
    payload_type: str
    is_text: bool
    is_empty: bool
    length: int
    gc_percent: float
    n_percent: float
    invalid_characters: tuple[str, ...]
    filter_issues: tuple[str, ...]
    is_duplicate: bool
    is_heavy: bool
    payload_key: str

    def to_dict(self) -> dict[str, Any]:
        """Convierte el perfil a dict compatible con el orquestador actual."""
        data = asdict(self)
        data["invalid_characters"] = list(self.invalid_characters)
        data["filter_issues"] = list(self.filter_issues)
        return data


def build_payload_key(payload: Any) -> str:
    """Genera una clave estable para memoria microbiota y duplicados."""
    if isinstance(payload, str):
        return normalize_dna_sequence(payload)
    return repr(payload)


def analyze_payload(
    payload: Any,
    *,
    source: str = "manual_input",
    packet_type: str = "unknown",
    packet_id: str | None = None,
    known_payload_keys: Collection[str] | None = None,
    heavy_payload_threshold: int = 10_000,
) -> SensoryProfile:
    """Analiza señales locales del payload sin decidir todavía la ruta."""
    is_text = isinstance(payload, str)
    normalized = normalize_dna_sequence(payload) if is_text else ""
    invalid_characters = tuple(sorted(set(normalized) - DNA_ALPHABET)) if is_text else tuple()
    filter_issues = tuple(validate_dna_sequence(normalized)) if is_text else ("El payload no es texto.",)
    payload_key = build_payload_key(payload)
    known_keys = set(known_payload_keys or [])

    return SensoryProfile(
        packet_id=packet_id,
        source=source,
        packet_type=packet_type,
        payload_type=type(payload).__name__,
        is_text=is_text,
        is_empty=is_text and len(normalized) == 0,
        length=len(normalized) if is_text else 0,
        gc_percent=gc_percent(normalized) if is_text else 0.0,
        n_percent=n_percent(normalized) if is_text else 0.0,
        invalid_characters=invalid_characters,
        filter_issues=filter_issues,
        is_duplicate=payload_key in known_keys,
        is_heavy=is_text and len(normalized) >= heavy_payload_threshold,
        payload_key=payload_key,
    )


def analyze_packet(
    packet: EcoPacket,
    *,
    known_payload_keys: Collection[str] | None = None,
    heavy_payload_threshold: int = 10_000,
) -> SensoryProfile:
    """Analiza un EcoPacket y conserva su trazabilidad básica."""
    return analyze_payload(
        packet.payload,
        source=packet.source,
        packet_type=packet.packet_type,
        packet_id=packet.packet_id,
        known_payload_keys=known_payload_keys,
        heavy_payload_threshold=heavy_payload_threshold,
    )
