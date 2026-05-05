from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from scripts.run_sne_eco_governed_ml_evaluation_gate import (
    build_report as build_governed_gate_report,
)


OUTPUT_JSON = Path("results/sne_eco_responsible_experiment_manifest.json")
OUTPUT_MD = Path("results/sne_eco_responsible_experiment_manifest.md")

EXPERIMENT_ID = "sne-eco-governed-ml-evaluation-v1"

RESPONSIBLE_LIMIT = (
    "Manifiesto educativo/experimental S.N.E.-E.C.O.; documenta trazabilidad "
    "de evaluación ML gobernada; no ingiere datos reales, no entrena modelos nuevos, "
    "no diagnostica, no tiene uso clínico aplicado, no realiza inferencias forenses, "
    "no afirma conciencia humana real, no recalibra umbrales y no modifica baseline estable."
)


def build_manifest(write_outputs: bool = False) -> dict:
    gate_report = build_governed_gate_report(write_outputs=True)

    status = "green" if gate_report.get("evaluation_allowed") is True else "red"

    manifest = {
        "status": status,
        "experiment_id": EXPERIMENT_ID,
        "experiment_kind": "evaluate_results",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "evaluation_allowed": gate_report.get("evaluation_allowed"),
        "governance_status": gate_report.get("governance_status"),
        "baseline_status": gate_report.get("baseline_status"),
        "challenge_status": gate_report.get("challenge_status"),
        "baseline_accuracy": gate_report.get("baseline_accuracy"),
        "challenge_accuracy": gate_report.get("challenge_accuracy"),
        "action_scope": {
            "study_data": True,
            "train_models": False,
            "evaluate_results": True,
            "make_applied_claims": False,
            "modify_stable_baseline": False,
            "recalibrate_thresholds": False,
        },
        "data_classification": {
            "allowed": [
                "synthetic_examples",
                "public_taxonomies",
                "open_literature_for_theoretical_context",
            ],
            "conditional": [
                "anonymized_or_licensed_research_datasets",
                "public_legal_texts_for_non_applied_study",
                "experimental_threshold_deltas_only_with_audit",
            ],
            "blocked": [
                "personal_medical_records",
                "real_person_diagnosis",
                "human_consciousness_detection_claims",
                "forensic_liability_decisions",
                "hidden_threshold_changes",
            ],
        },
        "input_reports": [
            "results/sne_eco_sensitive_governance_summary.md",
            "results/sne_eco_empirical_train_eval_split_report.md",
            "results/sne_eco_ml_baseline_report.md",
            "results/sne_eco_ml_challenge_eval_report.md",
            "results/sne_eco_governed_ml_evaluation_gate.md",
        ],
        "blocked_items": gate_report.get("blocked_items", {}),
        "conditional_items": gate_report.get("conditional_items", {}),
        "decision": (
            "allowed_experimental_evaluation"
            if status == "green"
            else "blocked_experimental_evaluation"
        ),
        "responsible_limit": RESPONSIBLE_LIMIT,
    }

    if write_outputs:
        OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_JSON.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        OUTPUT_MD.write_text(to_markdown(manifest), encoding="utf-8")

    return manifest


def to_markdown(manifest: dict) -> str:
    icon = {
        "green": "🟢",
        "attention": "🟡",
        "red": "🔴",
    }.get(manifest["status"], "⚪")

    action_scope = manifest["action_scope"]
    data_classification = manifest["data_classification"]

    lines = [
        "# Manifiesto responsable de experimento S.N.E.-E.C.O.",
        "",
        f"Estado: {icon} `{manifest['status']}`",
        f"Experimento: `{manifest['experiment_id']}`",
        f"Tipo: `{manifest['experiment_kind']}`",
        f"Decisión: `{manifest['decision']}`",
        f"Evaluación permitida: `{manifest['evaluation_allowed']}`",
        "",
        "## Estados heredados",
        "",
        "| Componente | Estado / valor |",
        "|---|---|",
        f"| Gobernanza sensible | `{manifest['governance_status']}` |",
        f"| Baseline ML | `{manifest['baseline_status']}` |",
        f"| Challenge eval | `{manifest['challenge_status']}` |",
        f"| Accuracy baseline | `{manifest['baseline_accuracy']}` |",
        f"| Accuracy challenge | `{manifest['challenge_accuracy']}` |",
        "",
        "## Alcance de acción",
        "",
        "| Acción | Permitida en este experimento |",
        "|---|---:|",
        f"| Estudiar datos | `{action_scope['study_data']}` |",
        f"| Entrenar modelos | `{action_scope['train_models']}` |",
        f"| Evaluar resultados | `{action_scope['evaluate_results']}` |",
        f"| Hacer afirmaciones aplicadas | `{action_scope['make_applied_claims']}` |",
        f"| Modificar baseline estable | `{action_scope['modify_stable_baseline']}` |",
        f"| Recalibrar umbrales | `{action_scope['recalibrate_thresholds']}` |",
        "",
        "## Clasificación de datos",
        "",
        "### Permitido",
        "",
    ]

    lines.extend(f"- `{item}`" for item in data_classification["allowed"])

    lines.extend(["", "### Condicional", ""])
    lines.extend(f"- `{item}`" for item in data_classification["conditional"])

    lines.extend(["", "### Bloqueado", ""])
    lines.extend(f"- `{item}`" for item in data_classification["blocked"])

    lines.extend(
        [
            "",
            "## Reportes usados como evidencia",
            "",
        ]
    )

    lines.extend(f"- `{report}`" for report in manifest["input_reports"])

    lines.extend(
        [
            "",
            "## Lectura operativa",
            "",
            "- Este manifiesto registra qué hizo el experimento y qué no hizo.",
            "- La evaluación ML solo se permite porque pasó por gobernanza sensible.",
            "- Este documento no cambia reglas, baseline ni umbrales.",
            "- Este documento no transforma E.C.O. en herramienta clínica, diagnóstica, forense ni de conciencia humana.",
            "",
            "## Límite responsable",
            "",
            manifest["responsible_limit"],
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    manifest = build_manifest(write_outputs=True)
    print(to_markdown(manifest))
    print("OK: manifiesto responsable de experimento S.N.E.-E.C.O. generado.")
    print(f"- {OUTPUT_JSON}")
    print(f"- {OUTPUT_MD}")


if __name__ == "__main__":
    main()
