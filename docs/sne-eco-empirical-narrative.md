# S.N.E.-E.C.O. — Narrativa empírica del pipeline

## Propósito

Este documento resume la evolución empírica del pipeline **E.C.O. — Entérico Codificador Orgánico**, específicamente su capa **S.N.E.-E.C.O.** para transición adaptativa de estados.

La intención no es afirmar que el sistema modele conciencia humana, biología clínica o neurogastroenterología real. La intención es documentar una arquitectura computacional bioinspirada que usa metáforas entéricas como marco de diseño para procesar, auditar y estabilizar rutas informacionales.

## Límite responsable

Este pipeline es educativo y experimental. No tiene uso clínico, diagnóstico, forense ni biomédico. Sus términos digestivos, entéricos y homeostáticos funcionan como analogías técnicas para organizar decisiones de software.

## Hipótesis de diseño

El sistema parte de una hipótesis bioinspirada simple:

> Un flujo de datos puede tratarse como un tránsito digestivo: se ingiere, se filtra, se sensa, se absorbe, se descarta, se pone en cuarentena, se reconoce por memoria y se estabiliza mediante homeostasis operativa.

Desde esta perspectiva, una secuencia no se evalúa solo como válida o inválida. También se evalúa por su efecto sobre el equilibrio del sistema.

## Capas funcionales

El pipeline se organiza como una arquitectura entérica computacional:

| Capa | Rol técnico | Analogía bioinspirada |
|---|---|---|
| Ingestión | Entrada de payloads | Ingreso de alimento/dato |
| Filtrado | Validación inicial | Barrera epitelial/mucosa |
| Sensado local | Lectura de señales del payload | Plexo submucoso |
| Motilidad | Decisión de tránsito | Movimiento intestinal |
| Microbiota | Memoria de exposición y redundancia | Microbiota informacional |
| Defensa | Invalidación, ambigüedad, redundancia | Respuesta inmune local |
| Homeostasis | Estado operativo agregado | Equilibrio del sistema |
| Baseline adaptativo | Predicción de transición de estado | Reflejo aprendido/auditable |
| Confusión y cobertura | Diagnóstico de fallos | Auditoría del tránsito |
| Estabilidad | Prevención de regresión | Mantenimiento homeostático |

## Evolución empírica por sprints

### SNE-03 — Variantes dirigidas

Se agregaron variantes sintéticas dirigidas para cubrir rutas confundidas detectadas por el reporte de confusión.

Focos abordados:

- payloads demasiado cortos;
- payloads inválidos;
- payloads ambiguos con `N`;
- payloads recurrentes o duplicados.

Resultado observado:

```text
Rutas confundidas: 5 → 2
```

Lectura: el sistema mejoró al recibir experiencias digestivas más representativas, sin modificar la defensa central.

### SNE-04 — Baseline jerárquico digestivo

El baseline dejó de depender solo de una clave exacta.

Orden de decisión incorporado:

```text
feature_key → digestive_key → defense_key → default_state
```

Resultado observado:

- desaparece el uso prematuro de `default_state`;
- una ruta antes desconocida pasa a ser interpretada por familia digestiva.

Lectura: el sistema empezó a reconocer familias de rutas, no solo rutas idénticas.

### SNE-05 — Resolución por confianza homeostática

Se agregó una proyección homeostática como desempate cuando una regla de bajo soporte contradice la presión esperada del sistema.

Se usaron señales previas como:

- `absorption_ratio_before`;
- `immune_load_before`;
- `quarantine_ratio_before`;
- `final_decision`.

Resultado observado:

```text
Rutas confundidas: 2 → 1
```

Lectura: el sistema empezó a usar equilibrio operativo, no solo memoria de rutas.

### SNE-06 — Auditoría de recurrencia

Se creó un script específico para auditar rutas recurrentes, duplicadas o redundantes.

Salida principal:

```text
Filas de recurrencia evaluadas: 7
Rutas confundidas de recurrencia: 1
```

La auditoría aisló el caso residual:

```text
recurrent_valid_d
observed: watch
predicted: attention
rule: digestive_key
decision: discard_duplicate
defense: redundant_payload/low
```

Lectura: el problema no era la redundancia en general, sino cómo se interpreta una repetición baja cuando el sistema ya viene desde `watch`.

### SNE-07 — Recurrence guard

Se agregó una regla delimitada para evitar escalar redundancia baja desde `watch` hacia `attention` cuando no hay carga crítica.

Condición conceptual:

```text
si final_decision == discard_duplicate
y defense_category == redundant_payload
y defense_severity == low
y state_before == watch
y immune_load_before <= 0.4
y quarantine_ratio_before <= 0.3
entonces favorecer watch
```

Resultado observado:

```text
Rutas confundidas: 1 → 0
Rutas confundidas de recurrencia: 1 → 0
```

Lectura: no toda recurrencia es inflamación. Algunas repeticiones deben mantenerse en vigilancia.

### SNE-08 — Suite de estabilidad

Se agregó una suite de regresión para proteger el estado alcanzado.

La suite verifica que:

- no reaparezcan rutas confundidas;
- no vuelva el fallback inesperado a `default_state`;
- no aparezcan predicciones incorrectas en holdout extendido;
- la auditoría de recurrencia permanezca limpia.

Resultado observado:

```text
153 passed
Rutas confundidas: 0
Rutas confundidas de recurrencia: 0
```

Lectura: el sistema dejó de enfocarse en corregir errores puntuales y pasó a proteger estabilidad.

## Resultado consolidado

Evolución resumida:

```text
Tests: 150 → 153
Rutas confundidas: 5 → 2 → 1 → 0
Recurrencia confundida: 1 → 0
Default_state inesperado: eliminado en rutas confundidas
```

## Interpretación arquitectónica

El pipeline pasó por cuatro estados de madurez:

1. **Cobertura**: agregar variantes para que el sistema observe más casos.
2. **Generalización jerárquica**: reconocer familias digestivas y defensivas.
3. **Autorregulación**: usar presión homeostática como criterio de desempate.
4. **Estabilidad**: bloquear regresiones mediante pruebas específicas.

## Lectura UX conversacional

Para explicar el sistema a personas no técnicas, puede describirse así:

> E.C.O. funciona como un intestino informacional. No solo revisa si un dato entra o no entra; observa cómo ese dato afecta el equilibrio del sistema. Si el dato es útil, lo absorbe. Si es ambiguo, lo pone en cuarentena. Si es inválido, lo rechaza. Si es repetido, lo reconoce. Y si la repetición no es peligrosa, no sobrerreacciona.

## Valor técnico

Este avance deja una base útil para:

- explicar el proyecto en portafolio;
- justificar decisiones de arquitectura;
- demostrar iteración empírica con tests;
- separar metáfora bioinspirada de afirmaciones clínicas;
- preparar futuros módulos de evaluación, documentación y visualización.

## Próximo paso recomendado

Después de esta documentación, el siguiente avance debería ser:

```text
SNE-10 — README integration and reproducible commands
```

Objetivo: integrar esta narrativa al README principal y dejar comandos reproducibles para que cualquier persona pueda ejecutar:

```bash
python -m pytest -q
make sne-state-confusion
python scripts/run_sne_eco_recurrence_audit.py
```

## Cierre

E.C.O. no debe presentarse como un sistema biológico real ni como una conciencia artificial. Su valor actual está en ser una arquitectura de software bioinspirada, auditable y progresivamente estabilizada.

La metáfora entérica aquí no reemplaza a la ciencia biológica: funciona como lenguaje de diseño para construir software que procesa información con filtrado, memoria, defensa, equilibrio y estabilidad.
