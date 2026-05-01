from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from .absorption import absorb_dna_packet
from .barrier import evaluate_barrier
from .discard import discard_packet
from .filtering import filter_dna_packet, has_rejection
from .flow import EcoPacket, route_packet
from .ingestion import ingest_text
from .motility import MotilityDecision, decide_motility
from .sensor_local import SensoryProfile, analyze_packet, build_payload_key


@dataclass(frozen=True)
class EntericDecision:
    action: str
    status: str
    reason: str
    confidence: float
    route: str


@dataclass(frozen=True)
class EntericHomeostasis:
    total_packets: int
    absorbed_packets: int
    quarantined_packets: int
    discarded_packets: int
    rejected_packets: int
    duplicate_packets: int
    state: str
    notes: List[str]


class EntericSystem:
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
        if isinstance(payload, str):
            return ingest_text(payload, source=source, packet_type=packet_type)
        packet = EcoPacket(payload=payload, source=source, packet_type=packet_type)
        return route_packet(packet, stage="ingestion", message="Dato no textual ingerido por E.C.O.")

    def sense(self, packet: EcoPacket) -> Dict[str, Any]:
        profile = analyze_packet(
            packet,
            known_payload_keys=self.microbiome_memory.keys(),
            heavy_payload_threshold=self.heavy_payload_threshold,
        )
        return profile.to_dict()

    def motility_reflex(self, sensory_profile: Dict[str, Any]) -> MotilityDecision:
        """Decide movimiento operativo usando barrera + plexo mientérico digital."""
        profile = self._sensory_profile_from_dict(sensory_profile)
        barrier_result = evaluate_barrier(
            is_text=profile.is_text,
            is_empty=profile.is_empty,
            invalid_characters=list(profile.invalid_characters),
            length=profile.length,
            min_length=self.min_length,
            n_percent=profile.n_percent,
            max_n_percent=self.max_n_percent,
        )
        return decide_motility(profile, barrier_result)

    def local_reflex(
        self,
        sensory_profile: Dict[str, Any],
        motility_decision: MotilityDecision | None = None,
    ) -> EntericDecision:
        """Convierte la motilidad mientérica en decisión compatible con el flujo histórico."""
        motility = motility_decision or self.motility_reflex(sensory_profile)

        if motility.action == "immune_discard":
            return EntericDecision("reject", motility.status, motility.reason, 0.97, motility.route)
        if motility.action == "discard_duplicate":
            return EntericDecision("discard_duplicate", motility.status, motility.reason, 0.9, motility.route)
        if motility.action == "quarantine":
            return EntericDecision("quarantine", motility.status, motility.reason, 0.84, motility.route)
        if motility.action == "batch_advance":
            return EntericDecision("batch_absorb", motility.status, motility.reason, 0.78, motility.route)
        return EntericDecision("absorb", motility.status, motility.reason, 0.92, motility.route)

    def process_packet(self, packet: EcoPacket) -> EcoPacket:
        route_packet(packet, stage="enteric_epithelium", message="El paquete entra a la barrera epitelial informacional.")
        sensory_profile = self.sense(packet)
        packet.metadata["enteric_sensory_profile"] = sensory_profile
        route_packet(packet, stage="enteric_sensing", message="Perfil sensorial generado antes de la microdecisión local.")

        motility_decision = self.motility_reflex(sensory_profile)
        packet.metadata["myenteric_motility_decision"] = asdict(motility_decision)
        route_packet(
            packet,
            stage="enteric_motility",
            status=motility_decision.status,
            message=motility_decision.reason,
        )

        decision = self.local_reflex(sensory_profile, motility_decision)
        packet.metadata["enteric_decision"] = asdict(decision)
        route_packet(packet, stage="enteric_reflex", status=decision.status, message=decision.reason)

        if decision.action == "reject":
            discard_packet(packet, reason=decision.reason)
        elif decision.action == "discard_duplicate":
            discard_packet(packet, reason=decision.reason)
        elif decision.action == "quarantine":
            packet.metadata["quarantine_reason"] = decision.reason
            route_packet(packet, stage="enteric_quarantine", status="quarantined", message="Paquete conservado para revisión; no se absorbe todavía.")
        elif decision.action in {"absorb", "batch_absorb"}:
            packet = filter_dna_packet(packet)
            if has_rejection(packet):
                discard_packet(packet, reason="Filtro ADN rechazó el paquete durante validación secundaria.")
            else:
                if decision.action == "batch_absorb":
                    packet.metadata["batch_recommended"] = True
                    route_packet(packet, stage="enteric_batch_flow", status="batched", message="Plexo mientérico digital marca el paquete para procesamiento por lotes.")
                packet = absorb_dna_packet(packet)

        self.update_microbiome(packet)
        self.processed_packets.append(packet)
        return packet

    def process_dna_sequence(self, sequence: str, source: str = "manual_sequence") -> EcoPacket:
        packet = self.ingest(sequence, source=source, packet_type="dna")
        return self.process_packet(packet)

    def update_microbiome(self, packet: EcoPacket) -> None:
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
        total = len(self.processed_packets)
        absorbed = sum(1 for packet in self.processed_packets if "absorbed_features" in packet.metadata)
        quarantined = sum(self._has_status(packet, "quarantined") for packet in self.processed_packets)
        discarded = sum(self._has_status(packet, "discarded") for packet in self.processed_packets)
        rejected = sum(self._has_status(packet, "rejected") for packet in self.processed_packets)
        duplicates = sum(1 for packet in self.processed_packets if packet.metadata.get("enteric_decision", {}).get("action") == "discard_duplicate")
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
        return EntericHomeostasis(total, absorbed, quarantined, discarded, rejected, duplicates, state, notes)

    @staticmethod
    def _has_status(packet: EcoPacket, status: str) -> bool:
        return any(log.status == status for log in packet.history)

    @staticmethod
    def _payload_key(payload: Any) -> str:
        return build_payload_key(payload)

    @staticmethod
    def _sensory_profile_from_dict(data: Dict[str, Any]) -> SensoryProfile:
        return SensoryProfile(
            packet_id=data.get("packet_id"),
            source=data.get("source", "manual_input"),
            packet_type=data.get("packet_type", "unknown"),
            payload_type=data.get("payload_type", "unknown"),
            is_text=bool(data.get("is_text", False)),
            is_empty=bool(data.get("is_empty", False)),
            length=int(data.get("length", 0)),
            gc_percent=float(data.get("gc_percent", 0.0)),
            n_percent=float(data.get("n_percent", 0.0)),
            invalid_characters=tuple(data.get("invalid_characters", [])),
            filter_issues=tuple(data.get("filter_issues", [])),
            is_duplicate=bool(data.get("is_duplicate", False)),
            is_heavy=bool(data.get("is_heavy", False)),
            payload_key=str(data.get("payload_key", "")),
        )
