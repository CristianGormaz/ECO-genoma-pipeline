# S.N.E.-E.C.O. v1.0 — Release Candidate

## Estado

Este documento marca el estado **S.N.E.-E.C.O. v1.0 Release Candidate** del pipeline E.C.O. — Entérico Codificador Orgánico.

La versión candidata se declara después de integrar:

- variantes dirigidas para rutas confundidas;
- baseline jerárquico digestivo;
- proyección homeostática;
- auditoría de recurrencia;
- recurrence guard;
- suite de estabilidad;
- narrativa empírica;
- README con comandos reproducibles.

## Validación local reportada

```text
153 passed
Rutas confundidas: 0
Rutas confundidas de recurrencia: 0
Auditoría de recurrencia: limpia
```

## Comandos reproducibles

```bash
source .venv/bin/activate
python -m pytest -q
make sne-state-confusion
python scripts/run_sne_eco_recurrence_audit.py
```

En entornos donde `python` no existe fuera del entorno virtual, usar:

```bash
.venv/bin/python -m pytest -q
.venv/bin/python scripts/run_sne_eco_recurrence_audit.py
```

## Criterios de estabilidad

La versión candidata se considera estable mientras se cumpla:

| Criterio | Estado esperado |
|---|---|
| Tests automatizados | `153 passed` o superior |
| Rutas confundidas extendidas | `0` |
| Recurrencia confundida | `0` |
| `default_state` inesperado | ausente en rutas confundidas |
| Reportes JSON/Markdown | generados correctamente |
| Uso responsable | explícito en documentación y reportes |

## Alcance técnico

S.N.E.-E.C.O. v1.0 RC estabiliza la capa adaptativa entérica del pipeline:

- construcción de filas entrenables de transición;
- baseline jerárquico auditable;
- evaluación holdout;
- diagnóstico de cobertura;
- análisis de rutas confundidas;
- auditoría de recurrencia;
- pruebas de regresión para estabilidad.

## Lectura arquitectónica

La arquitectura alcanzó una primera forma estable:

```text
ingestión → filtrado → sensado → motilidad → defensa → microbiota → homeostasis → predicción adaptativa → auditoría → estabilidad
```

El sistema ya no solo procesa payloads: también audita sus propias rutas, identifica confusiones, corrige sobre-reacciones y protege el estado alcanzado mediante tests.

## Límite responsable

S.N.E.-E.C.O. v1.0 RC es una arquitectura de software bioinspirada, educativa y experimental. No modela conciencia humana, no entrega diagnóstico clínico, no tiene uso forense y no reemplaza evaluación profesional.

La metáfora entérica funciona como lenguaje de diseño para organizar decisiones computacionales con filtrado, memoria, defensa, equilibrio y estabilidad.

## Próximo paso sugerido

Después de validar esta versión candidata, el siguiente avance recomendado es:

```text
SNE-12 — Release tag and changelog
```

Objetivo: preparar un changelog breve y, si corresponde, crear una etiqueta de versión para marcar el estado estable del módulo.
