from __future__ import annotations

import json
from pathlib import Path


SOURCE = Path("docs/operations/eco-agentic-scaffold-proposal-registry.md")
JSON_OUTPUT = Path("results/eco_agentic_scaffold_proposal_registry_report.json")
MD_OUTPUT = Path("results/eco_agentic_scaffold_proposal_registry_report.md")

RESPONSIBLE_LIMITS = [
    "sin autonomía real",
    "sin conciencia",
    "sin libre albedrío real",
    "sin datos reales",
    "sin entrenamiento",
    "sin modificación de baseline",
    "sin recalibración de umbrales",
    "sin afirmaciones biomédicas aplicadas",
]

PROPOSAL_FIELDS = [
    "proposal_id",
    "title",
    "associated_document",
    "candidate_module",
    "type",
    "state",
    "proposal_classification",
    "human_review",
    "final_human_decision",
    "expected_validations",
    "responsible_limits",
    "notes",
]


def _split_markdown_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def load_registry() -> str:
    return SOURCE.read_text(encoding="utf-8")


def extract_proposals(registry_text: str) -> list[dict[str, str]]:
    proposals: list[dict[str, str]] = []
    in_registry_table = False

    for line in registry_text.splitlines():
        if line.startswith("| proposal_id |"):
            in_registry_table = True
            continue
        if not in_registry_table:
            continue
        if line.startswith("| ---"):
            continue
        if not line.startswith("|"):
            break

        cells = _split_markdown_row(line)
        if len(cells) != len(PROPOSAL_FIELDS):
            continue
        proposals.append(dict(zip(PROPOSAL_FIELDS, cells)))

    return proposals


def build_report(registry_text: str) -> dict:
    proposals = extract_proposals(registry_text)
    return {
        "title": "E.C.O. agentic scaffold proposal registry report",
        "status": "passed",
        "classification": "permitted",
        "source": str(SOURCE),
        "proposal_count": len(proposals),
        "proposals": proposals,
        "responsible_limits": RESPONSIBLE_LIMITS,
        "human_review_required": True,
        "final_human_decision_required": True,
        "scope": "read-only documentary registry summary",
        "no_real_data": True,
        "training_enabled": False,
        "baseline_modified": False,
        "thresholds_recalibrated": False,
        "applied_biomedical_claims": False,
        "real_autonomy_implied": False,
        "consciousness_implied": False,
        "real_free_will_implied": False,
    }


def write_markdown(report: dict) -> None:
    lines = [
        "# E.C.O. agentic scaffold proposal registry report",
        "",
        f"Estado: {report['status']}",
        f"Fuente del registro: `{report['source']}`",
        f"Cantidad de propuestas: {report['proposal_count']}",
        "",
        "## Propuestas detectadas",
        "",
    ]

    if report["proposals"]:
        for proposal in report["proposals"]:
            lines.extend(
                [
                    f"- `{proposal['proposal_id']}`: {proposal['title']}",
                    f"  - Documento asociado: `{proposal['associated_document']}`",
                    f"  - Estado: {proposal['state']}",
                    f"  - Clasificación registrada: {proposal['proposal_classification']}",
                ]
            )
    else:
        lines.append("- No se detectaron propuestas registradas.")

    lines.extend(
        [
            "",
            "## Revisión humana requerida",
            "",
            f"Revisión humana requerida: {str(report['human_review_required']).lower()}",
            "",
            "## Decisión final humana requerida",
            "",
            f"Decisión final humana requerida: {str(report['final_human_decision_required']).lower()}",
            "",
            "## Límites responsables",
            "",
        ]
    )
    lines.extend(f"- {limit}" for limit in report["responsible_limits"])
    lines.extend(
        [
            "",
            "Este reporte es de solo lectura: no usa datos reales, no entrena modelos, no modifica baseline, no recalibra umbrales y no formula afirmaciones biomédicas aplicadas.",
        ]
    )
    MD_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs(report: dict) -> None:
    JSON_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)


def main() -> int:
    report = build_report(load_registry())
    write_outputs(report)
    print("# E.C.O. agentic scaffold proposal registry report")
    print(f"Estado: {report['status']}")
    print(f"Fuente del registro: {report['source']}")
    print(f"Propuestas detectadas: {report['proposal_count']}")
    print(f"Salida JSON: {JSON_OUTPUT}")
    print(f"Salida Markdown: {MD_OUTPUT}")
    print("Límite: solo lectura documental; sin datos reales; sin entrenamiento; sin baseline ni umbrales.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
