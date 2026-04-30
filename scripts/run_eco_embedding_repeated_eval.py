#!/usr/bin/env python3
"""Evaluación repetida de la ruta embedding placeholder para E.C.O.

Compara el contrato vectorial experimental contra baseline_v1 y baseline_v3
usando splits estratificados repetidos. No descarga modelos pesados.
"""

from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
import sys
from typing import Dict, List, Sequence

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from scripts.run_eco_classifier_repeated_eval import mean, stddev, stratified_resplit, table  # noqa: E402
from scripts.run_eco_embedding_placeholder import build_embedding_report  # noqa: E402
from src.eco_sequence_classifier import LabeledSequence, parse_labeled_sequences_tsv, write_json_report  # noqa: E402

DEFAULT_INPUT = PROJECT_ROOT / "examples" / "eco_labeled_sequences.tsv"
DEFAULT_JSON = PROJECT_ROOT / "results" / "eco_embedding_repeated_eval_report.json"
DEFAULT_MD = PROJECT_ROOT / "results" / "eco_embedding_repeated_eval_report.md"
DEFAULT_HTML = PROJECT_ROOT / "results" / "eco_embedding_repeated_eval_report.html"

MODEL_ORDER = ["baseline_v1", "baseline_v3", "embedding_placeholder"]
MODEL_ROLES = {
    "baseline_v1": "control_explicable",
    "baseline_v3": "candidato_pre_embeddings",
    "embedding_placeholder": "contrato_vectorial_experimental",
}


def e(value: object) -> str:
    return escape(str(value), quote=True)


def html_table(headers: List[str], rows: List[List[object]]) -> str:
    head = "".join(f"<th>{e(header)}</th>" for header in headers)
    body = "".join("<tr>" + "".join(f"<td>{e(value)}</td>" for value in row) + "</tr>" for row in rows)
    return f"<div class='table-scroll'><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"


def extract_scores(report: Dict[str, object]) -> Dict[str, Dict[str, float]]:
    scores: Dict[str, Dict[str, float]] = {}
    for row in report["comparison"]:
        scores[row["model"]] = {
            "test_accuracy": row["test_accuracy"],
            "test_macro_f1": row["test_macro_f1"],
        }
    return scores


def run_once(records: Sequence[LabeledSequence], seed: int, test_ratio: float, embedding_k: int, dimensions: int) -> Dict[str, object]:
    split_records = stratified_resplit(records, test_ratio=test_ratio, seed=seed)
    report = build_embedding_report(split_records, k=embedding_k, dimensions=dimensions)
    scores = extract_scores(report)
    best_model = max(scores, key=lambda model: scores[model]["test_macro_f1"])
    split = report["embedding_report"]["data_split"]
    return {
        "seed": seed,
        "train": split["train"],
        "test": split["test"],
        "models": scores,
        "best_model": best_model,
        "delta_macro_f1_vs_v3": round(scores["embedding_placeholder"]["test_macro_f1"] - scores["baseline_v3"]["test_macro_f1"], 4),
        "delta_macro_f1_vs_v1": round(scores["embedding_placeholder"]["test_macro_f1"] - scores["baseline_v1"]["test_macro_f1"], 4),
    }


def summarize_runs(runs: Sequence[Dict[str, object]]) -> Dict[str, object]:
    summary: Dict[str, object] = {}
    for model in MODEL_ORDER:
        summary[model] = {}
        for metric in ["test_accuracy", "test_macro_f1"]:
            values = [run["models"][model][metric] for run in runs]
            summary[model][metric] = {"mean": mean(values), "std": stddev(values), "values": values}

    for comparison_key, delta_key in [
        ("embedding_vs_v3", "delta_macro_f1_vs_v3"),
        ("embedding_vs_v1", "delta_macro_f1_vs_v1"),
    ]:
        values = [run[delta_key] for run in runs]
        summary[comparison_key] = {
            "delta_macro_f1": {"mean": mean(values), "std": stddev(values), "values": values},
            "outcomes": {
                "wins": sum(1 for value in values if value > 0),
                "ties": sum(1 for value in values if value == 0),
                "losses": sum(1 for value in values if value < 0),
            },
        }

    summary["best_counts"] = {model: sum(1 for run in runs if run["best_model"] == model) for model in MODEL_ORDER}
    summary["best_average_model"] = max(MODEL_ORDER, key=lambda model: summary[model]["test_macro_f1"]["mean"])
    return summary


def interpretation(summary: Dict[str, object]) -> str:
    best = summary["best_average_model"]
    delta_vs_v3 = summary["embedding_vs_v3"]["delta_macro_f1"]["mean"]
    if best == "embedding_placeholder" and delta_vs_v3 > 0:
        return "El placeholder supera a v3 en promedio, pero debe leerse solo como señal arquitectónica; aún no es embedding profundo real."
    if best == "baseline_v3" and delta_vs_v3 < 0:
        return "baseline_v3 sigue siendo la referencia más fuerte; el placeholder valida contrato vectorial, no superioridad de modelo."
    return "La comparación deja una señal mixta; conviene mantener v1/v3 como controles y usar el placeholder solo como puente hacia embeddings reales."


def build_payload(records: Sequence[LabeledSequence], repeats: int, test_ratio: float, base_seed: int, embedding_k: int, dimensions: int) -> Dict[str, object]:
    runs = [
        run_once(records, seed=base_seed + index, test_ratio=test_ratio, embedding_k=embedding_k, dimensions=dimensions)
        for index in range(repeats)
    ]
    summary = summarize_runs(runs)
    return {
        "pipeline": "E.C.O. embedding placeholder repeated evaluation",
        "dataset_size": len(records),
        "repeats": repeats,
        "test_ratio": test_ratio,
        "base_seed": base_seed,
        "embedding": {
            "type": "kmer_frequency_placeholder",
            "k": embedding_k,
            "dimensions": dimensions,
            "scaling": "minmax_train",
        },
        "models": MODEL_ROLES,
        "summary": summary,
        "runs": runs,
        "interpretation": interpretation(summary),
        "limits": [
            "Evaluación repetida sobre dataset demostrativo pequeño.",
            "El embedding placeholder usa frecuencias k-mer; no es DNABERT ni embedding profundo real.",
            "Sirve para probar estabilidad del contrato vectorial antes de integrar modelos pesados.",
            "No representa benchmark científico ni desempeño clínico.",
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
        for model in MODEL_ORDER
    ]
    outcome_rows = [
        [
            "embedding_placeholder vs baseline_v3",
            summary["embedding_vs_v3"]["delta_macro_f1"]["mean"],
            summary["embedding_vs_v3"]["delta_macro_f1"]["std"],
            summary["embedding_vs_v3"]["outcomes"]["wins"],
            summary["embedding_vs_v3"]["outcomes"]["ties"],
            summary["embedding_vs_v3"]["outcomes"]["losses"],
        ],
        [
            "embedding_placeholder vs baseline_v1",
            summary["embedding_vs_v1"]["delta_macro_f1"]["mean"],
            summary["embedding_vs_v1"]["delta_macro_f1"]["std"],
            summary["embedding_vs_v1"]["outcomes"]["wins"],
            summary["embedding_vs_v1"]["outcomes"]["ties"],
            summary["embedding_vs_v1"]["outcomes"]["losses"],
        ],
    ]
    run_rows = [
        [
            run["seed"],
            run["train"],
            run["test"],
            run["models"]["baseline_v1"]["test_macro_f1"],
            run["models"]["baseline_v3"]["test_macro_f1"],
            run["models"]["embedding_placeholder"]["test_macro_f1"],
            run["delta_macro_f1_vs_v3"],
            run["best_model"],
        ]
        for run in payload["runs"]
    ]
    lines = [
        "# E.C.O. - Evaluación repetida de embeddings placeholder",
        "",
        "## Propósito",
        "",
        "Este informe repite la ruta `embedding_placeholder` con distintos splits estratificados y la compara contra `baseline_v1` y `baseline_v3`.",
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
                ["Embedding", payload["embedding"]["type"]],
                ["k", payload["embedding"]["k"]],
                ["Dimensiones", payload["embedding"]["dimensions"]],
                ["Mejor promedio", summary["best_average_model"]],
            ],
        ),
        "",
        "## Resumen promedio",
        "",
        *table(["Modelo", "Rol", "Test acc promedio", "Macro F1 prom.", "Macro F1 std", "Mejor en repeticiones"], rows),
        "",
        "## Resultado del placeholder",
        "",
        *table(["Comparación", "Delta macro F1 prom.", "Delta std", "Gana", "Empata", "Pierde"], outcome_rows),
        "",
        "## Detalle por repetición",
        "",
        *table(["Seed", "Train", "Test", "v1 macro F1", "v3 macro F1", "embedding macro F1", "Delta embedding-v3", "Mejor"], run_rows),
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
        f"<span>{model}</span><small>{payload['models'][model]}</small></div>"
        for model in MODEL_ORDER
    )
    rows = [
        [model, payload["models"][model], summary[model]["test_accuracy"]["mean"], summary[model]["test_macro_f1"]["mean"], summary[model]["test_macro_f1"]["std"]]
        for model in MODEL_ORDER
    ]
    limits = "".join(f"<li>{e(limit)}</li>" for limit in payload["limits"])
    return f"""<!doctype html>
<html lang='es'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>E.C.O. Embedding repeated eval</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 0; background: #f6f7fb; color: #172033; }}
    header {{ background: #172033; color: white; padding: 2rem; }}
    main {{ max-width: 1080px; margin: auto; padding: 1.5rem; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 1rem; }}
    .card, .section {{ background: white; border-radius: 16px; padding: 1rem; box-shadow: 0 8px 24px rgba(23,32,51,.08); margin-bottom: 1rem; }}
    strong {{ display: block; font-size: 1.8rem; }}
    small {{ display: block; margin-top: .35rem; color: #667085; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ text-align: left; padding: .7rem; border-bottom: 1px solid #e6e8f0; }}
    th {{ background: #eef1f8; }}
    .table-scroll {{ overflow-x: auto; }}
    .warning {{ border-left: 6px solid #9b6b00; }}
  </style>
</head>
<body>
  <header><h1>E.C.O. - Evaluación repetida de embeddings placeholder</h1><p>Contrato vectorial repetido contra v1 y v3.</p></header>
  <main>
    <section class='grid'>{cards}<div class='card'><strong>{e(summary['best_average_model'])}</strong><span>Mejor promedio</span></div></section>
    <section class='section'><h2>Resumen promedio</h2>{html_table(['Modelo', 'Rol', 'Test acc promedio', 'Macro F1 prom.', 'Macro F1 std'], rows)}</section>
    <section class='section'><h2>Lectura E.C.O.</h2><p>{e(payload['interpretation'])}</p></section>
    <section class='section warning'><h2>Límites</h2><ul>{limits}</ul></section>
  </main>
</body>
</html>
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluación repetida de embeddings placeholder E.C.O.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--repeats", type=int, default=10)
    parser.add_argument("--test-ratio", type=float, default=0.4)
    parser.add_argument("--base-seed", type=int, default=42)
    parser.add_argument("--embedding-k", type=int, default=3)
    parser.add_argument("--dimensions", type=int, default=64)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_MD)
    parser.add_argument("--output-html", type=Path, default=DEFAULT_HTML)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    records = parse_labeled_sequences_tsv(args.input)
    payload = build_payload(
        records,
        repeats=args.repeats,
        test_ratio=args.test_ratio,
        base_seed=args.base_seed,
        embedding_k=args.embedding_k,
        dimensions=args.dimensions,
    )
    write_json_report(payload, args.output_json)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(build_markdown(payload, args.input), encoding="utf-8")
    args.output_html.write_text(build_html(payload), encoding="utf-8")

    summary = payload["summary"]
    print("E.C.O. EMBEDDING PLACEHOLDER REPEATED EVALUATION")
    print("================================================")
    print(f"Dataset: {args.input}")
    print(f"Repeticiones: {payload['repeats']}")
    for model in MODEL_ORDER:
        print(f"{model} macro F1 promedio: {summary[model]['test_macro_f1']['mean']}")
    print(f"Mejor promedio: {summary['best_average_model']}")
    print(f"Delta embedding vs v3 macro F1 promedio: {summary['embedding_vs_v3']['delta_macro_f1']['mean']}")
    print(f"Reporte JSON: {args.output_json}")
    print(f"Reporte Markdown: {args.output_md}")
    print(f"Reporte HTML: {args.output_html}")
    print("Estado: OK, evaluación repetida de embedding placeholder generada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
