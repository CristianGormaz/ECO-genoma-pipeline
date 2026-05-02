# S.N.E.-E.C.O. v1.0 RC1 — Próximos pasos seguros

## Principio rector

Después de `sne-eco-v1.0-rc1`, la prioridad es **no romper estabilidad**.

El módulo alcanzó:

```text
153 tests passing
Rutas confundidas: 0
Rutas confundidas de recurrencia: 0
```

Por lo tanto, los próximos avances deben separar claramente:

1. cambios seguros de documentación/observabilidad;
2. cambios técnicos experimentales;
3. cambios que podrían afectar el baseline estable.

## Qué no tocar inmediatamente

No modificar todavía:

- `adaptive_state_baseline.py`;
- dataset extendido de transición;
- reglas de `recurrence_guard`;
- umbrales de homeostasis;
- lógica de defensa central.

Cualquier cambio en esas piezas debe ir en branch experimental, con comparación contra el tag `sne-eco-v1.0-rc1`.

## Sprint recomendado: SNE-13 — Portfolio packaging

Objetivo: convertir el hito en material profesional reutilizable.

Entregables:

- resumen de portafolio;
- textos para LinkedIn/CV/GitHub;
- explicación para entrevista;
- diagrama simple de arquitectura;
- capturas o reportes del estado `153 passed / 0 rutas confundidas`.

Riesgo: bajo.  
No modifica lógica del sistema.

## Sprint recomendado: SNE-14 — Observability dashboard

Objetivo: crear visualizaciones sin alterar la lógica estable.

Posibles vistas:

- conteo de estados `stable/watch/attention`;
- rutas por decisión final;
- recurrencias por `source`;
- métricas de confusión;
- estado de estabilidad del RC1;
- lectura tipo semáforo.

Regla: el dashboard debe leer reportes JSON existentes, no recalibrar reglas.

Riesgo: bajo/medio.  
Debe operar como capa externa.

## Sprint recomendado: SNE-15 — Comparison against RC1

Objetivo: crear un comando que compare cualquier branch futuro contra `sne-eco-v1.0-rc1`.

Preguntas que debería responder:

- ¿aumentaron rutas confundidas?;
- ¿reapareció `default_state`?;
- ¿cambió la auditoría de recurrencia?;
- ¿bajó el número de tests?;
- ¿se modificaron documentos de límite responsable?

Riesgo: bajo.  
Fortalece control de regresión.

## Sprint técnico futuro: SNE-16 — External scenario expansion

Solo después de empaquetar y observar.

Objetivo: agregar nuevos escenarios sintéticos o semirreales, pero sin alterar el RC1.

Regla clave:

```text
El RC1 queda como línea base congelada.
Todo escenario nuevo se compara contra ese hito.
```

Riesgo: medio/alto.  
Puede generar nuevas rutas confundidas, lo cual no sería fracaso si queda bien documentado.

## Estrategia recomendada

Orden seguro:

```text
SNE-13 → empaquetar portafolio
SNE-14 → dashboard de observabilidad
SNE-15 → comparación contra RC1
SNE-16 → expansión controlada de escenarios
```

## Criterio de estabilidad futura

Todo sprint posterior debe reportar:

```text
Tests actuales
Rutas confundidas actuales
Recurrencias confundidas actuales
Diferencia contra sne-eco-v1.0-rc1
Riesgo de regresión
```

## Cierre

El valor del RC1 no está solo en haber llegado a cero rutas confundidas. Está en haber creado una base reproducible, explicable y defendible para avanzar sin perder trazabilidad.
