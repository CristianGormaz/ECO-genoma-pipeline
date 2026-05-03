# Glosario técnico-bioinspirado — S.N.E.-E.C.O.

Este glosario explica los términos principales del proyecto **E.C.O. — Entérico Codificador Orgánico** en lenguaje simple, técnico y responsable.

## Propósito

Facilitar la lectura del pipeline S.N.E.-E.C.O. para usuarios no expertos, revisores técnicos y contexto de portafolio.

## Términos principales

| Término | Explicación simple | Uso operativo en E.C.O. |
|---|---|---|
| E.C.O. | Sistema que organiza datos usando una metáfora digestiva. | Permite observar cómo entra, cambia y se reporta la información. |
| S.N.E. | Capa inspirada en el sistema nervioso entérico. | Da lenguaje al flujo interno del pipeline. |
| Entrada | Información que ingresa al sistema. | Secuencia, paquete o caso evaluado. |
| Barrera | Filtro que decide si algo puede pasar. | Se observa con `barrier_status`. |
| Motilidad | Movimiento del dato dentro del sistema. | Se observa con `motility_action`. |
| Defensa | Respuesta ante invalidez, redundancia o tensión. | Se observa con `defense_category` y `defense_severity`. |
| Inmunidad informacional | Protección contra datos problemáticos. | Evita aceptar rutas inválidas o riesgosas. |
| Microbiota / memoria | Registro de recurrencias y familiaridad. | Ayuda a distinguir novedad, repetición útil y redundancia. |
| Interocepción | Lectura interna del estado del sistema. | Resume cómo queda el pipeline tras procesar datos. |
| Señal aferente | Señal que sube hacia un reporte entendible. | Convierte datos internos en lectura humana. |
| Homeostasis | Estado estable del flujo. | Se representa como `stable`. |
| Vigilancia | Estado donde conviene observar con atención. | Se representa como `watch`. |
| Atención | Estado de tensión defensiva o auditoría prioritaria. | Se representa como `attention`. |
| Ruta confundida | Caso donde lo observado y lo esperado no coinciden. | Se revisa en el reporte de confusión. |
| Baseline | Punto de comparación estable. | Permite detectar regresiones. |
| RC1 | Versión candidata usada como referencia. | Sirve para comparar estabilidad del pipeline. |
| Dashboard | Resumen consolidado de reportes. | Permite ver estado general del sistema. |

## Lectura responsable

Los términos bioinspirados son metáforas operativas para explicar un pipeline de datos. No describen órganos reales, no diagnostican, no tienen uso clínico, no tienen uso forense y no modelan conciencia humana.

## Comando de validación

```bash
make sne-portfolio-demo
```
