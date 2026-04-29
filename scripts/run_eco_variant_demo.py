#!/usr/bin/env python3
"""Demo E.C.O. para interpretación segura de variantes.

Lee un TSV reducido estilo ClinVar, clasifica significado clínico declarado por
la fuente y genera reportes JSON/Markdown. No diagnostica ni calcula riesgo
personal.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from src.eco_variant_interpretation import build_report, parse_variant_tsv, write_json_report  # noqa: E402

DEFAULT_INPUT = PROJECT_ROOT / "examples" / "clinvar_style_demo_variants.tsv"
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "results" / "eco_variant_demo_report.json"
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "results" / "eco_variant_demo_report.md"


def table(headers: List[str], rows: List[List[object]]) -> List[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        safe = [str(value).replace("|", "\\|").replace("\n", " ") for value in row]
        lines.append("| " + " | ".join(safe) + " |")
    return lines


def build_markdown(report: Dict[str, object], input_path: Path) -> str:
    summary = report["summary"]
    interpretations = report["interpretations"]

    rows = []
    for item in interpretations:
        variant = item["variant"]
        rows.append(
            [
                variant["variant_id"],
                variant["gene"],
                variant["condition"],
                variant["clinical_significance"],
                item["category"],
                item["evidence_strength"],
                item["recommended_next_step"],
            ]
        )

    detailed_sections: List[str] = []
    for index, item in enumerate(interpretations, start=1):
        variant = item["variant"]
        detailed_sections.extend(
            [
                f"### {index}. {variant['gene']} — {variant['variant_name']}",
                "",
                *table(
                    ["Campo", "Valor"],
                    [
                        ["ID", variant["variant_id"]],
                        ["HGVS", variant["hgvs"]],
                        ["Condición asociada", variant["condition"]],
                        ["Significado clínico declarado", variant["clinical_significance"]],
                        ["Estado de revisión", variant["review_status"]],
                        ["Categoría E.C.O.", item["category"]],
                        ["Fuerza de evidencia", item["evidence_strength"]],
                    ],
                ),
                "",
                f"**Lectura práctica:** {item['practical_reading']}",
                "",
                f"**Siguiente paso recomendado:** {item['recommended_next_step']}",
                "",
            ]
        )

    lines: List[str] = [
        "# Informe E.C.O. de interpretación segura de variantes",
        "",
        "## 1. Propósito",
        "",
        "Este informe muestra cómo E.C.O. puede transformar registros de variantes en una lectura explicativa, trazable y prudente. "
        "La estructura se inspira en informes clínicos, pero el resultado es bioinformático/educativo y no diagnóstico.",
        "",
        "## 2. Identificación del análisis",
        "",
        *table(
            ["Campo", "Valor"],
            [
                ["Entrada", input_path],
                ["Tipo de datos", "TSV reducido estilo ClinVar"],
                ["Variantes procesadas", summary["variants_processed"]],
                ["Estado diagnóstico", summary["diagnostic_status"]],
            ],
        ),
        "",
        "## 3. Resumen por categoría",
        "",
        *table(["Categoría E.C.O.", "Cantidad"], [[key, value] for key, value in summary["category_counts"].items()]),
        "",
        "## 4. Resumen ejecutivo de variantes",
        "",
        *table(
            ["ID", "Gen", "Condición", "Clasificación externa", "Categoría E.C.O.", "Evidencia", "Acción prudente"],
            rows,
        ),
        "",
        "## 5. Lectura detallada",
        "",
        *detailed_sections,
        "## 6. Límites científicos y clínicos",
        "",
        "- Este reporte interpreta registros de variantes, no interpreta a una persona.",
        "- No incorpora zigosidad, edad, sexo, etnia, historia familiar, síntomas, laboratorio, penetrancia ni consentimiento clínico.",
        "- Una variante patogénica en una base pública no equivale automáticamente a enfermedad en una persona concreta.",
        "- Una VUS no debe guiar decisiones médicas por sí sola.",
        "- Una clasificación benigna no descarta otros riesgos no analizados.",
        "- Toda conclusión clínica requiere validación profesional y fuente actualizada.",
        "",
        "## 7. Próximo salto empírico",
        "",
        "Conectar este módulo a una descarga real y reducida desde ClinVar/NCBI para generar un informe reproducible con fuente externa actualizada. "
        "Ese paso debe mantener los mismos límites: investigación, educación y apoyo interpretativo, no diagnóstico médico.",
        "",
    ]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Genera un informe E.C.O. seguro de interpretación de variantes.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="TSV de variantes estilo ClinVar.")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON, help="Ruta del reporte JSON.")
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD, help="Ruta del reporte Markdown.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    records = parse_variant_tsv(args.input)
    if not records:
        parser.exit(status=1, message="Error: no se encontraron variantes en la entrada.\n")

    report = build_report(records)
    write_json_report(report, args.output_json)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(build_markdown(report, args.input), encoding="utf-8")

    summary = report["summary"]
    print("E.C.O. VARIANT INTERPRETATION DEMO")
    print("==================================")
    print(f"Entrada: {args.input}")
    print(f"Variantes procesadas: {summary['variants_processed']}")
    print(f"Categorías: {summary['category_counts']}")
    print(f"Evidencia: {summary['evidence_strength_counts']}")
    print(f"Reporte JSON: {args.output_json}")
    print(f"Reporte Markdown: {args.output_md}")
    print("Estado: OK, interpretación de variantes generada sin diagnóstico médico.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
