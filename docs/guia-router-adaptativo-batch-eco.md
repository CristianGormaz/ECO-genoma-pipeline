# Guía de inferencia por lote con router adaptativo E.C.O.

## Rol del documento

Esta guía explica cómo usar la ruta de **inferencia por lote** del router adaptativo dentro del pipeline **E.C.O. — Entérico Codificador Orgánico**.

El objetivo es evaluar varias secuencias en un archivo TSV y obtener un reporte JSON/Markdown/HTML con:

- secuencias procesadas;
- secuencias rechazadas;
- ruta seleccionada por caso;
- predicción final;
- nivel de cautela;
- contradicciones internas entre rutas;
- homeostasis del lote;
- lectura UX del lote.

---

## 1. Archivo de entrada

El TSV debe incluir al menos la columna `sequence`.

Formato recomendado:

```text
sequence_id	sequence	description
lote_001	ACGTCCAATGGTATAAAGGCGGGCGGAATAAAGTAC	secuencia demo con motivos regulatorios
lote_002	TTTTACACACACGTTTACACACACGTTTACACACAC	secuencia repetitiva demo
lote_003	ACGTXYZCCAAT	secuencia inválida para probar rechazo inmune informacional
```

Archivo demo incluido:

```text
examples/demo_adaptive_router_batch.tsv
```

---

## 2. Comando Makefile recomendado

```bash
make adaptive-router-batch
make open-adaptive-router-batch
```

También puedes usar otro TSV:

```bash
make adaptive-router-batch BATCH_INPUT=examples/mi_lote_router.tsv
```

---

## 3. Comando directo

```bash
python scripts/run_eco_adaptive_router_batch.py \
  --batch-input examples/demo_adaptive_router_batch.tsv \
  --threshold 0.20 \
  --embedding-k 4 \
  --dimensions 128 \
  --output-json results/eco_adaptive_router_batch_report.json \
  --output-md results/eco_adaptive_router_batch_report.md \
  --output-html results/eco_adaptive_router_batch_report.html
```

Salida esperada:

```text
E.C.O. ADAPTIVE ROUTER BATCH
============================
Entrada batch: examples/demo_adaptive_router_batch.tsv
Secuencias totales: 3
Procesadas: 2
Rechazadas: 1
Contradicciones internas: 1
Cautela alta: 2
Homeostasis: atencion
Riesgo operativo: 0.6667
Estado: OK, inferencia por lote generada.
```

---

## 4. Lectura entérica del batch

| Elemento | Lectura E.C.O. |
|---|---|
| Secuencias procesadas | Datos que cruzaron la barrera epitelial informacional |
| Secuencias rechazadas | Activación del reflejo inmune de rechazo |
| Contradicciones internas | `baseline_v3` y `embedding_semireal` no coinciden |
| Cautela alta | Las rutas están demasiado cercanas o el caso requiere revisión |
| Ruta seleccionada | Reflejo local activado por el router |
| Homeostasis | Lectura agregada de estabilidad del lote |

---

## 5. Homeostasis del lote

La homeostasis convierte métricas sueltas en una señal UX de estabilidad:

```text
estable  → el lote no muestra alertas relevantes
atencion → el lote es procesable, pero requiere revisión
critico  → el lote muestra inestabilidad alta
idle     → no hay secuencias para evaluar
```

La lectura se calcula con tres señales:

| Señal | Qué representa |
|---|---|
| Tasa de rechazo | Calidad mínima de entrada |
| Tasa de contradicción | Conflicto entre rutas internas |
| Tasa de cautela alta | Baja separación o empate operativo |

En el lote demo, el estado esperado es:

```text
Homeostasis: atencion
```

Porque hay:

```text
1 secuencia rechazada
1 contradicción interna
2 casos con cautela alta
```

Lectura simple:

> El lote se puede procesar, pero no debe leerse como estable. Primero revisa rechazos, contradicciones y casos de cautela alta.

---

## 6. Por qué esto importa

La inferencia individual sirve para probar una secuencia.

La inferencia por lote sirve para observar **patrones del sistema**:

```text
¿cuántas secuencias pasan la barrera?
¿cuántas se rechazan?
¿qué ruta domina?
¿dónde aparecen contradicciones?
¿cuánta cautela pide el sistema?
¿el lote completo está estable, en atención o crítico?
```

Esto permite pasar de una predicción aislada a una lectura de comportamiento del pipeline.

---

## 7. Valor para portafolio

Este módulo demuestra que E.C.O. ya puede:

- recibir múltiples secuencias;
- validar entradas;
- rechazar datos inválidos;
- comparar rutas predictivas;
- reportar contradicciones internas;
- generar salida JSON/Markdown/HTML;
- comunicar incertidumbre de forma legible;
- emitir una lectura de homeostasis del lote;
- funcionar como pipeline reproducible.

Frase sugerida:

> Implementé una ruta de inferencia por lote para E.C.O. que evalúa múltiples secuencias con un router adaptativo, detecta rechazos y contradicciones internas, calcula homeostasis del lote y genera reportes interpretables para análisis técnico y presentación UX.

---

## 8. Límite responsable

Este flujo es demostrativo. No es diagnóstico clínico, no es benchmark científico y no reemplaza validación externa.

La salida debe leerse como una prueba de arquitectura y experiencia explicable, no como conclusión biológica definitiva.
