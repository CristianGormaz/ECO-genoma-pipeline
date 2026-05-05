from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


INPUT_PATH = Path("data/governance/sne_eco_sensitive_source_registry.jsonl")
OUTPUT_JSON = Path("results/sne_eco_sensitive_source_registry_report.json")
OUTPUT_MD = Path("results/sne_eco_sensitive_source_registry_report.md")

REQUIRED_FIELDS = {
    "id",
    "domain",
    "source_kind",
    "source_name",
    "access_class",
    "license_status",
    "contains_personal_data",
    "permitted_use",
    "gate_required",
    "expected_registry_status",
}

RESPONSIBLE_LIMIT = (
    "Registro educativo/experimental de fuentes sensibles S.N.E.-E.C.O.; "
    "no ingiere datos reales, no entrena modelos, no diagnostica, "
    "no tiene uso clínico aplicado, no realiza inferencias forenses, "
    "no afirma conciencia humana real, no recalibra umbrales "
    "y no modifica baseline estable."
)


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []

    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def classify_source(row: dict) -> str:
    source_kind = row.get("source_kind", "")
    license_status = row.get("license_status", "")
    permitted_use = row.get("permitted_use", "")
    contains_personal_data = bool(row.get("contains_personal_data"))
    gate_required = bool(row.get("gate_required"))

    if contains_personal_data:
        return "blocked"

    if permitted_use in {
        "applied_diagnosis",
        "applied_forensic",
        "applied_claim",
        "silent_change",
    }:
        return "blocked"

    if source_kind in {
        "personal_medical_record",
        "user_case",
        "person_case",
        "hidden_change",
        "human_claim",
    }:
        return "blocked"

    if license_status in {"not_allowed", "unknown"}:
        return "blocked"

    if gate_required:
        return "conditional"

    if source_kind in {
        "anonymized_dataset",
        "licensed_dataset",
        "public_legal_text",
        "experimental_delta",
        "public_dataset",
    }:
        return "conditional"

    if license_status in {"requires_review", "licensed"}:
        return "conditional"

    if source_kind in {
        "synthetic",
        "taxonomy_public",
        "literature",
        "educational_example",
    } and license_status in {"synthetic", "public", "open"}:
        return "allowed"

    return "conditional"


def build_report(write_outputs: bool = False) -> dict:
    rows = read_jsonl(INPUT_PATH)
    errors = []
    warnings = []
    evaluated = []

    if not rows:
        errors.append(f"Registro de fuentes no encontrado o vacío: {INPUT_PATH}")

    ids = [row.get("id") for row in rows]
    duplicate_ids = sorted([item for item, count in Counter(ids).items() if count > 1])

    if duplicate_ids:
        errors.append(f"IDs duplicados: {duplicate_ids}")

    for row in rows:
        missing = sorted(REQUIRED_FIELDS - set(row.keys()))
        predicted = classify_source(row)
        expected = row.get("expected_registry_status")
        ok = predicted == expected

        if missing:
            errors.append(f"{row.get('id', 'sin_id')}: faltan campos {missing}")

        if not ok:
            errors.append(
                f"{row.get('id', 'sin_id')}: esperado={expected}, obtenido={predicted}"
            )

        evaluated.append(
            {
                "id": row.get("id"),
                "domain": row.get("domain"),
                "source_kind": row.get("source_kind"),
                "license_status": row.get("license_status"),
                "access_class": row.get("access_class"),
                "permitted_use": row.get("permitted_use"),
                "expected_registry_status": expected,
                "predicted_registry_status": predicted,
                "ok": ok,
            }
        )

    counts = Counter(item["predicted_registry_status"] for item in evaluated)
    blocked_sources = [
        item["id"] for item in evaluated if item["predicted_registry_status"] == "blocked"
    ]
    conditional_sources = [
        item["id"] for item in evaluated if item["predicted_registry_status"] == "conditional"
    ]

    status = "red" if errors else "attention" if warnings else "green"

    report = {
        "status": status,
        "source_count": len(rows),
        "counts": dict(sorted(counts.items())),
        "blocked_sources": blocked_sources,
        "conditional_sources": conditional_sources,
        "evaluated": evaluated,
        "warnings": warnings,
        "errors": errors,
        "responsible_limit": RESPONSIBLE_LIMIT,
    }

    if write_outputs:
        OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_JSON.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        OUTPUT_MD.write_text(to_markdown(report), encoding="utf-8")

    return report


def to_markdown(report: dict) -> str:
    icon = {"green": "🟢", "attention": "🟡", "red": "🔴"}.get(report["status"], "⚪")

    lines = [
        "# Registro de fuentes sensibles S.N.E.-E.C.O.",
        "",
        f"Estado: {icon} `{report['status']}`",
        f"Fuentes evaluadas: `{report['source_count']}`",
        "",
        "## Distribución por estado",
        "",
        "| Estado | Conteo |",
        "|---|---:|",
    ]

    for key, value in report["counts"].items():
        lines.append(f"| `{key}` | {value} |")

    lines.extend(["", "## Fuentes bloqueadas", ""])

    if report["blocked_sources"]:
        lines.extend(f"- `{item}`" for item in report["blocked_sources"])
    else:
        lines.append("- Ninguna.")

    lines.extend(["", "## Fuentes condicionales", ""])

    if report["conditional_sources"]:
        lines.extend(f"- `{item}`" for item in report["conditional_sources"])
    else:
        lines.append("- Ninguna.")

    lines.extend(
        [
            "",
            "## Evaluación fuente por fuente",
            "",
            "| ID | Dominio | Fuente | Licencia | Acceso | Uso | Esperado | Obtenido | OK |",
            "|---|---|---|---|---|---|---|---|---:|",
        ]
    )

    for item in report["evaluated"]:
        lines.append(
            f"| `{item['id']}` | `{item['domain']}` | `{item['source_kind']}` | "
            f"`{item['license_status']}` | `{item['access_class']}` | "
            f"`{item['permitted_use']}` | `{item['expected_registry_status']}` | "
            f"`{item['predicted_registry_status']}` | `{item['ok']}` |"
        )

    lines.extend(["", "## Advertencias", ""])

    if report["warnings"]:
        lines.extend(f"- {warning}" for warning in report["warnings"])
    else:
        lines.append("- Sin advertencias.")

    lines.extend(["", "## Errores", ""])

    if report["errors"]:
        lines.extend(f"- {error}" for error in report["errors"])
    else:
        lines.append("- Sin errores.")

    lines.extend(["", "## Límite responsable", "", report["responsible_limit"], ""])

    return "\n".join(lines)


def main() -> None:
    report = build_report(write_outputs=True)
    print(to_markdown(report))
    print("OK: registro de fuentes sensibles S.N.E.-E.C.O. generado.")
    print(f"- {OUTPUT_JSON}")
    print(f"- {OUTPUT_MD}")


if __name__ == "__main__":
    main()
