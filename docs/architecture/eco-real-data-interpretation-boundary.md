# E.C.O. real data interpretation boundary

## Propósito

Este documento define el límite entre observar datos reales, describir patrones, generar hipótesis e interpretar resultados dentro de E.C.O.
Su función es evitar que una lectura experimental se confunda con diagnóstico, recomendación clínica o afirmación biomédica aplicada.

## Lectura rápida

E.C.O. puede preparar estructura para datos reales, pero todavía no debe producir conclusiones aplicadas.
Antes de interpretar, debe existir manifiesto de fuente, validación de límites responsables y clasificación explícita del uso.

## Niveles de lectura

- Nivel 0: registrar fuente. Solo describe origen, permiso, tipo de dato y límites.
- Nivel 1: observar estructura. Revisa formato, campos, presencia, ausencia y consistencia básica.
- Nivel 2: describir patrones. Resume distribuciones, señales o relaciones sin explicar causalidad.
- Nivel 3: comparar patrones. Contrasta contra ejemplos sintéticos, referencias documentales o estados operativos.
- Nivel 4: generar hipótesis. Propone posibilidades explícitamente no aplicadas y no clínicas.
- Nivel 5: interpretar con alcance controlado. Solo permitido con datos no sensibles, fuente clara, límites documentados y revisión previa.

## Bloqueos explícitos

- No diagnosticar.
- No recomendar tratamiento.
- No afirmar causalidad biomédica aplicada.
- No interpretar datos genéticos privados.
- No usar datos personales sensibles.
- No recalibrar umbrales estables sin auditoría.
- No modificar baseline sin comparación documentada.

## Condiciones mínimas para interpretar

- Existe manifiesto de fuente validado.
- La fuente no contiene datos sensibles o tiene autorización explícita y marco responsable.
- El objetivo está clasificado como estudiar, simular, evaluar o generar hipótesis.
- La salida declara límites, incertidumbre y alcance no aplicado.
- La interpretación no se presenta como verdad clínica, genética, forense ni diagnóstica.

## Decisión operativa

- Permitido: observar, describir y comparar datos sintéticos o manifiestos descriptivos.
- Condicional: describir patrones de datos reales no sensibles con fuente clara.
- Bloqueado: diagnóstico, datos sensibles, datos genéticos privados, uso clínico, uso forense o afirmaciones biomédicas aplicadas.

## Límite responsable

Este documento es preventivo y arquitectónico.
No usa datos sensibles, no ingiere datos reales, no entrena modelos, no modifica baseline, no recalibra umbrales y no realiza afirmaciones biomédicas aplicadas.

## Explicación simple

Antes de que E.C.O. diga que entiende un dato real, debe demostrar que solo está observando, describiendo o generando hipótesis dentro de límites seguros.
