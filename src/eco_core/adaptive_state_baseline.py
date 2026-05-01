"""
Baseline adaptativo de transición de estados E.C.O.
==================================================

Modelo mínimo, auditable y sin dependencias externas para predecir `state_after`
a partir de señales internas del dataset adaptativo S.N.E.-E.C.O.

No es deep learning. No modela conciencia. No es clínico ni forense.
Su función es comparar una regla aprendida simple contra el estado observado del
pipeline y preparar el camino para futuros modelos más robustos.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from typing import Iterable

from .adaptive_state_dataset import AdaptiveStateRow

FeatureKey = tuple[str, str, str, str, str]


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
    """Tabla entrenada de transiciones categóricas observadas."""

    transition_table: dict[FeatureKey, dict[str, int]]
    default_state: str
    default_confidence: float
    training_rows: int

    def predict(self, row: AdaptiveStateRow) -> StateBaselinePrediction:
        key = feature_key(row)
        counts = self.transition_table.get(key)
        if counts:
            predicted, votes = _winner(counts)
            total = sum(counts.values())
            confidence = round(votes / total, 4)
            matched_rule = "feature_key"
        else:
            predicted = self.default_state
            confidence = self.default_confidence
            matched_rule = "default_state"

        return StateBaselinePrediction(
            source=row.source,
            observed_state=row.state_after,
            predicted_state=predicted,
            matched_rule=matched_rule,
            confidence=confidence,
            correct=predicted == row.state_after,
        )


def feature_key(row: AdaptiveStateRow) -> FeatureKey:
    """Claves categóricas mínimas para aprender transiciones auditables."""
    return (
        row.state_before,
        row.barrier_status,
        row.motility_action,
        row.defense_category,
        row.final_decision,
    )


def train_state_transition_baseline(rows: Iterable[AdaptiveStateRow]) -> StateTransitionBaseline:
    """Entrena una tabla de transición categórica desde filas adaptativas."""
    row_list = list(rows)
    table: dict[FeatureKey, Counter[str]] = defaultdict(Counter)
    state_counts: Counter[str] = Counter()

    for row in row_list:
        table[feature_key(row)][row.state_after] += 1
        state_counts[row.state_after] += 1

    if state_counts:
        default_state, votes = state_counts.most_common(1)[0]
        default_confidence = round(votes / len(row_list), 4)
    else:
        default_state = "unknown"
        default_confidence = 0.0

    return StateTransitionBaseline(
        transition_table={key: dict(value) for key, value in table.items()},
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
        "model_name": "adaptive_state_baseline_v0",
        "training_rows": model.training_rows,
        "rule_count": len(model.transition_table),
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
        f"Reglas aprendidas: {report.get('rule_count')}",
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


def _winner(counts: dict[str, int]) -> tuple[str, int]:
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0]
