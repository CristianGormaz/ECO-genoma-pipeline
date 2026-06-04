#!/usr/bin/env python3
"""
Exportador de flujo de observabilidad distribuida S.N.E.-E.C.O.
=============================================================

Genera un diagrama Mermaid (Markdown) que visualiza el tránsito de paquetes
entre los diferentes plexos entéricos, incluyendo micro-trazas internas.

Uso:
    python3 scripts/export_eco_distributed_observability_flow.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PROJECT_ROOT / "results" / "eco_enteric_system_report.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "results" / "eco_distributed_observability_flow.md"


def generate_mermaid_flow(record: Dict[str, Any]) -> str:
    """Genera un diagrama Mermaid para un registro individual."""
    history = record.get("history", [])
    if not history:
        return "%% Sin historial para este paquete."

    lines = ["graph TD"]
    
    # Estilos de plexos
    lines.append("    classDef mucosa fill:#e1f5fe,stroke:#01579b,stroke-width:2px;")
    lines.append("    classDef submucoso fill:#f3e5f5,stroke:#4a148c,stroke-width:2px;")
    lines.append("    classDef mienterico fill:#fff3e0,stroke:#e65100,stroke-width:2px;")
    lines.append("    classDef inmune fill:#ffebee,stroke:#b71c1c,stroke-width:2px;")
    lines.append("    classDef unknown fill:#f5f5f5,stroke:#9e9e9e,stroke-width:1px;")

    plexus_map = {
        "mucosa_epithelial": "mucosa",
        "plexo_submucoso": "submucoso",
        "plexo_mienterico": "mienterico",
        "sistema_inmune_entérico": "inmune",
    }

    prev_node = None
    for i, step in enumerate(history):
        stage = step["stage"].replace(":", "_")
        node_id = f"node_{i}_{stage}"
        label = f"{step['stage']}<br/>({step['status']})"
        
        lines.append(f"    {node_id}[\"{label}\"]")
        
        plexus = step.get("plexus", "unknown")
        style_class = plexus_map.get(plexus, "unknown")
        lines.append(f"    class {node_id} {style_class}")

        if prev_node:
            lines.append(f"    {prev_node} --> {node_id}")
        
        prev_node = node_id

    return "\n".join(lines)


def build_report(report: Dict[str, Any]) -> str:
    """Construye un reporte Markdown con diagramas de flujo para cada paquete."""
    lines = [
        "# Observabilidad Distribuida S.N.E.-E.C.O. v1.2",
        "",
        "Visualización del flujo informacional entre plexos entéricos.",
        "",
        "## Leyenda de Plexos",
        "- 🟦 **Mucosa Epitelial:** Ingestión, barrera física, filtrado y absorción.",
        "- 🟪 **Plexo Submucoso:** Sensado local y perfil sensorial.",
        "- 🟧 **Plexo Mientérico:** Motilidad operativa y reflejos locales.",
        "- 🟥 **Sistema Inmune Entérico:** Señales de defensa y riesgo técnico.",
        "",
    ]

    for record in report.get("records", []):
        lines.append(f"### Flujo: {record['label']}")
        lines.append(f"Origen: `{record['source']}` | Decisión: `{record['decision'].get('action')}`")
        lines.append("")
        lines.append("```mermaid")
        lines.append(generate_mermaid_flow(record))
        lines.append("```")
        lines.append("")

    lines.append("## Lectura técnica")
    lines.append(
        "Este diagrama muestra cómo la micro-trazabilidad (logs internos) y la segmentación "
        "por plexos permiten auditar el tránsito informacional de forma granular. "
        "La v1.2 de E.C.O. habilita esta visibilidad distribuida para mejorar la transparencia "
        "del pipeline bioinspirado."
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Exporta diagramas de flujo de observabilidad distribuida.")
    parser.add_argument("--input-json", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    if not args.input_json.exists():
        print(f"Error: no existe {args.input_json}. Ejecuta scripts/run_eco_enteric_report.py primero.")
        return 1

    report = json.loads(args.input_json.read_text(encoding="utf-8"))
    markdown = build_report(report)
    
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(markdown, encoding="utf-8")

    print("E.C.O. DISTRIBUTED OBSERVABILITY FLOW EXPORT")
    print("============================================")
    print(f"Entrada JSON: {args.input_json}")
    print(f"Salida Markdown: {args.output_md}")
    print("Estado: OK, diagramas de flujo generados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
