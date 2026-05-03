# Mapa de arquitectura — S.N.E.-E.C.O.

Este documento resume el flujo interno del pipeline **E.C.O. — Entérico Codificador Orgánico** usando una lectura bioinspirada, técnica y auditable.

## 1. Flujo principal

```text
entrada → barrera → motilidad → defensa → estado → reporte
```

## 2. Lectura por capas

| Capa | Rol técnico | Lectura bioinspirada | Evidencia observable |
|---|---|---|---|
| Entrada | Recibe una secuencia o paquete de datos | Ingesta informacional | `source`, payload, secuencia |
| Barrera | Decide si el paquete puede pasar | Filtro intestinal / barrera de protección | `barrier_status` |
| Motilidad | Define el movimiento operativo del dato | Avance, retención, descarte o cuarentena | `motility_action` |
| Defensa | Identifica invalidez, redundancia o tensión | Inmunidad informacional | `defense_category`, `defense_severity` |
| Estado | Resume la condición interna del sistema | Homeostasis, vigilancia o atención | `stable`, `watch`, `attention` |
| Reporte | Comunica el resultado de forma auditable | Señal aferente hacia lectura humana | JSON, Markdown, dashboard |

## 3. Estados principales

- `stable`: el flujo se mantiene sin intervención especial.
- `watch`: el flujo funciona, pero conviene observarlo.
- `attention`: existe tensión defensiva o condición que requiere auditoría.

## 4. Comando de validación

```bash
make sne-portfolio-demo
```

## 5. Límites responsables

Este mapa es educativo y experimental. No tiene uso clínico, no es diagnóstico, no es forense y no pretende modelar conciencia humana.
