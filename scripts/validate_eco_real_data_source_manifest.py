import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "docs" / "architecture"
SCHEMA_PATH = ARCH / "eco-real-data-source-manifest-schema.json"
MANIFEST_DIR = ARCH / "real-data-source-manifests"
MANIFEST_PATTERN = "*.json"

EXPECTED_REQUIRED = {
    "source_id",
    "source_name",
    "source_kind",
    "origin",
    "license_or_permission",
    "sensitivity_classification",
    "contains_identifiable_people",
    "contains_genetic_data",
    "contains_clinical_data",
    "allowed_use",
    "blocked_use",
    "readiness_decision",
    "responsible_limits",
}

EXPECTED_FALSE_LIMITS = [
    "ingests_real_data",
    "uses_sensitive_data",
    "trains_model",
    "modifies_baseline",
    "recalibrates_thresholds",
    "makes_applied_biomedical_claims",
]

LIMIT_TEXT = "datos sintéticos o manifiestos descriptivos; sin ingestión de datos reales; sin entrenamiento; sin datos sensibles; sin modificación de baseline; sin recalibración; sin afirmaciones biomédicas aplicadas."


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema(schema):
    errors = []
    if schema.get("schema_id") != "eco_real_data_source_manifest_v1":
        errors.append("schema_id inválido o ausente")

    required = set(schema.get("required_fields", []))
    missing_required = sorted(EXPECTED_REQUIRED - required)
    if missing_required:
        errors.append(f"faltan campos requeridos en schema: {missing_required}")

    allowed = schema.get("allowed_values", {})
    if "condicional" not in allowed.get("sensitivity_classification", []):
        errors.append("falta sensibilidad condicional")
    if "block" not in allowed.get("readiness_decision", []):
        errors.append("falta decisión block")

    limits = schema.get("responsible_limits", {})
    for key in EXPECTED_FALSE_LIMITS:
        if limits.get(key) is not False:
            errors.append(f"límite responsable inválido en schema: {key}")

    return errors


def validate_manifest(schema, manifest, path):
    errors = []
    required = set(schema.get("required_fields", []))
    missing = sorted(required - set(manifest.keys()))
    if missing:
        errors.append(f"{path}: faltan campos requeridos: {missing}")

    allowed = schema.get("allowed_values", {})
    for field in ("source_kind", "sensitivity_classification", "readiness_decision"):
        if field in manifest and manifest[field] not in allowed.get(field, []):
            errors.append(f"{path}: valor inválido en {field}: {manifest[field]}")

    for field in ("contains_identifiable_people", "contains_genetic_data", "contains_clinical_data"):
        if field in manifest and not isinstance(manifest[field], bool):
            errors.append(f"{path}: {field} debe ser booleano")

    limits = manifest.get("responsible_limits", {})
    for key in EXPECTED_FALSE_LIMITS:
        if limits.get(key) is not False:
            errors.append(f"{path}: límite responsable inválido: {key}")

    return errors


def main():
    if not SCHEMA_PATH.exists():
        raise SystemExit("No existe eco-real-data-source-manifest-schema.json. Cierra #139 antes de #140.")

    schema = load_json(SCHEMA_PATH)
    errors = validate_schema(schema)

    manifests = []
    if MANIFEST_DIR.exists():
        manifests = sorted(MANIFEST_DIR.glob(MANIFEST_PATTERN))

    for manifest_path in manifests:
        errors.extend(validate_manifest(schema, load_json(manifest_path), manifest_path))

    print("# E.C.O. real data source manifest validation")
    if errors:
        print("Estado: failed")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("Estado: passed")
    print(f"Schema validado: {SCHEMA_PATH.relative_to(ROOT)}")
    print(f"Manifiestos candidatos: {len(manifests)}")
    print(f"Límite: {LIMIT_TEXT}")


if __name__ == "__main__":
    main()
