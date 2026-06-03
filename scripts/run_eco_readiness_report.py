#!/usr/bin/env python3
"""Imprime un reporte sintético de readiness operativo E.C.O."""

from __future__ import annotations


def build_report() -> str:
    return "\n".join(
        [
            "E.C.O. READINESS REPORT",
            "",
            "Tipo de reporte:",
            "- sintético",
            "- operativo",
            "- documental/verificable",
            "- no clínico",
            "- no biomédico aplicado",
            "- no productivo externo",
            "",
            "readiness report sintético:",
            "- checklist documental de readiness",
            "- no verifica el estado actual de git",
            "- no ejecuta pytest",
            "- no debe interpretarse como prueba de que el repo está green",
            "",
            "validación real externa:",
            "- ejecutar make eco-status",
            "- ejecutar pytest",
            "- ejecutar make eco-check-clean",
            "",
            "límites responsables:",
            "- sin datos reales",
            "- sin entrenamiento",
            "- sin modificación de baseline",
            "- sin recalibración de umbrales",
            "- sin afirmaciones biomédicas aplicadas",
            "- sin diagnóstico clínico",
            "- sin datos genéticos privados",
            "",
            "decisión operativa:",
            "- continuar con sprint panel o micro-sprint controlado",
            "- pausar y entrar en modo recuperación",
            "",
        ]
    )


def main() -> None:
    print(build_report())


if __name__ == "__main__":
    main()
