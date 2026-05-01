"""
Análisis de rutas confundidas E.C.O.
====================================

Convierte los errores del holdout en recomendaciones accionables para ampliar
escenarios sintéticos sin agregar datos a ciegas.

No busca subir métricas artificialmente. Busca explicar qué rutas digestivas
faltan y qué estados quedan confundidos.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .adaptive_state_baseline import feature_key
from .adaptive_state_dataset import AdaptiveStateRow
from .adaptive_state_evaluation import split_rows_holdout
from .adaptive_state_evaluation import evaluate_state_transition_holdout


@dataclass(frozen=True)
class ConfusedRoute:
    """Ruta de prueba donde el baseline falló o usó default_state."""

    source: str
    state_before: str
    observed_state: str
    predicted_state: str
    matched_rule: str
    confidence: float
    final_decision: str
    barrier_status: str
    motility_action: str
    defense_category: str
    defense_severity: str
    feature_route: tuple[str, str, str, str, str]
    suggested_scenario: str
    reason: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class ConfusedRouteReport:
    """Reporte de rutas confundidas y siguientes escenarios sugeridos."""

    test_rows: int
    confused_routes: tuple[ConfusedRoute, ...]
    suggested_focus: tuple[str, ...]
    responsible_limit: str = (
        "Análisis educativo/experimental; no representa desempeño general, "
        "no modela conciencia humana y no tiene uso clínico/forense."
    )

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["confused_routes"] = [route.to_dict() for route in self.confused_routes]
        return payload


def analyze_confused_routes(rows: Iterable[AdaptiveStateRow]) -> ConfusedRouteReport:
    """Analiza filas de prueba donde el baseline falló o usó default_state."""
    row_list = list(rows)
    _, test_rows = split_rows_holdout(row_list)
    evaluation = evaluate_state_transition_holdout(row_list)
    test_by_source = {row.source: row for row in test_rows}

    confused: list[ConfusedRoute] = []
    for prediction in evaluation.predictions:
        if prediction.correct and prediction.matched_rule != "default_state":
            continue
        row = test_by_source[prediction.source]
        route = feature_key(row)
        confused.append(
            ConfusedRoute(
                source=row.source,
                state_before=row.state_before,
                observed_state=prediction.observed_state,
                predicted_state=prediction.predicted_state,
                matched_rule=prediction.matched_rule,
                confidence=prediction.confidence,
                final_decision=row.final_decision,
                barrier_status=row.barrier_status,
                motility_action=row.motility_action,
                defense_category=row.defense_category,
                defense_severity=row.defense_severity,
                feature_route=route,
                suggested_scenario=suggest_scenario(row, prediction.matched_rule),
                reason=explain_confusion(row, prediction.predicted_state, prediction.matched_rule),
            )
        )

    return ConfusedRouteReport(
        test_rows=len(test_rows),
        confused_routes=tuple(confused),
        suggested_focus=tuple(build_suggested_focus(confused)),
    )


def suggest_scenario(row: AdaptiveStateRow, matched_rule: str) -> str:
    """Sugiere el tipo de escenario sintético que cubriría mejor la ruta."""
    if matched_rule == "default_state":
        return f"add_training_route:{row.final_decision}:{row.defense_category}:{row.state_after}"
    if row.final_decision == "discard_duplicate":
        return "add_recurrence_variants_for_duplicate_routes"
    if row.final_decision == "quarantine":
        return "add_retained_payload_length_variants"
    if row.final_decision == "reject":
        return "add_invalid_payload_variants"
    if row.final_decision == "absorb":
        return "add_absorption_variants_for_stable_routes"
    return "review_route_manually"


def explain_confusion(row: AdaptiveStateRow, predicted_state: str, matched_rule: str) -> str:
    """Explica la confusión de forma breve y accionable."""
    if matched_rule == "default_state":
        return (
            "El baseline no vio una ruta equivalente durante entrenamiento y cayó al estado por defecto; "
            f"agregar más ejemplos con decisión {row.final_decision} y defensa {row.defense_category}."
        )
    return (
        f"La ruta fue conocida pero predijo {predicted_state} en vez de {row.state_after}; "
        "agregar variantes cercanas para separar mejor esos estados."
    )


def build_suggested_focus(routes: Iterable[ConfusedRoute]) -> list[str]:
    """Agrupa focos de mejora sin repetirlos."""
    focus: list[str] = []
    seen: set[str] = set()
    for route in routes:
        item = route.suggested_scenario
        if item not in seen:
            focus.append(item)
            seen.add(item)
    return focus


def confused_routes_to_markdown(report: ConfusedRouteReport) -> str:
    """Renderiza reporte de rutas confundidas en Markdown."""
    lines = [
        "# Análisis de rutas confundidas E.C.O.",
        "",
        "Lectura accionable de rutas donde el baseline falló o usó estado por defecto.",
        "",
        f"Filas de prueba: {report.test_rows}",
        f"Rutas confundidas: {len(report.confused_routes)}",
        "",
        "## Rutas",
        "",
        "| source | observed | predicted | rule | decision | defense | suggested_scenario |",
        "|---|---|---|---|---|---|---|",
    ]
    for route in report.confused_routes:
        lines.append(
            "| "
            f"{route.source} | "
            f"{route.observed_state} | "
            f"{route.predicted_state} | "
            f"{route.matched_rule} | "
            f"{route.final_decision} | "
            f"{route.defense_category}/{route.defense_severity} | "
            f"{route.suggested_scenario} |"
        )

    lines.extend(["", "## Focos sugeridos", ""])
    if report.suggested_focus:
        for item in report.suggested_focus:
            lines.append(f"- {item}")
    else:
        lines.append("- Sin rutas confundidas relevantes.")

    lines.extend(["", "## Lectura responsable", "", report.responsible_limit])
    return "\n".join(lines)
