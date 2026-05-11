# Ejemplo sintético de dataset adaptativo E.C.O.

Este archivo acompaña el contrato documental de dataset adaptativo con una muestra mínima, sintética y no operativa.

## Objetivo

Mostrar cómo podría verse una estructura de registros adaptativos sin incorporar datos reales, datos sensibles, entrenamiento, baseline ni recalibración de umbrales.

## Archivos relacionados

- Contrato: `docs/architecture/eco-adaptive-dataset-contract.md`
- Ejemplo JSON: `docs/architecture/eco-adaptive-dataset-example.json`

## Clasificación

- Tipo: ejemplo sintético documental.
- Clasificación: permitido.
- Estado: experimental controlado.
- Uso: validación estructural y explicación operativa.

## Qué contiene

El ejemplo contiene dos registros sintéticos:

1. Un registro candidato sin riesgo declarado.
2. Un registro que requiere revisión operativa.

## Qué no contiene

- No contiene datos reales.
- No contiene datos personales.
- No contiene datos sensibles.
- No contiene datos genéticos privados.
- No entrena modelos.
- No modifica baseline.
- No recalibra umbrales.
- No genera afirmaciones biomédicas aplicadas.

## Uso permitido

Este ejemplo sirve para comprobar que el contrato documental puede traducirse a una estructura simple, trazable y verificable.

## Uso bloqueado

No usar este ejemplo como fuente de entrenamiento, evaluación aplicada, diagnóstico, comparación biomédica o calibración de modelos.

## Resultado esperado

El ejemplo debe poder validarse con tests simples, mantenerse dentro de documentación y actuar como plantilla controlada para futuros ejemplos sintéticos.
