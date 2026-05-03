from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from scripts.run_sne_eco_ml_baseline import read_jsonl, predict_decision


TRAIN_PATH = Path("data/training/sne_eco_empirical_train_split.jsonl")
CHALLENGE_PATH = Path("data/training/sne_eco_empirical_challenge_eval.jsonl")

OUTPUT_JSON = Path("results/sne_eco_ml_challenge_eval_report.json")
OUTPUT_MD = Path("results/sne_eco_ml_challenge_eval_report.md")

RESPONSIBLE_LIMIT = (
    "Evaluación de desafío ML educativa/experimental S.N.E.-E.C.O.; "
    "no entrena modelos, no modifica reglas, no recalibra umbrales, "
    "no tiene uso clínico, diagnóstico ni forense, y no modela conciencia humana."
)


def build_report(write_outputs: bool = False) -> dict:
    train_rows = read_jsonl(TRAIN_PATH)
    challenge_rows = read_jsonl(CHALLENGE_PATH)

    errors = []
    warnings = []

    if not TRAIN_PATH.exists():
        errors.append(f"No existe train split: {TRAIN_PATH}")

    if not CHALLENGE_PATH.exists():
        errors.append(f"No existe challenge eval: {CHALLENGE_PATH}")

    if not train_rows:
        errors.append("Train split vacío.")

    if not challenge_rows:
        errors.append("Challenge eval vacío.")

    predictions = []

    if train_rows and challenge_rows:
        for row in challenge_rows:
            pred = predict_decision(row, train_rows)
            expected = row["expected_decision"]
            predicted = pred["predicted_decision"]

            predictions.append(
                {
                    "id": row["id"],
                    "input_type": row["input_type"],
                    "defense_category": row["defense_category"],
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

    forbidden_rows = [
        row["id"]
        for row in challenge_rows
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
        errors.append(f"Reclamos límite no rechazados: {forbidden_not_rejected}")

    if accuracy < 0.75 and total:
        warnings.append(
            f"Accuracy baja en challenge eval: {accuracy}. Requiere ampliar datos o mejorar features."
        )

    status = "red" if errors else "attention" if warnings else "green"

    report = {
        "status": status,
        "train_path": str(TRAIN_PATH),
        "challenge_path": str(CHALLENGE_PATH),
        "train_count": len(train_rows),
        "challenge_count": len(challenge_rows),
        "correct": correct,
        "total": total,
        "accuracy": accuracy,
        "expected_counts": dict(sorted(Counter(row["expected_decision"] for row in challenge_rows).items())),
        "predicted_counts": dict(sorted(Counter(row["predicted_decision"] for row in predictions).items())),
        "forbidden_rows": forbidden_rows,
        "forbidden_not_rejected": forbidden_not_rejected,
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
        "| ID | Defensa | Esperado | Predicho | Correcto | Vecino train | Similitud |",
        "|---|---|---|---|---:|---|---:|",
    ]

    for row in predictions:
        lines.append(
            f"| `{row['id']}` | `{row['defense_category']}` | "
            f"`{row['expected_decision']}` | `{row['predicted_decision']}` | "
            f"`{row['correct']}` | `{row['nearest_train_id']}` | {row['similarity']} |"
        )

    return "\n".join(lines)


def to_markdown(report: dict) -> str:
    icon = {"green": "🟢", "attention": "🟡", "red": "🔴"}.get(report["status"], "⚪")

    lines = [
        "# Evaluación de desafío ML S.N.E.-E.C.O.",
        "",
        f"Estado: {icon} `{report['status']}`",
        f"Accuracy challenge: `{report['accuracy']}`",
        "",
        f"Train: `{report['train_path']}`",
        f"Challenge eval: `{report['challenge_path']}`",
        "",
        f"Filas train: `{report['train_count']}`",
        f"Filas challenge: `{report['challenge_count']}`",
        f"Aciertos: `{report['correct']}` de `{report['total']}`",
        "",
        "## Lectura operativa",
        "",
        "- Este reporte prueba el baseline ML contra ejemplos nuevos de desafío.",
        "- No entrena modelos ni modifica reglas.",
        "- Verifica especialmente que reclamos clínicos, diagnósticos, forenses o de conciencia humana sean rechazados.",
        "",
        "## Distribución esperada",
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
        "## Reclamos límite",
        "",
    ]

    if report["forbidden_rows"]:
        lines.extend(f"- `{row_id}`" for row_id in report["forbidden_rows"])
    else:
        lines.append("- Sin reclamos límite.")

    lines.extend(["", "## Reclamos límite no rechazados", ""])

    if report["forbidden_not_rejected"]:
        lines.extend(f"- `{row_id}`" for row_id in report["forbidden_not_rejected"])
    else:
        lines.append("- Ninguno.")

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
    report = build_report(write_outputs=True)
    print(to_markdown(report))
    print("OK: evaluación de desafío ML S.N.E.-E.C.O. generada.")
    print(f"- {OUTPUT_JSON}")
    print(f"- {OUTPUT_MD}")


if __name__ == "__main__":
    main()
