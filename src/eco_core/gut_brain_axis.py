from __future__ import annotations

from dataclasses import dataclass

from .homeostasis import HomeostasisSnapshot


@dataclass(frozen=True)
class GutBrainReport:
    title: str
    state: str
    summary: str
    attention_required: bool
    key_metrics: dict[str, float | int]
    notes: tuple[str, ...]
    recommended_actions: tuple[str, ...]

    def to_markdown(self) -> str:
        lines = [f"# {self.title}", "", f"**Estado:** `{self.state}`", "", self.summary, "", "## Métricas clave"]
        for key, value in self.key_metrics.items():
            lines.append(f"- `{key}`: {value}")
        lines.extend(["", "## Señales internas"])
        for note in self.notes:
            lines.append(f"- {note}")
        lines.extend(["", "## Acciones sugeridas"])
        for action in self.recommended_actions:
            lines.append(f"- {action}")
        return "\n".join(lines)


def build_gut_brain_report(snapshot: HomeostasisSnapshot) -> GutBrainReport:
    return GutBrainReport(
        title="Reporte eje intestino-cerebro E.C.O.",
        state=snapshot.state,
        summary=_build_summary(snapshot),
        attention_required=snapshot.needs_attention,
        key_metrics={
            "total_packets": snapshot.total_packets,
            "absorption_ratio": snapshot.absorption_ratio,
            "immune_load": snapshot.immune_load,
            "quarantine_ratio": snapshot.quarantine_ratio,
            "recurrence_ratio": snapshot.recurrence_ratio,
            "defense_alerts": snapshot.defense_alerts,
        },
        notes=snapshot.notes,
        recommended_actions=_recommend_actions(snapshot),
    )


def _build_summary(snapshot: HomeostasisSnapshot) -> str:
    summaries = {
        "idle": "El sistema aún no procesa paquetes; no hay actividad entérica que interpretar.",
        "stable": "El flujo informacional está estable: la absorción domina y no aparecen alertas críticas.",
        "watch": "El flujo está en observación: hay actividad, pero la absorción aún no domina claramente.",
        "attention": "El sistema requiere atención: existen señales de defensa o cuarentena sobre el rango esperado.",
        "overload": "El sistema muestra sobrecarga defensiva: conviene revisar entradas, filtros y criterios de rechazo.",
    }
    return summaries.get(snapshot.state, "Estado entérico no reconocido; revisar snapshot de homeostasis.")


def _recommend_actions(snapshot: HomeostasisSnapshot) -> tuple[str, ...]:
    if snapshot.state == "idle":
        return ("Procesar un lote mínimo de paquetes para generar una lectura inicial.",)

    actions: list[str] = []
    if snapshot.immune_load > 0.4:
        actions.append("Revisar calidad de entrada, caracteres inválidos y reglas de defensa informacional.")
    if snapshot.quarantine_ratio > 0.3:
        actions.append("Revisar criterios de longitud mínima y ambigüedad de secuencias.")
    if snapshot.recurrence_ratio > 0:
        actions.append("Revisar duplicados detectados por la microbiota informacional.")
    if snapshot.absorption_ratio >= 0.7 and not actions:
        actions.append("Mantener flujo actual y registrar el estado como referencia estable.")
    if not actions:
        actions.append("Monitorear el próximo lote antes de ajustar reglas del pipeline.")
    return tuple(actions)
