from __future__ import annotations

import subprocess
from pathlib import Path


def run_git(args: list[str]) -> str:
    result = subprocess.run(["git", *args], capture_output=True, text=True, check=False)
    return result.stdout.strip()


def main() -> int:
    branch = run_git(["branch", "--show-current"]) or "desconocida"
    status_short = run_git(["status", "--short"])
    status_full = run_git(["status", "--branch", "--short"])
    last_commit = run_git(["log", "--oneline", "--decorate", "-1"])
    origin_main = run_git(["rev-parse", "--short", "origin/main"])
    head = run_git(["rev-parse", "--short", "HEAD"])

    clean = status_short == ""
    on_main = branch == "main"
    synced_hint = "origin/main" in status_full or "main" in status_full

    state = "green" if clean else "attention"

    lines = [
        "# E.C.O. status operativo",
        "",
        f"- Estado: {state}",
        f"- Rama actual: {branch}",
        f"- HEAD: {head}",
        f"- origin/main: {origin_main}",
        f"- Último commit: {last_commit}",
        f"- Árbol limpio: {clean}",
        f"- En main: {on_main}",
        "",
        "## Lectura rápida",
        "",
    ]

    if clean and on_main:
        lines.append("Semáforo verde: puedes detenerte o iniciar un nuevo sprint desde main.")
    elif clean:
        lines.append("Atención: el árbol está limpio, pero no estás en main. Cierra o integra la rama antes de iniciar otro objetivo.")
    else:
        lines.append("Atención: hay cambios sin guardar. No cambies de sprint todavía.")

    lines.extend([
        "",
        "## Límite operativo",
        "",
        "Este comando solo inspecciona el estado del repositorio. No modifica archivos, no entrena modelos, no cambia baseline y no recalibra umbrales.",
    ])

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
