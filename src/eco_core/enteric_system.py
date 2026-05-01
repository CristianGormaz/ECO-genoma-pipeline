"""
Sistema Entérico Integrado E.C.O.
=================================

Orquestador bioinspirado que une ingesta, sensado, reflejo local,
motilidad, absorción, cuarentena, descarte y homeostasis.

La analogía correcta no es "el código está vivo". La idea técnica es más
precisa: el Sistema Nervioso Entérico muestra cómo una red distribuida puede
tomar microdecisiones locales sin enviar cada señal a un centro único. Este
módulo traduce ese patrón a una arquitectura de datos trazable y testeable.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from .absorption import absorb_dna_packet, gc_percent, n_percent
from .discard import discard_packet
from .filtering import (
    DNA_ALPHABET,
    filter_dna_packet,
    has_rejection,
    normalize_dna_sequence,
    validate_dna_sequence,
)
from .flow import EcoPacket, route_packet
from .ingestion import ingest_text


@dataclass(frozen=True)
class EntericDecision:
    """Decisión local del sistema entérico informacional."""

    action: str
    status: str
    reason: str
    confidence: float
    route: str


@dataclass(frozen=True)
class EntericHomeostasis:
    """Resumen del estado interno del sistema entérico E.C.O."""

    total_packets: int
    absorbed_packets: int
    quarantined_packets: int
    discarded_packets: int
    rejected_packets: int
    duplicate_packets: int
    state: str
    notes: List[str]


class EntericSystem:
    """Capa de coordinación entérica para paquetes E.C.O.

    La clase no reemplaza los scripts existentes: los organiza bajo una lógica
    de reflejos locales. Su objetivo es responder preguntas como:

    - ¿El dato puede entrar?
    - ¿Debe absorberse, rechazarse o quedar en cuarentena?
    - ¿Es duplicado o demasiado ambiguo?
    - ¿Qué estado general está dejando el flujo?
    """

    def __init__(
        self,
        *,
        min_length: int = 6,
        max_n_percent: float = 25.0,
        heavy_payload_threshold: int = 10_000,
    ) -> None:
        self.min_length = min_length
        self.max_n_percent = max_n_percent
        self.heavy_payload_threshold = heavy_payload_threshold
        self.microbiome_memory: Dict[str, Dict[str, Any]] = {}
        self.processed_packets: List[EcoPacket] = []

    def ingest(self, payload: Any, source: str = "manual_input", packet_type: str = "dna") -> EcoPacket:
        """Ingiere un dato como paquete E.C.O. trazable."""
        if isinstance(payload, str):
            return ingest_text(payload, source=source, packet_type=packet_type)

        packet = EcoPacket(payload=payload, source=source, packet_type=packet_type)
        return route_packet(packet, stage="ingestion", message="Dato no textual ingerido por E.C.O.")

    def sense(self, packet: EcoPacket) -> Dict[str, Any]:
        """Genera un perfil sensorial del paquete antes de decidir qué hacer."""
        is_text = isinstance(packet.payload, str)
        normalized = normalize_dna_sequence(packet.payload) if is_text else ""
        invalid_characters = sorted(set(normalized) - DNA_ALPHABET) if is_text else []
        issues = validate_dna_sequence(normalized) if is_text else ["El payload no es texto."]
        payload_key = self._payload_key(packet.payload)

        return {
            "packet_id": packet.packet_id,
            "source": packet.source,
            "packet_type": packet.packet_type,
            "payload_type": type(packet.payload).__name__,
            "is_text": is_text,
            "is_empty": is_text and len(normalized) == 0,
            "length": len(normalized) if is_text else 0,
            "gc_percent": gc_percent(normalized) if is_text else 0.0,
            "n_percent": n_percent(normalized) if is_text else 0.0,
            "invalid_characters": invalid_characters,
            "filter_issues": issues,
            "is_duplicate": payload_key in self.microbiome_memory,
            "is_heavy": is_text and len(normalized) >= self.heavy_payload_threshold,
            "payload_key": payload_key,
        }

    def local_reflex(self, sensory_profile: Dict[str, Any]) -> EntericDecision:
        """Decide la ruta local del paquete según su perfil sensorial."""
        if not sensory_profile["is_text"]:
            return EntericDecision(
                action="reject",
                status="rejected",
                reason="Payload no textual: el epitelio informacional no puede validarlo como ADN.",
                confidence=0.98,
                route="immune_discard",
            )

        if sensory_profile["is_empty"]:
            return EntericDecision(
                action="reject",
                status="rejected",
                reason="Secuencia vacía: no contiene nutriente informacional.",
                confidence=0.99,
                route="immune_discard",
            )

        if sensory_profile["invalid_characters"]:
            invalid = ", ".join(sensory_profile["invalid_characters"])
            return EntericDecision(
                action="reject",
                status="rejected",
                reason=f"Secuencia con caracteres no válidos: {invalid}.",
                confidence=0.97,
                route="immune_discard",
            )

        if sensory_profile["is_duplicate"]:
            return EntericDecision(
                action="discard_duplicate",
                status="discarded",
                reason="Secuencia duplicada: se evita absorber redundancia como conocimiento nuevo.",
                confidence=0.9,
                route="controlled_discard",
            )

        if sensory_profile["length"] < self.min_length:
            return EntericDecision(
                action="quarantine",
                status="quarantined",
                reason="Secuencia demasiado corta: requiere revisión antes de absorberse.",
                confidence=0.82,
                route="quarantine",
            )

        if sensory_profile["n_percent"] > self.max_n_percent:
            return EntericDecision(
                action="quarantine",
                status="quarantined",
                reason="Secuencia con exceso de bases ambiguas N: se deriva a cuarentena.",
                confidence=0.86,
                route="quarantine",
            )

        if sensory_profile["is_heavy"]:
            return EntericDecision(
                action="batch_absorb",
                status="batched",
                reason="Secuencia grande: se absorbe con marca de procesamiento por lotes.",
                confidence=0.78,
                route="myenteric_batch_flow",
            )

        return EntericDecision(
            action="absorb",
            status="ok",
            reason="Secuencia apta para absorción informacional.",
            confidence=0.92,
            route="submucosal_absorption",
        )

    def process_packet(self, packet: EcoPacket) -> EcoPacket:
        """Procesa un paquete completo con lógica entérica integrada."""
        route_packet(
            packet,
            stage="enteric_epithelium",
            message="El paquete entra a la barrera epitelial informacional.",
        )

        sensory_profile = self.sense(packet)
        packet.metadata["enteric_sensory_profile"] = sensory_profile
        route_packet(
            packet,
            stage="enteric_sensing",
            message="Perfil sensorial generado antes de la microdecisión local.",
        )

        decision = self.local_reflex(sensory_profile)
        packet.metadata["enteric_decision"] = asdict(decision)
        route_packet(
            packet,
            stage="enteric_reflex",
            status=decision.status,
            message=decision.reason,
        )

        if decision.action == "reject":
            discard_packet(packet, reason=decision.reason)
        elif decision.action == "discard_duplicate":
            discard_packet(packet, reason=decision.reason)
        elif decision.action == "quarantine":
            packet.metadata["quarantine_reason"] = decision.reason
            route_packet(
                packet,
                stage="enteric_quarantine",
                status="quarantined",
                message="Paquete conservado para revisión; no se absorbe todavía.",
            )
        elif decision.action in {"absorb", "batch_absorb"}:
            packet = filter_dna_packet(packet)
            if has_rejection(packet):
                discard_packet(packet, reason="Filtro ADN rechazó el paquete durante validación secundaria.")
            else:
                if decision.action == "batch_absorb":
                    packet.metadata["batch_recommended"] = True
                    route_packet(
                        packet,
                        stage="enteric_motility",
                        status="batched",
                        message="Plexo mientérico digital marca el paquete para procesamiento por lotes.",
                    )
                packet = absorb_dna_packet(packet)

        self.update_microbiome(packet)
        self.processed_packets.append(packet)
        return packet

    def process_dna_sequence(self, sequence: str, source: str = "manual_sequence") -> EcoPacket:
        """Atajo UX para ingerir y procesar una secuencia ADN."""
        packet = self.ingest(sequence, source=source, packet_type="dna")
        return self.process_packet(packet)

    def update_microbiome(self, packet: EcoPacket) -> None:
        """Actualiza memoria adaptativa mínima del sistema."""
        payload_key = self._payload_key(packet.payload)
        previous = self.microbiome_memory.get(payload_key, {})
        seen_count = int(previous.get("seen_count", 0)) + 1
        decision = packet.metadata.get("enteric_decision", {})

        self.microbiome_memory[payload_key] = {
            "seen_count": seen_count,
            "last_packet_id": packet.packet_id,
            "last_source": packet.source,
            "last_action": decision.get("action", "unknown"),
            "last_status": decision.get("status", "unknown"),
        }
        packet.metadata["microbiome_seen_count"] = seen_count

    def homeostasis_report(self) -> EntericHomeostasis:
        """Resume estabilidad del flujo entérico procesado hasta ahora."""
        total = len(self.processed_packets)
        absorbed = sum(1 for packet in self.processed_packets if "absorbed_features" in packet.metadata)
        quarantined = sum(self._has_status(packet, "quarantined") for packet in self.processed_packets)
        discarded = sum(self._has_status(packet, "discarded") for packet in self.processed_packets)
        rejected = sum(self._has_status(packet, "rejected") for packet in self.processed_packets)
        duplicates = sum(
            1
            for packet in self.processed_packets
            if packet.metadata.get("enteric_decision", {}).get("action") == "discard_duplicate"
        )

        notes: List[str] = []
        if total == 0:
            return EntericHomeostasis(0, 0, 0, 0, 0, 0, "idle", ["Sin paquetes procesados."])
        if rejected / total > 0.4:
            notes.append("Alta respuesta inmune: revisar calidad de entrada.")
        if quarantined / total > 0.3:
            notes.append("Cuarentena elevada: revisar longitud mínima o ambigüedad de secuencias.")
        if duplicates:
            notes.append("Se detectó redundancia: la microbiota informacional evitó absorción duplicada.")
        if not notes:
            notes.append("Homeostasis estable: flujo informacional dentro de rangos esperados.")

        state = "attention" if rejected / total > 0.4 or quarantined / total > 0.3 else "stable"
        return EntericHomeostasis(
            total_packets=total,
            absorbed_packets=absorbed,
            quarantined_packets=quarantined,
            discarded_packets=discarded,
            rejected_packets=rejected,
            duplicate_packets=duplicates,
            state=state,
            notes=notes,
        )

    @staticmethod
    def _has_status(packet: EcoPacket, status: str) -> bool:
        return any(log.status == status for log in packet.history)

    @staticmethod
    def _payload_key(payload: Any) -> str:
        if isinstance(payload, str):
            return normalize_dna_sequence(payload)
        return repr(payload)
