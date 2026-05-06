from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DEMOS = [
    (
        "minimal simulation",
        ["scripts/run_eco_minimal_simulation.py"],
        "results/eco_minimal_simulation_demo.json",
    ),
    (
        "signal balance",
        ["scripts/run_eco_signal_balance_demo.py"],
        "results/eco_signal_balance_demo.json",
    ),
]


def run_step(label: str, args: list[str]) -> int:
    command = [sys.executable, *args]
    print(f"## {label}")
    print("Comando: " + " ".join(command))
    result = subprocess.run(command, cwd=ROOT, text=True, check=False)
    return result.returncode


def main() -> int:
    print("# E.C.O. synthetic demos validation")
    print("Estado: running")
    print("Clasificación: permitido")
    print("")

    failures: list[str] = []

    for name, demo_args, output_path in DEMOS:
        demo_code = run_step(f"Run demo: {name}", demo_args)
        if demo_code != 0:
            failures.append(f"{name}: demo failed")
            continue

        validate_code = run_step(
            f"Validate contract: {name}",
            ["scripts/validate_eco_synthetic_contract.py", output_path],
        )
        if validate_code != 0:
            failures.append(f"{name}: contract validation failed")

    print("")
    print("# Resultado global")

    if failures:
        print("Estado: failed")
        for failure in failures:
            print("- " + failure)
        return 1

    print("Estado: passed")
    print("Demos validadas: " + str(len(DEMOS)))
    print("Límite: datos sintéticos; sin entrenamiento; sin datos sensibles; sin recalibración.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
