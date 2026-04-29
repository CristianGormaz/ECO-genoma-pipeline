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

CATEGORY_TITLES = {
    "alerta_clinica_alta": "Hallazgos de atención alta",
    "incertidumbre_clinica": "Hallazgos inciertos",
    "probablemente_no_patogenica": "Hallazgos probablemente no patogénicos",
    "evidencia_conflictiva": "Hallazgos con evidencia conflictiva",
    "factor_de_riesgo_no_determinista": "Hallazgos de riesgo no determinista",
    "farmacogenomica_o_respuesta_a_farmacos": "Hallazgos farmacogenómicos",
    "clasificacion_no_estandarizada": "Hallazgos con clasificación no estandarizada",
}

CATEGORY_EXPLANATIONS = {
    "alerta_clinica_alta": (
        "La fuente externa declara variantes patogénicas o probablemente patogénicas. "
        "En una muestra real, estos registros merecen revisión clínica, pero no equivalen por sí solos a diagnóstico personal."
    ),
    "incertidumbre_clinica": (
        "Agrupa variantes de significado incierto. Una VUS no debe usarse sola para decidir tratamientos, cirugías o conductas médicas."
    ),
    "probablemente_no_patogenica": (
        "Incluye variantes benignas o probablemente benignas para la condición indicada. Esto no descarta otros riesgos genéticos no analizados."
    ),
    "evidencia_conflictiva": (
        "Indica desacuerdo entre submitters, criterios o interpretaciones. El resultado debe tratarse como zona de revisión manual."
    ),
    "factor_de_riesgo_no_determinista": (
        "Señala asociaciones o factores de riesgo. No significa enfermedad asegurada; depende de penetrancia, ambiente y otros factores."
    ),
    "farmacogenomica_o_respuesta_a_farmacos": (
        "Relaciona variantes con posible respuesta a medicamentos. No debe cambiarse ningún tratamiento sin evaluación profesional."
    ),
    "clasificacion_no_estandarizada": (
        "Contiene etiquetas que E.C.O. todavía no normaliza con precisión. Son candidatos para mejorar el diccionario de interpretación."
    ),
}

EVIDENCE_EXPLANATIONS = {
    "muy_alta": "La fuente indica guía práctica o respaldo especialmente fuerte.",
    "alta": "La fuente indica revisión por panel experto u otro respaldo sólido.",
    "moderada": "Hay criterios y múltiples aportes sin conflicto declarado, o respaldo razonable.",
    "limitada": "La clasificación depende de evidencia más acotada, por ejemplo un solo submitter con criterios.",
    "conflictiva": "Existen discrepancias declaradas; no conviene cerrar conclusión sin revisión manual.",
    "baja_o_no_informada": "La fuente no entrega criterios suficientes o no informa clasificación robusta.",
    "no_determinada": "E.C.O. no pudo mapear el estado de revisión a una fuerza clara.",
}


def table(headers: List[str], rows: List[List[object]]) -> List[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        safe = [str(value).replace("|", "\\|").replace("\n", " ") for value in row]
        lines.append("| " + " | ".join(safe) + " |")
    return lines


def category_title(category: str) -> str:
    return CATEGORY_TITLES.get(category, category.replace("_", " ").capitalize())


def category_explanation(category: str) -> str:
    return CATEGORY_EXPLANATIONS.get(
        category,
        "Categoría no reconocida por el diccionario actual de E.C.O.; requiere revisión manual.",
    )


def evidence_explanation(evidence: str) -> str:
    return EVIDENCE_EXPLANATIONS.get(
        evidence,
        "Nivel de evidencia no reconocido por el diccionario actual de E.C.O.",
    )


def build_grouped_category_sections(interpretations: List[Dict[str, object]]) -> List[str]:
    grouped: Dict[str, List[Dict[str, object]]] = {}
    for item in interpretations:
        grouped.setdefault(str(item["category"]), []).append(item)

    sections: List[str] = []
    for category, items in grouped.items():
        rows = []
        for item in items[:5]:
            variant = item["variant"]
            rows.append(
                [
                    variant["variant_id"],
                    variant["gene"],
                    variant["clinical_significance"],
                    item["evidence_strength"],
                    item["recommended_next_step"],
                ]
            )
        sections.extend(
            [
                f"### {category_title(category)}",
                "",
                category_explanation(category),
                "",
                *table(["ID", "Gen", "Clasificación externa", "Evidencia", "Acción prudente"], rows),
                "",
            ]
        )
    return sections


def build_evidence_quality_section(summary: Dict[str, object]) -> List[str]:
    evidence_counts = summary["evidence_strength_counts"]
    rows = [[key, value, evidence_explanation(key)] for key, value in evidence_counts.items()]
    return [
        "### Calidad global de evidencia",
        "",
        "Esta sección resume qué tan sólido parece el respaldo declarado por la fuente externa. "
        "No mide certeza personal; mide fuerza de revisión del registro.",
        "",
        *table(["Nivel", "Cantidad", "Lectura E.C.O."], rows),
        "",
    ]


def build_cautious_set_reading(report: Dict[str, object]) -> List[str]:
    summary = report["summary"]
    interpretations = report["interpretations"]
    category_counts = summary["category_counts"]

    lines: List[str] = [
        "## 5. Lectura clínica prudente del conjunto",
        "",
        "Esta lectura resume el conjunto analizado como si fuera un informe de apoyo interpretativo. "
        "No transforma los datos en diagnóstico: ordena señales, evidencia y límites.",
        "",
        *table(
            ["Grupo interpretativo", "Cantidad", "Qué significa"],
            [
                [category_title(key), value, category_explanation(key)]
                for key, value in category_counts.items()
            ],
        ),
        "",
        *build_grouped_category_sections(interpretations),
        *build_evidence_quality_section(summary),
        "### Qué NO se puede concluir",
        "",
        "- No se puede concluir que una persona tenga una enfermedad solo porque una variante pública esté clasificada como patogénica.",
        "- No se puede calcular riesgo absoluto personal sin genotipo real, zigosidad, contexto clínico y antecedentes familiares.",
        "- No se puede usar una VUS como base única para decisiones médicas.",
        "- No se puede asumir que una variante benigna descarta todo riesgo genético.",
        "- No se puede cambiar medicación por hallazgos farmacogenómicos sin evaluación profesional.",
        "",
    ]
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
        *build_cautious_set_reading(report),
        "## 6. Lectura detallada por variante",
        "",
        *detailed_sections,
        "## 7. Límites científicos y clínicos",
        "",
        "- Este reporte interpreta registros de variantes, no interpreta a una persona.",
        "- No incorpora zigosidad, edad, sexo, etnia, historia familiar, síntomas, laboratorio, penetrancia ni consentimiento clínico.",
        "- Una variante patogénica en una base pública no equivale automáticamente a enfermedad en una persona concreta.",
        "- Una VUS no debe guiar decisiones médicas por sí sola.",
        "- Una clasificación benigna no descarta otros riesgos no analizados.",
        "- Toda conclusión clínica requiere validación profesional y fuente actualizada.",
        "",
        "## 8. Próximo salto empírico",
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
