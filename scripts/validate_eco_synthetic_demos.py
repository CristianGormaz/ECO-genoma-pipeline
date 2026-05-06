from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REGISTRY_PATH = Path("docs/architecture/eco-synthetic-demo-registry.json")
CONTRACT_VALIDATOR = Path("scripts/validate_eco_synthetic_contract.py")
REQUIRED_DEMO_KEYS = {"id", "name", "runner", "json_output", "markdown_output"}


def load_registry(path: Path = REGISTRY_PATH) -> dict:
    if not path.exists():
        raise ValueError(f"registry does not exist: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("registry must be a JSON object")
    if data.get("classification") != "allowed":
        raise ValueError("registry.classification must be allowed")
    if data.get("data_policy") != "synthetic_only":
        raise ValueError("registry.data_policy must be synthetic_only")
    for key in ["training", "sensitive_data", "baseline_changed", "threshold_recalibrated"]:
        if data.get(key) is not False:
            raise ValueError(f"registry.{key} must be False")
    demos = data.get("demos")
    if not isinstance(demos, list) or not demos:
        raise ValueError("registry.demos must be a non-empty list")
    for index, demo in enumerate(demos, start=1):
        if not isinstance(demo, dict):
            raise ValueError(f"demo {index} must be an object")
        missing = REQUIRED_DEMO_KEYS - set(demo)
        if missing:
            raise ValueError(f"demo {index} missing keys: " + ", ".join(sorted(missing)))
        if not Path(demo["runner"]).exists():
            raise ValueError(f"runner does not exist: {demo["runner"]}")
    return data


def run_command(command: list[str]) -> int:
    print("Comando: " + " ".join(command))
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    return result.returncode


def main() -> int:
    print("# E.C.O. synthetic demos validation")
    try:
        registry = load_registry()
    except ValueError as error:
        print("Estado: failed")
        print("- " + str(error))
        return 1
    print("Estado: running")
    print("Clasificación: permitido")
    print("Registro: " + str(REGISTRY_PATH))
    failures = 0
    demos = registry["demos"]
    for demo in demos:
        print()
        print("## Run demo: " + demo["name"])
        run_code = run_command([sys.executable, demo["runner"]])
        if run_code != 0:
            failures += 1
            continue
        print("## Validate contract: " + demo["name"])
        validate_code = run_command([sys.executable, str(CONTRACT_VALIDATOR), demo["json_output"]])
        if validate_code != 0:
            failures += 1
    print()
    print("# Resultado global")
    if failures:
        print("Estado: failed")
        print("Fallos: " + str(failures))
        return 1
    print("Estado: passed")
    print("Demos validadas: " + str(len(demos)))
    print("Límite: datos sintéticos; sin entrenamiento; sin datos sensibles; sin recalibración.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
