# E.C.O. — Contexto operativo del agente especializado

Este documento fija el contexto de trabajo para continuar el desarrollo de **E.C.O. — Entérico Codificador Orgánico** desde una combinación de roles:

- IA aplicada;
- arquitectura de sistemas;
- UX conversacional;
- neurogastroenterología computacional;
- arquitectura de software bioinspirada;
- bioinformática.

## 1. Estado actual reconocido

E.C.O. ya no debe tratarse como una idea suelta. El sistema tiene una arquitectura funcional basada en el metabolismo informacional:

```text
dato crudo → barrera → sensor local → motilidad → defensa → microbiota/memoria → absorción → homeostasis → reporte eje intestino-cerebro
```

El repositorio ya contiene pruebas, scripts, reportes y documentación suficientes para tratar el proyecto como un pipeline reproducible y defendible.

Estado técnico relevante:

```text
Rama de trabajo: eco-sne-confusion-command
Base estable: S.N.E.-E.C.O. v1.0 RC1
Criterio central: no romper estabilidad
Objetivo inmediato: avanzar por capas externas antes de tocar reglas internas
```

## 2. Principio rector

La arquitectura entérica de E.C.O. debe usarse como **metáfora computacional verificable**, no como afirmación clínica.

E.C.O. puede:

- validar datos;
- filtrar señales;
- detectar redundancia;
- clasificar rutas informacionales;
- producir reportes explicables;
- comparar estados del pipeline;
- generar observabilidad y trazabilidad.

E.C.O. no debe:

- diagnosticar enfermedades;
- reemplazar evaluación médica;
- afirmar causalidad biológica sin evidencia;
- confundir metáfora digestiva con fisiología real;
- modificar reglas estables sin pruebas de regresión.

## 3. Traducción bioinspirada

| Elemento biológico | Traducción E.C.O. | Función computacional |
|---|---|---|
| Mucosa intestinal | Barrera informacional | Permite, limita o rechaza datos |
| Plexo submucoso | Sensor local | Extrae métricas del payload |
| Plexo mientérico | Motilidad | Decide avance, cuarentena, lote o rechazo |
| Microbiota | Memoria adaptativa | Reconoce recurrencias y evita redundancia |
| Sistema inmune | Defensa informacional | Detecta invalidez, ambigüedad o riesgo |
| Homeostasis | Estado del flujo | Resume estabilidad, atención o vigilancia |
| Eje intestino-cerebro | Reporte comunicable | Convierte métricas internas en lenguaje útil |

## 4. Enfoque empírico mínimo

Cada avance nuevo debe responder cinco preguntas:

```text
1. ¿Qué dato entra?
2. ¿Qué módulo lo transforma?
3. ¿Qué métrica cambia?
4. ¿Qué reporte se genera?
5. ¿Qué prueba evita regresión?
```

Si una idea no puede responder esas cinco preguntas, todavía está en fase conceptual y no debe tocar el núcleo.

## 5. UX conversacional esperada

La interfaz conversacional de E.C.O. debe funcionar como traductor entre tres niveles:

```text
Nivel técnico: tests, scripts, JSON, métricas, rutas.
Nivel biológico-metafórico: barrera, motilidad, microbiota, homeostasis.
Nivel usuario: explicación clara, breve, accionable y no clínica.
```

Regla de respuesta UX:

```text
primero estado → luego causa → luego acción sugerida → luego límite responsable
```

Ejemplo:

```text
Estado: el flujo está en vigilancia.
Causa: aumentaron los paquetes retenidos en cuarentena.
Acción: revisar longitud y ambigüedad de las secuencias.
Límite: esto describe calidad de datos, no una condición médica.
```

## 6. Sprint recomendado: SNE-21 — Puente neurogastrocomputacional seguro

Objetivo: conectar el lenguaje de neurogastroenterología computacional con la arquitectura E.C.O. sin tocar el baseline estable.

### Entregables

1. Documento de correspondencias entre conceptos:
   - interocepción;
   - señal aferente;
   - predicción/error;
   - homeostasis/allostasis;
   - motilidad;
   - microbiota/memoria;
   - defensa/inmunidad informacional.

2. Script de reporte conversacional:
   - entrada: JSON de resultados existentes;
   - salida: explicación por niveles;
   - regla: no recalibrar modelos ni modificar decisiones internas.

3. Pruebas pytest:
   - confirma que el script ejecuta;
   - confirma que incluye límite responsable;
   - confirma que no afirma diagnóstico;
   - confirma que interpreta estados `stable`, `watch`, `attention`.

4. Ejemplo de salida para portafolio:
   - versión técnica;
   - versión usuario general;
   - versión entrevista laboral.

## 7. Orden de ejecución sugerido

```text
Paso 1: crear documento de correspondencias neurogastrocomputacionales.
Paso 2: crear script lector de reportes existentes.
Paso 3: generar salida conversacional en Markdown.
Paso 4: agregar pruebas de límites responsables.
Paso 5: comparar contra RC1 antes de proponer merge.
```

## 8. Criterio de aceptación

El sprint se considera correcto solo si:

```text
pytest pasa completo
no cambian reglas de baseline
no aumentan rutas confundidas
el reporte explica sin diagnosticar
la metáfora biológica queda marcada como arquitectura, no medicina
```

## 9. Próxima acción concreta

Crear el archivo:

```text
scripts/run_sne_eco_neurogastro_context_report.py
```

Debe leer resultados ya existentes y producir:

```text
results/sne_eco_neurogastro_context_report.md
results/sne_eco_neurogastro_context_report.json
```

Este será el puente entre E.C.O. como pipeline bioinformático y E.C.O. como sistema explicable de arquitectura entérica.
