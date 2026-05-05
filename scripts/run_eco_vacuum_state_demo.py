from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_SEQUENCE = [0.00, 0.03, -0.02, 0.05, -0.01, 0.00]


def build_payload(sequence=None):
    sequence = DEFAULT_SEQUENCE if sequence is None else sequence
    events = []

    for step, fluctuation in enumerate(sequence):
        boundary = "open" if step < 3 else "constrained"
        detector_limit = 0.03

        observable = abs(fluctuation) >= detector_limit
        event = "observable_variation" if observable else "basal_silence"

        events.append(
            {
                "step": step,
                "estado_base": 0.0,
                "ausencia": fluctuation == 0.0,
                "fluctuacion": fluctuation,
                "frontera": boundary,
                "medicion": observable,
                "evento": event,
            }
        )

    observable_events = sum(1 for item in events if item["medicion"])

    return {
        "model": "eco_vacuum_state_demo",
        "status": "experimental",
        "classification": "permitted",
        "not_physical_measurement": True,
        "sensitive_data_used": False,
        "training_executed": False,
        "baseline_modified": False,
        "thresholds_recalibrated": False,
        "controlled_vocabulary": [
            "estado_base",
            "ausencia",
            "fluctuacion",
            "frontera",
            "medicion",
            "evento",
        ],
        "events": events,
        "summary": {
            "total_steps": len(events),
            "observable_events": observable_events,
            "basal_silence_events": len(events) - observable_events,
        },
        "responsible_limit": (
            "Demo educativa y experimental. No mide el vacio cuantico real, "
            "no entrena modelos, no usa datos sensibles, no modifica baseline "
            "y no recalibra umbrales estables."
        ),
    }


def write_outputs(payload, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "eco_vacuum_state_demo.json"
    md_path = output_dir / "eco_vacuum_state_demo.md"

    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Demo E.C.O. - Vacuum State",
        "",
        "Estado: experimental.",
        "",
        "Clasificacion: permitido.",
        "",
        "## Lectura operativa",
        "",
        "Esta demo representa un estado informacional minimo inspirado en patrones del vacio cuantico.",
        "",
        "No mide el vacío cuántico real.",
        "",
        "No entrena modelos, no usa datos sensibles, no modifica baseline y no recalibra umbrales estables.",
        "",
        "## Resumen",
        "",
        f"- Pasos evaluados: {payload["summary"]["total_steps"]}",
        f"- Eventos observables: {payload["summary"]["observable_events"]}",
        f"- Silencios basales: {payload["summary"]["basal_silence_events"]}",
        "",
        "## Vocabulario controlado",
        "",
    ]

    for item in payload["controlled_vocabulary"]:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("## Limite responsable")
    lines.append("")
    lines.append(payload["responsible_limit"])
    lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")

    return json_path, md_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="results")
    args = parser.parse_args()

    payload = build_payload()
    json_path, md_path = write_outputs(payload, args.output_dir)

    print("OK: demo E.C.O. vacuum state generada.")
    print(f"- {json_path}")
    print(f"- {md_path}")


if __name__ == "__main__":
    main()
