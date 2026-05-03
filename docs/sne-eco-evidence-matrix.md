# Matriz de evidencias — S.N.E.-E.C.O.

Esta matriz conecta los documentos, reportes y validaciones del proyecto **E.C.O. — Entérico Codificador Orgánico** con evidencias observables del pipeline.

## Propósito

Facilitar una revisión rápida, técnica y responsable del sistema S.N.E.-E.C.O. sin asumir conocimiento avanzado de programación.

## Matriz principal

| Elemento | Qué demuestra | Evidencia observable | Validación asociada |
|---|---|---|---|
| `README.md` | Entrada general del proyecto | Enlaces principales del portafolio | `run_sne_eco_portfolio_check.py` |
| `docs/sne-eco-public-summary.md` | Explicación pública y no técnica | Resumen comprensible del sistema | Test de resumen público |
| `docs/sne-eco-quick-evaluation.md` | Ruta breve para evaluar el proyecto | Comando `make sne-portfolio-demo` | Test de guía rápida |
| `docs/sne-eco-architecture-map.md` | Flujo interno del pipeline | entrada → barrera → motilidad → defensa → estado → reporte | Test de mapa de arquitectura |
| `docs/sne-eco-glossary.md` | Lenguaje común del sistema | Definición de términos bioinspirados | Test de glosario |
| `results/sne_eco_state_dataset.json` | Transiciones observables | estado antes, estado después, decisión final | Pipeline neurogastrocomputacional |
| `results/sne_eco_observability_dashboard.json` | Estado consolidado del sistema | dashboard green/red/attention | Pipeline de observabilidad |
| `results/sne_eco_neurogastro_context_report.json` | Lectura bioinspirada del flujo | interocepción, motilidad, defensa, microbiota/memoria | Reporte neurogastrocomputacional |
| `results/sne_eco_compare_against_rc1.json` | Comparación contra línea base | regresiones frente a RC1 | Comparador contra RC1 |
| `tests/` | Protección contra regresiones | pruebas automatizadas | `pytest` |

## Lectura operativa

La matriz permite revisar si el proyecto tiene:

- documentos visibles;
- reportes generados;
- pruebas automatizadas;
- límites responsables explícitos;
- trazabilidad entre concepto, archivo y validación.

## Límite responsable

Esta matriz es educativa y experimental. No tiene uso clínico, diagnóstico ni forense. No modela conciencia humana. Su función es ordenar evidencia técnica y comunicacional del pipeline S.N.E.-E.C.O.
