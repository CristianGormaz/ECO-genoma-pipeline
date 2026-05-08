from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "docs" / "architecture"
EXAMPLE_PATTERN = "eco-operational-state-example-*.json"
RESULTS_DIR = ROOT / "results"
JSON_OUT = RESULTS_DIR / "eco_operational_state_examples_report.json"
MD_OUT = RESULTS_DIR / "eco_operational_state_examples_report.md"

LIMIT_TEXT = "datos sintéticos; sin entrenamiento; sin datos sensibles; sin modificación de baseline; sin recalibración; sin afirmaciones biomédicas aplicadas."


def _load_examples():
    examples = []
    for path in sorted(ARCH.glob(EXAMPLE_PATTERN)):
        data = json.loads(path.read_text(encoding="utf-8"))
        examples.append({
            "file": str(path.relative_to(ROOT)),
            "state_id": data["state_id"],
            "state_kind": data["state_kind"],
            "classification": data["classification"],
            "status": data["status"],
        })
    return examples


def main():
    examples = _load_examples()
    if not examples:
        raise SystemExit("No se encontraron ejemplos operacionales para reportar.")

    report = {
        "status": "passed",
        "classification": "permitido",
        "examples_count": len(examples),
        "examples": examples,
        "responsible_limit": LIMIT_TEXT,
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    md_lines = [
        "# E.C.O. operational state examples report",
        "",
        "Estado: passed",
        "Clasificación: permitido",
        f"Ejemplos reportados: {len(examples)}",
        "",
        "## Ejemplos",
        "",
    ]
    for example in examples:
        md_lines.append("- {state_id}: {state_kind} / {status} / {classification}.".format(**example))
    md_lines.extend(["", f"Límite: {LIMIT_TEXT}"])
    MD_OUT.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print("# E.C.O. operational state examples report")
    print("Estado: passed")
    print(f"Ejemplos reportados: {len(examples)}")
    print(f"Salida JSON: {JSON_OUT.relative_to(ROOT)}")
    print(f"Salida Markdown: {MD_OUT.relative_to(ROOT)}")
    print(f"Límite: {LIMIT_TEXT}")


if __name__ == "__main__":
    main()
