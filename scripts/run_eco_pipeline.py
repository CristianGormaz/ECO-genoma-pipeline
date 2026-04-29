#!/usr/bin/env python3
"""
Pipeline parametrizable E.C.O.
=============================

Permite ejecutar E.C.O. con archivos propios:

BED + FASTA de referencia -> FASTA extraído -> JSON integrado -> Markdown

Ejemplo:

    python3 scripts/run_eco_pipeline.py \
      --bed mi_archivo.bed \
      --reference mi_referencia.fa \
      --output-dir results \
      --prefix mi_analisis
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from export_eco_demo_markdown import build_markdown  # noqa: E402
from run_eco_demo_pipeline import run_demo_pipeline  # noqa: E402


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Ejecuta E.C.O. con un BED propio y un FASTA de referencia propio. "
            "Genera FASTA, JSON integrado y reporte Markdown."
        )
    )
    parser.add_argument(
        "--bed",
        type=Path,
        required=True,
        help="Archivo BED de entrada con coordenadas genómicas.",
    )
    parser.add_argument(
        "--reference",
        type=Path,
        required=True,
        help="Archivo FASTA de referencia compatible con las coordenadas BED.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "results",
        help="Carpeta donde guardar resultados. Por defecto: results/.",
    )
    parser.add_argument(
        "--prefix",
        default="eco_custom_pipeline",
        help="Prefijo para los archivos generados. Por defecto: eco_custom_pipeline.",
    )
    return parser


def print_pipeline_summary(report: dict, markdown_path: Path) -> None:
    """Imprime una salida breve para usuarios que ejecutan archivos propios."""
    feedback = report["summary"]["feedback"]

    print("E.C.O. PARAMETRIZABLE PIPELINE REPORT")
    print("=====================================")
    print("Flujo: BED propio -> FASTA -> eco_core -> análisis de motivos -> JSON/Markdown")
    print(f"Regiones procesadas: {report['summary']['regions_processed']}")
    print(f"Motivos encontrados: {report['summary']['total_motif_hits']}")
    print(f"Aceptados: {feedback['accepted_packets']}")
    print(f"Rechazados: {feedback['rejected_packets']}")
    print(f"Absorbidos: {feedback['absorbed_packets']}")
    print(f"Tasa de rechazo: {feedback['rejection_rate']}%")
    print(f"FASTA generado: {report['outputs']['fasta']}")
    print(f"Reporte JSON: {report['outputs']['json']}")
    print(f"Reporte Markdown: {markdown_path}")

    if feedback["rejected_packets"] == 0 and feedback["absorbed_packets"] == report["summary"]["regions_processed"]:
        print("Estado: OK, pipeline parametrizable E.C.O. funcionando.")
    else:
        print("Estado: REVISAR, hubo rechazos o absorción incompleta.")


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    output_dir = args.output_dir
    output_fasta = output_dir / f"{args.prefix}.fa"
    output_json = output_dir / f"{args.prefix}_report.json"
    output_markdown = output_dir / f"{args.prefix}_report.md"

    try:
        report = run_demo_pipeline(
            bed_path=args.bed,
            reference_path=args.reference,
            output_fasta=output_fasta,
            output_json=output_json,
        )
        markdown = build_markdown(report)
        output_markdown.parent.mkdir(parents=True, exist_ok=True)
        output_markdown.write_text(markdown, encoding="utf-8")

        report["outputs"]["markdown"] = str(output_markdown)
        print_pipeline_summary(report, output_markdown)

        feedback = report["summary"]["feedback"]
        return 0 if feedback["rejected_packets"] == 0 else 1
    except (FileNotFoundError, ValueError, KeyError) as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
