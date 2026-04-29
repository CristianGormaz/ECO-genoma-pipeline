#!/usr/bin/env python3
"""
Exportador Markdown del reporte integrado E.C.O.
===============================================

Convierte el JSON generado por scripts/run_eco_demo_pipeline.py en un reporte
Markdown legible para GitHub, portafolio o documentación técnica.

Uso recomendado desde la raíz del repositorio:

    python3 scripts/export_eco_demo_markdown.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict, Iterable, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PROJECT_ROOT / "results" / "eco_demo_pipeline_report.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "results" / "eco_demo_pipeline_report.md"


def load_report(path: Path) -> Dict[str, Any]:
    """Carga el JSON integrado generado por la demo E.C.O."""
    if not path.exists():
        raise FileNotFoundError(
            f"No existe el reporte JSON: {path}. Ejecuta primero: make demo"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def escape_md(value: Any) -> str:
    """Escapa valores para usarlos en tablas Markdown simples."""
    text = str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def motif_names(sequence_entry: Dict[str, Any]) -> str:
    """Devuelve nombres de motivos encontrados para una región."""
    motif_report = sequence_entry.get("motif_report") or {}
    hits = motif_report.get("hits") or []
    if not hits:
        return "sin motivos"
    return ", ".join(hit.get("motif_name", "motivo_desconocido") for hit in hits)


def history_summary(sequence_entry: Dict[str, Any]) -> str:
    """Resume el historial de etapas de una región."""
    history = sequence_entry.get("history", [])
    if not history:
        return "sin historial"
    return " → ".join(f"{item['stage']}:{item['status']}" for item in history)


def table(headers: List[str], rows: Iterable[List[Any]]) -> List[str]:
    """Construye una tabla Markdown."""
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(escape_md(value) for value in row) + " |")
    return lines


def build_markdown(report: Dict[str, Any]) -> str:
    """Construye el reporte Markdown final."""
    summary = report["summary"]
    feedback = summary["feedback"]
    sequences = report["sequences"]

    status_ok = (
        feedback["rejected_packets"] == 0
        and feedback["absorbed_packets"] == summary["regions_processed"]
    )
    status_text = (
        "OK: digestión informacional completa y sin rechazos."
        if status_ok
        else "REVISAR: hay rechazos o absorción incompleta."
    )

    lines: List[str] = [
        "# Reporte demo E.C.O.",
        "",
        "Este reporte resume el primer recorrido integrado del sistema E.C.O.:",
        "",
        "```text",
        "BED → FASTA → eco_core → análisis de motivos → reporte integrado",
        "```",
        "",
        "## Resumen ejecutivo",
        "",
        *table(
            ["Métrica", "Valor"],
            [
                ["Regiones procesadas", summary["regions_processed"]],
                ["Motivos encontrados", summary["total_motif_hits"]],
                ["Paquetes aceptados", feedback["accepted_packets"]],
                ["Paquetes rechazados", feedback["rejected_packets"]],
                ["Paquetes absorbidos", feedback["absorbed_packets"]],
                ["Tasa de rechazo", f"{feedback['rejection_rate']}%"],
                ["Tasa de absorción", f"{feedback['absorbed_rate']}%"],
            ],
        ),
        "",
        "## Entradas y salidas",
        "",
        *table(
            ["Tipo", "Ruta"],
            [
                ["BED de entrada", report["inputs"]["bed"]],
                ["FASTA de referencia", report["inputs"]["reference"]],
                ["FASTA generado", report["outputs"]["fasta"]],
                ["JSON integrado", report["outputs"]["json"]],
            ],
        ),
        "",
        "## Detalle por región",
        "",
        *table(
            ["Región", "Historial", "Longitud", "GC", "N ambiguas", "Motivos"],
            [
                [
                    entry["sequence_id"],
                    history_summary(entry),
                    f"{entry.get('metadata', {}).get('absorbed_features', {}).get('length', 'n/a')} bp",
                    f"{entry.get('metadata', {}).get('absorbed_features', {}).get('gc_percent', 'n/a')}%",
                    f"{entry.get('metadata', {}).get('absorbed_features', {}).get('n_percent', 'n/a')}%",
                    motif_names(entry),
                ]
                for entry in sequences
            ],
        ),
        "",
        "## Lectura final",
        "",
        status_text,
        "",
        "## Nota metodológica",
        "",
        "Esta demo usa archivos pequeños incluidos en `examples/`. Sirve para validar el flujo técnico y la trazabilidad del prototipo, no para obtener conclusiones biológicas reales.",
        "",
    ]

    return "\n".join(lines)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Exporta el reporte integrado E.C.O. desde JSON a Markdown."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Ruta al JSON integrado. Por defecto usa results/eco_demo_pipeline_report.json.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Ruta de salida Markdown. Por defecto usa results/eco_demo_pipeline_report.md.",
    )
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    try:
        report = load_report(args.input)
        markdown = build_markdown(report)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
        print(f"Reporte Markdown generado: {args.output}")
        return 0
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
