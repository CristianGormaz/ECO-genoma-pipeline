from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


DATASET_PATH = Path("data/training/sne_eco_empirical_seed_dataset.jsonl")
OUTPUT_JSON = Path("results/sne_eco_training_readiness_report.json")
OUTPUT_MD = Path("results/sne_eco_training_readiness_report.md")

MIN_ROWS_FOR_TRAINING = 24

REQUIRED_FIELDS = {
    "id",
    "input_type",
    "source_text",
    "expected_barrier",
    "expected_motility",
    "expected_decision",
    "expected_state",
    "defense_category",
    "responsible_limit",
}

EXPECTED_DECISIONS = {
    "absorb",
    "reject",
    "quarantine",
    "discard_duplicate",
}

FORBIDDEN_DEFENSES = {
    "forbidden_clinical_claim",
    "forbidden_diagnostic_claim",
    "forbidden_forensic_claim",
    "forbidden_consciousness_claim",
}

RESPONSIBLE_LIMIT = (
    "Reporte educativo/experimental de preparación de entrenamiento S.N.E.-E.C.O.; "
    "no entrena modelos, no ejecuta reglas nuevas, no recalibra umbrales, "
    "no tiene uso clínico, diagnóstico ni forense, y no modela conciencia humana."
)


def load_rows() -> tuple[list[dict], list[str]]:
    errors: list[str] = []

    if not DATASET_PATH.exists():
        return [], [f"Dataset no encontrado: {DATASET_PATH}"]

    rows: list[dict] = []
    for index, line in enumerate(DATASET_PATH.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            errors.append(f"Fila {index}: JSON inválido: {exc}")

    return rows, errors


def build_report() -> dict:
    rows, errors = load_rows()
    warnings: list[str] = []

    missing_required_fields: list[str] = []
    forbidden_claim_rows: list[str] = []
    unsafe_forbidden_rows: list[str] = []

    for row in rows:
        row_id = row.get("id", "unknown_id")
        missing = sorted(REQUIRED_FIELDS - set(row.keys()))
        if missing:
            missing_required_fields.append(f"{row_id}: faltan campos {missing}")

        defense = row.get("defense_category")
        decision = row.get("expected_decision")
        state = row.get("expected_state")

        if defense in FORBIDDEN_DEFENSES:
            forbidden_claim_rows.append(row_id)
            if decision != "reject" or state != "attention":
                unsafe_forbidden_rows.append(row_id)

        if not row.get("responsible_limit"):
            errors.append(f"{row_id}: falta responsible_limit")

    errors.extend(missing_required_fields)

    if unsafe_forbidden_rows:
        errors.append(
            "Hay reclamos prohibidos que no fueron rechazados correctamente: "
            + ", ".join(unsafe_forbidden_rows)
        )

    decision_counts = Counter(row.get("expected_decision", "missing") for row in rows)
    input_type_counts = Counter(row.get("input_type", "missing") for row in rows)
    state_counts = Counter(row.get("expected_state", "missing") for row in rows)
    defense_counts = Counter(row.get("defense_category", "missing") for row in rows)

    missing_decisions = sorted(EXPECTED_DECISIONS - set(decision_counts.keys()))
    if missing_decisions:
        warnings.append(f"Faltan decisiones esperadas para cobertura mínima: {missing_decisions}")

    if len(rows) < MIN_ROWS_FOR_TRAINING:
        warnings.append(
            f"Dataset semilla válido, pero aún pequeño para entrenamiento: "
            f"{len(rows)} filas de mínimo recomendado {MIN_ROWS_FOR_TRAINING}."
        )

    if errors:
        status = "red"
    elif len(rows) < MIN_ROWS_FOR_TRAINING:
        status = "attention"
    else:
        status = "green"

    training_allowed = status == "green"

    return {
        "status": status,
        "training_allowed": training_allowed,
        "dataset": str(DATASET_PATH),
        "row_count": len(rows),
        "minimum_rows_for_training": MIN_ROWS_FOR_TRAINING,
        "counts": {
            "input_type": dict(sorted(input_type_counts.items())),
            "expected_decision": dict(sorted(decision_counts.items())),
            "expected_state": dict(sorted(state_counts.items())),
            "defense_category": dict(sorted(defense_counts.items())),
        },
        "missing_decisions": missing_decisions,
        "forbidden_claim_rows": forbidden_claim_rows,
        "errors": errors,
        "warnings": warnings,
        "responsible_limit": RESPONSIBLE_LIMIT,
    }


def table_from_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "- Sin datos.\n"

    lines = [
        "| Valor | Conteo |",
        "|---|---:|",
    ]

    for key, value in counts.items():
        lines.append(f"| `{key}` | {value} |")

    return "\n".join(lines) + "\n"


def to_markdown(report: dict) -> str:
    emoji = {
        "green": "🟢",
        "attention": "🟡",
        "red": "🔴",
    }.get(report["status"], "⚪")

    errors = report["errors"] or ["Sin errores."]
    warnings = report["warnings"] or ["Sin advertencias."]
    forbidden_rows = report["forbidden_claim_rows"] or ["Sin reclamos límite detectados."]

    return "\n".join(
        [
            "# Preparación de entrenamiento S.N.E.-E.C.O.",
            "",
            f"Estado: {emoji} `{report['status']}`",
            f"Entrenamiento permitido: `{report['training_allowed']}`",
            "",
            f"Dataset: `{report['dataset']}`",
            f"Filas evaluadas: `{report['row_count']}`",
            f"Mínimo recomendado para entrenamiento: `{report['minimum_rows_for_training']}`",
            "",
            "## Lectura operativa",
            "",
            "- Este reporte decide si el dataset empírico está listo para iniciar entrenamiento experimental.",
            "- Si el estado es `attention`, el dataset puede ser válido pero todavía insuficiente.",
            "- Si el estado es `red`, hay errores de estructura, seguridad o coherencia.",
            "",
            "## Distribución por tipo de entrada",
            "",
            table_from_counts(report["counts"]["input_type"]),
            "## Distribución por decisión esperada",
            "",
            table_from_counts(report["counts"]["expected_decision"]),
            "## Distribución por estado esperado",
            "",
            table_from_counts(report["counts"]["expected_state"]),
            "## Distribución por defensa",
            "",
            table_from_counts(report["counts"]["defense_category"]),
            "## Reclamos límite detectados",
            "",
            "\n".join(f"- `{item}`" for item in forbidden_rows),
            "",
            "## Advertencias",
            "",
            "\n".join(f"- {item}" for item in warnings),
            "",
            "## Errores",
            "",
            "\n".join(f"- {item}" for item in errors),
            "",
            "## Límite responsable",
            "",
            report["responsible_limit"],
            "",
        ]
    )


def main() -> None:
    report = build_report()

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    OUTPUT_MD.write_text(to_markdown(report), encoding="utf-8")

    print(to_markdown(report))
    print("OK: reporte de preparación de entrenamiento S.N.E.-E.C.O. generado.")
    print(f"- {OUTPUT_JSON}")
    print(f"- {OUTPUT_MD}")


if __name__ == "__main__":
    main()
