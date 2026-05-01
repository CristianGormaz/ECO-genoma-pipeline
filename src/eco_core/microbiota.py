"""
Microbiota informacional E.C.O.
==============================

Capa inspirada en la microbiota intestinal: no reemplaza al sistema central,
pero conserva memoria local, detecta redundancia y aporta señales adaptativas
al tránsito informacional.

No diagnostica. No interpreta clínicamente. Solo registra exposiciones del
payload y ayuda a evitar absorber repetición como conocimiento nuevo.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, MutableMapping

from .sensor_local import build_payload_key


@dataclass(frozen=True)
class MicrobiotaRecord:
    """Registro adaptativo mínimo de una exposición informacional."""

    payload_key: str
    seen_count: int
    last_packet_id: str | None
    last_source: str
    last_action: str
    last_status: str

    @property
    def is_recurrent(self) -> bool:
        """Indica si el payload ya fue visto más de una vez."""
        return self.seen_count > 1


class InformationalMicrobiota:
    """Memoria adaptativa simple para paquetes E.C.O."""

    def __init__(self, initial_memory: Mapping[str, Mapping[str, Any]] | None = None) -> None:
        self.memory: dict[str, dict[str, Any]] = {
            key: dict(value) for key, value in (initial_memory or {}).items()
        }

    def has_seen(self, payload: Any) -> bool:
        """Indica si un payload ya existe en la memoria microbiota."""
        return self.payload_key(payload) in self.memory

    def payload_key(self, payload: Any) -> str:
        """Genera la clave de memoria usando el contrato compartido del sensor local."""
        return build_payload_key(payload)

    def observe(
        self,
        payload: Any,
        *,
        packet_id: str | None = None,
        source: str = "unknown",
        action: str = "unknown",
        status: str = "unknown",
    ) -> MicrobiotaRecord:
        """Registra una exposición del payload y devuelve el estado actualizado."""
        key = self.payload_key(payload)
        previous = self.memory.get(key, {})
        seen_count = int(previous.get("seen_count", 0)) + 1

        record = MicrobiotaRecord(
            payload_key=key,
            seen_count=seen_count,
            last_packet_id=packet_id,
            last_source=source,
            last_action=action,
            last_status=status,
        )
        self.memory[key] = {
            "seen_count": record.seen_count,
            "last_packet_id": record.last_packet_id,
            "last_source": record.last_source,
            "last_action": record.last_action,
            "last_status": record.last_status,
        }
        return record

    def export_memory(self) -> dict[str, dict[str, Any]]:
        """Entrega una copia simple de la memoria actual."""
        return {key: dict(value) for key, value in self.memory.items()}


def update_microbiota_memory(
    memory: MutableMapping[str, dict[str, Any]],
    payload: Any,
    *,
    packet_id: str | None = None,
    source: str = "unknown",
    action: str = "unknown",
    status: str = "unknown",
) -> MicrobiotaRecord:
    """Helper funcional para actualizar memoria existente sin instanciar clase."""
    microbiota = InformationalMicrobiota(memory)
    record = microbiota.observe(
        payload,
        packet_id=packet_id,
        source=source,
        action=action,
        status=status,
    )
    memory.clear()
    memory.update(microbiota.export_memory())
    return record
