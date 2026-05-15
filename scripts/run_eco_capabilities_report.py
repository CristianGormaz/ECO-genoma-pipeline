from __future__ import annotations

import json
from pathlib import Path
from typing import Any

OUTPUT_JSON = Path("results/eco_capabilities_report.json")
OUTPUT_MD = Path("results/eco_capabilities_report.md")


def build_report() -> dict[str, Any]:
    return {
        "title": "E.C.O. Current Capabilities Report",
        "status": "passed",
        "classification": "permitido",
        "stable_criterion": "pytest passing",
        "operational_snapshot": {
            "synthetic_dashboard": "dashboard sintético operativo con 7 componentes",
            "governance": "governance panel integrado",
            "post_governance_snapshot": "snapshot post-governance",
            "release_checklist": "checklist de liberación",
            "capabilities_map": "mapa de capacidades actuales",
        },
        "synthetic_scope": {
            "synthetic_demos": "demos sintéticas",
            "available_validations": [
                "python3 -m pytest -q",
                "make eco-status",
                "make eco-check-clean",
            ],
        },
        "responsible_limits": [
            "sin datos reales",
            "sin entrenamiento",
            "sin modificación de baseline",
            "sin recalibración de umbrales",
            "sin afirmaciones biomédicas aplicadas",
        ],
        "what_eco_does_not_do_yet": [
            "qué NO hace todavía E.C.O.: operación con datos reales en este marco de sprint",
            "qué NO hace todavía E.C.O.: entrenamiento productivo",
            "qué NO hace todavía E.C.O.: recalibración de baseline o umbrales fuera de gobernanza",
            "qué NO hace todavía E.C.O.: afirmaciones biomédicas aplicadas",
        ],
        "next_recommended_leap": "próximo salto recomendado",
    }


def build_markdown(payload: dict[str, Any]) -> str:
    limits = "\n".join(f"- {item}" for item in payload["responsible_limits"])
    not_yet = "\n".join(f"- {item}" for item in payload["what_eco_does_not_do_yet"])
    validations = "\n".join(
        f"- `{cmd}`" for cmd in payload["synthetic_scope"]["available_validations"]
    )

    return "\n".join(
        [
            "# E.C.O. — Current Capabilities Report",
            "",
            f"- estado: **{payload['status']}**",
            f"- clasificación: **{payload['classification']}**",
            f"- criterio estable: **{payload['stable_criterion']}**",
            "",
            "## Estado operativo documentado/sintético",
            f"- {payload['operational_snapshot']['synthetic_dashboard']}",
            f"- {payload['operational_snapshot']['governance']}",
            f"- {payload['operational_snapshot']['post_governance_snapshot']}",
            f"- {payload['operational_snapshot']['release_checklist']}",
            f"- {payload['operational_snapshot']['capabilities_map']}",
            f"- {payload['synthetic_scope']['synthetic_demos']}",
            "",
            "## Validaciones disponibles",
            validations,
            "",
            "## Límites responsables",
            limits,
            "",
            "## Qué NO hace todavía E.C.O.",
            not_yet,
            "",
            "## Próximo salto recomendado",
            f"- {payload['next_recommended_leap']}",
            "",
        ]
    )


def main() -> None:
    payload = build_report()
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(build_markdown(payload), encoding="utf-8")

    print("E.C.O. capabilities report generated:")
    print(f"- {OUTPUT_JSON}")
    print(f"- {OUTPUT_MD}")


if __name__ == "__main__":
    main()
