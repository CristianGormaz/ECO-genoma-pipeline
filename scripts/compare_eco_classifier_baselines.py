#!/usr/bin/env python3
"""Compara reportes de clasificadores baseline E.C.O. v1/v2."""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path
from typing import Dict, List

DEFAULT_V1_JSON = Path("results/eco_classifier_baseline_report.json")
DEFAULT_V2_JSON = Path("results/eco_classifier_baseline_v2_report.json")
DEFAULT_MD = Path("results/eco_classifier_comparison_report.md")
DEFAULT_HTML = Path("results/eco_classifier_comparison_report.html")


def e(value: object) -> str:
    return escape(str(value), quote=True)


def load_json(path: Path) -> Dict[str, object]:
    if not path.exists():
        raise FileNotFoundError(f"No existe {path}. Ejecuta make classifier-baseline y make classifier-baseline-v2 primero.")
    return json.loads(path.read_text(encoding="utf-8"))


def metric(report: Dict[str, object], split: str, metric_name: str) -> object:
    evaluation = report[f"{split}_evaluation"]
    if metric_name == "accuracy":
        return evaluation["accuracy"]
    if metric_name == "macro_f1":
        return evaluation["classification_metrics"]["macro_avg"]["f1"]
    if metric_name == "weighted_f1":
        return evaluation["classification_metrics"]["weighted_avg"]["f1"]
    raise ValueError(f"Métrica no soportada: {metric_name}")


def summarize_report(name: str, report: Dict[str, object]) -> Dict[str, object]:
    split = report["data_split"]
    return {
        "name": name,
        "model_type": report["model_type"],
        "feature_mode": report.get("feature_mode", "motif"),
        "kmer_k": report.get("kmer_k") or "no_aplica",
        "train": split["train"],
        "test": split["test"],
        "train_accuracy": metric(report, "train", "accuracy"),
        "test_accuracy": metric(report, "test", "accuracy"),
        "test_macro_f1": metric(report, "test", "macro_f1"),
        "test_weighted_f1": metric(report, "test", "weighted_f1"),
    }


def compare_rows(summaries: List[Dict[str, object]]) -> List[List[object]]:
    return [
        [
            item["name"],
            item["model_type"],
            item["feature_mode"],
            item["kmer_k"],
            item["train"],
            item["test"],
            item["train_accuracy"],
            item["test_accuracy"],
            item["test_macro_f1"],
            item["test_weighted_f1"],
        ]
        for item in summaries
    ]


def markdown_table(headers: List[str], rows: List[List[object]]) -> List[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return lines


def html_table(headers: List[str], rows: List[List[object]]) -> str:
    head = "".join(f"<th>{e(header)}</th>" for header in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{e(value)}</td>" for value in row) + "</tr>"
        for row in rows
    )
    return f"<div class='table-scroll'><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"


def interpretation(v1: Dict[str, object], v2: Dict[str, object]) -> str:
    v1_f1 = float(v1["test_macro_f1"])
    v2_f1 = float(v2["test_macro_f1"])
    if v2_f1 > v1_f1:
        return "El baseline v2 mejora el macro F1 de prueba frente a v1. Conviene revisar si la mejora se mantiene con un dataset más grande."
    if v2_f1 < v1_f1:
        return "El baseline v2 baja el macro F1 de prueba frente a v1. Los k-mers agregan complejidad, pero no mejoran esta muestra."
    return "Ambos baselines obtienen el mismo macro F1 de prueba en esta muestra. La comparación valida el flujo, pero aún no demuestra superioridad del v2."


def limitation_lines(v1: Dict[str, object], v2: Dict[str, object]) -> List[str]:
    v1_f1 = float(v1["test_macro_f1"])
    v2_f1 = float(v2["test_macro_f1"])
    lines = [
        "La muestra actual es demostrativa y todavía pequeña para conclusiones fuertes.",
        "La comparación mide esta muestra específica; no representa desempeño general sobre datasets reales grandes.",
        "La comparación se vuelve más útil al ampliar el dataset y agregar secuencias ambiguas adicionales.",
        "El baseline v2 solo agrega k-mers simples; no reemplaza embeddings ni modelos profundos.",
    ]
    if v1_f1 == v2_f1:
        lines.insert(1, "El empate actual indica rendimiento equivalente en esta muestra, no equivalencia general entre modelos.")
    return lines


def next_step(v1: Dict[str, object], v2: Dict[str, object]) -> str:
    v1_f1 = float(v1["test_macro_f1"])
    v2_f1 = float(v2["test_macro_f1"])
    if v1_f1 == v2_f1:
        return "Diseñar casos donde los motivos aislados confundan al baseline v1 y la composición k-mer pueda aportar una señal diferente."
    return "Ampliar el dataset etiquetado y repetir esta comparación para observar si la diferencia se mantiene."


def build_markdown(v1: Dict[str, object], v2: Dict[str, object]) -> str:
    headers = ["Modelo", "Tipo", "Feature mode", "k", "Train", "Test", "Train acc", "Test acc", "Test macro F1", "Test weighted F1"]
    summaries = [v1, v2]
    lines = [
        "# E.C.O. - Comparación de baselines de clasificación",
        "",
        "## Propósito",
        "",
        "Este informe compara el baseline v1 basado en motivos contra el baseline v2 que agrega frecuencias k-mer. "
        "La comparación es pre-embeddings y sirve como control antes de incorporar modelos más complejos.",
        "",
        "## Resumen comparativo",
        "",
        *markdown_table(headers, compare_rows(summaries)),
        "",
        "## Lectura E.C.O.",
        "",
        interpretation(v1, v2),
        "",
        "## Límites",
        "",
        *[f"- {line}" for line in limitation_lines(v1, v2)],
        "",
        "## Próximo paso recomendado",
        "",
        next_step(v1, v2),
        "",
    ]
    return "\n".join(lines)


def build_html(v1: Dict[str, object], v2: Dict[str, object]) -> str:
    headers = ["Modelo", "Tipo", "Feature mode", "k", "Train", "Test", "Train acc", "Test acc", "Test macro F1", "Test weighted F1"]
    rows = compare_rows([v1, v2])
    limits_html = "".join(f"<li>{e(line)}</li>" for line in limitation_lines(v1, v2))
    return f"""<!doctype html>
<html lang='es'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>E.C.O. Comparación de baselines</title>
  <style>
    body {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; background: #f6f7fb; color: #172033; }}
    header {{ background: #172033; color: white; padding: 2rem; }}
    main {{ max-width: 1100px; margin: 0 auto; padding: 1.5rem; }}
    .section {{ background: white; border-radius: 16px; padding: 1rem; box-shadow: 0 8px 24px rgba(23, 32, 51, 0.08); margin-bottom: 1rem; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; }}
    .metric {{ background: white; border-radius: 16px; padding: 1rem; box-shadow: 0 8px 24px rgba(23, 32, 51, 0.08); }}
    .metric strong {{ display: block; font-size: 1.8rem; }}
    table {{ width: 100%; border-collapse: collapse; background: white; }}
    th, td {{ text-align: left; padding: .7rem; border-bottom: 1px solid #e6e8f0; vertical-align: top; }}
    th {{ background: #eef1f8; }}
    .table-scroll {{ overflow-x: auto; }}
    .warning {{ border-left: 6px solid #9b6b00; }}
  </style>
</head>
<body>
  <header>
    <h1>E.C.O. - Comparación de baselines</h1>
    <p>Baseline v1 basado en motivos versus baseline v2 con motivos + k-mers.</p>
  </header>
  <main>
    <section class='grid'>
      <div class='metric'><strong>{e(v1['test_macro_f1'])}</strong><span>v1 Test macro F1</span></div>
      <div class='metric'><strong>{e(v2['test_macro_f1'])}</strong><span>v2 Test macro F1</span></div>
      <div class='metric'><strong>{e(v1['test_accuracy'])}</strong><span>v1 Test accuracy</span></div>
      <div class='metric'><strong>{e(v2['test_accuracy'])}</strong><span>v2 Test accuracy</span></div>
    </section>
    <section class='section'>
      <h2>Resumen comparativo</h2>
      {html_table(headers, rows)}
    </section>
    <section class='section'>
      <h2>Lectura E.C.O.</h2>
      <p>{e(interpretation(v1, v2))}</p>
    </section>
    <section class='section warning'>
      <h2>Límites</h2>
      <ul>{limits_html}</ul>
    </section>
    <section class='section'>
      <h2>Próximo paso recomendado</h2>
      <p>{e(next_step(v1, v2))}</p>
    </section>
  </main>
</body>
</html>
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compara baselines E.C.O. v1/v2.")
    parser.add_argument("--v1-json", type=Path, default=DEFAULT_V1_JSON)
    parser.add_argument("--v2-json", type=Path, default=DEFAULT_V2_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_MD)
    parser.add_argument("--output-html", type=Path, default=DEFAULT_HTML)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    v1_report = load_json(args.v1_json)
    v2_report = load_json(args.v2_json)
    v1 = summarize_report("baseline_v1", v1_report)
    v2 = summarize_report("baseline_v2", v2_report)

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(build_markdown(v1, v2), encoding="utf-8")
    args.output_html.write_text(build_html(v1, v2), encoding="utf-8")

    print("E.C.O. CLASSIFIER BASELINE COMPARISON")
    print("=====================================")
    print(f"v1: {args.v1_json}")
    print(f"v2: {args.v2_json}")
    print(f"v1 Test macro F1: {v1['test_macro_f1']}")
    print(f"v2 Test macro F1: {v2['test_macro_f1']}")
    print(f"Reporte Markdown: {args.output_md}")
    print(f"Reporte HTML: {args.output_html}")
    print("Estado: OK, comparación baseline v1/v2 generada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
