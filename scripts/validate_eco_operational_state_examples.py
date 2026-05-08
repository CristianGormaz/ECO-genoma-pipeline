import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "docs" / "architecture"
SCHEMA_PATH = ARCH / "eco-operational-state-schema.json"
EXAMPLE_PATTERN = "eco-operational-state-example-*.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_example(schema, example, path):
    errors = []
    required = set(schema["required_fields"])
    missing = sorted(required - set(example.keys()))
    if missing:
        errors.append(f"{path}: faltan campos requeridos: {missing}")

    allowed = schema["allowed_values"]
    for field in ("classification", "state_kind", "status"):
        if field in example and example[field] not in allowed[field]:
            errors.append(f"{path}: valor inválido en {field}: {example[field]}")

    limits = example.get("responsible_limits", {})
    expected_false = [
        "uses_sensitive_data",
        "trains_model",
        "modifies_baseline",
        "recalibrates_thresholds",
        "makes_applied_biomedical_claims",
    ]
    for key in expected_false:
        if limits.get(key) is not False:
            errors.append(f"{path}: límite responsable inválido: {key}")
    return errors


def main():
    schema = load_json(SCHEMA_PATH)
    examples = sorted(ARCH.glob(EXAMPLE_PATTERN))
    if not examples:
        raise SystemExit("No se encontraron ejemplos operacionales sintéticos.")

    errors = []
    for path in examples:
        errors.extend(validate_example(schema, load_json(path), path))

    print("# E.C.O. operational state examples validation")
    if errors:
        print("Estado: failed")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("Estado: passed")
    print(f"Ejemplos validados: {len(examples)}")
    print("Clasificación: permitido")
    print("Límite: datos sintéticos; sin entrenamiento; sin datos sensibles; sin modificación de baseline; sin recalibración; sin afirmaciones biomédicas aplicadas.")


if __name__ == "__main__":
    main()
