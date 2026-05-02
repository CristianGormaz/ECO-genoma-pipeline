"""
Dataset adaptativo de transición de estados E.C.O.
=================================================

Construye filas entrenables a partir del tránsito de paquetes por S.N.E.-E.C.O.

Cada fila resume:
- señales digestivas del paquete;
- homeostasis antes de procesarlo;
- homeostasis después de procesarlo.

No modela conciencia humana, no diagnostica y no interpreta casos forenses. Solo
convierte eventos técnicos del pipeline en datos de transición observables.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Sequence

from .enteric_system import EntericSystem
from .homeostasis import HomeostasisSnapshot
from .packet_trace import PacketTrace, build_packet_trace


@dataclass(frozen=True)
class AdaptiveStateRow:
    """Fila mínima para entrenar o auditar transiciones de estado E.C.O."""

    packet_id: str
    source: str
    payload_length: int
    barrier_status: str
    barrier_permeability: float
    motility_action: str
    defense_category: str
    defense_severity: str
    final_decision: str
    microbiota_seen_count: int
    state_before: str
    state_after: str
    total_packets_before: int
    total_packets_after: int
    absorption_ratio_before: float
    absorption_ratio_after: float
    immune_load_before: float
    immune_load_after: float
    quarantine_ratio_before: float
    quarantine_ratio_after: float
    recurrence_ratio_before: float
    recurrence_ratio_after: float
    responsible_limit: str = "Pipeline educativo/experimental; no modela conciencia humana ni uso clínico/forense."

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def build_adaptive_state_row(
    *,
    trace: PacketTrace,
    before: HomeostasisSnapshot,
    after: HomeostasisSnapshot,
) -> AdaptiveStateRow:
    """Combina una traza digestiva con homeostasis antes/después."""
    return AdaptiveStateRow(
        packet_id=trace.packet_id,
        source=trace.source,
        payload_length=trace.payload_length,
        barrier_status=trace.barrier_status,
        barrier_permeability=trace.barrier_permeability,
        motility_action=trace.motility_action,
        defense_category=trace.defense_category,
        defense_severity=trace.defense_severity,
        final_decision=trace.final_decision,
        microbiota_seen_count=trace.microbiota_seen_count,
        state_before=before.state,
        state_after=after.state,
        total_packets_before=before.total_packets,
        total_packets_after=after.total_packets,
        absorption_ratio_before=before.absorption_ratio,
        absorption_ratio_after=after.absorption_ratio,
        immune_load_before=before.immune_load,
        immune_load_after=after.immune_load,
        quarantine_ratio_before=before.quarantine_ratio,
        quarantine_ratio_after=after.quarantine_ratio,
        recurrence_ratio_before=before.recurrence_ratio,
        recurrence_ratio_after=after.recurrence_ratio,
    )


def build_adaptive_state_rows(
    packets: Sequence[tuple[str, str]] | Iterable[tuple[str, str]],
    *,
    system: EntericSystem | None = None,
) -> list[AdaptiveStateRow]:
    """Procesa secuencias y genera una fila de transición por paquete."""
    active_system = system or EntericSystem(min_length=6, max_n_percent=25.0, heavy_payload_threshold=10_000)
    rows: list[AdaptiveStateRow] = []

    for source, sequence in packets:
        before = active_system.homeostasis_snapshot()
        packet = active_system.process_dna_sequence(sequence, source=source)
        after = active_system.homeostasis_snapshot()
        trace = build_packet_trace(packet)
        rows.append(build_adaptive_state_row(trace=trace, before=before, after=after))

    return rows


def rows_to_dicts(rows: Iterable[AdaptiveStateRow]) -> list[dict[str, object]]:
    """Convierte filas adaptativas en diccionarios serializables."""
    return [row.to_dict() for row in rows]


def adaptive_rows_to_markdown(rows: Iterable[AdaptiveStateRow]) -> str:
    """Renderiza un resumen Markdown del dataset adaptativo."""
    row_list = list(rows)
    lines = [
        "# Dataset adaptativo E.C.O.",
        "",
        "Transiciones observables del pipeline: estado antes + señales del paquete + estado después.",
        "",
        f"Filas generadas: {len(row_list)}",
        "",
        "| source | state_before | state_after | final_decision | barrier | motility | defense | immune_after |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in row_list:
        lines.append(
            "| "
            f"{row.source} | "
            f"{row.state_before} | "
            f"{row.state_after} | "
            f"{row.final_decision} | "
            f"{row.barrier_status} | "
            f"{row.motility_action} | "
            f"{row.defense_category}/{row.defense_severity} | "
            f"{row.immune_load_after} |"
        )

    lines.extend(
        [
            "",
            "## Límite responsable",
            "",
            "Este dataset no modela conciencia humana, no diagnostica y no debe usarse como herramienta clínica o forense.",
            "Su función es preparar datos auditables para estudiar transiciones internas del pipeline E.C.O.",
        ]
    )
    return "\n".join(lines)


def get_transition_packets(*, extended: bool = False) -> tuple[tuple[str, str], ...]:
    """Obtiene el catálogo mínimo o extendido de escenarios sintéticos."""
    return EXTENDED_TRANSITION_PACKETS if extended else DEFAULT_TRANSITION_PACKETS


DEFAULT_TRANSITION_PACKETS: tuple[tuple[str, str], ...] = (
    ("valid_sequence", "ACGTCCAATGGTATAAA"),
    ("invalid_sequence", "ACGTXYZ"),
    ("short_sequence", "ACG"),
    ("duplicate_sequence", "ACGTCCAATGGTATAAA"),
)


EXTENDED_TRANSITION_PACKETS: tuple[tuple[str, str], ...] = (
    # Absorción estable: rutas válidas que permiten observar homeostasis normal.
    ("valid_sequence_a", "ACGTCCAATGGTATAAA"),
    ("valid_sequence_b", "TTGACCGTAACCGGTA"),
    ("valid_gc_rich", "GGCGGCGGCGGCTAAT"),
    ("valid_at_rich", "ATATATAAACCCGGTT"),
    ("long_valid_sequence", "ACGTCCAATGGTATAAAGGCGGGCGGAATAAAGTAC"),

    # Retención/cuarentena: payloads demasiado cortos para absorber con confianza.
    ("short_sequence_a", "ACG"),
    ("short_sequence_b", "TTT"),
    ("short_sequence_c", "A"),
    ("short_sequence_d", "TG"),
    ("short_sequence_e", "CCCC"),

    # Rechazo defensivo: letras/símbolos externos al alfabeto técnico esperado.
    ("invalid_letters_a", "ACGTXYZ"),
    ("invalid_letters_b", "MUGICA"),
    ("invalid_letters_c", "XYZXYZ"),
    ("invalid_letters_d", "ACGT123"),
    ("invalid_letters_e", "ACGT-XYZ"),
    ("long_invalid_tail", "ACGTCCAATGGTATAAAGGCGGGCGGAATAAAGTACXYZ"),

    # Ambigüedad: presencia de N como señal de incertidumbre informacional.
    ("high_n_content", "NNNNNNNNACGT"),
    ("mixed_n_content", "ACGTNNNNACGT"),
    ("mixed_n_content_b", "ACNNGTACGT"),
    ("mixed_n_content_c", "ACGTNACGTN"),
    ("high_n_content_b", "NNNNACGTNNNN"),

    # Recurrencia/microbiota: repetición controlada para separar memoria de novedad.
    ("duplicate_sequence_a", "ACGTCCAATGGTATAAA"),
    ("duplicate_sequence_b", "TTGACCGTAACCGGTA"),
    ("recurrent_valid_a", "ACGTCCAATGGTATAAA"),
    ("recurrent_valid_b", "TTGACCGTAACCGGTA"),
    ("recurrent_valid_c", "GGCGGCGGCGGCTAAT"),
    ("duplicate_sequence_c", "GGCGGCGGCGGCTAAT"),
    ("recurrent_valid_d", "ATATATAAACCCGGTT"),
)

