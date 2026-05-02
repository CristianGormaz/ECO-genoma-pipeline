"""
Baseline adaptativo de transición de estados E.C.O.
==================================================

Modelo mínimo, auditable y sin dependencias externas para predecir `state_after`
a partir de señales internas del dataset adaptativo S.N.E.-E.C.O.

No es deep learning. No modela conciencia. No es clínico ni forense.
Su función es comparar reglas aprendidas simples contra el estado observado del
pipeline y preparar el camino para futuros modelos más robustos.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from typing import Iterable

from .adaptive_state_dataset import AdaptiveStateRow

FeatureKey = tuple[str, str, str, str, str]
DigestiveKey = tuple[str, str, str, str]
DefenseKey = tuple[str, str]


@dataclass(frozen=True)
class StateBaselinePrediction:
    """Predicción auditable para una fila adaptativa."""

    source: str
    observed_state: str
    predicted_state: str
    matched_rule: str
    confidence: float
    correct: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class StateTransitionBaseline:
    """Tabla entrenada de transiciones categóricas observadas.

    La predicción usa una jerarquía auditable:
    1. feature_key: ruta exacta completa.
    2. digestive_key: familia digestiva sin `state_before`.
    3. defense_key: familia defensiva mínima.
    4. homeostasis_projection: desempate técnico cuando una regla de bajo
       soporte contradice la presión homeostática estimada.
    5. default_state: estado dominante del entrenamiento.
    """

    transition_table: dict[FeatureKey, dict[str, int]]
    digestive_table: dict[DigestiveKey, dict[str, int]]
    defense_table: dict[DefenseKey, dict[str, int]]
    default_state: str
    default_confidence: float
    training_rows: int

    def predict(self, row: AdaptiveStateRow) -> StateBaselinePrediction:
        projected_state = project_homeostatic_state(row)

        for matched_rule, counts in (
            ("feature_key", self.transition_table.get(feature_key(row))),
            ("digestive_key", self.digestive_table.get(digestive_key(row))),
            ("defense_key", self.defense_table.get(defense_key(row))),
        ):
            if counts:
                predicted, votes = _winner(counts)
                total = sum(counts.values())
                confidence = round(votes / total, 4)
                if _should_use_homeostasis_projection(
                    learned_state=predicted,
                    projected_state=projected_state,
                    support=total,
                ):
                    return StateBaselinePrediction(
                        source=row.source,
                        observed_state=row.state_after,
                        predicted_state=projected_state,
                        matched_rule="homeostasis_projection",
                        confidence=0.75,
                        correct=projected_state == row.state_after,
                    )
                return StateBaselinePrediction(
                    source=row.source,
                    observed_state=row.state_after,
                    predicted_state=predicted,
                    matched_rule=matched_rule,
                    confidence=confidence,
                    correct=predicted == row.state_after,
                )

        return StateBaselinePrediction(
            source=row.source,
            observed_state=row.state_after,
            predicted_state=projected_state,
            matched_rule="homeostasis_projection",
            confidence=0.6,
            correct=projected_state == row.state_after,
        )


def feature_key(row: AdaptiveStateRow) -> FeatureKey:
    """Clave categórica completa para aprender transiciones auditables."""
    return (
        row.state_before,
        row.barrier_status,
        row.motility_action,
        row.defense_category,
        row.final_decision,
    )


def digestive_key(row: AdaptiveStateRow) -> DigestiveKey:
    """Familia digestiva sin depender del estado previo exacto."""
    return (
        row.barrier_status,
        row.motility_action,
        row.defense_category,
        row.final_decision,
    )


def defense_key(row: AdaptiveStateRow) -> DefenseKey:
    """Familia defensiva mínima para evitar fallback prematuro."""
    return (
        row.defense_category,
        row.final_decision,
    )


def project_homeostatic_state(row: AdaptiveStateRow) -> str:
    """Proyecta el estado homeostático después de aplicar la decisión actual.

    Usa métricas previas + decisión final del paquete, evitando depender de
    `state_after`. Sirve como desempate técnico cuando una regla aprendida tiene
    bajo soporte y contradice la presión homeostática esperada.
    """
    total_before = row.total_packets_before
    total_after = total_before + 1
    if total_after <= 0:
        return "idle"

    absorbed = _count_from_ratio(row.absorption_ratio_before, total_before)
    immune = _count_from_ratio(row.immune_load_before, total_before)
    quarantined = _count_from_ratio(row.quarantine_ratio_before, total_before)

    if row.final_decision == "absorb":
        absorbed += 1
    elif row.final_decision == "quarantine":
        quarantined += 1
    elif row.final_decision == "reject":
        immune += 1

    absorption_ratio = round(absorbed / total_after, 4)
    immune_load = round(immune / total_after, 4)
    quarantine_ratio = round(quarantined / total_after, 4)

    return _classify_projected_state(
        immune_load=immune_load,
        quarantine_ratio=quarantine_ratio,
        absorption_ratio=absorption_ratio,
    )


def train_state_transition_baseline(rows: Iterable[AdaptiveStateRow]) -> StateTransitionBaseline:
    """Entrena tablas jerárquicas de transición categórica desde filas adaptativas."""
    row_list = list(rows)
    table: dict[FeatureKey, Counter[str]] = defaultdict(Counter)
    digestive: dict[DigestiveKey, Counter[str]] = defaultdict(Counter)
    defense: dict[DefenseKey, Counter[str]] = defaultdict(Counter)
    state_counts: Counter[str] = Counter()

    for row in row_list:
        table[feature_key(row)][row.state_after] += 1
        digestive[digestive_key(row)][row.state_after] += 1
        defense[defense_key(row)][row.state_after] += 1
        state_counts[row.state_after] += 1

    if state_counts:
        default_state, votes = state_counts.most_common(1)[0]
        default_confidence = round(votes / len(row_list), 4)
    else:
        default_state = "unknown"
        default_confidence = 0.0

    return StateTransitionBaseline(
        transition_table={key: dict(value) for key, value in table.items()},
        digestive_table={key: dict(value) for key, value in digestive.items()},
        defense_table={key: dict(value) for key, value in defense.items()},
        default_state=default_state,
        default_confidence=default_confidence,
        training_rows=len(row_list),
    )


def evaluate_state_transition_baseline(rows: Iterable[AdaptiveStateRow]) -> dict[str, object]:
    """Entrena y evalúa el baseline sobre las filas entregadas.

    Esta evaluación es demostrativa/resustitución si se usa el mismo set para
    entrenar y predecir. No debe presentarse como desempeño general.
    """
    row_list = list(rows)
    model = train_state_transition_baseline(row_list)
    predictions = [model.predict(row) for row in row_list]
    correct = sum(prediction.correct for prediction in predictions)
    total = len(predictions)
    accuracy = round(correct / total, 4) if total else 0.0

    return {
        "model_name": "adaptive_state_baseline_v0_hierarchical",
        "training_rows": model.training_rows,
        "rule_count": len(model.transition_table),
        "digestive_rule_count": len(model.digestive_table),
        "defense_rule_count": len(model.defense_table),
        "default_state": model.default_state,
        "accuracy_demo": accuracy,
        "predictions": [prediction.to_dict() for prediction in predictions],
        "responsible_limit": "Evaluación demostrativa sobre dataset mínimo; no representa desempeño general ni modelo de conciencia humana.",
    }


def baseline_report_to_markdown(report: dict[str, object]) -> str:
    """Renderiza el reporte del baseline en Markdown simple."""
    predictions = report.get("predictions", [])
    lines = [
        "# Baseline adaptativo E.C.O. v0",
        "",
        "Modelo categórico mínimo para predecir `state_after` desde señales internas del pipeline.",
        "",
        f"Modelo: `{report.get('model_name')}`",
        f"Filas de entrenamiento: {report.get('training_rows')}",
        f"Reglas exactas aprendidas: {report.get('rule_count')}",
        f"Reglas digestivas aprendidas: {report.get('digestive_rule_count')}",
        f"Reglas defensivas aprendidas: {report.get('defense_rule_count')}",
        f"Estado por defecto: `{report.get('default_state')}`",
        f"Accuracy demostrativa: {report.get('accuracy_demo')}",
        "",
        "| source | observed | predicted | rule | confidence | correct |",
        "|---|---|---|---|---|---|",
    ]
    for item in predictions:
        if isinstance(item, dict):
            lines.append(
                "| "
                f"{item.get('source')} | "
                f"{item.get('observed_state')} | "
                f"{item.get('predicted_state')} | "
                f"{item.get('matched_rule')} | "
                f"{item.get('confidence')} | "
                f"{item.get('correct')} |"
            )

    lines.extend(
        [
            "",
            "## Límite responsable",
            "",
            str(report.get("responsible_limit")),
        ]
    )
    return "\n".join(lines)


def _should_use_homeostasis_projection(*, learned_state: str, projected_state: str, support: int) -> bool:
    """Usa proyección si una regla de muy bajo soporte contradice la homeostasis."""
    return support <= 1 and learned_state != projected_state


def _count_from_ratio(ratio: float, total: int) -> int:
    if total <= 0:
        return 0
    return int(round(ratio * total))


def _classify_projected_state(*, immune_load: float, quarantine_ratio: float, absorption_ratio: float) -> str:
    if immune_load > 0.6:
        return "overload"
    if immune_load > 0.4 or quarantine_ratio > 0.3:
        return "attention"
    if absorption_ratio >= 0.7:
        return "stable"
    return "watch"


def _winner(counts: dict[str, int]) -> tuple[str, int]:
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0]
