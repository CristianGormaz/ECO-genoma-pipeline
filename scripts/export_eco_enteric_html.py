#!/usr/bin/env python3
"""Exporta el reporte JSON del Sistema Entérico E.C.O. a HTML estático."""

from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path
from typing import Any, Dict, List

DEFAULT_INPUT = Path("results/eco_enteric_system_report.json")
DEFAULT_OUTPUT = Path("results/eco_enteric_system_report.html")


def e(value: object) -> str:
    """Escapa valores para HTML seguro y legible."""
    return escape(str(value), quote=True)


def badge(value: object) -> str:
    """Devuelve una etiqueta visual simple para acciones/rutas."""
    return f"<span class='badge'>{e(value)}</span>"


def history_list(history: List[Dict[str, Any]]) -> str:
    """Renderiza la trazabilidad completa de un paquete."""
    items = []
    for step in history:
        items.append(
            "<li>"
            f"<code>{e(step.get('stage'))}</code> → "
            f"<strong>{e(step.get('status'))}</strong>: "
            f"{e(step.get('message'))}"
            "</li>"
        )
    return "<ul class='history'>" + "".join(items) + "</ul>"


def record_card(record: Dict[str, Any]) -> str:
    """Renderiza una tarjeta por paquete evaluado."""
    decision = record.get("decision", {})
    sensory = record.get("sensory_profile", {})
    absorbed = bool(record.get("absorbed_features"))
    quarantine = record.get("quarantine_reason")
    discard = record.get("discard_reason")

    extra_lines = []
    if absorbed:
        features = record.get("absorbed_features", {})
        extra_lines.append(
            "<p><strong>Nutrientes informacionales:</strong> "
            f"longitud {e(features.get('length'))}, GC {e(features.get('gc_percent'))}%, "
            f"N {e(features.get('n_percent'))}%.</p>"
        )
    if quarantine:
        extra_lines.append(f"<p><strong>Cuarentena:</strong> {e(quarantine)}</p>")
    if discard:
        extra_lines.append(f"<p><strong>Descarte:</strong> {e(discard)}</p>")

    return f"""
    <article class='card'>
      <div class='card-head'>
        <h3>{e(record.get('label'))}</h3>
        {badge(decision.get('action'))}
      </div>
      <p class='muted'>Origen: <code>{e(record.get('source'))}</code></p>
      <p><strong>Payload:</strong> <code>{e(record.get('payload'))}</code></p>
      <div class='grid small'>
        <div class='metric'><strong>{e(sensory.get('length'))}</strong><span>Longitud</span></div>
        <div class='metric'><strong>{e(sensory.get('gc_percent'))}%</strong><span>GC</span></div>
        <div class='metric'><strong>{e(sensory.get('n_percent'))}%</strong><span>N</span></div>
        <div class='metric'><strong>{e(sensory.get('is_duplicate'))}</strong><span>Duplicado</span></div>
      </div>
      <p><strong>Ruta:</strong> {badge(decision.get('route'))}</p>
      <p><strong>Motivo:</strong> {e(decision.get('reason'))}</p>
      <p><strong>Confianza local:</strong> {e(decision.get('confidence'))}</p>
      {''.join(extra_lines)}
      <details>
        <summary>Ver trazabilidad completa</summary>
        {history_list(record.get('history', []))}
      </details>
    </article>
    """


def build_html(report: Dict[str, Any]) -> str:
    """Construye HTML estático desde el reporte entérico JSON."""
    homeostasis = report["homeostasis"]
    cards = "".join(record_card(record) for record in report.get("records", []))
    notes = "".join(f"<li>{e(note)}</li>" for note in homeostasis.get("notes", []))
    expected_actions = ", ".join(report.get("expected_actions", []))
    actual_actions = ", ".join(report.get("actual_actions", []))

    return f"""<!doctype html>
<html lang='es'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>E.C.O. Sistema entérico</title>
  <style>
    body {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; background: #f5f7fb; color: #172033; }}
    header {{ background: linear-gradient(135deg, #172033, #263653); color: white; padding: 2.2rem; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 1.5rem; }}
    .subtitle {{ color: #dce5ff; max-width: 940px; line-height: 1.55; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 1rem; }}
    .grid.small {{ grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); }}
    .metric, .section, .card {{ background: white; border-radius: 18px; padding: 1rem; box-shadow: 0 8px 24px rgba(23, 32, 51, 0.08); margin-bottom: 1rem; }}
    .metric strong {{ display: block; font-size: 1.55rem; margin-bottom: .2rem; }}
    .metric span, .muted {{ color: #65708a; }}
    .card-head {{ display: flex; align-items: center; justify-content: space-between; gap: 1rem; }}
    .badge {{ display: inline-block; background: #eef2ff; color: #263653; border: 1px solid #d9e1ff; border-radius: 999px; padding: .24rem .65rem; font-size: .86rem; font-weight: 700; }}
    code {{ background: #f0f2f7; border-radius: 7px; padding: .12rem .32rem; }}
    details {{ border-top: 1px solid #e5e8f0; margin-top: 1rem; padding-top: .8rem; }}
    summary {{ cursor: pointer; font-weight: 700; }}
    .history li {{ margin-bottom: .45rem; }}
    .attention {{ border-left: 6px solid #b26b00; }}
    .ok {{ border-left: 6px solid #19764b; }}
  </style>
</head>
<body>
  <header>
    <h1>E.C.O. - Sistema Entérico Integrado</h1>
    <p class='subtitle'>{e(report['purpose'])}</p>
    <p class='subtitle'>Capa técnica: <code>{e(report['architecture_layer'])}</code></p>
  </header>
  <main>
    <section class='grid'>
      <div class='metric'><strong>{e(homeostasis['total_packets'])}</strong><span>Procesados</span></div>
      <div class='metric'><strong>{e(homeostasis['absorbed_packets'])}</strong><span>Absorbidos</span></div>
      <div class='metric'><strong>{e(homeostasis['quarantined_packets'])}</strong><span>Cuarentena</span></div>
      <div class='metric'><strong>{e(homeostasis['discarded_packets'])}</strong><span>Descartados</span></div>
      <div class='metric'><strong>{e(homeostasis['rejected_packets'])}</strong><span>Rechazados</span></div>
      <div class='metric'><strong>{e(homeostasis['duplicate_packets'])}</strong><span>Duplicados</span></div>
    </section>

    <section class='section {'attention' if homeostasis['state'] == 'attention' else 'ok'}'>
      <h2>Resumen homeostático</h2>
      <p><strong>Estado:</strong> {badge(homeostasis['state'])}</p>
      <ul>{notes}</ul>
      <p><strong>Acciones esperadas:</strong> {e(expected_actions)}</p>
      <p><strong>Acciones obtenidas:</strong> {e(actual_actions)}</p>
    </section>

    <section class='section'>
      <h2>Paquetes evaluados</h2>
      <p>Esta sección muestra cómo la barrera, el sensado, el reflejo local y la memoria microbiota cambian el destino de cada entrada.</p>
    </section>

    {cards}

    <section class='section'>
      <h2>Lectura arquitectónica</h2>
      <p>La capa entérica demuestra que E.C.O. puede tomar microdecisiones locales antes de absorber información. Esto permite distinguir datos útiles, inválidos, insuficientes o redundantes sin tratar todas las entradas como equivalentes.</p>
      <p>La analogía se mantiene como arquitectura bioinspirada: no afirma que el software esté vivo, sino que usa principios del Sistema Nervioso Entérico para diseñar un pipeline más distribuido, trazable y resiliente.</p>
    </section>
  </main>
</body>
</html>
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Exporta el reporte entérico E.C.O. a HTML estático.")
    parser.add_argument("--input-json", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-html", type=Path, default=DEFAULT_OUTPUT)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not args.input_json.exists():
        parser.exit(status=1, message=f"Error: no existe {args.input_json}. Ejecuta scripts/run_eco_enteric_report.py primero.\n")

    report = json.loads(args.input_json.read_text(encoding="utf-8"))
    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.write_text(build_html(report), encoding="utf-8")

    print("E.C.O. ENTERIC HTML EXPORT")
    print("==========================")
    print(f"Entrada JSON: {args.input_json}")
    print(f"Salida HTML: {args.output_html}")
    print("Estado: OK, HTML del sistema entérico generado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
