from __future__ import annotations

import subprocess
from pathlib import Path


def run_git(args: list[str]) -> str:
    result = subprocess.run(["git", *args], capture_output=True, text=True, check=False)
    return result.stdout.strip()


def is_synced_with_origin_main(*, head: str, origin_main: str) -> bool:
    return bool(head and origin_main and head == origin_main)


def compute_operational_state(*, clean: bool, on_main: bool, synced: bool) -> str:
    return "green" if clean and on_main and synced else "attention"


def build_quick_reading(*, clean: bool, on_main: bool, synced: bool) -> str:
    if clean and on_main and synced:
        return (
            "Semáforo verde: puedes detenerte aquí. Para iniciar un nuevo sprint, "
            "crea una rama nueva desde main antes de modificar archivos."
        )
    if clean and on_main:
        return (
            "Atención: estás en main, pero HEAD no coincide con origin/main. "
            "Sincroniza antes de declarar estado green."
        )
    if clean:
        return (
            "Atención: el árbol está limpio, pero no estás en main. "
            "Cierra o integra la rama antes de iniciar otro objetivo."
        )
    return "Atención: hay cambios sin guardar. No cambies de sprint todavía."


def main() -> int:
    branch = run_git(["branch", "--show-current"]) or "desconocida"
    status_short = run_git(["status", "--short"])
    last_commit = run_git(["log", "--oneline", "--decorate", "-1"])
    origin_main = run_git(["rev-parse", "--short", "origin/main"])
    head = run_git(["rev-parse", "--short", "HEAD"])

    clean = status_short == ""
    on_main = branch == "main"
    synced = is_synced_with_origin_main(head=head, origin_main=origin_main)

    state = compute_operational_state(clean=clean, on_main=on_main, synced=synced)

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
        f"- Sincronizado con origin/main: {synced}",
        "",
        "## Lectura rápida",
        "",
    ]

    lines.append(build_quick_reading(clean=clean, on_main=on_main, synced=synced))

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
