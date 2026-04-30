#!/usr/bin/env python3
"""Evaluación repetida v1/v2 para clasificador E.C.O."""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path
import sys
from typing import Dict, List, Sequence, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from src.eco_sequence_classifier import (  # noqa: E402
    LabeledSequence,
    build_classifier_report,
    parse_labeled_sequences_tsv,
    write_json_report,
)

DEFAULT_INPUT = PROJECT_ROOT / "examples" / "eco_labeled_sequences.tsv"
DEFAULT_JSON = PROJECT_ROOT / "results" / "eco_classifier_repeated_eval_report.json"
DEFAULT_MD = PROJECT_ROOT / "results" / "eco_classifier_repeated_eval_report.md"
DEFAULT_HTML = PROJECT_ROOT / "results" / "eco_classifier_repeated_eval_report.html"


def mean(values: Sequence[float]) -> float:
    return round(sum(values) / len(values), 4) if values else 0.0


def stddev(values: Sequence[float]) -> float:
    if len(values) < 2:
        return 0.0
    avg = sum(values) / len(values)
    variance = sum((value - avg) ** 2 for value in values) / (len(values) - 1)
    return round(variance ** 0.5, 4)


def table(headers: List[str], rows: List[List[object]]) -> List[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return lines


def stratified_resplit(records: Sequence[LabeledSequence], test_ratio: float, seed: int) -> List[LabeledSequence]:
    rng = random.Random(seed)
    by_label: Dict[str, List[LabeledSequence]] = defaultdict(list)
    for record in records:
        by_label[record.label].append(record)

    resplit: List[LabeledSequence] = []
    for label, items in sorted(by_label.items()):
        shuffled = list(items)
        rng.shuffle(shuffled)
        test_count = max(1, round(len(shuffled) * test_ratio))
        if test_count >= len(shuffled):
            test_count = len(shuffled) - 1
        for index, record in enumerate(shuffled):
            split = "test" if index < test_count else "train"
            resplit.append(LabeledSequence(record.sequence_id, record.sequence, record.label, split))
    return sorted(resplit, key=lambda record: record.sequence_id)


def extract_scores(report: Dict[str, object]) -> Dict[str, float]:
    test = report["test_evaluation"]
    train = report["train_evaluation"]
    return {
        "train_accuracy": train["accuracy"],
        "test_accuracy": test["accuracy"],
        "test_macro_f1": test["classification_metrics"]["macro_avg"]["f1"],
        "test_weighted_f1": test["classification_metrics"]["weighted_avg"]["f1"],
    }


def run_once(records: Sequence[LabeledSequence], seed: int, test_ratio: float) -> Dict[str, object]:
    split_records = stratified_resplit(records, test_ratio=test_ratio, seed=seed)
    v1 = build_classifier_report(split_records, feature_mode="motif")
    v2 = build_classifier_report(split_records, feature_mode="motif_kmer", kmer_k=2, normalize_features=True)
    v1_scores = extract_scores(v1)
    v2_scores = extract_scores(v2)
    return {
        "seed": seed,
        "train": v1["data_split"]["train"],
        "test": v1["data_split"]["test"],
        "v1": v1_scores,
        "v2": v2_scores,
        "delta_macro_f1": round(v2_scores["test_macro_f1"] - v1_scores["test_macro_f1"], 4),
        "delta_accuracy": round(v2_scores["test_accuracy"] - v1_scores["test_accuracy"], 4),
    }


def summarize_runs(runs: Sequence[Dict[str, object]]) -> Dict[str, object]:
    summary = {}
    for model in ["v1", "v2"]:
        summary[model] = {}
        for metric in ["train_accuracy", "test_accuracy", "test_macro_f1", "test_weighted_f1"]:
            values = [run[model][metric] for run in runs]
            summary[model][metric] = {"mean": mean(values), "std": stddev(values), "values": values}
    deltas = [run["delta_macro_f1"] for run in runs]
    summary["delta_macro_f1"] = {"mean": mean(deltas), "std": stddev(deltas), "values": deltas}
    wins = sum(1 for value in deltas if value > 0)
    ties = sum(1 for value in deltas if value == 0)
    losses = sum(1 for value in deltas if value < 0)
    summary["v2_outcomes"] = {"wins": wins, "ties": ties, "losses": losses}
    return summary


def interpretation(summary: Dict[str, object]) -> str:
    outcomes = summary["v2_outcomes"]
    delta = summary["delta_macro_f1"]["mean"]
    if outcomes["wins"] > outcomes["losses"] and delta > 0:
        return "v2 muestra ventaja promedio frente a v1 en esta evaluación repetida. Aun así, sigue siendo una muestra demostrativa."
    if outcomes["losses"] > outcomes["wins"] and delta < 0:
        return "v2 no mejora de forma consistente frente a v1 en esta evaluación repetida. Conviene revisar features y dataset."
    return "v1 y v2 muestran rendimiento comparable en esta evaluación repetida. Se requiere más dataset para diferenciar modelos."


def build_payload(records: Sequence[LabeledSequence], repeats: int, test_ratio: float, base_seed: int) -> Dict[str, object]:
    runs = [run_once(records, seed=base_seed + index, test_ratio=test_ratio) for index in range(repeats)]
    summary = summarize_runs(runs)
    return {
        "dataset_size": len(records),
        "repeats": repeats,
        "test_ratio": test_ratio,
        "base_seed": base_seed,
        "models": {
            "v1": "motif + scaling none",
            "v2": "motif_kmer k=2 + scaling minmax_train",
        },
        "summary": summary,
        "runs": runs,
        "interpretation": interpretation(summary),
        "limits": [
            "Evaluación repetida sobre un dataset demostrativo pequeño.",
            "Los splits repetidos reducen dependencia de una sola partición, pero no reemplazan validación externa.",
            "No debe interpretarse como benchmark científico general.",
        ],
    }


def build_markdown(payload: Dict[str, object], input_path: Path) -> str:
    summary = payload["summary"]
    rows = [
        ["v1", payload["models"]["v1"], summary["v1"]["test_accuracy"]["mean"], summary["v1"]["test_macro_f1"]["mean"], summary["v1"]["test_macro_f1"]["std"]],
        ["v2", payload["models"]["v2"], summary["v2"]["test_accuracy"]["mean"], summary["v2"]["test_macro_f1"]["mean"], summary["v2"]["test_macro_f1"]["std"]],
    ]
    run_rows = [
        [
            run["seed"],
            run["train"],
            run["test"],
            run["v1"]["test_macro_f1"],
            run["v2"]["test_macro_f1"],
            run["delta_macro_f1"],
        ]
        for run in payload["runs"]
    ]
    lines = [
        "# E.C.O. - Evaluación repetida de baselines",
        "",
        "## Propósito",
        "",
        "Este informe repite la comparación entre v1 y v2 con distintos splits estratificados. "
        "Su objetivo es revisar si la mejora observada depende de una sola partición o aparece de forma más estable.",
        "",
        "## Configuración",
        "",
        *table(
            ["Campo", "Valor"],
            [
                ["Dataset", input_path],
                ["Tamaño", payload["dataset_size"]],
                ["Repeticiones", payload["repeats"]],
                ["Test ratio", payload["test_ratio"]],
                ["Seed base", payload["base_seed"]],
            ],
        ),
        "",
        "## Resumen promedio",
        "",
        *table(["Modelo", "Configuración", "Test acc promedio", "Test macro F1 prom.", "Test macro F1 std"], rows),
        "",
        "## Resultado v2",
        "",
        *table(
            ["Indicador", "Valor"],
            [
                ["Delta macro F1 promedio", summary["delta_macro_f1"]["mean"]],
                ["Delta macro F1 std", summary["delta_macro_f1"]["std"]],
                ["Veces v2 gana", summary["v2_outcomes"]["wins"]],
                ["Empates", summary["v2_outcomes"]["ties"]],
                ["Veces v2 pierde", summary["v2_outcomes"]["losses"]],
            ],
        ),
        "",
        "## Detalle por repetición",
        "",
        *table(["Seed", "Train", "Test", "v1 macro F1", "v2 macro F1", "Delta"], run_rows),
        "",
        "## Lectura E.C.O.",
        "",
        payload["interpretation"],
        "",
        "## Límites",
        "",
        *[f"- {limit}" for limit in payload["limits"]],
        "",
    ]
    return "\n".join(lines)


def build_html(payload: Dict[str, object]) -> str:
    summary = payload["summary"]
    return f"""<!doctype html>
<html lang='es'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>E.C.O. Evaluación repetida</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 0; background: #f6f7fb; color: #172033; }}
    header {{ background: #172033; color: white; padding: 2rem; }}
    main {{ max-width: 980px; margin: auto; padding: 1.5rem; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; }}
    .card {{ background: white; border-radius: 16px; padding: 1rem; box-shadow: 0 8px 24px rgba(23,32,51,.08); }}
    strong {{ display: block; font-size: 1.8rem; }}
  </style>
</head>
<body>
  <header><h1>E.C.O. - Evaluación repetida</h1><p>Comparación v1/v2 con splits estratificados repetidos.</p></header>
  <main>
    <section class='grid'>
      <div class='card'><strong>{summary['v1']['test_macro_f1']['mean']}</strong><span>v1 macro F1 promedio</span></div>
      <div class='card'><strong>{summary['v2']['test_macro_f1']['mean']}</strong><span>v2 macro F1 promedio</span></div>
      <div class='card'><strong>{summary['delta_macro_f1']['mean']}</strong><span>Delta macro F1 promedio</span></div>
      <div class='card'><strong>{summary['v2_outcomes']['wins']}/{payload['repeats']}</strong><span>Veces que gana v2</span></div>
    </section>
    <section class='card' style='margin-top:1rem'>
      <h2>Lectura E.C.O.</h2>
      <p>{payload['interpretation']}</p>
    </section>
  </main>
</body>
</html>
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluación repetida de baselines E.C.O.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--repeats", type=int, default=10)
    parser.add_argument("--test-ratio", type=float, default=0.4)
    parser.add_argument("--base-seed", type=int, default=42)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_MD)
    parser.add_argument("--output-html", type=Path, default=DEFAULT_HTML)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    records = parse_labeled_sequences_tsv(args.input)
    payload = build_payload(records, repeats=args.repeats, test_ratio=args.test_ratio, base_seed=args.base_seed)
    write_json_report(payload, args.output_json)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(build_markdown(payload, args.input), encoding="utf-8")
    args.output_html.write_text(build_html(payload), encoding="utf-8")

    summary = payload["summary"]
    print("E.C.O. CLASSIFIER REPEATED EVALUATION")
    print("=====================================")
    print(f"Dataset: {args.input}")
    print(f"Repeticiones: {payload['repeats']}")
    print(f"v1 macro F1 promedio: {summary['v1']['test_macro_f1']['mean']}")
    print(f"v2 macro F1 promedio: {summary['v2']['test_macro_f1']['mean']}")
    print(f"Delta macro F1 promedio: {summary['delta_macro_f1']['mean']}")
    print(f"Reporte JSON: {args.output_json}")
    print(f"Reporte Markdown: {args.output_md}")
    print(f"Reporte HTML: {args.output_html}")
    print("Estado: OK, evaluación repetida generada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
