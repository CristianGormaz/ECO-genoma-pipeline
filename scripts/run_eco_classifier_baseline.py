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


def build_markdown(report: Dict[str, object], input_path: Path) -> str:
    evaluation = report["evaluation"]
    predictions = evaluation["predictions"]
    labels = evaluation["labels"]
    matrix = evaluation["confusion_matrix"]

    prediction_rows = [
        [
            item["sequence_id"],
            item["true_label"],
            item["predicted_label"],
            item["confidence"],
            item["features"]["motif_count"],
            item["features"]["gc_percent"],
        ]
        for item in predictions
    ]
    matrix_rows = [[true_label, *[matrix[true_label][pred] for pred in labels]] for true_label in labels]

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
        *table(["Campo", "Valor"], [["Dataset", input_path], ["Modelo", report["model_type"]]]),
        "",
        "## Métricas",
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
        "## Matriz de confusión",
        "",
        *table(["Real / Predicho", *labels], matrix_rows),
        "",
        "## Predicciones",
        "",
        *table(["ID", "Real", "Predicho", "Confianza", "Motivos", "GC %"], prediction_rows),
        "",
        "## Límites",
        "",
        *[f"- {limit}" for limit in report["limits"]],
        "",
        "## Lectura E.C.O.",
        "",
        "Esta etapa convierte la digestión de motivos en una primera decisión algorítmica. "
        "No pretende ser un modelo final; funciona como control base para medir mejoras futuras.",
        "",
    ]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Entrena/evalúa baseline de clasificación de secuencias E.C.O.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_MD)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    records = parse_labeled_sequences_tsv(args.input)
    report = build_classifier_report(records)
    write_json_report(report, args.output_json)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(build_markdown(report, args.input), encoding="utf-8")

    evaluation = report["evaluation"]
    print("E.C.O. CLASSIFIER BASELINE REPORT")
    print("=================================")
    print(f"Dataset: {args.input}")
    print(f"Total: {evaluation['total']}")
    print(f"Correctas: {evaluation['correct']}")
    print(f"Accuracy: {evaluation['accuracy']}")
    print(f"Reporte JSON: {args.output_json}")
    print(f"Reporte Markdown: {args.output_md}")
    print("Estado: OK, baseline explicable ejecutado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
