# E.C.O. real data first safe candidate policy

## Propósito

Este documento define cuál debe ser el primer tipo de dato real seguro para E.C.O.
Su función es evitar que el sistema pase desde pruebas sintéticas hacia datos reales sin una selección responsable.

## Lectura rápida

El primer candidato seguro no debe ser genético, clínico, personal, forense ni biomédico aplicado.
Debe ser público, no sensible, trazable, pequeño, reproducible y útil solo para probar estructura operativa.

## Primer candidato seguro

El primer candidato recomendado para E.C.O. son datos ambientales públicos agregados.

Ejemplos de categoría permitida:

- Temperatura agregada por fecha o zona amplia.
- Humedad agregada.
- Precipitación agregada.
- Señales ambientales no personales.
- Series públicas simples sin identificación individual.

Estos datos sirven para probar lectura, contrato, manifiesto, trazabilidad y resumen estructural sin tocar información sensible.

## Criterios mínimos

- Fuente pública o con licencia clara.
- No contiene personas identificables.
- No contiene datos clínicos.
- No contiene datos genéticos humanos.
- No contiene datos biomédicos aplicados.
- No requiere inferir salud, conducta, identidad ni riesgo individual.
- Puede representarse como CSV, JSON o tabla simple.
- Puede validarse con un manifiesto antes de cualquier uso.

## Qué se permite probar

- Registrar la fuente.
- Validar el manifiesto.
- Revisar estructura de columnas o campos.
- Describir presencia, ausencia y consistencia básica.
- Generar un resumen técnico no aplicado.

## Qué sigue bloqueado

- Diagnóstico.
- Recomendación clínica.
- Interpretación genética humana.
- Datos personales sensibles.
- Datos privados.
- Datos clínicos.
- Entrenamiento de modelos.
- Recalibración de umbrales.
- Modificación de baseline.
- Afirmaciones biomédicas aplicadas.

## Decisión operativa

- Permitido: documentar esta política y preparar criterios de selección.
- Condicional: usar datos reales públicos no sensibles solo después de manifiesto validado.
- Bloqueado: ingerir datos reales sin manifiesto, permiso, trazabilidad y revisión de límites.

## Límite responsable

Este documento es preventivo y documental.
No ingiere datos reales, no usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no realiza afirmaciones biomédicas aplicadas.

## Explicación simple

Antes de que E.C.O. digiera datos reales, elegimos un primer alimento seguro: público, pequeño, no sensible y sin riesgo clínico ni personal.

## Evidencia de smoke test

- Comando: `scripts/run_smoke_eco_real_data_first_safe_candidate_policy.sh`
- Última evidencia: `results/smoke-eco-real-data-first-safe-candidate-policy-20260508T203911Z.log`
