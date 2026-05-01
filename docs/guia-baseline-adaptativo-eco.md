# Guía del baseline adaptativo E.C.O. v0

Esta guía explica el primer baseline de transición de estados para S.N.E.-E.C.O.

## Qué hace

El baseline aprende reglas categóricas simples desde el dataset adaptativo:

```text
state_before + barrier_status + motility_action + defense_category + final_decision → state_after
```

No usa deep learning ni dependencias externas. Es una tabla auditable de transiciones observadas.

## Comando directo

```bash
python scripts/run_sne_eco_state_baseline.py --output-json results/sne_eco_state_baseline_report.json --output-md results/sne_eco_state_baseline_report.md
```

## Artefactos generados

```text
results/sne_eco_state_baseline_report.json
results/sne_eco_state_baseline_report.md
```

## Cómo leer accuracy_demo

`accuracy_demo` se calcula usando el mismo conjunto mínimo para entrenar y evaluar. Por eso sirve solo como prueba de funcionamiento, no como desempeño general.

## Límite responsable

Este baseline no modela conciencia humana, no diagnostica, no identifica personas y no debe usarse como herramienta clínica o forense. Sirve para comparar una regla aprendida simple contra los estados observados del pipeline E.C.O.

## Próximo paso

Cuando este baseline sea estable, el siguiente avance puede ser separar datos de entrenamiento/prueba o aumentar escenarios sintéticos antes de incorporar modelos externos.
