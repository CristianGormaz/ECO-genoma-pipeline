#!/usr/bin/env python3
"""Compara reportes de clasificadores baseline E.C.O. v1/v2/v3."""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_V1_JSON = Path("results/eco_classifier_baseline_report.json")
DEFAULT_V2_JSON = Path("results/eco_classifier_baseline_v2_report.json")
DEFAULT_V3_JSON = Path("results/eco_classifier_baseline_v3_report.json")
DEFAULT_MD = Path("results/eco_classifier_comparison_report.md")
DEFAULT_HTML = Path("results/eco_classifier_comparison_report.html")


def e(value: object) -> str:
    return escape(str(value), quote=True)


def load_json(path: Path) -> Dict[str, object]:
    if not path.exists():
        raise FileNotFoundError(f"No existe {path}. Genera el reporte del clasificador antes de comparar.")
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
        "feature_scaling": report.get("feature_scaling", "none"),
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
            item["feature_scaling"],
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


def headers() -> List[str]:
    return [
        "Modelo",
        "Tipo",
        "Feature mode",
        "Scaling",
        "k",
        "Train",
        "Test",
        "Train acc",
        "Test acc",
        "Test macro F1",
        "Test weighted F1",
    ]


def markdown_table(headers_: List[str], rows: List[List[object]]) -> List[str]:
    lines = [
        "| " + " | ".join(headers_) + " |",
        "| " + " | ".join("---" for _ in headers_) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return lines


def html_table(headers_: List[str], rows: List[List[object]]) -> str:
    head = "".join(f"<th>{e(header)}</th>" for header in headers_)
    body = "".join(
        "<tr>" + "".join(f"<td>{e(value)}</td>" for value in row) + "</tr>"
        for row in rows
    )
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def best_summary(summaries: List[Dict[str, object]]) -> Dict[str, object]:
    sorted_items = sorted(summaries, key=lambda item: float(item["test_macro_f1"]), reverse=True)
    return sorted_items[0]


def interpretation(*summaries: Dict[str, object]) -> str:
    items = list(summaries)
    baseline = items[0]
    best = best_summary(items)
    delta = round(float(best["test_macro_f1"]) - float(baseline["test_macro_f1"]), 4)
    if best["name"] == baseline["name"]:
        return "El baseline v1 sigue siendo la mejor referencia en este split fijo. Las configuraciones con k-mers agregan complejidad, pero no mejoran esta muestra."
    if delta > 0:
        return f"{best['name']} obtiene el mejor macro F1 de prueba en este split fijo y mejora a v1 en {delta}. Conviene contrastarlo con sensibilidad y evaluación repetida."
    return "Los baselines quedan cercanos en este split fijo. La comparación valida el flujo, pero no demuestra una mejora estable."


def limitation_lines(*summaries: Dict[str, object]) -> List[str]:
    return [
        "La muestra actual es demostrativa y todavía pequeña para conclusiones fuertes.",
        "La comparación mide este split fijo; no representa desempeño general sobre datasets reales grandes.",
        "La evaluación repetida y la sensibilidad ayudan a detectar estabilidad, pero no reemplazan validación externa.",
        "Los k-mers simples no reemplazan embeddings ni modelos profundos.",
        "La normalización min-max, cuando está activa, se ajusta solo con train para evitar fuga de información desde test.",
    ]


def next_step(*summaries: Dict[str, object]) -> str:
    best = best_summary(list(summaries))
    if best["name"] == "baseline_v3":
        return "Tratar v3 como candidato principal pre-embeddings, actualizar documentación técnica y usar sensibilidad para decidir si k=3 se mantiene como configuración oficial."
    if best["name"] == "baseline_v1":
        return "Mantener v1 como baseline principal y revisar features k-mer antes de promover una versión más compleja."
    return "Ampliar el dataset etiquetado y repetir comparación, sensibilidad y evaluación repetida para observar si la diferencia se mantiene."


def build_markdown(v1: Dict[str, object], v2: Dict[str, object], v3: Optional[Dict[str, object]] = None) -> str:
    summaries = [v1, v2] + ([v3] if v3 else [])
    best = best_summary(summaries)
    delta = round(float(best["test_macro_f1"]) - float(v1["test_macro_f1"]), 4)
    lines = [
        "# E.C.O. - Comparación de baselines de clasificación",
        "",
        "## Propósito",
        "",
        "Este informe compara baselines pre-embeddings basados en motivos, k-mers y normalización opcional.",
        "",
        "## Resumen comparativo",
        "",
        *markdown_table(headers(), compare_rows(summaries)),
        "",
        "## Mejor configuración del split fijo",
        "",
        f"- Mejor modelo: `{best['name']}`",
        f"- Test macro F1: `{best['test_macro_f1']}`",
        f"- Delta vs v1: `{delta}`",
        "",
        "## Lectura E.C.O.",
        "",
        interpretation(*summaries),
        "",
        "## Límites",
        "",
        *[f"- {line}" for line in limitation_lines(*summaries)],
        "",
        "## Próximo paso recomendado",
        "",
        next_step(*summaries),
        "",
    ]
    return "\n".join(lines)


def build_html(v1: Dict[str, object], v2: Dict[str, object], v3: Optional[Dict[str, object]] = None) -> str:
    summaries = [v1, v2] + ([v3] if v3 else [])
    best = best_summary(summaries)
    rows = compare_rows(summaries)
    metrics = "".join(
        f"<div class='metric'><strong>{e(item['test_macro_f1'])}</strong><span>{e(item['name'])} Test macro F1</span></div>"
        for item in summaries
    )
    limits = "".join(f"<li>{e(line)}</li>" for line in limitation_lines(*summaries))
    return f"""<!doctype html>
<html lang='es'>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>E.C.O. Comparación de baselines</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 0; background: #f6f7fb; color: #172033; }}
header {{ background: #172033; color: white; padding: 2rem; }}
main {{ max-width: 1100px; margin: 0 auto; padding: 1.5rem; }}
.section, .metric {{ background: white; border-radius: 16px; padding: 1rem; box-shadow: 0 8px 24px rgba(23,32,51,.08); margin-bottom: 1rem; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; }}
.metric strong {{ display: block; font-size: 1.8rem; }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ text-align: left; padding: .7rem; border-bottom: 1px solid #e6e8f0; vertical-align: top; }}
th {{ background: #eef1f8; }}
.table-scroll {{ overflow-x: auto; }}
.warning {{ border-left: 6px solid #9b6b00; }}
</style>
</head>
<body>
<header><h1>E.C.O. - Comparación de baselines</h1><p>Comparación pre-embeddings entre motivos, k-mers y normalización.</p></header>
<main>
<section class='grid'>{metrics}</section>
<section class='section'><h2>Mejor configuración del split fijo</h2><p><strong>{e(best['name'])}</strong> con Test macro F1 <strong>{e(best['test_macro_f1'])}</strong>.</p></section>
<section class='section'><h2>Resumen comparativo</h2><div class='table-scroll'>{html_table(headers(), rows)}</div></section>
<section class='section'><h2>Lectura E.C.O.</h2><p>{e(interpretation(*summaries))}</p></section>
<section class='section warning'><h2>Límites</h2><ul>{limits}</ul></section>
<section class='section'><h2>Próximo paso recomendado</h2><p>{e(next_step(*summaries))}</p></section>
</main>
</body>
</html>
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compara baselines E.C.O. v1/v2/v3.")
    parser.add_argument("--v1-json", type=Path, default=DEFAULT_V1_JSON)
    parser.add_argument("--v2-json", type=Path, default=DEFAULT_V2_JSON)
    parser.add_argument("--v3-json", type=Path, default=DEFAULT_V3_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_MD)
    parser.add_argument("--output-html", type=Path, default=DEFAULT_HTML)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    v1 = summarize_report("baseline_v1", load_json(args.v1_json))
    v2 = summarize_report("baseline_v2", load_json(args.v2_json))
    v3 = summarize_report("baseline_v3", load_json(args.v3_json)) if args.v3_json.exists() else None
    summaries = [v1, v2] + ([v3] if v3 else [])
    best = best_summary(summaries)

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(build_markdown(v1, v2, v3), encoding="utf-8")
    args.output_html.write_text(build_html(v1, v2, v3), encoding="utf-8")

    print("E.C.O. CLASSIFIER BASELINE COMPARISON")
    print("=====================================")
    for item in summaries:
        print(f"{item['name']} Test macro F1: {item['test_macro_f1']}")
    print(f"Mejor configuración: {best['name']}")
    print(f"Reporte Markdown: {args.output_md}")
    print(f"Reporte HTML: {args.output_html}")
    print("Estado: OK, comparación baseline v1/v2/v3 generada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
