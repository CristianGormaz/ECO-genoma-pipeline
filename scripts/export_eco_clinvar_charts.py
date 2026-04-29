#!/usr/bin/env python3
"""Exporta visualizaciones SVG simples desde el reporte JSON ClinVar de E.C.O.

No usa dependencias externas. La intención es mantener una salida portable,
reproducible y adecuada para portafolio.
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Iterable, List, Mapping, Tuple

DEFAULT_INPUT = Path("results/eco_clinvar_sample_report.json")
DEFAULT_OUTPUT_DIR = Path("results/eco_clinvar_sample_charts")

CATEGORY_LABELS = {
    "alerta_clinica_alta": "Atención alta",
    "incertidumbre_clinica": "Inciertos / VUS",
    "probablemente_no_patogenica": "Probablemente no patogénicos",
    "evidencia_conflictiva": "Evidencia conflictiva",
    "farmacogenomica_o_respuesta_a_farmacos": "Farmacogenómica",
    "factor_de_riesgo_no_determinista": "Riesgo no determinista",
    "clasificacion_no_estandarizada": "No estandarizada",
}

EVIDENCE_LABELS = {
    "muy_alta": "Muy alta",
    "alta": "Alta",
    "moderada": "Moderada",
    "limitada": "Limitada",
    "conflictiva": "Conflictiva",
    "baja_o_no_informada": "Baja / no informada",
}

PALETTE = [
    "#4f46e5",
    "#0891b2",
    "#059669",
    "#ca8a04",
    "#dc2626",
    "#7c3aed",
    "#475569",
]


def load_report(path: Path) -> Mapping[str, object]:
    if not path.exists():
        raise FileNotFoundError(
            f"No existe el reporte JSON: {path}. Ejecuta primero: make clinvar-sample"
        )
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def label_for(key: str, labels: Mapping[str, str]) -> str:
    return labels.get(key, key.replace("_", " "))


def sorted_items(counts: Mapping[str, int], preferred_order: Iterable[str] | None = None) -> List[Tuple[str, int]]:
    if preferred_order:
        ordered = [(key, int(counts[key])) for key in preferred_order if key in counts]
        ordered_keys = {key for key, _ in ordered}
        rest = sorted(
            ((key, int(value)) for key, value in counts.items() if key not in ordered_keys),
            key=lambda item: item[0],
        )
        return ordered + rest
    return sorted(((key, int(value)) for key, value in counts.items()), key=lambda item: item[0])


def write_svg_bar_chart(
    path: Path,
    title: str,
    counts: Mapping[str, int],
    labels: Mapping[str, str] | None = None,
    preferred_order: Iterable[str] | None = None,
) -> None:
    labels = labels or {}
    items = sorted_items(counts, preferred_order)
    width = 980
    row_height = 44
    top = 86
    left = 280
    bar_max_width = 560
    height = top + max(1, len(items)) * row_height + 48
    max_value = max([value for _, value in items] or [1])

    rows = []
    for idx, (key, value) in enumerate(items):
        y = top + idx * row_height
        bar_width = int((value / max_value) * bar_max_width) if max_value else 0
        color = PALETTE[idx % len(PALETTE)]
        label = label_for(key, labels)
        rows.append(
            f'<text x="24" y="{y + 24}" class="label">{esc(label)}</text>'
            f'<rect x="{left}" y="{y}" width="{bar_width}" height="24" rx="6" fill="{color}" />'
            f'<text x="{left + bar_width + 12}" y="{y + 18}" class="value">{value}</text>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
    .title {{ font: 700 26px system-ui, -apple-system, Segoe UI, sans-serif; fill: #0f172a; }}
    .subtitle {{ font: 400 14px system-ui, -apple-system, Segoe UI, sans-serif; fill: #475569; }}
    .label {{ font: 500 14px system-ui, -apple-system, Segoe UI, sans-serif; fill: #334155; }}
    .value {{ font: 700 14px system-ui, -apple-system, Segoe UI, sans-serif; fill: #0f172a; }}
    .card {{ fill: #ffffff; stroke: #e2e8f0; stroke-width: 1; }}
  </style>
  <rect class="card" x="1" y="1" width="{width - 2}" height="{height - 2}" rx="18" />
  <text x="24" y="42" class="title">{esc(title)}</text>
  <text x="24" y="66" class="subtitle">Reporte E.C.O. generado desde JSON; conteos no diagnósticos.</text>
  {''.join(rows)}
</svg>
'''
    path.write_text(svg, encoding="utf-8")


def write_gene_category_matrix(
    path: Path,
    matrix: Mapping[str, Mapping[str, int]],
) -> None:
    genes = sorted(matrix.keys())
    category_order = [key for key in CATEGORY_LABELS if any(key in matrix.get(gene, {}) for gene in genes)]
    for gene in genes:
        for category in matrix.get(gene, {}):
            if category not in category_order:
                category_order.append(category)

    cell_w = 138
    cell_h = 54
    left = 170
    top = 112
    width = left + max(1, len(category_order)) * cell_w + 40
    height = top + max(1, len(genes)) * cell_h + 70
    max_value = max([int(matrix.get(gene, {}).get(category, 0)) for gene in genes for category in category_order] or [1])

    def shade(value: int) -> str:
        if value <= 0:
            return "#f8fafc"
        ratio = value / max_value if max_value else 0
        if ratio >= 0.8:
            return "#4338ca"
        if ratio >= 0.5:
            return "#6366f1"
        return "#a5b4fc"

    header = []
    for idx, category in enumerate(category_order):
        x = left + idx * cell_w + cell_w / 2
        header.append(
            f'<text x="{x}" y="92" class="small" text-anchor="middle">{esc(label_for(category, CATEGORY_LABELS))}</text>'
        )

    rows = []
    for row_idx, gene in enumerate(genes):
        y = top + row_idx * cell_h
        rows.append(f'<text x="24" y="{y + 34}" class="gene">{esc(gene)}</text>')
        for col_idx, category in enumerate(category_order):
            x = left + col_idx * cell_w
            value = int(matrix.get(gene, {}).get(category, 0))
            fill = shade(value)
            text_fill = "#ffffff" if value > 0 and fill in {"#4338ca", "#6366f1"} else "#0f172a"
            rows.append(
                f'<rect x="{x}" y="{y}" width="{cell_w - 8}" height="{cell_h - 8}" rx="10" fill="{fill}" stroke="#e2e8f0" />'
                f'<text x="{x + (cell_w - 8) / 2}" y="{y + 31}" class="value" text-anchor="middle" fill="{text_fill}">{value}</text>'
            )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
    .title {{ font: 700 26px system-ui, -apple-system, Segoe UI, sans-serif; fill: #0f172a; }}
    .subtitle {{ font: 400 14px system-ui, -apple-system, Segoe UI, sans-serif; fill: #475569; }}
    .small {{ font: 600 11px system-ui, -apple-system, Segoe UI, sans-serif; fill: #334155; }}
    .gene {{ font: 700 16px system-ui, -apple-system, Segoe UI, sans-serif; fill: #0f172a; }}
    .value {{ font: 800 18px system-ui, -apple-system, Segoe UI, sans-serif; }}
    .card {{ fill: #ffffff; stroke: #e2e8f0; stroke-width: 1; }}
  </style>
  <rect class="card" x="1" y="1" width="{width - 2}" height="{height - 2}" rx="18" />
  <text x="24" y="42" class="title">Matriz gen × categoría</text>
  <text x="24" y="66" class="subtitle">Distribución exploratoria del subconjunto ClinVar procesado por E.C.O.</text>
  {''.join(header)}
  {''.join(rows)}
</svg>
'''
    path.write_text(svg, encoding="utf-8")


def write_index(path: Path, chart_files: Iterable[str]) -> None:
    links = "\n".join(
        f'<li><a href="{esc(filename)}">{esc(filename)}</a></li>' for filename in chart_files
    )
    html_doc = f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>E.C.O. ClinVar Charts</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 32px; color: #0f172a; background: #f8fafc; }}
    main {{ max-width: 1100px; margin: auto; }}
    h1 {{ margin-bottom: 0.25rem; }}
    p {{ color: #475569; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; }}
    .card {{ background: white; border: 1px solid #e2e8f0; border-radius: 18px; padding: 16px; box-shadow: 0 10px 24px rgba(15,23,42,.06); }}
    img {{ width: 100%; height: auto; display: block; }}
    code {{ background: #e2e8f0; padding: 2px 6px; border-radius: 6px; }}
  </style>
</head>
<body>
  <main>
    <h1>Visualizaciones E.C.O. — ClinVar</h1>
    <p>Gráficos generados desde <code>results/eco_clinvar_sample_report.json</code>. Uso educativo/bioinformático; no diagnóstico.</p>
    <div class="grid">
      {''.join(f'<section class="card"><img src="{esc(filename)}" alt="{esc(filename)}" /></section>' for filename in chart_files)}
    </div>
    <h2>Archivos</h2>
    <ul>{links}</ul>
  </main>
</body>
</html>
'''
    path.write_text(html_doc, encoding="utf-8")


def main() -> int:
    report = load_report(DEFAULT_INPUT)
    summary = report.get("summary", {})
    if not isinstance(summary, dict):
        raise ValueError("El JSON no contiene un bloque summary válido.")

    output_dir = DEFAULT_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    gene_counts = summary.get("gene_counts", {})
    category_counts = summary.get("category_counts", {})
    evidence_counts = summary.get("evidence_strength_counts", {})
    matrix = summary.get("gene_category_matrix", {})

    if not all(isinstance(obj, dict) for obj in [gene_counts, category_counts, evidence_counts, matrix]):
        raise ValueError("El JSON no contiene conteos suficientes para generar gráficos.")

    chart_files = [
        "variants_by_gene.svg",
        "categories.svg",
        "evidence_strength.svg",
        "gene_category_matrix.svg",
    ]

    write_svg_bar_chart(output_dir / chart_files[0], "Variantes por gen", gene_counts)
    write_svg_bar_chart(
        output_dir / chart_files[1],
        "Categorías E.C.O.",
        category_counts,
        labels=CATEGORY_LABELS,
        preferred_order=CATEGORY_LABELS.keys(),
    )
    write_svg_bar_chart(
        output_dir / chart_files[2],
        "Fuerza de evidencia",
        evidence_counts,
        labels=EVIDENCE_LABELS,
        preferred_order=EVIDENCE_LABELS.keys(),
    )
    write_gene_category_matrix(output_dir / chart_files[3], matrix)  # type: ignore[arg-type]
    write_index(output_dir / "index.html", chart_files)

    print("E.C.O. CLINVAR CHART EXPORT")
    print("===========================")
    print(f"Entrada JSON: {DEFAULT_INPUT}")
    print(f"Salida: {output_dir}")
    for filename in chart_files:
        print(f"- {output_dir / filename}")
    print(f"Índice HTML: {output_dir / 'index.html'}")
    print("Estado: OK, visualizaciones ClinVar generadas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
