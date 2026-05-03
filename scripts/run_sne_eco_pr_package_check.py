from __future__ import annotations

import json
from pathlib import Path


DOC = Path("docs/sne-eco-pr-package.md")
OUTPUT_JSON = Path("results/sne_eco_pr_package_check.json")
OUTPUT_MD = Path("results/sne_eco_pr_package_check.md")

REQUIRED_PHRASES = [
    "Integrate governed experimental S.N.E.-E.C.O. pipeline",
    "Qué hace este PR",
    "Qué NO hace este PR",
    "Clasificación de datos",
    "Permitido",
    "Condicional",
    "Bloqueado",
    "No ingiere datos reales",
    "No diagnostica personas",
    "No tiene uso clínico aplicado",
    "No realiza inferencias forenses aplicadas",
    "No afirma conciencia humana real",
    "No recalibra umbrales estables",
    "No modifica baseline estable sin comparación",
]

RESPONSIBLE_LIMIT = (
    "Chequeo educativo/experimental de paquete PR S.N.E.-E.C.O.; "
    "no ingiere datos reales, no entrena modelos nuevos, no diagnostica, "
    "no tiene uso clínico aplicado, no realiza inferencias forenses, "
    "no afirma conciencia humana real, no recalibra umbrales "
    "y no modifica baseline estable."
)


def build_report(write_outputs: bool = False) -> dict:
    errors: list[str] = []

    if not DOC.exists():
        text = ""
        errors.append(f"No existe el documento esperado: {DOC}")
    else:
        text = DOC.read_text(encoding="utf-8")

    missing_phrases = [phrase for phrase in REQUIRED_PHRASES if phrase not in text]

    if missing_phrases:
        errors.append("Faltan frases obligatorias en el paquete PR.")

    report = {
        "status": "green" if not errors else "red",
        "document": str(DOC),
        "required_phrase_count": len(REQUIRED_PHRASES),
        "missing_phrases": missing_phrases,
        "warnings": [],
        "errors": errors,
        "responsible_limit": RESPONSIBLE_LIMIT,
    }

    if write_outputs:
        OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        OUTPUT_MD.write_text(to_markdown(report), encoding="utf-8")

    return report


def to_markdown(report: dict) -> str:
    icon = "🟢" if report["status"] == "green" else "🔴"
    lines = [
        "# Chequeo de paquete PR S.N.E.-E.C.O.",
        "",
        f"Estado: {icon} `{report['status']}`",
        f"Documento: `{report['document']}`",
        f"Frases requeridas: `{report['required_phrase_count']}`",
        "",
        "## Frases faltantes",
        "",
    ]

    if report["missing_phrases"]:
        lines.extend(f"- `{phrase}`" for phrase in report["missing_phrases"])
    else:
        lines.append("- Ninguna.")

    lines.extend(["", "## Advertencias", "", "- Sin advertencias.", "", "## Errores", ""])

    if report["errors"]:
        lines.extend(f"- {error}" for error in report["errors"])
    else:
        lines.append("- Sin errores.")

    lines.extend([
        "",
        "## Lectura operativa",
        "",
        "- Este chequeo valida que el paquete PR declare alcance, límites y validación.",
        "- No ejecuta entrenamiento.",
        "- No modifica reglas, baseline ni umbrales.",
        "- Sirve como preparación antes de abrir Pull Request hacia main.",
        "",
        "## Límite responsable",
        "",
        report["responsible_limit"],
        "",
    ])

    return "\n".join(lines)


def main() -> None:
    report = build_report(write_outputs=True)
    print(to_markdown(report))
    print("OK: chequeo de paquete PR S.N.E.-E.C.O. generado.")
    print(f"- {OUTPUT_JSON}")
    print(f"- {OUTPUT_MD}")


if __name__ == "__main__":
    main()
