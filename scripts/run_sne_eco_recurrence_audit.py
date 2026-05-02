from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.eco_core import (
    EXTENDED_TRANSITION_PACKETS,
    analyze_confused_routes,
    build_adaptive_state_rows,
)


OUTPUT_JSON = PROJECT_ROOT / "results" / "sne_eco_recurrence_audit.json"
OUTPUT_MD = PROJECT_ROOT / "results" / "sne_eco_recurrence_audit.md"


def row_payload(row: Any, confused_by_source: dict[str, Any]) -> dict[str, Any]:
    confused = confused_by_source.get(row.source)

    return {
        "source": row.source,
        "state_before": row.state_before,
        "state_after": row.state_after,
        "final_decision": row.final_decision,
        "defense_category": row.defense_category,
        "defense_severity": row.defense_severity,
        "microbiota_seen_count": row.microbiota_seen_count,
        "recurrence_ratio_before": row.recurrence_ratio_before,
        "recurrence_ratio_after": row.recurrence_ratio_after,
        "is_confused": confused is not None,
        "predicted_state": confused.predicted_state if confused else None,
        "matched_rule": confused.matched_rule if confused else None,
        "suggested_scenario": confused.suggested_scenario if confused else None,
    }


def to_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Auditoría de recurrencia S.N.E.-E.C.O.",
        "",
        "Diagnóstico específico de rutas recurrentes, duplicadas o redundantes.",
        "",
        f"Filas totales: {payload['total_rows']}",
        f"Filas de recurrencia evaluadas: {payload['recurrence_rows']}",
        f"Rutas confundidas de recurrencia: {payload['confused_recurrence_rows']}",
        "",
        "## Rutas de recurrencia",
        "",
        "| source | before | after | decision | defense | seen | rec_before | rec_after | confused | predicted | rule | suggested |",
        "|---|---|---|---|---|---:|---:|---:|---|---|---|---|",
    ]

    for row in payload["rows"]:
        lines.append(
            "| "
            f"{row['source']} | "
            f"{row['state_before']} | "
            f"{row['state_after']} | "
            f"{row['final_decision']} | "
            f"{row['defense_category']}/{row['defense_severity']} | "
            f"{row['microbiota_seen_count']} | "
            f"{row['recurrence_ratio_before']} | "
            f"{row['recurrence_ratio_after']} | "
            f"{row['is_confused']} | "
            f"{row['predicted_state']} | "
            f"{row['matched_rule']} | "
            f"{row['suggested_scenario']} |"
        )

    lines.extend(
        [
            "",
            "## Lectura accionable",
            "",
            "- Si una ruta recurrente aparece como confundida, revisar si falta evidencia de repetición o si la homeostasis está interpretando la recurrencia como tensión.",
            "- No conviene forzar accuracy 0-error sin antes distinguir entre error real y ambigüedad aceptable.",
            "- Este reporte no modifica el baseline; solo observa el comportamiento recurrente.",
            "",
            "## Límite responsable",
            "",
            payload["responsible_limit"],
        ]
    )

    return "\n".join(lines)


def main() -> None:
    rows = build_adaptive_state_rows(EXTENDED_TRANSITION_PACKETS)
    confusion = analyze_confused_routes(rows)
    confused_by_source = {route.source: route for route in confusion.confused_routes}

    recurrence_rows = [
        row
        for row in rows
        if row.final_decision == "discard_duplicate"
        or row.defense_category == "redundant_payload"
        or "duplicate" in row.source
        or "recurrent" in row.source
    ]

    payload = {
        "total_rows": len(rows),
        "recurrence_rows": len(recurrence_rows),
        "confused_recurrence_rows": sum(1 for row in recurrence_rows if row.source in confused_by_source),
        "suggested_focus": list(confusion.suggested_focus),
        "rows": [row_payload(row, confused_by_source) for row in recurrence_rows],
        "responsible_limit": (
            "Auditoría educativa/experimental; no representa desempeño general, "
            "no modela conciencia humana y no tiene uso clínico/forense."
        ),
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(to_markdown(payload) + "\n", encoding="utf-8")

    print("OK: auditoría de recurrencia S.N.E.-E.C.O. generada.")
    print(f"- {OUTPUT_JSON}")
    print(f"- {OUTPUT_MD}")


if __name__ == "__main__":
    main()
