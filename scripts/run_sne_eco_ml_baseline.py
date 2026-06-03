from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

try:
    from scripts._eco_console import configure_windows_safe_console
except ModuleNotFoundError:
    from _eco_console import configure_windows_safe_console


TRAIN_PATH = Path("data/training/sne_eco_empirical_train_split.jsonl")
EVAL_PATH = Path("data/training/sne_eco_empirical_eval_split.jsonl")

OUTPUT_JSON = Path("results/sne_eco_ml_baseline_report.json")
OUTPUT_MD = Path("results/sne_eco_ml_baseline_report.md")

RESPONSIBLE_LIMIT = (
    "Baseline ML educativo/experimental S.N.E.-E.C.O.; "
    "sanity check con datos sintéticos/curados del pipeline; es no clínico, "
    "no diagnóstico, no forense, no modela conciencia humana, "
    "no autoriza entrenamiento, no modifica reglas, baseline estable ni umbrales, "
    "y no representa desempeño real."
)

EMBEDDED_FIXTURE_WARNING = (
    "baseline sanity check con fixture sintético embebido; no entrenamiento autorizado"
)

FEATURE_POLICY = {
    "predictive_features": ["source_text_token_similarity", "input_type_match"],
    "excluded_from_prediction": [
        "expected_decision",
        "expected_state",
        "expected_barrier",
        "expected_motility",
        "defense_category",
    ],
    "audit_only_fields": ["defense_category", "responsible_limit"],
    "note": (
        "defense_category se conserva solo para auditoría de límites responsables; "
        "no participa en el puntaje predictivo."
    ),
}


EMBEDDED_TRAIN_ROWS = [
    {
        "id": "embedded_train_valid_001",
        "input_type": "sequence",
        "source_text": "paquete válido sintético estable para absorción",
        "expected_decision": "absorb",
        "defense_category": "none",
        "responsible_limit": "educational_experimental_not_clinical",
    },
    {
        "id": "embedded_train_valid_002",
        "input_type": "sequence",
        "source_text": "secuencia sintética válida con estructura suficiente",
        "expected_decision": "absorb",
        "defense_category": "none",
        "responsible_limit": "educational_experimental_not_clinical",
    },
    {
        "id": "embedded_train_invalid_001",
        "input_type": "sequence",
        "source_text": "paquete sintético inválido con formato roto",
        "expected_decision": "reject",
        "defense_category": "invalid_payload",
        "responsible_limit": "educational_experimental_not_clinical",
    },
    {
        "id": "embedded_train_invalid_002",
        "input_type": "claim",
        "source_text": "reclamo diagnóstico humano prohibido",
        "expected_decision": "reject",
        "defense_category": "forbidden_diagnostic_claim",
        "responsible_limit": "reject_clinical_diagnostic_claim",
    },
    {
        "id": "embedded_train_quarantine_001",
        "input_type": "sequence",
        "source_text": "paquete ambiguo sintético para revisión",
        "expected_decision": "quarantine",
        "defense_category": "retained_payload",
        "responsible_limit": "educational_experimental_not_clinical",
    },
    {
        "id": "embedded_train_quarantine_002",
        "input_type": "sequence",
        "source_text": "dato breve ambiguo retenido",
        "expected_decision": "quarantine",
        "defense_category": "retained_payload",
        "responsible_limit": "educational_experimental_not_clinical",
    },
    {
        "id": "embedded_train_duplicate_001",
        "input_type": "sequence",
        "source_text": "paquete repetido sintético observado antes",
        "expected_decision": "discard_duplicate",
        "defense_category": "redundant_payload",
        "responsible_limit": "educational_experimental_not_clinical",
    },
    {
        "id": "embedded_train_duplicate_002",
        "input_type": "sequence",
        "source_text": "secuencia redundante sintética ya vista",
        "expected_decision": "discard_duplicate",
        "defense_category": "redundant_payload",
        "responsible_limit": "educational_experimental_not_clinical",
    },
]

EMBEDDED_EVAL_ROWS = [
    {
        "id": "embedded_eval_valid_001",
        "input_type": "sequence",
        "source_text": "paquete válido sintético para absorción",
        "expected_decision": "absorb",
        "defense_category": "none",
        "responsible_limit": "educational_experimental_not_clinical",
    },
    {
        "id": "embedded_eval_invalid_001",
        "input_type": "sequence",
        "source_text": "paquete sintético inválido roto",
        "expected_decision": "reject",
        "defense_category": "invalid_payload",
        "responsible_limit": "educational_experimental_not_clinical",
    },
    {
        "id": "embedded_eval_quarantine_001",
        "input_type": "sequence",
        "source_text": "paquete ambiguo sintético retenido para revisión",
        "expected_decision": "quarantine",
        "defense_category": "retained_payload",
        "responsible_limit": "educational_experimental_not_clinical",
    },
    {
        "id": "embedded_eval_duplicate_001",
        "input_type": "sequence",
        "source_text": "paquete repetido sintético ya observado",
        "expected_decision": "discard_duplicate",
        "defense_category": "redundant_payload",
        "responsible_limit": "educational_experimental_not_clinical",
    },
]

REQUIRED_FIELDS = (
    "id",
    "input_type",
    "source_text",
    "expected_decision",
    "defense_category",
    "responsible_limit",
)


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []

    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-záéíóúñü0-9]+", text.lower()))


def similarity(a: str, b: str) -> float:
    left = tokenize(a)
    right = tokenize(b)

    if not left or not right:
        return 0.0

    return len(left & right) / len(left | right)


def predict_decision(row: dict, train_rows: list[dict]) -> dict:
    scored = []

    for train_row in train_rows:
        score = similarity(row["source_text"], train_row["source_text"])

        if row.get("input_type") == train_row.get("input_type"):
            score += 0.10

        scored.append((score, train_row))

    scored.sort(key=lambda item: item[0], reverse=True)
    best_score, best_row = scored[0]

    return {
        "predicted_decision": best_row["expected_decision"],
        "nearest_train_id": best_row["id"],
        "similarity": round(min(best_score, 1.0), 4),
    }


def validate_rows(rows: list[dict], *, label: str) -> list[str]:
    errors = []
    for index, row in enumerate(rows, start=1):
        missing = [field for field in REQUIRED_FIELDS if field not in row]
        if missing:
            row_id = row.get("id", f"{label}_{index}")
            errors.append(f"{label} fila {row_id} sin campos requeridos: {', '.join(missing)}")
    return errors


def load_splits(train_path: Path, eval_path: Path, *, allow_embedded_fixture: bool) -> tuple[list[dict], list[dict], bool, list[str]]:
    warnings = []
    train_exists = train_path.exists()
    eval_exists = eval_path.exists()

    if train_exists and eval_exists:
        return read_jsonl(train_path), read_jsonl(eval_path), False, warnings

    if allow_embedded_fixture:
        warnings.append(EMBEDDED_FIXTURE_WARNING)
        return list(EMBEDDED_TRAIN_ROWS), list(EMBEDDED_EVAL_ROWS), True, warnings

    return read_jsonl(train_path), read_jsonl(eval_path), False, warnings


def build_report(
    train_path: str | Path | None = None,
    eval_path: str | Path | None = None,
    write_outputs: bool = False,
) -> dict:
    active_train_path = Path(train_path) if train_path is not None else TRAIN_PATH
    active_eval_path = Path(eval_path) if eval_path is not None else EVAL_PATH
    allow_embedded_fixture = train_path is None and eval_path is None

    train_rows, eval_rows, using_embedded_fixture, fixture_warnings = load_splits(
        active_train_path,
        active_eval_path,
        allow_embedded_fixture=allow_embedded_fixture,
    )

    errors = []
    warnings = list(fixture_warnings)

    if not using_embedded_fixture and not active_train_path.exists():
        errors.append(f"No existe train split: {active_train_path}")

    if not using_embedded_fixture and not active_eval_path.exists():
        errors.append(f"No existe eval split: {active_eval_path}")

    if not train_rows:
        errors.append("Train split vacío.")

    if not eval_rows:
        errors.append("Eval split vacío.")

    errors.extend(validate_rows(train_rows, label="train"))
    errors.extend(validate_rows(eval_rows, label="eval"))

    predictions = []

    if train_rows and eval_rows:
        for row in eval_rows:
            pred = predict_decision(row, train_rows)
            expected = row["expected_decision"]
            predicted = pred["predicted_decision"]

            predictions.append(
                {
                    "id": row["id"],
                    "input_type": row["input_type"],
                    "expected_decision": expected,
                    "predicted_decision": predicted,
                    "correct": expected == predicted,
                    "nearest_train_id": pred["nearest_train_id"],
                    "similarity": pred["similarity"],
                    "responsible_limit": row["responsible_limit"],
                }
            )

    correct = sum(1 for row in predictions if row["correct"])
    total = len(predictions)
    accuracy = round(correct / total, 4) if total else 0.0

    expected_counts = Counter(row["expected_decision"] for row in eval_rows)
    predicted_counts = Counter(row["predicted_decision"] for row in predictions)

    forbidden_rows = [
        row["id"]
        for row in eval_rows
        if str(row.get("defense_category", "")).startswith("forbidden")
        or "reject_clinical" in row.get("responsible_limit", "")
        or "reject_forensic" in row.get("responsible_limit", "")
        or "reject_human_consciousness" in row.get("responsible_limit", "")
    ]

    forbidden_not_rejected = [
        row["id"]
        for row in predictions
        if row["id"] in forbidden_rows and row["predicted_decision"] != "reject"
    ]

    if forbidden_not_rejected:
        errors.append(f"Reclamos límite no rechazados por el baseline ML: {forbidden_not_rejected}")

    if accuracy < 0.75 and total:
        warnings.append(
            f"Accuracy inicial baja para baseline experimental: {accuracy}. Requiere más datos o mejores features."
        )

    status = "red" if errors else "attention" if using_embedded_fixture or warnings else "green"

    report = {
        "status": status,
        "train_path": str(active_train_path),
        "eval_path": str(active_eval_path),
        "using_embedded_fixture": using_embedded_fixture,
        "sanity_check_only": True,
        "training_allowed": False,
        "feature_policy": FEATURE_POLICY,
        "train_count": len(train_rows),
        "eval_count": len(eval_rows),
        "correct": correct,
        "total": total,
        "accuracy": accuracy,
        "expected_counts": dict(sorted(expected_counts.items())),
        "predicted_counts": dict(sorted(predicted_counts.items())),
        "forbidden_eval_rows": forbidden_rows,
        "predictions": predictions,
        "errors": errors,
        "warnings": warnings,
        "responsible_limit": RESPONSIBLE_LIMIT,
    }

    if write_outputs:
        OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        OUTPUT_MD.write_text(to_markdown(report), encoding="utf-8")

    return report


def table_counts(counts: dict) -> str:
    if not counts:
        return "- Sin datos."

    lines = ["| Valor | Conteo |", "|---|---:|"]
    for key, value in counts.items():
        lines.append(f"| `{key}` | {value} |")
    return "\n".join(lines)


def table_predictions(predictions: list[dict]) -> str:
    if not predictions:
        return "- Sin predicciones."

    lines = [
        "| ID | Esperado | Predicho | Correcto | Vecino train | Similitud |",
        "|---|---|---|---:|---|---:|",
    ]

    for row in predictions:
        lines.append(
            f"| `{row['id']}` | `{row['expected_decision']}` | "
            f"`{row['predicted_decision']}` | `{row['correct']}` | "
            f"`{row['nearest_train_id']}` | {row['similarity']} |"
        )

    return "\n".join(lines)


def to_markdown(report: dict) -> str:
    icon = {"green": "🟢", "attention": "🟡", "red": "🔴"}.get(report["status"], "⚪")
    feature_policy = report["feature_policy"]

    lines = [
        "# Baseline ML experimental S.N.E.-E.C.O.",
        "",
        f"Estado: {icon} `{report['status']}`",
        f"Sanity check solamente: `{report['sanity_check_only']}`",
        f"Entrenamiento autorizado: `{report['training_allowed']}`",
        f"Fixture embebido usado: `{report['using_embedded_fixture']}`",
        f"Accuracy de sanity check: `{report['accuracy']}`",
        "",
        f"Train: `{report['train_path']}`",
        f"Eval: `{report['eval_path']}`",
        "",
        f"Filas train: `{report['train_count']}`",
        f"Filas eval: `{report['eval_count']}`",
        f"Aciertos: `{report['correct']}` de `{report['total']}`",
        "",
        "## Lectura operativa",
        "",
        "- Este baseline es un sanity check educativo/experimental.",
        "- No mide desempeño real y no debe presentarse como métrica de generalización.",
        "- No autoriza entrenamiento; no usa datos reales.",
        "- Usa similitud textual simple e igualdad de tipo de entrada como señales predictivas.",
        "- `defense_category` se usa solo para auditoría responsable, no para predecir.",
        "- No modifica reglas, baseline estable ni umbrales.",
        "- No tiene uso clínico, diagnóstico, forense ni modela conciencia humana.",
        "",
        "## Política de features",
        "",
        "- Features predictivas: "
        + ", ".join(f"`{item}`" for item in feature_policy["predictive_features"]),
        "- Excluidos de predicción: "
        + ", ".join(f"`{item}`" for item in feature_policy["excluded_from_prediction"]),
        f"- Nota: {feature_policy['note']}",
        "",
        "## Distribución esperada en eval",
        "",
        table_counts(report["expected_counts"]),
        "",
        "## Distribución predicha",
        "",
        table_counts(report["predicted_counts"]),
        "",
        "## Predicciones",
        "",
        table_predictions(report["predictions"]),
        "",
        "## Reclamos límite en eval",
        "",
    ]

    if report["forbidden_eval_rows"]:
        lines.extend(f"- `{row_id}`" for row_id in report["forbidden_eval_rows"])
    else:
        lines.append("- Sin reclamos límite en eval.")

    lines.extend(["", "## Advertencias", ""])

    if report["warnings"]:
        lines.extend(f"- {warning}" for warning in report["warnings"])
    else:
        lines.append("- Sin advertencias.")

    lines.extend(["", "## Errores", ""])

    if report["errors"]:
        lines.extend(f"- {error}" for error in report["errors"])
    else:
        lines.append("- Sin errores.")

    lines.extend(["", "## Límite responsable", "", report["responsible_limit"], ""])

    return "\n".join(lines)


def main() -> None:
    configure_windows_safe_console()
    report = build_report(write_outputs=True)
    print(to_markdown(report))
    print("OK: baseline ML experimental S.N.E.-E.C.O. generado.")
    print(f"- {OUTPUT_JSON}")
    print(f"- {OUTPUT_MD}")


if __name__ == "__main__":
    main()
