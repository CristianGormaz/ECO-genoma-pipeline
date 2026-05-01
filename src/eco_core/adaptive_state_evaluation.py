"""
Evaluación honesta del baseline adaptativo E.C.O.
=================================================

Evalúa el baseline v0 separando filas de entrenamiento y prueba. La intención
no es inflar métricas, sino detectar si el baseline memoriza o si puede
responder ante transiciones no vistas.

No requiere dependencias externas.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .adaptive_state_baseline import StateBaselinePrediction, train_state_transition_baseline
from .adaptive_state_dataset import AdaptiveStateRow


@dataclass(frozen=True)
class HoldoutEvaluation:
    """Resultado auditable de evaluación holdout."""

    model_name: str
    training_rows: int
    test_rows: int
    accuracy_holdout: float
    macro_f1_holdout: float
    labels: tuple[str, ...]
    confusion_matrix: dict[str, dict[str, int]]
    predictions: tuple[StateBaselinePrediction, ...]
    responsible_limit: str = (
        "Evaluación holdout mínima sobre dataset pequeño; no representa desempeño general, "
        "no modela conciencia humana y no tiene uso clínico/forense."
    )

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["predictions"] = [prediction.to_dict() for prediction in self.predictions]
        return payload


def split_rows_holdout(rows: Iterable[AdaptiveStateRow]) -> tuple[list[AdaptiveStateRow], list[AdaptiveStateRow]]:
    """Divide filas de forma determinista: índices pares entrenan, impares prueban."""
    row_list = list(rows)
    if len(row_list) < 2:
        return row_list, []
    train = [row for index, row in enumerate(row_list) if index % 2 == 0]
    test = [row for index, row in enumerate(row_list) if index % 2 == 1]
    return train, test


def evaluate_state_transition_holdout(rows: Iterable[AdaptiveStateRow]) -> HoldoutEvaluation:
    """Entrena con una partición y evalúa en filas no usadas para entrenar."""
    train_rows, test_rows = split_rows_holdout(rows)
    model = train_state_transition_baseline(train_rows)
    predictions = tuple(model.predict(row) for row in test_rows)

    labels = tuple(sorted({row.state_after for row in test_rows} | {pred.predicted_state for pred in predictions}))
    matrix = build_confusion_matrix(predictions, labels)
    accuracy = _accuracy(predictions)
    macro_f1 = _macro_f1(matrix, labels)

    return HoldoutEvaluation(
        model_name="adaptive_state_baseline_v0_holdout",
        training_rows=len(train_rows),
        test_rows=len(test_rows),
        accuracy_holdout=accuracy,
        macro_f1_holdout=macro_f1,
        labels=labels,
        confusion_matrix=matrix,
        predictions=predictions,
    )


def build_confusion_matrix(
    predictions: Iterable[StateBaselinePrediction], labels: Iterable[str]
) -> dict[str, dict[str, int]]:
    """Construye matriz de confusión observed -> predicted."""
    label_list = list(labels)
    matrix = {observed: {predicted: 0 for predicted in label_list} for observed in label_list}
    for prediction in predictions:
        matrix.setdefault(prediction.observed_state, {label: 0 for label in label_list})
        matrix[prediction.observed_state].setdefault(prediction.predicted_state, 0)
        matrix[prediction.observed_state][prediction.predicted_state] += 1
    return matrix


def holdout_report_to_markdown(evaluation: HoldoutEvaluation) -> str:
    """Renderiza la evaluación holdout en Markdown."""
    lines = [
        "# Evaluación holdout del baseline adaptativo E.C.O. v0",
        "",
        "Evaluación mínima para distinguir funcionamiento de memorización.",
        "",
        f"Modelo: `{evaluation.model_name}`",
        f"Filas de entrenamiento: {evaluation.training_rows}",
        f"Filas de prueba: {evaluation.test_rows}",
        f"Accuracy holdout: {evaluation.accuracy_holdout}",
        f"Macro-F1 holdout: {evaluation.macro_f1_holdout}",
        "",
        "## Predicciones",
        "",
        "| source | observed | predicted | rule | confidence | correct |",
        "|---|---|---|---|---|---|",
    ]
    for prediction in evaluation.predictions:
        lines.append(
            "| "
            f"{prediction.source} | "
            f"{prediction.observed_state} | "
            f"{prediction.predicted_state} | "
            f"{prediction.matched_rule} | "
            f"{prediction.confidence} | "
            f"{prediction.correct} |"
        )

    lines.extend(["", "## Matriz de confusión", ""])
    labels = list(evaluation.labels)
    lines.append("| observed \\ predicted | " + " | ".join(labels) + " |")
    lines.append("|---|" + "---|" * len(labels))
    for observed in labels:
        row = [str(evaluation.confusion_matrix.get(observed, {}).get(predicted, 0)) for predicted in labels]
        lines.append(f"| {observed} | " + " | ".join(row) + " |")

    lines.extend(
        [
            "",
            "## Lectura responsable",
            "",
            evaluation.responsible_limit,
            "",
            "Una métrica baja en holdout no es fracaso: indica que el dataset mínimo todavía no cubre suficientes rutas de transición.",
        ]
    )
    return "\n".join(lines)


def _accuracy(predictions: tuple[StateBaselinePrediction, ...]) -> float:
    if not predictions:
        return 0.0
    correct = sum(prediction.correct for prediction in predictions)
    return round(correct / len(predictions), 4)


def _macro_f1(matrix: dict[str, dict[str, int]], labels: tuple[str, ...]) -> float:
    if not labels:
        return 0.0
    scores: list[float] = []
    for label in labels:
        tp = matrix.get(label, {}).get(label, 0)
        fp = sum(matrix.get(other, {}).get(label, 0) for other in labels if other != label)
        fn = sum(value for predicted, value in matrix.get(label, {}).items() if predicted != label)
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
        scores.append(f1)
    return round(sum(scores) / len(scores), 4)
