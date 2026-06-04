from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from .absorption import absorb_dna_packet
from .barrier import BarrierResult, evaluate_barrier
from .defense import DefenseSignal, evaluate_defense
from .discard import discard_packet
from .filtering import filter_dna_packet, has_rejection
from .flow import EcoPacket, route_packet
from .gut_brain_axis import GutBrainReport, build_gut_brain_report
from .homeostasis import HomeostasisSnapshot, build_homeostasis_snapshot
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
        return route_packet(
            packet,
            stage="ingestion",
            message="Dato no textual ingerido por E.C.O.",
            plexus="mucosa_epithelial",
        )

    def sense(self, packet: EcoPacket) -> Dict[str, Any]:
        profile = analyze_packet(
            packet,
            known_payload_keys=self.microbiome_memory.keys(),
            heavy_payload_threshold=self.heavy_payload_threshold,
        )
        return profile.to_dict()

    def barrier_reflex(self, sensory_profile: Dict[str, Any]) -> BarrierResult:
        """Evalúa permeabilidad usando la barrera/mucosa informacional."""
        profile = self._sensory_profile_from_dict(sensory_profile)
        return evaluate_barrier(
            is_text=profile.is_text,
            is_empty=profile.is_empty,
            invalid_characters=list(profile.invalid_characters),
            length=profile.length,
            min_length=self.min_length,
            n_percent=profile.n_percent,
            max_n_percent=self.max_n_percent,
        )

    def motility_reflex(
        self,
        sensory_profile: Dict[str, Any],
        barrier_result: BarrierResult | None = None,
    ) -> MotilityDecision:
        """Decide movimiento operativo usando barrera + plexo mientérico digital."""
        profile = self._sensory_profile_from_dict(sensory_profile)
        barrier = barrier_result or self.barrier_reflex(sensory_profile)
        return decide_motility(profile, barrier)

    def defense_reflex(
        self,
        sensory_profile: Dict[str, Any],
        barrier_result: BarrierResult,
        motility_decision: MotilityDecision,
    ) -> DefenseSignal:
        """Evalúa la respuesta defensiva informacional del paquete."""
        profile = self._sensory_profile_from_dict(sensory_profile)
        return evaluate_defense(profile, barrier_result, motility_decision)

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
        route_packet(
            packet,
            stage="enteric_epithelium",
            message="El paquete entra a la barrera epitelial informacional.",
            plexus="mucosa_epithelial",
        )
        sensory_profile = self.sense(packet)
        packet.metadata["enteric_sensory_profile"] = sensory_profile
        route_packet(
            packet,
            stage="enteric_sensing",
            message="Perfil sensorial generado antes de la microdecisión local.",
            plexus="plexo_submucoso",
        )

        barrier_result = self.barrier_reflex(sensory_profile)
        packet.metadata["enteric_barrier_result"] = asdict(barrier_result)
        for log_msg in barrier_result.internal_logs:
            route_packet(
                packet,
                stage="enteric_barrier:internal",
                status=barrier_result.status,
                message=log_msg,
                plexus="mucosa_epithelial",
            )
        route_packet(
            packet,
            stage="enteric_barrier",
            status=barrier_result.status,
            message=barrier_result.reason,
            plexus="mucosa_epithelial",
        )

        motility_decision = self.motility_reflex(sensory_profile, barrier_result)
        packet.metadata["myenteric_motility_decision"] = asdict(motility_decision)
        for log_msg in motility_decision.internal_logs:
            route_packet(
                packet,
                stage="enteric_motility:internal",
                status=motility_decision.status,
                message=log_msg,
                plexus="plexo_mienterico",
            )
        route_packet(
            packet,
            stage="enteric_motility",
            status=motility_decision.status,
            message=motility_decision.reason,
            plexus="plexo_mienterico",
        )

        defense_signal = self.defense_reflex(sensory_profile, barrier_result, motility_decision)
        packet.metadata["enteric_defense_signal"] = asdict(defense_signal)
        for log_msg in defense_signal.internal_logs:
            route_packet(
                packet,
                stage="enteric_defense:internal",
                status=defense_signal.severity,
                message=log_msg,
                plexus="sistema_inmune_entérico",
            )
        route_packet(
            packet,
            stage="enteric_defense",
            status=defense_signal.severity,
            message=defense_signal.reason,
            plexus="sistema_inmune_entérico",
        )

        decision = self.local_reflex(sensory_profile, motility_decision)
        packet.metadata["enteric_decision"] = asdict(decision)
        route_packet(
            packet,
            stage="enteric_reflex",
            status=decision.status,
            message=decision.reason,
            plexus="plexo_mienterico",
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
                plexus="plexo_mienterico",
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
                        stage="enteric_batch_flow",
                        status="batched",
                        message="Plexo mientérico digital marca el paquete para procesamiento por lotes.",
                        plexus="plexo_mienterico",
                    )
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

    def homeostasis_snapshot(self) -> HomeostasisSnapshot:
        """Entrega la lectura homeostática moderna del flujo procesado."""
        return build_homeostasis_snapshot(self.processed_packets)

    def gut_brain_report(self) -> GutBrainReport:
        """Construye un reporte comunicable del eje intestino-cerebro E.C.O."""
        return build_gut_brain_report(self.homeostasis_snapshot())

    def gut_brain_markdown(self) -> str:
        """Entrega el reporte del eje intestino-cerebro en Markdown."""
        return self.gut_brain_report().to_markdown()

    def homeostasis_report(self) -> EntericHomeostasis:
        """Mantiene el contrato histórico usando la snapshot canónica actual."""
        snapshot = self.homeostasis_snapshot()
        return EntericHomeostasis(
            snapshot.total_packets,
            snapshot.absorbed_packets,
            snapshot.quarantined_packets,
            snapshot.discarded_packets,
            snapshot.rejected_packets,
            snapshot.duplicate_packets,
            snapshot.state,
            list(snapshot.notes),
        )

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
