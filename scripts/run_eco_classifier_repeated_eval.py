#!/usr/bin/env python3
"""Evaluación repetida v1/v2/v3 para clasificador E.C.O."""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path
import sys
from typing import Dict, List, Sequence

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

MODEL_CONFIGS = {
    "v1": {
        "label": "baseline_v1",
        "description": "motif + scaling none",
        "feature_mode": "motif",
        "kmer_k": None,
        "normalize_features": False,
    },
    "v2": {
        "label": "baseline_v2",
        "description": "motif_kmer k=2 + scaling minmax_train",
        "feature_mode": "motif_kmer",
        "kmer_k": 2,
        "normalize_features": True,
    },
    "v3": {
        "label": "baseline_v3",
        "description": "motif_kmer k=3 + scaling minmax_train",
        "feature_mode": "motif_kmer",
        "kmer_k": 3,
        "normalize_features": True,
    },
}


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


def build_model_report(records: Sequence[LabeledSequence], model_key: str) -> Dict[str, object]:
    config = MODEL_CONFIGS[model_key]
    kwargs = {"feature_mode": config["feature_mode"]}
    if config["kmer_k"] is not None:
        kwargs["kmer_k"] = config["kmer_k"]
    if config["normalize_features"]:
        kwargs["normalize_features"] = True
    return build_classifier_report(records, **kwargs)


def run_once(records: Sequence[LabeledSequence], seed: int, test_ratio: float) -> Dict[str, object]:
    split_records = stratified_resplit(records, test_ratio=test_ratio, seed=seed)
    reports = {model: build_model_report(split_records, model) for model in MODEL_CONFIGS}
    scores = {model: extract_scores(report) for model, report in reports.items()}
    best_model = max(scores, key=lambda model: scores[model]["test_macro_f1"])
    return {
        "seed": seed,
        "train": reports["v1"]["data_split"]["train"],
        "test": reports["v1"]["data_split"]["test"],
        "models": scores,
        "best_model": best_model,
        "delta_macro_f1_vs_v1": {
            model: round(scores[model]["test_macro_f1"] - scores["v1"]["test_macro_f1"], 4)
            for model in scores
            if model != "v1"
        },
        "delta_accuracy_vs_v1": {
            model: round(scores[model]["test_accuracy"] - scores["v1"]["test_accuracy"], 4)
            for model in scores
            if model != "v1"
        },
    }


def summarize_runs(runs: Sequence[Dict[str, object]]) -> Dict[str, object]:
    summary: Dict[str, object] = {}
    for model in MODEL_CONFIGS:
        summary[model] = {}
        for metric in ["train_accuracy", "test_accuracy", "test_macro_f1", "test_weighted_f1"]:
            values = [run["models"][model][metric] for run in runs]
            summary[model][metric] = {"mean": mean(values), "std": stddev(values), "values": values}

    for model in ["v2", "v3"]:
        deltas = [run["delta_macro_f1_vs_v1"][model] for run in runs]
        wins = sum(1 for value in deltas if value > 0)
        ties = sum(1 for value in deltas if value == 0)
        losses = sum(1 for value in deltas if value < 0)
        summary[f"{model}_vs_v1"] = {
            "delta_macro_f1": {"mean": mean(deltas), "std": stddev(deltas), "values": deltas},
            "outcomes": {"wins": wins, "ties": ties, "losses": losses},
        }

    best_counts = {model: sum(1 for run in runs if run["best_model"] == model) for model in MODEL_CONFIGS}
    best_average_model = max(MODEL_CONFIGS, key=lambda model: summary[model]["test_macro_f1"]["mean"])
    summary["best_counts"] = best_counts
    summary["best_average_model"] = best_average_model
    return summary


def interpretation(summary: Dict[str, object]) -> str:
    best = summary["best_average_model"]
    v3_delta = summary["v3_vs_v1"]["delta_macro_f1"]["mean"]
    v3_outcomes = summary["v3_vs_v1"]["outcomes"]
    v2_delta = summary["v2_vs_v1"]["delta_macro_f1"]["mean"]

    if best == "v3" and v3_delta > 0 and v3_outcomes["wins"] >= v3_outcomes["losses"]:
        return (
            "v3 aparece como el candidato pre-embeddings más fuerte en la evaluación repetida. "
            "Conviene mantener v1 como control explicable y dejar v2 como variante exploratoria."
        )
    if best == "v1" and v2_delta < 0 and v3_delta <= 0:
        return (
            "v1 sigue siendo el control más estable en esta evaluación repetida. "
            "Los k-mers agregan complejidad, pero todavía no aportan mejora promedio suficiente."
        )
    return (
        "Las configuraciones muestran diferencias internas, pero la muestra sigue siendo demostrativa. "
        "Conviene ampliar datos y mantener comparación repetida antes de avanzar a embeddings."
    )


def build_payload(records: Sequence[LabeledSequence], repeats: int, test_ratio: float, base_seed: int) -> Dict[str, object]:
    runs = [run_once(records, seed=base_seed + index, test_ratio=test_ratio) for index in range(repeats)]
    summary = summarize_runs(runs)
    return {
        "dataset_size": len(records),
        "repeats": repeats,
        "test_ratio": test_ratio,
        "base_seed": base_seed,
        "models": {model: config["description"] for model, config in MODEL_CONFIGS.items()},
        "summary": summary,
        "runs": runs,
        "interpretation": interpretation(summary),
        "limits": [
            "Evaluación repetida sobre un dataset demostrativo pequeño.",
            "Los splits repetidos reducen dependencia de una sola partición, pero no reemplazan validación externa.",
            "No debe interpretarse como benchmark científico general.",
            "v3 es candidato pre-embeddings, no modelo final ni diagnóstico.",
        ],
    }


def build_markdown(payload: Dict[str, object], input_path: Path) -> str:
    summary = payload["summary"]
    rows = [
        [
            model,
            payload["models"][model],
            summary[model]["test_accuracy"]["mean"],
            summary[model]["test_macro_f1"]["mean"],
            summary[model]["test_macro_f1"]["std"],
            summary["best_counts"][model],
        ]
        for model in MODEL_CONFIGS
    ]
    outcome_rows = [
        [
            "v2 vs v1",
            summary["v2_vs_v1"]["delta_macro_f1"]["mean"],
            summary["v2_vs_v1"]["delta_macro_f1"]["std"],
            summary["v2_vs_v1"]["outcomes"]["wins"],
            summary["v2_vs_v1"]["outcomes"]["ties"],
            summary["v2_vs_v1"]["outcomes"]["losses"],
        ],
        [
            "v3 vs v1",
            summary["v3_vs_v1"]["delta_macro_f1"]["mean"],
            summary["v3_vs_v1"]["delta_macro_f1"]["std"],
            summary["v3_vs_v1"]["outcomes"]["wins"],
            summary["v3_vs_v1"]["outcomes"]["ties"],
            summary["v3_vs_v1"]["outcomes"]["losses"],
        ],
    ]
    run_rows = [
        [
            run["seed"],
            run["train"],
            run["test"],
            run["models"]["v1"]["test_macro_f1"],
            run["models"]["v2"]["test_macro_f1"],
            run["models"]["v3"]["test_macro_f1"],
            run["delta_macro_f1_vs_v1"]["v2"],
            run["delta_macro_f1_vs_v1"]["v3"],
            run["best_model"],
        ]
        for run in payload["runs"]
    ]
    lines = [
        "# E.C.O. - Evaluación repetida de baselines",
        "",
        "## Propósito",
        "",
        "Este informe repite la comparación entre v1, v2 y v3 con distintos splits estratificados. "
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
                ["Mejor promedio", summary["best_average_model"]],
            ],
        ),
        "",
        "## Resumen promedio",
        "",
        *table(["Modelo", "Configuración", "Test acc promedio", "Test macro F1 prom.", "Test macro F1 std", "Mejor en repeticiones"], rows),
        "",
        "## Resultado contra v1",
        "",
        *table(["Comparación", "Delta macro F1 prom.", "Delta std", "Gana", "Empata", "Pierde"], outcome_rows),
        "",
        "## Detalle por repetición",
        "",
        *table(["Seed", "Train", "Test", "v1 macro F1", "v2 macro F1", "v3 macro F1", "Delta v2-v1", "Delta v3-v1", "Mejor"], run_rows),
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
    cards = "\n".join(
        f"<div class='card'><strong>{summary[model]['test_macro_f1']['mean']}</strong>"
        f"<span>{model} macro F1 promedio</span><small>{payload['models'][model]}</small></div>"
        for model in MODEL_CONFIGS
    )
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
    small {{ display: block; margin-top: .35rem; color: #667085; }}
  </style>
</head>
<body>
  <header><h1>E.C.O. - Evaluación repetida</h1><p>Comparación v1/v2/v3 con splits estratificados repetidos.</p></header>
  <main>
    <section class='grid'>
      {cards}
      <div class='card'><strong>{summary['best_average_model']}</strong><span>Mejor promedio</span></div>
      <div class='card'><strong>{summary['v3_vs_v1']['delta_macro_f1']['mean']}</strong><span>Delta v3 vs v1</span></div>
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
    for model in MODEL_CONFIGS:
        print(f"{model} macro F1 promedio: {summary[model]['test_macro_f1']['mean']}")
    print(f"Mejor promedio: {summary['best_average_model']}")
    print(f"Delta v3 vs v1 macro F1 promedio: {summary['v3_vs_v1']['delta_macro_f1']['mean']}")
    print(f"Reporte JSON: {args.output_json}")
    print(f"Reporte Markdown: {args.output_md}")
    print(f"Reporte HTML: {args.output_html}")
    print("Estado: OK, evaluación repetida v1/v2/v3 generada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
