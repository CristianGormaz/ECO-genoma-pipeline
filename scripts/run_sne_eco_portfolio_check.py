from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "results" / "sne_eco_portfolio_check.json"
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "results" / "sne_eco_portfolio_check.md"

REQUIRED_FILES = [
    "README.md",
    "docs/sne-eco-portfolio-index.md",
    "docs/case-study-sne-eco-neurogastro-pipeline.md",
    "docs/sne-eco-public-summary.md",
    "docs/sne-eco-quick-evaluation.md",
    "docs/sne-eco-architecture-map.md",
    "docs/sne-eco-glossary.md",
    "docs/sne-eco-evidence-matrix.md",
    "docs/sne-eco-claims-and-limits.md",
]

RECOMMENDED_REPORTS = [
    "results/sne_eco_neurogastro_pipeline_summary.json",
    "results/sne_eco_compare_against_rc1.json",
    "results/sne_eco_neurogastro_context_report.json",
]

README_REQUIRED_TEXT = [
    "Para lectura rápida de portafolio S.N.E.-E.C.O.",
    "docs/sne-eco-portfolio-index.md",
    "docs/case-study-sne-eco-neurogastro-pipeline.md",
    "docs/sne-eco-public-summary.md",
    "docs/sne-eco-quick-evaluation.md",
    "docs/sne-eco-architecture-map.md",
    "docs/sne-eco-glossary.md",
    "docs/sne-eco-evidence-matrix.md",
    "docs/sne-eco-claims-and-limits.md",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verifica que los materiales de portafolio S.N.E.-E.C.O. estén presentes."
    )
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    return parser.parse_args()


def file_state(relative_path: str) -> dict[str, Any]:
    path = PROJECT_ROOT / relative_path
    return {
        "path": relative_path,
        "exists": path.exists(),
        "is_file": path.is_file(),
        "size_bytes": path.stat().st_size if path.exists() and path.is_file() else 0,
    }


def read_text_safe(relative_path: str) -> str:
    path = PROJECT_ROOT / relative_path
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def build_portfolio_check() -> dict[str, Any]:
    required = [file_state(item) for item in REQUIRED_FILES]
    reports = [file_state(item) for item in RECOMMENDED_REPORTS]
    readme_text = read_text_safe("README.md")

    readme_checks = [
        {"text": item, "present": item in readme_text}
        for item in README_REQUIRED_TEXT
    ]

    missing_required = [item["path"] for item in required if not item["exists"]]
    missing_readme_text = [item["text"] for item in readme_checks if not item["present"]]
    missing_reports = [item["path"] for item in reports if not item["exists"]]

    status = "green"
    if missing_required or missing_readme_text:
        status = "red"
    elif missing_reports:
        status = "yellow"

    return {
        "check_name": "sne_eco_portfolio_check",
        "status": status,
        "required_files": required,
        "recommended_reports": reports,
        "readme_checks": readme_checks,
        "missing_required_files": missing_required,
        "missing_readme_text": missing_readme_text,
        "missing_recommended_reports": missing_reports,
        "summary": {
            "required_files_ok": not missing_required,
            "readme_links_ok": not missing_readme_text,
            "recommended_reports_ok": not missing_reports,
        },
        "responsible_limit": (
            "Chequeo operativo de materiales de portafolio. No modifica reglas, baseline, "
            "umbrales ni resultados del pipeline."
        ),
    }


def to_markdown(payload: dict[str, Any]) -> str:
    icon = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(
        str(payload["status"]), "⚪"
    )

    lines = [
        "# Chequeo de portafolio S.N.E.-E.C.O.",
        "",
        f"Estado: {icon} `{payload['status']}`",
        "",
        "## Archivos requeridos",
        "",
        "| Archivo | Existe | Tamaño |",
        "|---|---:|---:|",
    ]

    for item in payload["required_files"]:
        lines.append(f"| `{item['path']}` | {item['exists']} | {item['size_bytes']} |")

    lines.extend([
        "",
        "## Enlaces esperados en README",
        "",
        "| Texto | Presente |",
        "|---|---:|",
    ])

    for item in payload["readme_checks"]:
        lines.append(f"| `{item['text']}` | {item['present']} |")

    lines.extend([
        "",
        "## Reportes recomendados",
        "",
        "| Reporte | Existe | Tamaño |",
        "|---|---:|---:|",
    ])

    for item in payload["recommended_reports"]:
        lines.append(f"| `{item['path']}` | {item['exists']} | {item['size_bytes']} |")

    lines.extend([
        "",
        "## Lectura operativa",
        "",
    ])

    if payload["status"] == "green":
        lines.append("- Portafolio técnico completo: documentos, enlaces y reportes recomendados presentes.")
    elif payload["status"] == "yellow":
        lines.append("- Documentos principales presentes, pero faltan reportes recomendados. Ejecuta `make sne-neurogastro-pipeline`.")
    else:
        lines.append("- Faltan archivos o referencias esenciales del portafolio. Revisar README y docs.")

    lines.extend([
        "",
        "## Límite operativo",
        "",
        str(payload["responsible_limit"]),
    ])
    return "\n".join(lines) + "\n"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    args = parse_args()
    payload = build_portfolio_check()
    markdown = to_markdown(payload)

    write_json(args.output_json, payload)
    write_text(args.output_md, markdown)

    print(markdown)
    print("OK: chequeo de portafolio S.N.E.-E.C.O. generado.")
    print(f"- {args.output_json}")
    print(f"- {args.output_md}")


if __name__ == "__main__":
    main()
