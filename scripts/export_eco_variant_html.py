#!/usr/bin/env python3
"""Exporta un reporte JSON de variantes E.C.O. a HTML estático.

Uso esperado:
    make clinvar-sample
    make clinvar-charts
    make clinvar-html

El HTML generado es una vista de lectura para portafolio/demostración. No es
un informe médico y conserva los límites de interpretación del JSON original.
Si existen visualizaciones SVG generadas por `make clinvar-charts`, las integra
automáticamente en el reporte.
"""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path
from typing import Dict, Iterable, List

DEFAULT_INPUT = Path("results/eco_clinvar_sample_report.json")
DEFAULT_OUTPUT = Path("results/eco_clinvar_sample_report.html")
DEFAULT_CHARTS_DIR = Path("results/eco_clinvar_sample_charts")

CATEGORY_LABELS = {
    "alerta_clinica_alta": "Atención alta",
    "incertidumbre_clinica": "Incierto / VUS",
    "probablemente_no_patogenica": "Probablemente no patogénica",
    "evidencia_conflictiva": "Evidencia conflictiva",
    "factor_de_riesgo_no_determinista": "Factor de riesgo",
    "farmacogenomica_o_respuesta_a_farmacos": "Farmacogenómica",
    "clasificacion_no_estandarizada": "No estandarizada",
}

CHART_FILES = [
    ("variants_by_gene.svg", "Variantes por gen"),
    ("categories.svg", "Categorías E.C.O."),
    ("evidence_strength.svg", "Fuerza de evidencia"),
    ("gene_category_matrix.svg", "Matriz gen × categoría"),
]


def e(value: object) -> str:
    return escape(str(value), quote=True)


def shorten(value: object, max_chars: int = 140) -> str:
    text = " ".join(str(value).split())
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "…"


def label_category(category: str) -> str:
    return CATEGORY_LABELS.get(category, category.replace("_", " ").title())


def rows_from_mapping(mapping: Dict[str, int]) -> str:
    if not mapping:
        return "<tr><td colspan='2'>Sin datos</td></tr>"
    return "\n".join(
        f"<tr><td>{e(label_category(key))}</td><td>{e(value)}</td></tr>"
        for key, value in mapping.items()
    )


def gene_rows(gene_counts: Dict[str, int]) -> str:
    if not gene_counts:
        return "<tr><td colspan='2'>Sin datos</td></tr>"
    return "\n".join(f"<tr><td>{e(gene)}</td><td>{e(count)}</td></tr>" for gene, count in gene_counts.items())


def gene_category_matrix(summary: Dict[str, object]) -> str:
    matrix = summary.get("gene_category_matrix", {}) or {}
    category_counts = summary.get("category_counts", {}) or {}
    if not matrix or not category_counts:
        return "<p>Sin matriz gen × categoría disponible.</p>"

    categories = list(category_counts.keys())
    header = "".join(f"<th>{e(label_category(category))}</th>" for category in categories)
    body_rows: List[str] = []
    for gene, by_category in matrix.items():
        values = "".join(f"<td>{e(by_category.get(category, 0))}</td>" for category in categories)
        body_rows.append(f"<tr><th>{e(gene)}</th>{values}</tr>")
    return f"""
    <div class='table-scroll'>
      <table>
        <thead><tr><th>Gen</th>{header}</tr></thead>
        <tbody>{''.join(body_rows)}</tbody>
      </table>
    </div>
    """


def charts_section(output_html: Path, charts_dir: Path) -> str:
    available = [(filename, title) for filename, title in CHART_FILES if (charts_dir / filename).exists()]
    if not available:
        return """
        <section class='section'>
          <h2>Visualizaciones</h2>
          <p class='muted'>No se encontraron gráficos todavía. Ejecuta <code>make clinvar-charts</code> y luego <code>make clinvar-html</code> para integrarlos en esta vista.</p>
        </section>
        """

    cards = []
    for filename, title in available:
        rel_path = (charts_dir / filename).relative_to(output_html.parent)
        cards.append(
            "<article class='chart-card'>"
            f"<h3>{e(title)}</h3>"
            f"<img src='{e(rel_path)}' alt='{e(title)}' loading='lazy'>"
            "</article>"
        )

    index_link = ""
    index_path = charts_dir / "index.html"
    if index_path.exists():
        rel_index = index_path.relative_to(output_html.parent)
        index_link = f"<p><a href='{e(rel_index)}'>Abrir índice completo de visualizaciones</a></p>"

    return f"""
    <section class='section'>
      <h2>Visualizaciones del conjunto</h2>
      <p class='muted'>Gráficos generados desde el JSON del reporte. Ayudan a revisar distribución por gen, categoría y evidencia sin reemplazar la lectura prudente.</p>
      <div class='chart-grid'>{''.join(cards)}</div>
      {index_link}
    </section>
    """


def variant_table(interpretations: Iterable[Dict[str, object]]) -> str:
    rows: List[str] = []
    for item in interpretations:
        variant = item.get("variant", {})
        rows.append(
            "<tr>"
            f"<td>{e(variant.get('variant_id', ''))}</td>"
            f"<td>{e(variant.get('gene', ''))}</td>"
            f"<td>{e(shorten(variant.get('condition', ''), 110))}</td>"
            f"<td>{e(variant.get('clinical_significance', ''))}</td>"
            f"<td><span class='pill'>{e(label_category(str(item.get('category', ''))))}</span></td>"
            f"<td>{e(item.get('evidence_strength', ''))}</td>"
            f"<td>{e(shorten(item.get('recommended_next_step', ''), 120))}</td>"
            "</tr>"
        )
    return "\n".join(rows) if rows else "<tr><td colspan='7'>Sin variantes</td></tr>"


def variant_cards(interpretations: Iterable[Dict[str, object]], limit: int = 8) -> str:
    cards: List[str] = []
    for index, item in enumerate(interpretations):
        if index >= limit:
            break
        variant = item.get("variant", {})
        source_url = variant.get("source_url", "")
        source_link = f"<a href='{e(source_url)}'>Fuente</a>" if source_url else "Sin fuente"
        cards.append(
            "<article class='card'>"
            f"<h3>{e(variant.get('gene', 'Gen no informado'))} · {e(shorten(variant.get('variant_name', ''), 90))}</h3>"
            f"<p><strong>ID:</strong> {e(variant.get('variant_id', ''))} · <strong>Categoría:</strong> {e(label_category(str(item.get('category', ''))))}</p>"
            f"<p><strong>Evidencia:</strong> {e(item.get('evidence_strength', ''))} · <strong>Clasificación externa:</strong> {e(variant.get('clinical_significance', ''))}</p>"
            f"<p>{e(shorten(item.get('practical_reading', ''), 260))}</p>"
            f"<p>{source_link}</p>"
            "</article>"
        )
    return "\n".join(cards) if cards else "<p>Sin detalle de variantes.</p>"


def build_html(report: Dict[str, object], output_html: Path = DEFAULT_OUTPUT, charts_dir: Path = DEFAULT_CHARTS_DIR) -> str:
    summary = report.get("summary", {})
    interpretations = report.get("interpretations", [])
    source = report.get("source", {})
    limits = report.get("limits", [])

    return f"""<!doctype html>
<html lang='es'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>Informe E.C.O. de variantes</title>
  <style>
    body {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; background: #f6f7fb; color: #172033; }}
    header {{ background: #172033; color: white; padding: 2rem; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 1.5rem; }}
    h1, h2, h3 {{ line-height: 1.2; }}
    .subtitle {{ color: #d8e0ff; max-width: 850px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }}
    .chart-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1rem; }}
    .metric, .section, .card, .chart-card {{ background: white; border-radius: 16px; padding: 1rem; box-shadow: 0 8px 24px rgba(23, 32, 51, 0.08); }}
    .chart-card img {{ width: 100%; height: auto; display: block; border-radius: 12px; border: 1px solid #e6e8f0; }}
    .metric strong {{ display: block; font-size: 1.8rem; margin-bottom: .2rem; }}
    table {{ width: 100%; border-collapse: collapse; background: white; }}
    th, td {{ text-align: left; padding: .7rem; border-bottom: 1px solid #e6e8f0; vertical-align: top; }}
    th {{ background: #eef1f8; }}
    .table-scroll {{ overflow-x: auto; }}
    .pill {{ display: inline-block; border-radius: 999px; padding: .2rem .55rem; background: #eef1f8; font-size: .9rem; }}
    .warning {{ border-left: 6px solid #9b6b00; }}
    .muted {{ color: #5f6b80; }}
    code {{ background: #eef1f8; border-radius: 6px; padding: .1rem .35rem; }}
    a {{ color: #2346a0; }}
  </style>
</head>
<body>
  <header>
    <h1>Informe E.C.O. de interpretación segura de variantes</h1>
    <p class='subtitle'>Vista HTML estática generada desde JSON. Uso educativo y bioinformático; no interpreta pacientes ni reemplaza evaluación profesional.</p>
  </header>
  <main>
    <section class='grid'>
      <div class='metric'><strong>{e(summary.get('variants_processed', 0))}</strong><span>Variantes procesadas</span></div>
      <div class='metric'><strong>{e(len(summary.get('gene_counts', {}) or {}))}</strong><span>Genes representados</span></div>
      <div class='metric'><strong>{e(len(summary.get('category_counts', {}) or {}))}</strong><span>Categorías E.C.O.</span></div>
      <div class='metric'><strong>{e(source.get('sampling', 'demo/local'))}</strong><span>Muestreo</span></div>
    </section>

    {charts_section(output_html, charts_dir)}

    <section class='section'>
      <h2>Resumen por categoría</h2>
      <table><tbody>{rows_from_mapping(summary.get('category_counts', {}) or {})}</tbody></table>
    </section>

    <section class='section'>
      <h2>Resumen por gen</h2>
      <table><tbody>{gene_rows(summary.get('gene_counts', {}) or {})}</tbody></table>
      <h3>Matriz gen × categoría</h3>
      {gene_category_matrix(summary)}
    </section>

    <section class='section'>
      <h2>Resumen ejecutivo de variantes</h2>
      <div class='table-scroll'>
        <table>
          <thead><tr><th>ID</th><th>Gen</th><th>Condición</th><th>Clasificación externa</th><th>Categoría E.C.O.</th><th>Evidencia</th><th>Acción prudente</th></tr></thead>
          <tbody>{variant_table(interpretations)}</tbody>
        </table>
      </div>
    </section>

    <section class='section'>
      <h2>Lectura detallada breve</h2>
      <div class='grid'>{variant_cards(interpretations)}</div>
      <p class='muted'>Se muestran las primeras variantes para mantener el HTML legible. El JSON conserva el detalle estructurado completo.</p>
    </section>

    <section class='section warning'>
      <h2>Límites de uso</h2>
      <ul>{''.join(f'<li>{e(limit)}</li>' for limit in limits)}</ul>
      <p>Este reporte organiza evidencia pública o demostrativa. No calcula riesgo personal absoluto, no confirma enfermedad y no reemplaza evaluación profesional.</p>
    </section>
  </main>
</body>
</html>
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Exporta un reporte JSON de variantes E.C.O. a HTML estático.")
    parser.add_argument("--input-json", type=Path, default=DEFAULT_INPUT, help="Reporte JSON de variantes E.C.O.")
    parser.add_argument("--output-html", type=Path, default=DEFAULT_OUTPUT, help="Ruta del HTML generado.")
    parser.add_argument("--charts-dir", type=Path, default=DEFAULT_CHARTS_DIR, help="Directorio con SVG generados por make clinvar-charts.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.input_json.exists():
        parser.exit(status=1, message=f"Error: no existe {args.input_json}. Ejecuta make clinvar-sample primero.\n")

    report = json.loads(args.input_json.read_text(encoding="utf-8"))
    html = build_html(report, output_html=args.output_html, charts_dir=args.charts_dir)
    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.write_text(html, encoding="utf-8")

    print("E.C.O. VARIANT HTML EXPORT")
    print("==========================")
    print(f"Entrada JSON: {args.input_json}")
    print(f"Salida HTML: {args.output_html}")
    print(f"Gráficos: {args.charts_dir if args.charts_dir.exists() else 'no encontrados'}")
    print("Estado: OK, reporte HTML estático generado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
