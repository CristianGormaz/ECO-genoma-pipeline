from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


TRAIN_PATH = Path("data/training/sne_eco_empirical_train_split.jsonl")
EVAL_PATH = Path("data/training/sne_eco_empirical_eval_split.jsonl")

OUTPUT_JSON = Path("results/sne_eco_ml_baseline_report.json")
OUTPUT_MD = Path("results/sne_eco_ml_baseline_report.md")

RESPONSIBLE_LIMIT = (
    "Baseline ML educativo/experimental S.N.E.-E.C.O.; "
    "usa datos sintéticos/curados del pipeline; es no clínico, "
    "no diagnóstico, no forense, no modela conciencia humana, "
    "no modifica reglas, baseline estable ni umbrales."
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

        if row.get("defense_category") == train_row.get("defense_category"):
            score += 0.20

        scored.append((score, train_row))

    scored.sort(key=lambda item: item[0], reverse=True)
    best_score, best_row = scored[0]

    return {
        "predicted_decision": best_row["expected_decision"],
        "nearest_train_id": best_row["id"],
        "similarity": round(min(best_score, 1.0), 4),
    }


def build_report(write_outputs: bool = False) -> dict:
    train_rows = read_jsonl(TRAIN_PATH)
    eval_rows = read_jsonl(EVAL_PATH)

    errors = []
    warnings = []

    if not TRAIN_PATH.exists():
        errors.append(f"No existe train split: {TRAIN_PATH}")

    if not EVAL_PATH.exists():
        errors.append(f"No existe eval split: {EVAL_PATH}")

    if not train_rows:
        errors.append("Train split vacío.")

    if not eval_rows:
        errors.append("Eval split vacío.")

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

    status = "red" if errors else "attention" if warnings else "green"

    report = {
        "status": status,
        "train_path": str(TRAIN_PATH),
        "eval_path": str(EVAL_PATH),
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

    lines = [
        "# Baseline ML experimental S.N.E.-E.C.O.",
        "",
        f"Estado: {icon} `{report['status']}`",
        f"Accuracy: `{report['accuracy']}`",
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
        "- Este baseline usa similitud textual simple entre ejemplos train/eval.",
        "- Sirve como punto de partida medible, no como modelo final.",
        "- No modifica reglas, baseline estable ni umbrales.",
        "- No tiene uso clínico, diagnóstico, forense ni modela conciencia humana.",
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
    report = build_report(write_outputs=True)
    print(to_markdown(report))
    print("OK: baseline ML experimental S.N.E.-E.C.O. generado.")
    print(f"- {OUTPUT_JSON}")
    print(f"- {OUTPUT_MD}")


if __name__ == "__main__":
    main()
