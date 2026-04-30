#!/usr/bin/env python3
"""Evaluación de sensibilidad de configuraciones del clasificador E.C.O."""

from __future__ import annotations

import argparse
import html
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
DEFAULT_JSON = PROJECT_ROOT / "results" / "eco_classifier_sensitivity_report.json"
DEFAULT_MD = PROJECT_ROOT / "results" / "eco_classifier_sensitivity_report.md"
DEFAULT_HTML = PROJECT_ROOT / "results" / "eco_classifier_sensitivity_report.html"

CONFIGS = [
    {
        "id": "v1_motif_none",
        "label": "v1 motif sin normalización",
        "feature_mode": "motif",
        "kmer_k": 2,
        "normalize_features": False,
    },
    {
        "id": "motif_minmax",
        "label": "motif con minmax_train",
        "feature_mode": "motif",
        "kmer_k": 2,
        "normalize_features": True,
    },
    {
        "id": "kmer2_none",
        "label": "motif + k-mer k=2 sin normalización",
        "feature_mode": "motif_kmer",
        "kmer_k": 2,
        "normalize_features": False,
    },
    {
        "id": "v2_kmer2_minmax",
        "label": "v2 motif + k-mer k=2 con minmax_train",
        "feature_mode": "motif_kmer",
        "kmer_k": 2,
        "normalize_features": True,
    },
    {
        "id": "kmer3_none",
        "label": "motif + k-mer k=3 sin normalización",
        "feature_mode": "motif_kmer",
        "kmer_k": 3,
        "normalize_features": False,
    },
    {
        "id": "kmer3_minmax",
        "label": "motif + k-mer k=3 con minmax_train",
        "feature_mode": "motif_kmer",
        "kmer_k": 3,
        "normalize_features": True,
    },
]


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
    for _label, items in sorted(by_label.items()):
        shuffled = list(items)
        rng.shuffle(shuffled)
        test_count = max(1, round(len(shuffled) * test_ratio))
        if test_count >= len(shuffled):
            test_count = len(shuffled) - 1
        for index, record in enumerate(shuffled):
            split = "test" if index < test_count else "train"
            resplit.append(LabeledSequence(record.sequence_id, record.sequence, record.label, split))
    return sorted(resplit, key=lambda record: record.sequence_id)


def scores_from_report(report: Dict[str, object]) -> Dict[str, float]:
    train = report["train_evaluation"]
    test = report["test_evaluation"]
    return {
        "train_accuracy": train["accuracy"],
        "test_accuracy": test["accuracy"],
        "test_macro_f1": test["classification_metrics"]["macro_avg"]["f1"],
        "test_weighted_f1": test["classification_metrics"]["weighted_avg"]["f1"],
    }


def evaluate_config(records: Sequence[LabeledSequence], config: Dict[str, object]) -> Dict[str, float]:
    report = build_classifier_report(
        records,
        feature_mode=str(config["feature_mode"]),
        kmer_k=int(config["kmer_k"]),
        normalize_features=bool(config["normalize_features"]),
    )
    return scores_from_report(report)


def build_payload(records: Sequence[LabeledSequence], repeats: int, test_ratio: float, base_seed: int) -> Dict[str, object]:
    runs = []
    by_config: Dict[str, List[Dict[str, float]]] = {str(config["id"]): [] for config in CONFIGS}

    for index in range(repeats):
        seed = base_seed + index
        split_records = stratified_resplit(records, test_ratio=test_ratio, seed=seed)
        run = {"seed": seed, "train": 0, "test": 0, "scores": {}}
        for config in CONFIGS:
            scores = evaluate_config(split_records, config)
            config_id = str(config["id"])
            by_config[config_id].append(scores)
            run["scores"][config_id] = scores
        first_report = build_classifier_report(split_records, feature_mode="motif")
        run["train"] = first_report["data_split"]["train"]
        run["test"] = first_report["data_split"]["test"]
        runs.append(run)

    summary = {}
    for config in CONFIGS:
        config_id = str(config["id"])
        items = by_config[config_id]
        summary[config_id] = {
            "label": config["label"],
            "feature_mode": config["feature_mode"],
            "kmer_k": config["kmer_k"] if config["feature_mode"] == "motif_kmer" else "no_aplica",
            "feature_scaling": "minmax_train" if config["normalize_features"] else "none",
            "test_accuracy_mean": mean([item["test_accuracy"] for item in items]),
            "test_macro_f1_mean": mean([item["test_macro_f1"] for item in items]),
            "test_macro_f1_std": stddev([item["test_macro_f1"] for item in items]),
            "test_weighted_f1_mean": mean([item["test_weighted_f1"] for item in items]),
            "values": [item["test_macro_f1"] for item in items],
        }

    best_id = max(summary, key=lambda key: summary[key]["test_macro_f1_mean"])
    baseline_id = "v1_motif_none"
    current_v2_id = "v2_kmer2_minmax"
    return {
        "dataset_size": len(records),
        "repeats": repeats,
        "test_ratio": test_ratio,
        "base_seed": base_seed,
        "configs": CONFIGS,
        "summary": summary,
        "best_config": best_id,
        "baseline_delta": round(summary[best_id]["test_macro_f1_mean"] - summary[baseline_id]["test_macro_f1_mean"], 4),
        "current_v2_delta": round(summary[current_v2_id]["test_macro_f1_mean"] - summary[baseline_id]["test_macro_f1_mean"], 4),
        "runs": runs,
        "interpretation": build_interpretation(summary, best_id, baseline_id, current_v2_id),
        "limits": [
            "Evaluación de sensibilidad sobre dataset demostrativo.",
            "Busca orientar decisiones de features, no declarar benchmark científico.",
            "Un mejor promedio interno no reemplaza validación externa ni datos reales más amplios.",
        ],
    }


def build_interpretation(summary: Dict[str, object], best_id: str, baseline_id: str, current_v2_id: str) -> str:
    best = summary[best_id]
    baseline = summary[baseline_id]
    current_v2 = summary[current_v2_id]
    if best_id == baseline_id:
        return "La configuración simple basada en motivos sigue siendo la más fuerte en esta muestra. Conviene no aumentar complejidad todavía."
    if current_v2["test_macro_f1_mean"] < baseline["test_macro_f1_mean"]:
        return "El v2 actual queda bajo v1 en promedio. La sensibilidad ayuda a decidir si otra configuración k-mer es más estable o si conviene mantener v1 como baseline principal."
    return "Alguna configuración enriquecida supera al baseline simple. Conviene documentarla como candidata, no como modelo final."


def build_markdown(payload: Dict[str, object], input_path: Path) -> str:
    summary = payload["summary"]
    rows = []
    for config_id, item in sorted(summary.items(), key=lambda pair: pair[1]["test_macro_f1_mean"], reverse=True):
        rows.append([
            config_id,
            item["label"],
            item["feature_mode"],
            item["feature_scaling"],
            item["kmer_k"],
            item["test_accuracy_mean"],
            item["test_macro_f1_mean"],
            item["test_macro_f1_std"],
        ])

    run_rows = []
    for run in payload["runs"]:
        row = [run["seed"], run["train"], run["test"]]
        for config in CONFIGS:
            config_id = str(config["id"])
            row.append(run["scores"][config_id]["test_macro_f1"])
        run_rows.append(row)

    lines = [
        "# E.C.O. - Sensibilidad del clasificador",
        "",
        "## Propósito",
        "",
        "Este informe compara varias configuraciones simples del clasificador para diagnosticar si el rendimiento cambia por k-mers, normalización o tamaño de k.",
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
                ["Mejor configuración", payload["best_config"]],
                ["Delta mejor vs v1", payload["baseline_delta"]],
                ["Delta v2 actual vs v1", payload["current_v2_delta"]],
            ],
        ),
        "",
        "## Ranking promedio",
        "",
        *table(["Config", "Lectura", "Feature mode", "Scaling", "k", "Test acc prom.", "Macro F1 prom.", "Macro F1 std"], rows),
        "",
        "## Detalle por repetición",
        "",
        *table(["Seed", "Train", "Test", *[str(config["id"]) for config in CONFIGS]], run_rows),
        "",
        "## Lectura E.C.O.",
        "",
        payload["interpretation"],
        "",
        "## Límites",
        "",
        *[f"- {limit}" for limit in payload["limits"]],
        "",
        "## Siguiente decisión técnica",
        "",
        "Usar este informe para decidir si el baseline oficial debe seguir siendo v1, si v2 necesita ajuste, o si conviene crear un v3 con selección/ponderación de features antes de avanzar a embeddings.",
        "",
    ]
    return "\n".join(lines)


def build_html(payload: Dict[str, object]) -> str:
    summary = payload["summary"]
    sorted_items = sorted(summary.items(), key=lambda pair: pair[1]["test_macro_f1_mean"], reverse=True)
    cards = []
    for config_id, item in sorted_items:
        cards.append(
            "<div class='card'>"
            f"<strong>{html.escape(str(item['test_macro_f1_mean']))}</strong>"
            f"<span>{html.escape(config_id)}</span>"
            f"<small>{html.escape(str(item['label']))}</small>"
            "</div>"
        )
    return f"""<!doctype html>
<html lang='es'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>E.C.O. Sensibilidad del clasificador</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 0; background: #f6f7fb; color: #172033; }}
    header {{ background: #172033; color: white; padding: 2rem; }}
    main {{ max-width: 1080px; margin: auto; padding: 1.5rem; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }}
    .card {{ background: white; border-radius: 16px; padding: 1rem; box-shadow: 0 8px 24px rgba(23,32,51,.08); }}
    strong {{ display: block; font-size: 1.8rem; }}
    span {{ display: block; font-weight: 700; }}
    small {{ color: #5c667a; }}
  </style>
</head>
<body>
  <header><h1>E.C.O. - Sensibilidad del clasificador</h1><p>Diagnóstico de feature modes, k-mers y normalización.</p></header>
  <main>
    <section class='grid'>{''.join(cards)}</section>
    <section class='card' style='margin-top:1rem'>
      <h2>Lectura E.C.O.</h2>
      <p>{html.escape(payload['interpretation'])}</p>
      <p><strong>Mejor configuración:</strong> {html.escape(payload['best_config'])}</p>
    </section>
  </main>
</body>
</html>
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evalúa sensibilidad de configuraciones del clasificador E.C.O.")
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

    print("E.C.O. CLASSIFIER SENSITIVITY REPORT")
    print("====================================")
    print(f"Dataset: {args.input}")
    print(f"Repeticiones: {payload['repeats']}")
    print(f"Mejor configuración: {payload['best_config']}")
    print(f"Delta mejor vs v1: {payload['baseline_delta']}")
    print(f"Delta v2 actual vs v1: {payload['current_v2_delta']}")
    print(f"Reporte JSON: {args.output_json}")
    print(f"Reporte Markdown: {args.output_md}")
    print(f"Reporte HTML: {args.output_html}")
    print("Estado: OK, sensibilidad del clasificador generada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
