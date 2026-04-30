#!/usr/bin/env python3
"""Ruta experimental de embeddings placeholder para E.C.O.

Este script NO descarga DNABERT ni modelos pesados. Su objetivo es crear el
contrato de arquitectura para comparar una ruta vectorial futura contra los
baselines explicables v1 y v3.
"""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path
import sys
from typing import Dict, List, Sequence

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from src.eco_sequence_classifier import (  # noqa: E402
    FeatureVector,
    LabeledSequence,
    build_classifier_report,
    evaluate_with_feature_map,
    fit_minmax_scaler,
    parse_labeled_sequences_tsv,
    scale_feature_map,
    split_train_test,
    train_centroid_classifier_from_features,
    write_json_report,
)

DEFAULT_INPUT = PROJECT_ROOT / "examples" / "eco_labeled_sequences.tsv"
DEFAULT_JSON = PROJECT_ROOT / "results" / "eco_embedding_placeholder_report.json"
DEFAULT_MD = PROJECT_ROOT / "results" / "eco_embedding_placeholder_report.md"
DEFAULT_HTML = PROJECT_ROOT / "results" / "eco_embedding_placeholder_report.html"
DNA_TO_NUM = {"A": 0, "C": 1, "G": 2, "T": 3}


def table(headers: List[str], rows: List[List[object]]) -> List[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return lines


def e(value: object) -> str:
    return escape(str(value), quote=True)


def html_table(headers: List[str], rows: List[List[object]]) -> str:
    head = "".join(f"<th>{e(header)}</th>" for header in headers)
    body = "".join("<tr>" + "".join(f"<td>{e(value)}</td>" for value in row) + "</tr>" for row in rows)
    return f"<div class='table-scroll'><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"


def kmer_index(window: str) -> int:
    value = 0
    for base in window:
        value = (value * 4) + DNA_TO_NUM[base]
    return value


def build_placeholder_embedding(sequence: str, k: int = 3, dimensions: int = 64) -> FeatureVector:
    """Construye un vector determinista tipo embedding usando frecuencias k-mer.

    Es intencionalmente simple y sin dependencias externas. Sirve como sustituto
    temporal para validar el flujo embeddings -> clasificador -> comparación.
    """
    if k <= 0:
        raise ValueError("k debe ser mayor que cero.")
    if dimensions <= 0:
        raise ValueError("dimensions debe ser mayor que cero.")

    sequence = sequence.upper()
    vector: FeatureVector = {f"embed_{index:02d}": 0.0 for index in range(dimensions)}
    valid_windows = 0

    for start in range(0, max(len(sequence) - k + 1, 0)):
        window = sequence[start : start + k]
        if len(window) == k and all(base in DNA_TO_NUM for base in window):
            bucket = kmer_index(window) % dimensions
            vector[f"embed_{bucket:02d}"] += 1.0
            valid_windows += 1

    if valid_windows:
        for key in vector:
            vector[key] = round(vector[key] / valid_windows, 6)

    return vector


def build_embedding_feature_map(
    records: Sequence[LabeledSequence], k: int = 3, dimensions: int = 64
) -> Dict[str, FeatureVector]:
    return {record.sequence_id: build_placeholder_embedding(record.sequence, k=k, dimensions=dimensions) for record in records}


def macro_f1(report: Dict[str, object]) -> float:
    return report["test_evaluation"]["classification_metrics"]["macro_avg"]["f1"]


def accuracy(report: Dict[str, object]) -> float:
    return report["test_evaluation"]["accuracy"]


def build_embedding_report(records: Sequence[LabeledSequence], k: int = 3, dimensions: int = 64) -> Dict[str, object]:
    train_records, test_records = split_train_test(records)
    train_features = build_embedding_feature_map(train_records, k=k, dimensions=dimensions)
    test_features = build_embedding_feature_map(test_records, k=k, dimensions=dimensions)

    scaler = fit_minmax_scaler(list(train_features.values()))
    train_features = scale_feature_map(train_features, scaler)
    test_features = scale_feature_map(test_features, scaler)

    centroids = train_centroid_classifier_from_features(train_records, train_features)
    train_evaluation = evaluate_with_feature_map(train_records, centroids, train_features)
    test_evaluation = evaluate_with_feature_map(test_records, centroids, test_features)

    baseline_v1 = build_classifier_report(records, feature_mode="motif", kmer_k=2, normalize_features=False)
    baseline_v3 = build_classifier_report(records, feature_mode="motif_kmer", kmer_k=3, normalize_features=True)

    embedding_payload: Dict[str, object] = {
        "model_type": "centroid_placeholder_embedding",
        "embedding_type": "kmer_frequency_placeholder",
        "embedding_k": k,
        "embedding_dimensions": dimensions,
        "feature_scaling": "minmax_train",
        "purpose": "ruta_experimental_pre_dnaber_para_validar_contrato_de_embeddings",
        "data_split": {
            "train": len(train_records),
            "test": len(test_records),
            "note": "Embeddings placeholder entrenados con split=train y evaluados en split=test.",
        },
        "centroids": centroids,
        "train_evaluation": train_evaluation,
        "test_evaluation": test_evaluation,
        "limits": [
            "Embedding placeholder determinista basado en frecuencias k-mer; no es DNABERT.",
            "No descarga modelos ni agrega dependencias pesadas.",
            "Sirve para validar arquitectura y contrato de comparación pre-embeddings reales.",
            "No representa benchmark científico ni desempeño clínico.",
        ],
    }

    comparison_rows = [
        {
            "model": "baseline_v1",
            "role": "control_explicable",
            "features": "motif",
            "test_accuracy": accuracy(baseline_v1),
            "test_macro_f1": macro_f1(baseline_v1),
        },
        {
            "model": "baseline_v3",
            "role": "candidato_pre_embeddings",
            "features": "motif_kmer_k3_minmax",
            "test_accuracy": accuracy(baseline_v3),
            "test_macro_f1": macro_f1(baseline_v3),
        },
        {
            "model": "embedding_placeholder",
            "role": "contrato_vectorial_experimental",
            "features": f"kmer_embedding_k{k}_dim{dimensions}_minmax",
            "test_accuracy": accuracy(embedding_payload),
            "test_macro_f1": macro_f1(embedding_payload),
        },
    ]
    best = max(comparison_rows, key=lambda item: item["test_macro_f1"])

    return {
        "pipeline": "E.C.O. embedding placeholder route",
        "dataset": str(DEFAULT_INPUT),
        "embedding_report": embedding_payload,
        "comparison": comparison_rows,
        "best_model_by_test_macro_f1": best,
        "baseline_references": {
            "v1": {
                "model_type": baseline_v1["model_type"],
                "test_accuracy": accuracy(baseline_v1),
                "test_macro_f1": macro_f1(baseline_v1),
            },
            "v3": {
                "model_type": baseline_v3["model_type"],
                "test_accuracy": accuracy(baseline_v3),
                "test_macro_f1": macro_f1(baseline_v3),
            },
        },
        "limits": embedding_payload["limits"],
    }


def build_markdown(report: Dict[str, object], input_path: Path) -> str:
    embedding = report["embedding_report"]
    split = embedding["data_split"]
    comparison_rows = [
        [row["model"], row["role"], row["features"], row["test_accuracy"], row["test_macro_f1"]]
        for row in report["comparison"]
    ]
    best = report["best_model_by_test_macro_f1"]
    lines = [
        "# E.C.O. - Ruta experimental de embeddings placeholder",
        "",
        "## Propósito",
        "",
        "Este informe prepara una ruta vectorial experimental sin descargar modelos pesados. "
        "Su objetivo es validar el contrato `secuencia → embedding → clasificador → comparación` antes de incorporar DNABERT u otro modelo real.",
        "",
        "## Entrada",
        "",
        *table(
            ["Campo", "Valor"],
            [
                ["Dataset", input_path],
                ["Train", split["train"]],
                ["Test", split["test"]],
                ["Embedding", embedding["embedding_type"]],
                ["k", embedding["embedding_k"]],
                ["Dimensiones", embedding["embedding_dimensions"]],
                ["Scaling", embedding["feature_scaling"]],
            ],
        ),
        "",
        "## Comparación contra baselines",
        "",
        *table(["Modelo", "Rol", "Features", "Test accuracy", "Test macro F1"], comparison_rows),
        "",
        "## Mejor modelo del split fijo",
        "",
        f"- Mejor modelo: `{best['model']}`",
        f"- Test macro F1: `{best['test_macro_f1']}`",
        "",
        "## Lectura E.C.O.",
        "",
        "Esta ruta no reemplaza a v1 ni v3. Funciona como una pieza de conexión: deja preparado el intestino informacional para recibir embeddings reales más adelante y medirlos contra referencias ya existentes.",
        "",
        "## Límites",
        "",
        *[f"- {limit}" for limit in report["limits"]],
        "",
        "## Próximo paso",
        "",
        "Mantener esta ruta como `placeholder` y, cuando corresponda, crear una variante real de embeddings que use el mismo contrato de entrada/salida.",
        "",
    ]
    return "\n".join(lines)


def build_html(report: Dict[str, object]) -> str:
    embedding = report["embedding_report"]
    split = embedding["data_split"]
    best = report["best_model_by_test_macro_f1"]
    comparison_rows = [
        [row["model"], row["role"], row["features"], row["test_accuracy"], row["test_macro_f1"]]
        for row in report["comparison"]
    ]
    limit_items = "".join(f"<li>{e(limit)}</li>" for limit in report["limits"])
    return f"""<!doctype html>
<html lang='es'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>E.C.O. Embedding placeholder</title>
  <style>
    body {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; background: #f6f7fb; color: #172033; }}
    header {{ background: #172033; color: white; padding: 2rem; }}
    main {{ max-width: 1100px; margin: 0 auto; padding: 1.5rem; }}
    .subtitle {{ color: #d8e0ff; max-width: 900px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 1rem; }}
    .metric, .section {{ background: white; border-radius: 16px; padding: 1rem; box-shadow: 0 8px 24px rgba(23, 32, 51, 0.08); margin-bottom: 1rem; }}
    .metric strong {{ display: block; font-size: 1.6rem; margin-bottom: .2rem; }}
    table {{ width: 100%; border-collapse: collapse; background: white; }}
    th, td {{ text-align: left; padding: .7rem; border-bottom: 1px solid #e6e8f0; vertical-align: top; }}
    th {{ background: #eef1f8; }}
    .table-scroll {{ overflow-x: auto; }}
    .warning {{ border-left: 6px solid #9b6b00; }}
  </style>
</head>
<body>
  <header>
    <h1>E.C.O. - Ruta experimental de embeddings placeholder</h1>
    <p class='subtitle'>Contrato vectorial sin modelos pesados: secuencia → embedding placeholder → centroides → comparación contra v1 y v3.</p>
  </header>
  <main>
    <section class='grid'>
      <div class='metric'><strong>{e(split['train'])}</strong><span>Train</span></div>
      <div class='metric'><strong>{e(split['test'])}</strong><span>Test</span></div>
      <div class='metric'><strong>{e(embedding['embedding_dimensions'])}</strong><span>Dimensiones</span></div>
      <div class='metric'><strong>{e(best['model'])}</strong><span>Mejor macro F1</span></div>
      <div class='metric'><strong>{e(best['test_macro_f1'])}</strong><span>Test macro F1</span></div>
    </section>
    <section class='section'>
      <h2>Comparación contra baselines</h2>
      {html_table(['Modelo', 'Rol', 'Features', 'Test accuracy', 'Test macro F1'], comparison_rows)}
    </section>
    <section class='section'>
      <h2>Lectura E.C.O.</h2>
      <p>Esta ruta no intenta ganar por ahora: deja lista la pieza arquitectónica para que un embedding real pueda compararse de forma honesta contra v1 y v3.</p>
    </section>
    <section class='section warning'>
      <h2>Límites</h2>
      <ul>{limit_items}</ul>
    </section>
  </main>
</body>
</html>
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ejecuta ruta experimental de embeddings placeholder E.C.O.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_MD)
    parser.add_argument("--output-html", type=Path, default=DEFAULT_HTML)
    parser.add_argument("--embedding-k", type=int, default=3)
    parser.add_argument("--dimensions", type=int, default=64)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    records = parse_labeled_sequences_tsv(args.input)
    report = build_embedding_report(records, k=args.embedding_k, dimensions=args.dimensions)
    report["dataset"] = str(args.input)

    write_json_report(report, args.output_json)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(build_markdown(report, args.input), encoding="utf-8")
    args.output_html.write_text(build_html(report), encoding="utf-8")

    embedding = report["embedding_report"]
    test = embedding["test_evaluation"]
    macro = test["classification_metrics"]["macro_avg"]["f1"]
    best = report["best_model_by_test_macro_f1"]

    print("E.C.O. EMBEDDING PLACEHOLDER REPORT")
    print("====================================")
    print(f"Dataset: {args.input}")
    print(f"Embedding: {embedding['embedding_type']}")
    print(f"k: {embedding['embedding_k']} | dimensiones: {embedding['embedding_dimensions']}")
    print(f"Placeholder test accuracy: {test['accuracy']}")
    print(f"Placeholder test macro F1: {macro}")
    print(f"Mejor modelo comparado: {best['model']} | macro F1: {best['test_macro_f1']}")
    print(f"Reporte JSON: {args.output_json}")
    print(f"Reporte Markdown: {args.output_md}")
    print(f"Reporte HTML: {args.output_html}")
    print("Estado: OK, ruta experimental de embeddings placeholder generada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
