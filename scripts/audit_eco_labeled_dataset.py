#!/usr/bin/env python3
"""Audita el dataset etiquetado del clasificador E.C.O."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys
from typing import Dict, Iterable, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from src.eco_motif_analysis import scan_sequence  # noqa: E402
from src.eco_sequence_classifier import parse_labeled_sequences_tsv, write_json_report  # noqa: E402

DEFAULT_INPUT = PROJECT_ROOT / "examples" / "eco_labeled_sequences.tsv"
DEFAULT_JSON = PROJECT_ROOT / "results" / "eco_dataset_audit_report.json"
DEFAULT_MD = PROJECT_ROOT / "results" / "eco_dataset_audit_report.md"


def mean(values: Iterable[float]) -> float:
    values = list(values)
    return round(sum(values) / len(values), 4) if values else 0.0


def table(headers: List[str], rows: List[List[object]]) -> List[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return lines


def build_audit(records) -> Dict[str, object]:
    by_label: Dict[str, List[Dict[str, object]]] = defaultdict(list)
    by_split = Counter()
    by_label_split: Dict[str, Counter] = defaultdict(Counter)
    rows: List[Dict[str, object]] = []

    for record in records:
        motif_report = scan_sequence(record.sequence)
        row = {
            "sequence_id": record.sequence_id,
            "label": record.label,
            "split": record.split,
            "length": motif_report.length,
            "gc_percent": motif_report.gc_percent,
            "n_percent": motif_report.n_percent,
            "motif_count": len(motif_report.hits),
            "motifs": [hit.motif_name for hit in motif_report.hits],
        }
        rows.append(row)
        by_label[record.label].append(row)
        by_split[record.split] += 1
        by_label_split[record.label][record.split] += 1

    label_summary = {}
    for label, items in sorted(by_label.items()):
        label_summary[label] = {
            "count": len(items),
            "avg_length": mean(item["length"] for item in items),
            "avg_gc_percent": mean(item["gc_percent"] for item in items),
            "avg_n_percent": mean(item["n_percent"] for item in items),
            "avg_motif_count": mean(item["motif_count"] for item in items),
            "splits": dict(sorted(by_label_split[label].items())),
        }

    warnings = []
    if len(by_label) < 2:
        warnings.append("El dataset tiene menos de dos clases; no sirve para clasificación comparativa.")
    for label, counter in sorted(by_label_split.items()):
        if counter.get("train", 0) == 0:
            warnings.append(f"La clase {label} no tiene ejemplos train.")
        if counter.get("test", 0) == 0:
            warnings.append(f"La clase {label} no tiene ejemplos test.")
    counts = [len(items) for items in by_label.values()]
    if counts and max(counts) > min(counts) * 2:
        warnings.append("Existe posible desbalance fuerte entre clases.")

    return {
        "dataset": str(DEFAULT_INPUT),
        "total_sequences": len(records),
        "labels": dict(sorted(Counter(record.label for record in records).items())),
        "splits": dict(sorted(by_split.items())),
        "label_summary": label_summary,
        "records": rows,
        "warnings": warnings,
        "limits": [
            "Auditoría descriptiva; no evalúa rendimiento del modelo.",
            "Los promedios ayudan a detectar sesgos simples, pero no reemplazan validación externa.",
            "Un dataset equilibrado no garantiza generalización.",
        ],
    }


def build_markdown(audit: Dict[str, object], input_path: Path) -> str:
    label_rows = []
    for label, info in audit["label_summary"].items():
        label_rows.append(
            [
                label,
                info["count"],
                info["splits"].get("train", 0),
                info["splits"].get("test", 0),
                info["avg_length"],
                info["avg_gc_percent"],
                info["avg_motif_count"],
            ]
        )

    record_rows = [
        [
            row["sequence_id"],
            row["label"],
            row["split"],
            row["length"],
            row["gc_percent"],
            row["motif_count"],
            ", ".join(row["motifs"]) if row["motifs"] else "sin motivos",
        ]
        for row in audit["records"]
    ]

    lines = [
        "# E.C.O. - Auditoría del dataset etiquetado",
        "",
        "## Propósito",
        "",
        "Este informe revisa la composición del dataset usado por el clasificador baseline. "
        "Su objetivo es detectar tamaño, balance, distribución por split y señales simples antes de interpretar métricas.",
        "",
        "## Resumen",
        "",
        *table(
            ["Campo", "Valor"],
            [
                ["Dataset", input_path],
                ["Total de secuencias", audit["total_sequences"]],
                ["Clases", ", ".join(audit["labels"].keys())],
                ["Splits", audit["splits"]],
            ],
        ),
        "",
        "## Resumen por clase",
        "",
        *table(["Clase", "Total", "Train", "Test", "Longitud prom.", "GC % prom.", "Motivos prom."], label_rows),
        "",
        "## Alertas de auditoría",
        "",
        *([f"- {warning}" for warning in audit["warnings"]] if audit["warnings"] else ["- Sin alertas críticas de composición."]),
        "",
        "## Detalle por secuencia",
        "",
        *table(["ID", "Clase", "Split", "Longitud", "GC %", "Motivos", "Motivos detectados"], record_rows),
        "",
        "## Límites",
        "",
        *[f"- {limit}" for limit in audit["limits"]],
        "",
        "## Lectura E.C.O.",
        "",
        "La auditoría funciona como una revisión de calidad previa a la evaluación del clasificador. "
        "Si el dataset es pequeño, desbalanceado o demasiado fácil, las métricas pueden verse artificialmente altas.",
        "",
    ]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audita el dataset etiquetado E.C.O.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_MD)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    records = parse_labeled_sequences_tsv(args.input)
    audit = build_audit(records)
    audit["dataset"] = str(args.input)
    write_json_report(audit, args.output_json)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(build_markdown(audit, args.input), encoding="utf-8")

    print("E.C.O. DATASET AUDIT REPORT")
    print("===========================")
    print(f"Dataset: {args.input}")
    print(f"Total: {audit['total_sequences']}")
    print(f"Clases: {audit['labels']}")
    print(f"Splits: {audit['splits']}")
    print(f"Reporte JSON: {args.output_json}")
    print(f"Reporte Markdown: {args.output_md}")
    print("Estado: OK, auditoría del dataset generada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
