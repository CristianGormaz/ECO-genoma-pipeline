#!/usr/bin/env python3
"""Exporta el reporte JSON del clasificador baseline E.C.O. a HTML estático."""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path
from typing import Dict, Iterable, List

DEFAULT_INPUT = Path("results/eco_classifier_baseline_report.json")
DEFAULT_OUTPUT = Path("results/eco_classifier_baseline_report.html")


def e(value: object) -> str:
    return escape(str(value), quote=True)


def table(headers: List[str], rows: List[List[object]]) -> str:
    head = "".join(f"<th>{e(header)}</th>" for header in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{e(value)}</td>" for value in row) + "</tr>"
        for row in rows
    )
    return f"<div class='table-scroll'><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"


def metrics_rows(evaluation: Dict[str, object]) -> List[List[object]]:
    metrics = evaluation["classification_metrics"]
    rows: List[List[object]] = []
    for label, values in metrics["per_class"].items():
        rows.append([label, values["precision"], values["recall"], values["f1"], values["support"]])
    macro = metrics["macro_avg"]
    weighted = metrics["weighted_avg"]
    rows.append(["macro_avg", macro["precision"], macro["recall"], macro["f1"], macro["support"]])
    rows.append(["weighted_avg", weighted["precision"], weighted["recall"], weighted["f1"], weighted["support"]])
    return rows


def matrix_rows(evaluation: Dict[str, object]) -> tuple[List[str], List[List[object]]]:
    labels = evaluation["labels"]
    matrix = evaluation["confusion_matrix"]
    rows = [[true_label, *[matrix[true_label][pred_label] for pred_label in labels]] for true_label in labels]
    return ["Real / Predicho", *labels], rows


def prediction_rows(evaluation: Dict[str, object]) -> List[List[object]]:
    return [
        [
            item["sequence_id"],
            item["true_label"],
            item["predicted_label"],
            item["confidence"],
            item["features"]["motif_count"],
            item["features"]["gc_percent"],
            item["features"]["motif_density_per_100bp"],
        ]
        for item in evaluation["predictions"]
    ]


def evaluation_section(title: str, evaluation: Dict[str, object]) -> str:
    headers, rows = matrix_rows(evaluation)
    macro_f1 = evaluation["classification_metrics"]["macro_avg"]["f1"]
    weighted_f1 = evaluation["classification_metrics"]["weighted_avg"]["f1"]
    return f"""
    <section class='section'>
      <h2>{e(title)}</h2>
      <div class='grid'>
        <div class='metric'><strong>{e(evaluation['total'])}</strong><span>Total</span></div>
        <div class='metric'><strong>{e(evaluation['correct'])}</strong><span>Correctas</span></div>
        <div class='metric'><strong>{e(evaluation['accuracy'])}</strong><span>Accuracy</span></div>
        <div class='metric'><strong>{e(macro_f1)}</strong><span>Macro F1</span></div>
        <div class='metric'><strong>{e(weighted_f1)}</strong><span>Weighted F1</span></div>
      </div>
      <h3>Métricas por clase</h3>
      {table(['Clase', 'Precision', 'Recall', 'F1', 'Support'], metrics_rows(evaluation))}
      <h3>Matriz de confusión</h3>
      {table(headers, rows)}
      <h3>Predicciones</h3>
      {table(['ID', 'Real', 'Predicho', 'Confianza', 'Motivos', 'GC %', 'Densidad motivos'], prediction_rows(evaluation))}
    </section>
    """


def build_html(report: Dict[str, object]) -> str:
    split = report["data_split"]
    test_macro_f1 = report["test_evaluation"]["classification_metrics"]["macro_avg"]["f1"]
    limits = report.get("limits", [])
    return f"""<!doctype html>
<html lang='es'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>E.C.O. Clasificador baseline</title>
  <style>
    body {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; background: #f6f7fb; color: #172033; }}
    header {{ background: #172033; color: white; padding: 2rem; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 1.5rem; }}
    .subtitle {{ color: #d8e0ff; max-width: 900px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; }}
    .metric, .section {{ background: white; border-radius: 16px; padding: 1rem; box-shadow: 0 8px 24px rgba(23, 32, 51, 0.08); margin-bottom: 1rem; }}
    .metric strong {{ display: block; font-size: 1.8rem; margin-bottom: .2rem; }}
    table {{ width: 100%; border-collapse: collapse; background: white; }}
    th, td {{ text-align: left; padding: .7rem; border-bottom: 1px solid #e6e8f0; vertical-align: top; }}
    th {{ background: #eef1f8; }}
    .table-scroll {{ overflow-x: auto; }}
    .warning {{ border-left: 6px solid #9b6b00; }}
  </style>
</head>
<body>
  <header>
    <h1>E.C.O. - Clasificador baseline de secuencias</h1>
    <p class='subtitle'>Vista HTML estática del baseline pre-embeddings. Muestra separación train/test, métricas por clase, matriz de confusión y predicciones.</p>
  </header>
  <main>
    <section class='grid'>
      <div class='metric'><strong>{e(split['train'])}</strong><span>Train</span></div>
      <div class='metric'><strong>{e(split['test'])}</strong><span>Test</span></div>
      <div class='metric'><strong>{e(report['test_evaluation']['accuracy'])}</strong><span>Test accuracy</span></div>
      <div class='metric'><strong>{e(test_macro_f1)}</strong><span>Test macro F1</span></div>
      <div class='metric'><strong>{e(report['model_type'])}</strong><span>Modelo</span></div>
    </section>

    {evaluation_section('Evaluación de entrenamiento', report['train_evaluation'])}
    {evaluation_section('Evaluación de prueba', report['test_evaluation'])}

    <section class='section warning'>
      <h2>Límites de uso</h2>
      <ul>{''.join(f'<li>{e(limit)}</li>' for limit in limits)}</ul>
      <p>Este baseline es una referencia demostrativa antes de embeddings/modelos más complejos. No representa desempeño general sobre datasets grandes.</p>
    </section>
  </main>
</body>
</html>
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Exporta el reporte JSON del baseline E.C.O. a HTML estático.")
    parser.add_argument("--input-json", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-html", type=Path, default=DEFAULT_OUTPUT)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.input_json.exists():
        parser.exit(status=1, message=f"Error: no existe {args.input_json}. Ejecuta make classifier-baseline primero.\n")
    report = json.loads(args.input_json.read_text(encoding="utf-8"))
    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.write_text(build_html(report), encoding="utf-8")

    print("E.C.O. CLASSIFIER HTML EXPORT")
    print("=============================")
    print(f"Entrada JSON: {args.input_json}")
    print(f"Salida HTML: {args.output_html}")
    print("Estado: OK, HTML del baseline generado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
