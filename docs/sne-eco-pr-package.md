# Pull Request Package — S.N.E.-E.C.O.

## Título sugerido del PR

Integrate governed experimental S.N.E.-E.C.O. pipeline

## Qué hace este PR

- Integra un pipeline experimental gobernado.
- Estudia datos sintéticos y curados.
- Evalúa resultados experimentales.
- Genera reportes reproducibles.
- Separa gobernanza sensible de evaluación ML.
- Declara límites responsables antes de integrar a main.

## Qué NO hace este PR

- No ingiere datos reales.
- No entrena modelos nuevos de producción.
- No diagnostica personas.
- No tiene uso clínico aplicado.
- No realiza inferencias forenses aplicadas.
- No afirma conciencia humana real.
- No recalibra umbrales estables.
- No modifica baseline estable sin comparación.

## Clasificación de datos

### Permitido

- Ejemplos sintéticos.
- Taxonomías públicas.
- Literatura abierta para contexto teórico.

### Condicional

- Datasets anonimizados o licenciados.
- Textos legales públicos solo para estudio no aplicado.
- Cambios experimentales de umbral solo con auditoría.

### Bloqueado

- Historiales médicos personales.
- Diagnósticos reales sobre personas.
- Detección de conciencia humana real.
- Decisiones de responsabilidad forense.
- Cambios ocultos de umbrales.

## Validación esperada

```bash
source .venv/bin/activate
make sne-pr-package-check
.venv/bin/python -m pytest -q tests/test_sne_eco_pr_package_check.py
.venv/bin/python -m pytest -q
```

## Lectura simple

Este PR no convierte E.C.O. en una herramienta aplicada sobre personas reales. Solo deja una base experimental, medible, trazable y gobernada para evaluar el pipeline S.N.E.-E.C.O. antes de integrarlo a main.

## Límite responsable

Este paquete PR es educativo y experimental. No tiene uso clínico, diagnóstico, forense ni de conciencia humana real. No ingiere datos personales, no recalibra umbrales y no modifica baseline estable sin comparación.
