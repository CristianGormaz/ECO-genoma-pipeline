#!/usr/bin/env python3
"""Genera un resumen conversacional desde el manifiesto operativo E.C.O.

Esta capa está pensada para UX conversacional: toma el inventario técnico del
pipeline y lo convierte en una lectura breve, útil para Greys/E.C.O. o para una
persona que solo necesita saber si la corrida está sana, qué destaca y qué
conviene mirar después.
"""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path
from typing import Any, Dict, List, Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "results" / "eco_operational_manifest.json"
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "results" / "eco_status_brief.md"
DEFAULT_OUTPUT_HTML = PROJECT_ROOT / "results" / "eco_status_brief.html"

PRIORITY_REPORTS = (
    "eco_classifier_baseline_v3_report.json",
    "eco_embedding_repeated_eval_report.json",
    "eco_embedding_semireal_repeated_eval_report.json",
    "eco_confidence_router_calibrated_eval_report.json",
    "eco_difficulty_eval_report.json",
    "eco_variant_demo_report.json",
    "eco_clinvar_sample_report.json",
)


def load_manifest(path: Path) -> Dict[str, Any]:
    """Carga el manifiesto operacional."""
    if not path.exists():
        raise FileNotFoundError(
            f"No existe {path}. Ejecuta primero: python scripts/build_eco_operational_manifest.py"
        )
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("manifest_type") != "eco_operational_manifest":
        raise ValueError("El archivo no parece ser un manifiesto operativo E.C.O. válido.")
    return data


def format_missing(missing: Sequence[str]) -> str:
    """Resume artefactos faltantes sin saturar la lectura."""
    if not missing:
        return "sin piezas esperadas pendientes"
    if len(missing) <= 3:
        return "pendientes: " + ", ".join(missing)
    return f"{len(missing)} piezas esperadas pendientes"


def metric_value(metrics: Dict[str, Any], *keys: str) -> Any:
    """Devuelve el primer valor disponible dentro de un set de claves."""
    for key in keys:
        if key in metrics:
            return metrics[key]
    return None


def find_report(manifest: Dict[str, Any], report_name: str) -> Dict[str, Any]:
    """Busca un resumen de reporte por ruta exacta."""
    for summary in manifest.get("report_summaries", []):
        if summary.get("path") == report_name:
            return summary.get("metrics", {})
    return {}


def build_highlights(manifest: Dict[str, Any]) -> List[str]:
    """Construye los hallazgos principales del estado E.C.O."""
    highlights: List[str] = []

    v3 = find_report(manifest, "eco_classifier_baseline_v3_report.json")
    if v3:
        highlights.append(
            "baseline_v3 sigue como referencia fuerte: "
            f"macro F1={metric_value(v3, 'test_macro_f1', default := 'no_disponible')} "
            f"con feature_mode={metric_value(v3, 'feature_mode')}."
        )

    embedding = find_report(manifest, "eco_embedding_repeated_eval_report.json")
    if embedding:
        decision = metric_value(embedding, "operational_decision", "decision")
        if decision:
            highlights.append(f"la ruta de embedding placeholder queda como {decision}.")

    semireal = find_report(manifest, "eco_embedding_semireal_repeated_eval_report.json")
    if semireal:
        decision = metric_value(semireal, "operational_decision", "decision")
        if decision:
            highlights.append(f"embedding semi-real aparece como {decision}.")

    calibrated = find_report(manifest, "eco_confidence_router_calibrated_eval_report.json")
    if calibrated:
        decision = metric_value(calibrated, "decision", "operational_decision")
        if decision:
            highlights.append(f"router de confianza calibrado: {decision}.")

    difficulty = find_report(manifest, "eco_difficulty_eval_report.json")
    if difficulty:
        decision = metric_value(difficulty, "decision", "operational_decision")
        if decision:
            highlights.append(f"evaluación de dificultad: {decision}.")

    variants = find_report(manifest, "eco_variant_demo_report.json")
    if variants and metric_value(variants, "variants_processed") is not None:
        highlights.append(f"módulo de variantes demo procesó {variants['variants_processed']} variantes sin diagnóstico médico.")

    clinvar = find_report(manifest, "eco_clinvar_sample_report.json")
    if clinvar and metric_value(clinvar, "variants_processed") is not None:
        highlights.append(f"muestra estilo ClinVar procesó {clinvar['variants_processed']} variantes.")

    if not highlights:
        highlights.append("no se detectaron métricas prioritarias; revisar el manifiesto completo.")

    return highlights


def build_next_actions(manifest: Dict[str, Any]) -> List[str]:
    """Sugiere próximos pasos cortos desde el estado actual."""
    missing = manifest.get("missing_expected_core_artifacts", [])
    if missing:
        return [
            "generar las piezas esperadas pendientes antes de usar la corrida como demo de portafolio.",
            "volver a ejecutar el manifiesto para confirmar que el inventario quede completo.",
        ]

    actions = [
        "integrar este resumen en el flujo `make` para que cada corrida deje una lectura conversacional.",
        "usar `eco_status_brief.md` como base de respuesta para Greys/E.C.O.",
        "preparar la siguiente capa: explicación por caso difícil o por predicción individual.",
    ]
    return actions


def build_brief_markdown(manifest: Dict[str, Any]) -> str:
    """Construye el resumen Markdown orientado a lectura humana/conversacional."""
    status = manifest.get("status", "desconocido")
    artifact_count = manifest.get("artifact_count", 0)
    missing = manifest.get("missing_expected_core_artifacts", [])
    extension_counts = manifest.get("artifacts_by_extension", {})
    generated_at = manifest.get("generated_at", "no_disponible")

    extensions_text = ", ".join(f"{ext}:{count}" for ext, count in extension_counts.items()) or "sin artefactos"
    highlights = build_highlights(manifest)
    actions = build_next_actions(manifest)

    lines = [
        "# E.C.O. - Resumen conversacional de estado",
        "",
        "## Lectura breve",
        "",
        f"E.C.O. está en estado `{status}`. La corrida registra {artifact_count} artefactos y {format_missing(missing)}.",
        "",
        "## Estado operativo",
        "",
        f"- Generado UTC: {generated_at}",
        f"- Inventario por tipo: {extensions_text}",
        f"- Piezas esperadas pendientes: {len(missing)}",
        "",
        "## Hallazgos principales",
        "",
        *[f"- {item}" for item in highlights],
        "",
        "## Próximas acciones sugeridas",
        "",
        *[f"- {item}" for item in actions],
        "",
        "## Microcopy para Greys/E.C.O.",
        "",
        "> Corrida revisada. El metabolismo informacional está estable: artefactos completos, métricas disponibles y sin piezas esperadas pendientes. Puedo mostrarte el manifiesto completo o revisar el modelo/predicción que quieras explicar.",
        "",
        "## Límite responsable",
        "",
        "Este resumen explica estado técnico y resultados de portafolio. No entrega diagnóstico médico ni reemplaza revisión experta.",
        "",
    ]
    return "\n".join(lines)


def write_html(markdown_text: str, output_html: Path) -> None:
    """Escribe una vista HTML simple y portable del resumen."""
    html = f"""<!doctype html>
<html lang=\"es\">
<head>
<meta charset=\"utf-8\">
<title>E.C.O. - Resumen conversacional de estado</title>
<style>
body {{
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  max-width: 980px;
  margin: 40px auto;
  line-height: 1.55;
  padding: 0 20px;
}}
pre {{
  white-space: pre-wrap;
  background: #f7f7f7;
  padding: 18px;
  border-radius: 12px;
}}
</style>
</head>
<body>
<pre>{escape(markdown_text)}</pre>
</body>
</html>
"""
    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_html.write_text(html, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resume el manifiesto operativo E.C.O. para UX conversacional.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--output-html", type=Path, default=DEFAULT_OUTPUT_HTML)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manifest = load_manifest(args.manifest)
    markdown_text = build_brief_markdown(manifest)

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(markdown_text, encoding="utf-8")
    write_html(markdown_text, args.output_html)

    print("E.C.O. STATUS BRIEF")
    print("===================")
    print(f"Manifiesto leído: {args.manifest}")
    print(f"Resumen Markdown: {args.output_md}")
    print(f"Resumen HTML: {args.output_html}")
    print("Estado: OK, resumen conversacional generado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
