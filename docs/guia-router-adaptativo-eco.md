# Guía del router adaptativo E.C.O.

## Rol del documento

Esta guía explica el **router adaptativo E.C.O.** como pieza de arquitectura dentro del pipeline **E.C.O. — Entérico Codificador Orgánico**.

Conecta tres capas:

1. **IA aplicada:** comparación entre rutas predictivas.
2. **Arquitectura de sistemas:** selección de ruta según confianza y umbral.
3. **UX conversacional:** explicación clara de por qué el sistema eligió una ruta.

---

## 1. Idea central

El router adaptativo funciona como una **válvula de decisión**.

Primero evalúa una ruta rápida y explicable: `baseline_v3`. Si esa ruta supera el umbral de confianza, se usa como decisión principal. Si no lo supera, E.C.O. deriva hacia una ruta vectorial semi-real: `embedding_semireal`.

```text
secuencia
→ sensado básico
→ baseline_v3
→ ¿confianza suficiente?
   → sí: usar ruta explicable
   → no: derivar a embedding_semireal
→ predicción final
→ cautela operativa
→ reporte interpretable
```

---

## 2. Traducción entérica

| Capa inspirada en SNE | Función | Equivalente en E.C.O. |
|---|---|---|
| Sensado entérico | Detectar composición del contenido | Longitud, GC %, N ambiguas |
| Reflejo local | Decidir sin consultar todo el sistema | Selección automática de ruta |
| Plexo submucoso | Absorción fina y local | `baseline_v3` cuando la señal es clara |
| Plexo mientérico | Movimiento y redirección | Derivación hacia `embedding_semireal` |
| Homeostasis | Mantener estabilidad | Nivel de cautela y límite responsable |

La analogía es arquitectónica, no literal. E.C.O. toma principios funcionales del Sistema Nervioso Entérico para diseñar un flujo distribuido, trazable y prudente.

---

## 3. Comando demo principal

```bash
make adaptive-router-predict-demo
```

Salida esperada:

```text
E.C.O. ADAPTIVE ROUTER PREDICTION
=================================
Sequence ID: demo_adaptive_router
Longitud: 36
baseline_v3: regulatory | confianza=0.2615
embedding_semireal: non_regulatory | confianza=0.2461
Ruta seleccionada: baseline_v3
Predicción final: regulatory
Reflejo entérico: reflejo_explicable_rapido
Cautela: alta
Estado: OK, predicción adaptativa generada.
```

Archivos generados:

```text
results/eco_adaptive_router_prediction_demo.json
results/eco_adaptive_router_prediction_demo.md
results/eco_adaptive_router_prediction_demo.html
```

Para abrir el HTML demo:

```bash
make open-adaptive-router-predict-demo
```

---

## 4. Inferencia personalizada

La ruta personalizada permite evaluar una secuencia sin escribir el comando largo de Python.

```bash
make adaptive-router-predict SEQUENCE=ACGTCCAATGGTATAAAGGCGGGCGGAATAAAGTAC SEQUENCE_ID=prueba_cristian_001
```

También puedes ajustar parámetros:

```bash
make adaptive-router-predict \
  SEQUENCE=ACGTCCAATGGTATAAAGGCGGGCGGAATAAAGTAC \
  SEQUENCE_ID=mi_prueba_001 \
  THRESHOLD=0.20 \
  EMBEDDING_K=4 \
  DIMENSIONS=128
```

Salida personalizada:

```text
results/eco_adaptive_router_prediction_custom.json
results/eco_adaptive_router_prediction_custom.md
results/eco_adaptive_router_prediction_custom.html
```

Para abrirla:

```bash
make open-adaptive-router-predict
```

---

## 5. HTML visual del router

El reporte HTML ya no es solo un bloque técnico. Está organizado como una pantalla de lectura UX con tarjetas:

| Tarjeta | Propósito |
|---|---|
| Entrada | Muestra `sequence_id`, longitud, umbral y secuencia |
| Sensado entérico | Resume GC %, N ambiguas y composición básica |
| Rutas internas | Compara `baseline_v3` y `embedding_semireal` |
| Decisión final | Muestra ruta seleccionada y predicción final |
| Reflejo entérico | Explica el reflejo activado, brecha de confianza y cautela |
| Límite responsable | Recuerda que el resultado es demostrativo y no clínico |

Esta capa visual convierte la predicción en una explicación presentable. La idea UX es que una persona vea rápidamente:

```text
qué entró
qué sintió E.C.O.
qué rutas comparó
qué decidió
cuánta cautela exige
por qué no debe sobreinterpretarse
```

---

## 6. Campos principales del JSON

| Campo | Significado |
|---|---|
| `sequence_id` | Identificador de la secuencia evaluada |
| `sequence` | Secuencia usada para inferencia |
| `sensory_profile` | Lectura básica: longitud, GC %, N ambiguas |
| `baseline_v3` | Predicción y confianza de la ruta explicable |
| `embedding_semireal` | Predicción y confianza de la ruta vectorial |
| `selected_route` | Ruta elegida por el router |
| `final_prediction` | Predicción final emitida |
| `enteric_reflex` | Explicación entérica de la decisión |
| `limits` | Límites responsables del reporte |

---

## 7. Reflejos posibles

### `reflejo_explicable_rapido`

Se activa cuando `baseline_v3` supera el umbral operativo.

```text
La señal local fue suficiente.
E.C.O. usa la ruta explicable rápida.
```

### `reflejo_vectorial_de_derivacion`

Se activa cuando `baseline_v3` no alcanza el umbral.

```text
La señal local no fue suficiente.
E.C.O. deriva hacia una ruta vectorial semi-real.
```

---

## 8. Nivel de cautela

| Nivel | Lectura UX |
|---|---|
| `normal` | Decisión aceptable dentro del marco demostrativo |
| `media` | Conviene revisar con más datos o más evaluación |
| `alta` | Las rutas están muy cercanas; tratar como empate operativo |

En el resultado actual, la cautela aparece como `alta` porque las confianzas son muy cercanas:

```text
baseline_v3: 0.2615
embedding_semireal: 0.2461
brecha aproximada: 0.0154
```

Esto es útil: E.C.O. no oculta la incertidumbre.

---

## 9. Lectura para explicar el módulo

Versión simple:

> E.C.O. probó dos rutas. La ruta explicable ganó por poco, por eso el sistema entrega una predicción, pero marca cautela alta.

Versión técnica:

> El router compara la confianza de `baseline_v3` contra un umbral. Si supera el umbral, selecciona `baseline_v3`; si no, deriva a `embedding_semireal`. Además calcula la brecha entre confianzas para reportar cautela operativa.

Versión bioinspirada:

> El sistema actúa como un reflejo entérico: primero sensa el contenido, luego decide si absorber localmente la señal o redirigirla hacia una ruta de procesamiento más compleja.

Versión UX:

> La interfaz muestra el resultado como una historia corta: entrada, sensado, rutas comparadas, decisión final, reflejo activado y límite responsable.

---

## 10. Valor para portafolio

Este módulo demuestra que E.C.O. ya tiene:

- pipeline reproducible;
- pruebas automáticas;
- reportes JSON/Markdown/HTML;
- inferencia personalizada por Makefile;
- comparación de rutas predictivas;
- explicación de decisión;
- manejo explícito de incertidumbre;
- HTML visual con tarjetas de lectura;
- capa UX para hacer legible el resultado.

Frase sugerida:

> Diseñé un router adaptativo bioinspirado para E.C.O. que compara rutas predictivas, selecciona la salida según confianza, reporta cautela operativa y genera una explicación visual del reflejo entérico activado.

---

## 11. Próxima mejora sugerida

Crear una ruta de **inferencia por lote** para evaluar varias secuencias en un TSV:

```bash
make adaptive-router-batch INPUT=examples/mis_secuencias.tsv
```

Objetivo:

```text
leer varias secuencias
→ ejecutar router adaptativo por cada una
→ generar resumen JSON/Markdown/HTML
→ contar rutas seleccionadas
→ contar niveles de cautela
→ detectar casos donde las rutas empatan o se contradicen
```

Esta sería la siguiente pieza natural para pasar de una predicción individual a una operación más cercana a pipeline real.
