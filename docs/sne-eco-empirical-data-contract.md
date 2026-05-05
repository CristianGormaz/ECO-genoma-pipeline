# Fundamentos empíricos y contrato de datos — S.N.E.-E.C.O.

Este documento define cómo el proyecto **E.C.O. — Entérico Codificador Orgánico** entiende la empiricidad en su etapa experimental.

## Principio central

E.C.O. no afirma modelar biología humana real, diagnóstico médico, conciencia humana ni decisiones forenses. Su empiricidad se basa en observar datos, rutas, estados internos, decisiones del pipeline y reportes reproducibles.

## Qué significa empírico en E.C.O.

Una afirmación es empírica dentro de E.C.O. cuando puede conectarse con una señal observable del sistema.

| Concepto E.C.O. | Señal observable | Ejemplo medible | Límite responsable |
|---|---|---|---|
| Entrada informacional | texto, secuencia o paquete recibido | tamaño, formato, fuente, validez | no representa alimento real ni cuerpo humano |
| Barrera | aceptación, rechazo o cuarentena | `barrier_status` | no equivale a barrera intestinal biológica |
| Motilidad | avance, retención, descarte o cuarentena | `motility_action` | no mide motilidad humana |
| Defensa | categoría y severidad de riesgo informacional | `defense_category`, `defense_severity` | no diagnostica enfermedad |
| Estado interno | estable, vigilancia o atención | `state_after` | no representa estado mental humano |
| Recurrencia | repetición o familiaridad de patrones | conteo de repeticiones | no identifica intención humana |

## Datos admisibles para entrenamiento

Los datos de entrenamiento deben ser educativos, técnicos, sintéticos, públicos o curados manualmente. Deben describir rutas informacionales del pipeline, no personas.

## Datos no admisibles

- Datos clínicos reales.
- Historiales médicos.
- Diagnósticos humanos.
- Evaluaciones forenses.
- Inferencias sobre conciencia humana.
- Datos personales sensibles sin anonimización.

## Regla de coherencia

Cada fila entrenable debe conectar entrada, señales observables, decisión esperada y límite responsable.

## Objetivo del dataset semilla

Preparar ejemplos mínimos para entrenar, evaluar o auditar clasificadores futuros del pipeline S.N.E.-E.C.O. sin modificar reglas estables ni hacer afirmaciones indebidas.
