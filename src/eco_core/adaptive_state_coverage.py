"""
Diagnóstico de cobertura adaptativa E.C.O.
==========================================

Analiza si el dataset adaptativo cubre suficientes rutas digestivas para evaluar
un baseline de transición de estados.

No busca inflar métricas. Busca explicar qué rutas faltan y dónde el modelo cae
al estado por defecto.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from typing import Iterable

from .adaptive_state_baseline import feature_key
from .adaptive_state_dataset import AdaptiveStateRow
from .adaptive_state_evaluation import HoldoutEvaluation


@dataclass(frozen=True)
class CoverageDiagnostics:
    """Resumen auditable de cobertura de rutas adaptativas."""

    row_count: int
    unique_feature_routes: int
    state_counts: dict[str, int]
    decision_counts: dict[str, int]
    defense_counts: dict[str, int]
    motility_counts: dict[str, int]
    fallback_predictions: int
    incorrect_predictions: int
    coverage_warnings: tuple[str, ...]
    responsible_limit: str = (
        "Diagnóstico educativo/experimental; no representa desempeño general, "
        "no modela conciencia humana y no tiene uso clínico/forense."
    )

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def build_coverage_diagnostics(
    rows: Iterable[AdaptiveStateRow],
    *,
    evaluation: HoldoutEvaluation | None = None,
) -> CoverageDiagnostics:
    """Calcula cobertura de estados, decisiones y rutas categóricas."""
    row_list = list(rows)
    state_counts = Counter(row.state_after for row in row_list)
    decision_counts = Counter(row.final_decision for row in row_list)
    defense_counts = Counter(row.defense_category for row in row_list)
    motility_counts = Counter(row.motility_action for row in row_list)
    unique_routes = {feature_key(row) for row in row_list}

    fallback_predictions = 0
    incorrect_predictions = 0
    if evaluation:
        fallback_predictions = sum(pred.matched_rule == "default_state" for pred in evaluation.predictions)
        incorrect_predictions = sum(not pred.correct for pred in evaluation.predictions)

    warnings = build_coverage_warnings(
        row_count=len(row_list),
        state_counts=dict(state_counts),
        decision_counts=dict(decision_counts),
        fallback_predictions=fallback_predictions,
        incorrect_predictions=incorrect_predictions,
    )

    return CoverageDiagnostics(
        row_count=len(row_list),
        unique_feature_routes=len(unique_routes),
        state_counts=dict(sorted(state_counts.items())),
        decision_counts=dict(sorted(decision_counts.items())),
        defense_counts=dict(sorted(defense_counts.items())),
        motility_counts=dict(sorted(motility_counts.items())),
        fallback_predictions=fallback_predictions,
        incorrect_predictions=incorrect_predictions,
        coverage_warnings=tuple(warnings),
    )


def build_coverage_warnings(
    *,
    row_count: int,
    state_counts: dict[str, int],
    decision_counts: dict[str, int],
    fallback_predictions: int,
    incorrect_predictions: int,
) -> list[str]:
    """Genera advertencias accionables sobre cobertura insuficiente."""
    warnings: list[str] = []

    if row_count < 12:
        warnings.append("dataset_too_small: se recomiendan al menos 12 transiciones sintéticas para holdout inicial")

    for state in ("stable", "watch", "attention"):
        if state_counts.get(state, 0) < 3:
            warnings.append(f"state_underrepresented:{state}")

    for decision in ("absorb", "reject", "quarantine", "discard_duplicate"):
        if decision_counts.get(decision, 0) < 2:
            warnings.append(f"decision_underrepresented:{decision}")

    if fallback_predictions > 0:
        warnings.append("fallback_predictions_present: el baseline encontró rutas no vistas y usó estado por defecto")

    if incorrect_predictions > 0:
        warnings.append("incorrect_predictions_present: revisar rutas confundidas en matriz de confusión")

    return warnings


def coverage_report_to_markdown(diagnostics: CoverageDiagnostics) -> str:
    """Renderiza diagnóstico de cobertura en Markdown."""
    lines = [
        "# Diagnóstico de cobertura adaptativa E.C.O.",
        "",
        "Lectura de cobertura de rutas digestivas para el dataset adaptativo.",
        "",
        f"Filas: {diagnostics.row_count}",
        f"Rutas categóricas únicas: {diagnostics.unique_feature_routes}",
        f"Predicciones por defecto en holdout: {diagnostics.fallback_predictions}",
        f"Predicciones incorrectas en holdout: {diagnostics.incorrect_predictions}",
        "",
        "## Estados",
        "",
    ]
    for state, count in diagnostics.state_counts.items():
        lines.append(f"- `{state}`: {count}")

    lines.extend(["", "## Decisiones", ""])
    for decision, count in diagnostics.decision_counts.items():
        lines.append(f"- `{decision}`: {count}")

    lines.extend(["", "## Defensa", ""])
    for defense, count in diagnostics.defense_counts.items():
        lines.append(f"- `{defense}`: {count}")

    lines.extend(["", "## Advertencias accionables", ""])
    if diagnostics.coverage_warnings:
        for warning in diagnostics.coverage_warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- Sin advertencias críticas de cobertura.")

    lines.extend(
        [
            "",
            "## Límite responsable",
            "",
            diagnostics.responsible_limit,
        ]
    )
    return "\n".join(lines)
