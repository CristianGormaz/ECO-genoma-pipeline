from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.eco_core import (  # noqa: E402
    EXTENDED_TRANSITION_PACKETS,
    EntericSystem,
    build_adaptive_state_rows,
    train_state_transition_baseline,
)

DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "results" / "sne_eco_external_scenario_probe.json"
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "results" / "sne_eco_external_scenario_probe.md"

EXTERNAL_SCENARIO_PACKETS: tuple[tuple[str, str], ...] = (
    ("external_min_valid_boundary", "ACGTAC"),
    ("external_short_borderline", "ACGTA"),
    ("external_gc_dense_valid", "GGGCGCGCGCTA"),
    ("external_at_dense_valid", "ATATATATATGC"),
    ("external_mixed_n_low", "ACGTNNACGT"),
    ("external_mixed_n_high", "ACGTNNNNNN"),
    ("external_invalid_symbolic", "ACGT@@@"),
    ("external_invalid_numeric", "ACGT2026"),
    ("external_recurrent_gc_dense", "GGGCGCGCGCTA"),
    ("external_recurrent_min_valid", "ACGTAC"),
)

RESPONSIBLE_LIMIT = (
    "Sonda educativa/experimental de escenarios externos; no modifica dataset estable, "
    "baseline, reglas ni umbrales. No representa desempeño general, no modela conciencia humana "
    "y no tiene uso clínico/forense."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ejecuta sonda externa S.N.E.-E.C.O. sin modificar RC1.")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    return parser.parse_args()


def build_external_probe(
    external_packets: Iterable[tuple[str, str]] = EXTERNAL_SCENARIO_PACKETS,
) -> dict[str, Any]:
    """Evalúa escenarios externos contra un baseline entrenado solo con RC1/extendido.

    La función procesa primero `EXTENDED_TRANSITION_PACKETS` para construir el
    contexto homeostático estable y entrenar el baseline. Luego procesa los
    escenarios externos en el mismo sistema para observar transiciones nuevas,
    sin agregarlas al dataset estable ni recalibrar reglas.
    """
    system = EntericSystem(min_length=6, max_n_percent=25.0, heavy_payload_threshold=10_000)
    training_rows = build_adaptive_state_rows(EXTENDED_TRANSITION_PACKETS, system=system)
    model = train_state_transition_baseline(training_rows)

    external_rows = build_adaptive_state_rows(tuple(external_packets), system=system)
    predictions = [model.predict(row) for row in external_rows]

    rows: list[dict[str, Any]] = []
    for row, prediction in zip(external_rows, predictions, strict=True):
        rows.append(
            {
                "source": row.source,
                "state_before": row.state_before,
                "observed_state": row.state_after,
                "predicted_state": prediction.predicted_state,
                "matched_rule": prediction.matched_rule,
                "confidence": prediction.confidence,
                "correct": prediction.correct,
                "final_decision": row.final_decision,
                "defense": f"{row.defense_category}/{row.defense_severity}",
                "recurrence_ratio_before": row.recurrence_ratio_before,
                "recurrence_ratio_after": row.recurrence_ratio_after,
            }
        )

    confused_rows = [item for item in rows if not item["correct"]]
    homeostasis_projection_rows = [item for item in rows if item["matched_rule"] == "homeostasis_projection"]
    default_state_rows = [item for item in rows if item["matched_rule"] == "default_state"]

    status = "green"
    status_reason = "Escenarios externos observados sin confusiones."
    if confused_rows:
        status = "yellow"
        status_reason = "Escenarios externos generaron diferencias observadas; revisar antes de incorporar al dataset estable."
    if default_state_rows:
        status = "red"
        status_reason = "Escenarios externos activaron default_state; revisar cobertura antes de avanzar."

    return {
        "probe_name": "sne_eco_external_scenario_probe",
        "training_rows": len(training_rows),
        "external_rows": len(rows),
        "confused_external_rows": len(confused_rows),
        "homeostasis_projection_rows": len(homeostasis_projection_rows),
        "default_state_rows": len(default_state_rows),
        "status": status,
        "status_reason": status_reason,
        "rows": rows,
        "responsible_limit": RESPONSIBLE_LIMIT,
    }


def to_markdown(payload: dict[str, Any]) -> str:
    status_icon = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(str(payload["status"]), "⚪")
    lines = [
        "# Sonda de escenarios externos S.N.E.-E.C.O.",
        "",
        "Expansión externa en modo observación. No modifica el dataset estable ni recalibra reglas.",
        "",
        f"Estado: {status_icon} `{payload['status']}`",
        f"Motivo: {payload['status_reason']}",
        "",
        "## Métricas",
        "",
        "| Métrica | Valor |",
        "|---|---:|",
        f"| Filas de entrenamiento base | {payload['training_rows']} |",
        f"| Escenarios externos | {payload['external_rows']} |",
        f"| Escenarios externos confundidos | {payload['confused_external_rows']} |",
        f"| Rutas por proyección homeostática | {payload['homeostasis_projection_rows']} |",
        f"| Rutas por default_state | {payload['default_state_rows']} |",
        "",
        "## Escenarios",
        "",
        "| source | observed | predicted | rule | decision | defense | correct |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in payload["rows"]:
        lines.append(
            "| "
            f"{row['source']} | "
            f"{row['observed_state']} | "
            f"{row['predicted_state']} | "
            f"{row['matched_rule']} | "
            f"{row['final_decision']} | "
            f"{row['defense']} | "
            f"{row['correct']} |"
        )

    lines.extend(
        [
            "",
            "## Lectura operativa",
            "",
            "Una confusión externa no invalida RC1. Indica que apareció una ruta nueva que debe revisarse antes de entrenar, corregir o incorporar al dataset estable.",
            "",
            "## Límite responsable",
            "",
            str(payload["responsible_limit"]),
        ]
    )
    return "\n".join(lines)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    payload = build_external_probe()
    markdown = to_markdown(payload)

    write_json(args.output_json, payload)
    write_text(args.output_md, markdown)

    print(markdown)
    print("")
    print("OK: sonda de escenarios externos S.N.E.-E.C.O. generada.")
    print(f"- {args.output_json}")
    print(f"- {args.output_md}")


if __name__ == "__main__":
    main()
