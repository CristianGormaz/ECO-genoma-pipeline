from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


DATASET_PATH = Path("data/training/sne_eco_empirical_seed_dataset.jsonl")
TRAIN_PATH = Path("data/training/sne_eco_empirical_train_split.jsonl")
EVAL_PATH = Path("data/training/sne_eco_empirical_eval_split.jsonl")
OUTPUT_JSON = Path("results/sne_eco_empirical_train_eval_split_report.json")
OUTPUT_MD = Path("results/sne_eco_empirical_train_eval_split_report.md")

MIN_ROWS_FOR_SPLIT = 24
EVAL_RATIO = 0.25

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

RESPONSIBLE_LIMIT = (
    "Separación educativa/experimental de dataset S.N.E.-E.C.O.; "
    "no entrena modelos, no ejecuta reglas nuevas, no recalibra umbrales, "
    "no tiene uso clínico, diagnóstico ni forense, y no modela conciencia humana."
)


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []

    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows) + "\n",
        encoding="utf-8",
    )


def count_by(rows: list[dict], field: str) -> dict:
    return dict(sorted(Counter(row.get(field, "<missing>") for row in rows).items()))


def split_rows(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)

    for row in sorted(rows, key=lambda item: item["id"]):
        grouped[row["expected_decision"]].append(row)

    train_rows: list[dict] = []
    eval_rows: list[dict] = []

    for label in sorted(grouped):
        items = grouped[label]

        if len(items) == 1:
            train_rows.extend(items)
            continue

        eval_count = max(1, round(len(items) * EVAL_RATIO))
        eval_count = min(eval_count, len(items) - 1)

        train_rows.extend(items[:-eval_count])
        eval_rows.extend(items[-eval_count:])

    return (
        sorted(train_rows, key=lambda item: item["id"]),
        sorted(eval_rows, key=lambda item: item["id"]),
    )


def build_report(write_outputs: bool = False) -> dict:
    rows = read_jsonl(DATASET_PATH)

    errors: list[str] = []
    warnings: list[str] = []

    if not DATASET_PATH.exists():
        errors.append(f"Dataset no encontrado: {DATASET_PATH}")

    ids = [row.get("id") for row in rows]
    duplicate_ids = sorted([item for item, count in Counter(ids).items() if count > 1])

    if duplicate_ids:
        errors.append(f"IDs duplicados detectados: {duplicate_ids}")

    missing_fields_by_row = {}
    for row in rows:
        missing = sorted(REQUIRED_FIELDS - set(row.keys()))
        if missing:
            missing_fields_by_row[row.get("id", "<sin_id>")] = missing

    if missing_fields_by_row:
        errors.append(f"Filas con campos faltantes: {missing_fields_by_row}")

    forbidden_claim_rows = [
        row["id"]
        for row in rows
        if str(row.get("defense_category", "")).startswith("forbidden")
        or "reject_clinical" in row.get("responsible_limit", "")
        or "reject_forensic" in row.get("responsible_limit", "")
        or "reject_human_consciousness" in row.get("responsible_limit", "")
    ]

    forbidden_not_rejected = [
        row["id"]
        for row in rows
        if row["id"] in forbidden_claim_rows and row.get("expected_decision") != "reject"
    ]

    if forbidden_not_rejected:
        errors.append(f"Reclamos límite sin decisión reject: {forbidden_not_rejected}")

    train_rows, eval_rows = split_rows(rows)

    train_ids = {row["id"] for row in train_rows}
    eval_ids = {row["id"] for row in eval_rows}
    id_overlap = sorted(train_ids & eval_ids)

    train_texts = {row["source_text"] for row in train_rows}
    eval_texts = {row["source_text"] for row in eval_rows}
    source_text_overlap = sorted(train_texts & eval_texts)

    if id_overlap:
        errors.append(f"Fuga de datos por ID entre train/eval: {id_overlap}")

    if source_text_overlap:
        errors.append(f"Fuga de datos por source_text entre train/eval: {source_text_overlap}")

    all_labels = set(row.get("expected_decision") for row in rows)
    train_labels = set(row.get("expected_decision") for row in train_rows)
    eval_labels = set(row.get("expected_decision") for row in eval_rows)

    missing_train_labels = sorted(all_labels - train_labels)
    missing_eval_labels = sorted(all_labels - eval_labels)

    if missing_train_labels:
        warnings.append(f"Etiquetas ausentes en train: {missing_train_labels}")

    if missing_eval_labels:
        warnings.append(f"Etiquetas ausentes en eval: {missing_eval_labels}")

    if len(rows) < MIN_ROWS_FOR_SPLIT:
        warnings.append(
            f"Dataset pequeño para separación entrenable: {len(rows)} filas de mínimo recomendado {MIN_ROWS_FOR_SPLIT}."
        )

    if errors:
        status = "red"
    elif warnings:
        status = "attention"
    else:
        status = "green"

    training_split_ready = status == "green"

    report = {
        "status": status,
        "training_split_ready": training_split_ready,
        "dataset": str(DATASET_PATH),
        "train_output": str(TRAIN_PATH),
        "eval_output": str(EVAL_PATH),
        "row_count": len(rows),
        "train_count": len(train_rows),
        "eval_count": len(eval_rows),
        "minimum_rows_for_split": MIN_ROWS_FOR_SPLIT,
        "eval_ratio": EVAL_RATIO,
        "counts": {
            "all_expected_decision": count_by(rows, "expected_decision"),
            "train_expected_decision": count_by(train_rows, "expected_decision"),
            "eval_expected_decision": count_by(eval_rows, "expected_decision"),
            "all_defense_category": count_by(rows, "defense_category"),
        },
        "duplicate_ids": duplicate_ids,
        "id_overlap": id_overlap,
        "source_text_overlap_count": len(source_text_overlap),
        "missing_train_labels": missing_train_labels,
        "missing_eval_labels": missing_eval_labels,
        "forbidden_claim_rows": forbidden_claim_rows,
        "errors": errors,
        "warnings": warnings,
        "responsible_limit": RESPONSIBLE_LIMIT,
    }

    if write_outputs:
        write_jsonl(TRAIN_PATH, train_rows)
        write_jsonl(EVAL_PATH, eval_rows)
        OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        OUTPUT_MD.write_text(to_markdown(report), encoding="utf-8")

    return report


def table_from_counts(counts: dict) -> str:
    if not counts:
        return "- Sin datos."

    lines = ["| Valor | Conteo |", "|---|---:|"]
    for key, value in counts.items():
        lines.append(f"| `{key}` | {value} |")
    return "\n".join(lines)


def to_markdown(report: dict) -> str:
    icon = {"green": "🟢", "attention": "🟡", "red": "🔴"}.get(report["status"], "⚪")

    lines = [
        "# Separación train/eval empírica S.N.E.-E.C.O.",
        "",
        f"Estado: {icon} `{report['status']}`",
        f"Split listo para entrenamiento experimental: `{report['training_split_ready']}`",
        "",
        f"Dataset: `{report['dataset']}`",
        f"Train: `{report['train_output']}`",
        f"Eval: `{report['eval_output']}`",
        "",
        f"Filas totales: `{report['row_count']}`",
        f"Filas train: `{report['train_count']}`",
        f"Filas eval: `{report['eval_count']}`",
        f"Mínimo recomendado: `{report['minimum_rows_for_split']}`",
        "",
        "## Lectura operativa",
        "",
        "- Este reporte separa datos semilla en entrenamiento y evaluación.",
        "- No entrena modelos todavía.",
        "- Su objetivo es evitar fuga de datos antes de crear un baseline ML.",
        "- Mantiene límites responsables: no clínico, no diagnóstico, no forense, no conciencia humana.",
        "",
        "## Distribución total por decisión esperada",
        "",
        table_from_counts(report["counts"]["all_expected_decision"]),
        "",
        "## Distribución train por decisión esperada",
        "",
        table_from_counts(report["counts"]["train_expected_decision"]),
        "",
        "## Distribución eval por decisión esperada",
        "",
        table_from_counts(report["counts"]["eval_expected_decision"]),
        "",
        "## Reclamos límite detectados",
        "",
    ]

    if report["forbidden_claim_rows"]:
        lines.extend(f"- `{row_id}`" for row_id in report["forbidden_claim_rows"])
    else:
        lines.append("- Sin reclamos límite detectados.")

    lines.extend(
        [
            "",
            "## Fuga de datos",
            "",
            f"- IDs compartidos train/eval: `{len(report['id_overlap'])}`",
            f"- Textos compartidos train/eval: `{report['source_text_overlap_count']}`",
            "",
            "## Advertencias",
            "",
        ]
    )

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
    print("OK: separación train/eval empírica S.N.E.-E.C.O. generada.")
    print(f"- {OUTPUT_JSON}")
    print(f"- {OUTPUT_MD}")
    print(f"- {TRAIN_PATH}")
    print(f"- {EVAL_PATH}")


if __name__ == "__main__":
    main()
