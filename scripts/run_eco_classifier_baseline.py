#!/usr/bin/env python3
"""Ejecuta clasificador baseline de secuencias E.C.O."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from src.eco_sequence_classifier import (  # noqa: E402
    VALID_FEATURE_MODES,
    build_classifier_report,
    parse_labeled_sequences_tsv,
    write_json_report,
)

DEFAULT_INPUT = PROJECT_ROOT / "examples" / "eco_labeled_sequences.tsv"
DEFAULT_JSON = PROJECT_ROOT / "results" / "eco_classifier_baseline_report.json"
DEFAULT_MD = PROJECT_ROOT / "results" / "eco_classifier_baseline_report.md"


def table(headers: List[str], rows: List[List[object]]) -> List[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return lines


def classification_metric_rows(evaluation: Dict[str, object]) -> List[List[object]]:
    metrics = evaluation["classification_metrics"]
    rows: List[List[object]] = []
    for label, values in metrics["per_class"].items():
        rows.append([label, values["precision"], values["recall"], values["f1"], values["support"]])
    macro = metrics["macro_avg"]
    weighted = metrics["weighted_avg"]
    rows.append(["macro_avg", macro["precision"], macro["recall"], macro["f1"], macro["support"]])
    rows.append(["weighted_avg", weighted["precision"], weighted["recall"], weighted["f1"], weighted["support"]])
    return rows


def evaluation_tables(evaluation: Dict[str, object], title: str) -> List[str]:
    predictions = evaluation["predictions"]
    labels = evaluation["labels"]
    matrix = evaluation["confusion_matrix"]
    prediction_rows = [
        [
            item["sequence_id"],
            item["true_label"],
            item["predicted_label"],
            item["confidence"],
            item["features"].get("motif_count", ""),
            item["features"].get("gc_percent", ""),
        ]
        for item in predictions
    ]
    matrix_rows = [[true_label, *[matrix[true_label][pred] for pred in labels]] for true_label in labels]
    return [
        f"## {title}",
        "",
        *table(
            ["Métrica", "Valor"],
            [
                ["Total", evaluation["total"]],
                ["Correctas", evaluation["correct"]],
                ["Accuracy", evaluation["accuracy"]],
            ],
        ),
        "",
        "### Métricas por clase",
        "",
        *table(["Clase", "Precision", "Recall", "F1", "Support"], classification_metric_rows(evaluation)),
        "",
        "### Matriz de confusión",
        "",
        *table(["Real / Predicho", *labels], matrix_rows),
        "",
        "### Predicciones",
        "",
        *table(["ID", "Real", "Predicho", "Confianza", "Motivos", "GC %"], prediction_rows),
        "",
    ]


def build_markdown(report: Dict[str, object], input_path: Path) -> str:
    split = report["data_split"]
    rows = [
        ["Dataset", input_path],
        ["Modelo", report["model_type"]],
        ["Feature mode", report.get("feature_mode", "motif")],
        ["k-mer k", report.get("kmer_k") or "no_aplica"],
        ["Train", split["train"]],
        ["Test", split["test"]],
    ]
    lines = [
        "# E.C.O. - Clasificador baseline de secuencias",
        "",
        "## Propósito",
        "",
        "Este reporte entrena y evalúa un clasificador baseline transparente usando features simples de secuencia. "
        "Su objetivo es crear una línea base medible antes de incorporar embeddings tipo DNABERT u otros modelos más complejos.",
        "",
        "## Entrada",
        "",
        *table(["Campo", "Valor"], rows),
        "",
        *evaluation_tables(report["train_evaluation"], "Métricas de entrenamiento"),
        *evaluation_tables(report["test_evaluation"], "Métricas de prueba"),
        "## Límites",
        "",
        *[f"- {limit}" for limit in report["limits"]],
        "",
        "## Lectura E.C.O.",
        "",
        "Esta etapa convierte la digestión de motivos en una primera decisión algorítmica. "
        "La métrica relevante para mostrar avance es la de prueba, porque evalúa secuencias separadas del entrenamiento. "
        "Las métricas por clase permiten detectar si el baseline favorece una clase y falla en otra.",
        "",
    ]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Entrena/evalúa baseline de clasificación de secuencias E.C.O.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_MD)
    parser.add_argument("--feature-mode", choices=sorted(VALID_FEATURE_MODES), default="motif")
    parser.add_argument("--kmer-k", type=int, default=2)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    records = parse_labeled_sequences_tsv(args.input)
    report = build_classifier_report(records, feature_mode=args.feature_mode, kmer_k=args.kmer_k)
    write_json_report(report, args.output_json)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(build_markdown(report, args.input), encoding="utf-8")

    train = report["train_evaluation"]
    test = report["test_evaluation"]
    split = report["data_split"]
    macro_f1 = test["classification_metrics"]["macro_avg"]["f1"]
    print("E.C.O. CLASSIFIER BASELINE REPORT")
    print("=================================")
    print(f"Dataset: {args.input}")
    print(f"Feature mode: {report['feature_mode']}")
    print(f"k-mer k: {report['kmer_k'] or 'no_aplica'}")
    print(f"Train: {split['train']} | Test: {split['test']}")
    print(f"Train accuracy: {train['accuracy']}")
    print(f"Test accuracy: {test['accuracy']}")
    print(f"Test macro F1: {macro_f1}")
    print(f"Reporte JSON: {args.output_json}")
    print(f"Reporte Markdown: {args.output_md}")
    print("Estado: OK, baseline explicable con métricas por clase ejecutado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
