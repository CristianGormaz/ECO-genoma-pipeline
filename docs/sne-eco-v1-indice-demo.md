# S.N.E.-E.C.O. v1.0 — Índice técnico y demo

> Sistema Nervioso Entérico para E.C.O. — Entérico Codificador Orgánico.
>
> Este módulo traduce fundamentos del sistema nervioso entérico real a una arquitectura computacional bioinspirada para validar, sentir, mover, defender, recordar y reportar el flujo de datos dentro del pipeline E.C.O.

## 1. Estado de la versión

**Versión:** S.N.E.-E.C.O. v1.0  
**Estado:** funcional, testeado y demostrable  
**Validación esperada:** `106 passed`  
**Demo principal:** `make sne-validation`

Artefactos generados por la demo:

```text
results/sne_eco_validation_report.md
results/sne_eco_validation_report.json
```

## 2. Mapa de órganos computacionales

| Órgano S.N.E.-E.C.O. | Archivo | Analogía entérica | Función computacional |
|---|---|---|---|
| Barrera informacional | `src/eco_core/barrier.py` | Mucosa / barrera intestinal | Permite, limita o rechaza paquetes antes de la absorción. |
| Sensor local | `src/eco_core/sensor_local.py` | Plexo submucoso | Genera perfil sensorial del payload: longitud, GC%, N%, invalidez, duplicado, peso. |
| Motilidad | `src/eco_core/motility.py` | Plexo mientérico | Decide tránsito: avanzar, cuarentena, lote, descarte duplicado o descarte inmune. |
| Microbiota | `src/eco_core/microbiota.py` | Microbiota intestinal | Registra exposiciones, detecta recurrencia y evita absorber redundancia. |
| Defensa | `src/eco_core/defense.py` | Sistema inmune intestinal | Clasifica señales de invalidez, ambigüedad, redundancia o retención. |
| Homeostasis | `src/eco_core/homeostasis.py` | Equilibrio intestinal | Resume el estado general del flujo procesado. |
| Eje intestino-cerebro | `src/eco_core/gut_brain_axis.py` | Comunicación intestino-cerebro | Convierte métricas internas en reporte legible para usuario/sistema. |
| Orquestador | `src/eco_core/enteric_orchestrator.py` | Sistema entérico coordinado | Integra los órganos y mantiene trazabilidad en `EcoPacket`. |

## 3. Flujo operativo

```text
Ingesta
  ↓
Barrera / mucosa informacional
  ↓
Sensado submucoso
  ↓
Motilidad mientérica
  ↓
Defensa informacional
  ↓
Decisión local
  ↓
Absorción / cuarentena / descarte
  ↓
Microbiota informacional
  ↓
Homeostasis
  ↓
Reporte eje intestino-cerebro
```

## 4. Demo reproducible

Desde la raíz del repositorio:

```bash
cd ~/Proyectos/ECO-genoma-pipeline
git checkout main
git pull origin main
source .venv/bin/activate
python -m pytest -q
make sne-validation
ls -lh results/sne_eco_validation_report.*
```

Resultado esperado:

```text
106 passed
results/sne_eco_validation_report.md
results/sne_eco_validation_report.json
```

El reporte de validación procesa un lote mínimo con cuatro casos:

```text
valid_sequence
invalid_sequence
short_sequence
duplicate_sequence
```

Y produce una lectura de estado similar a:

```text
processed_packets: 4
absorbed_packets: 1
rejected_packets: 1
quarantined_packets: 1
discarded_packets: 2
duplicate_packets: 1
defense_alerts: 0
state: watch
```

## 5. Lectura UX del reporte

El estado `watch` significa que el sistema funciona, pero observa señales mixtas: hay absorción, rechazo, cuarentena y recurrencia. Esto es útil en una demo porque prueba que el sistema no responde siempre igual; regula el flujo según la calidad del dato.

Interpretación simple:

- Si el dato es válido, avanza hacia absorción.
- Si contiene caracteres no válidos, se descarta por defensa.
- Si es corto o ambiguo, se retiene en cuarentena.
- Si ya fue visto, la microbiota evita absorberlo como novedad.

## 6. Uso para portafolio técnico

Este módulo demuestra competencias concretas:

- Arquitectura modular bioinspirada.
- Diseño de pipeline trazable.
- Validación automatizada con `pytest`.
- UX conversacional aplicada a reportes técnicos.
- Separación entre procesamiento interno y salida comunicable.
- Uso responsable de metáforas biomédicas sin convertirlas en diagnóstico.

Texto breve sugerido para portafolio:

> Diseñé e implementé S.N.E.-E.C.O., una capa bioinspirada en el sistema nervioso entérico para validar y orquestar datos en un pipeline genómico. El módulo integra barrera informacional, sensado local, motilidad, microbiota, defensa, homeostasis y reporte intestino-cerebro, con validación automatizada y artefactos Markdown/JSON reproducibles.

## 7. Comandos útiles

```bash
make test             # Ejecuta la suite completa de pruebas
make sne-validation   # Genera reporte S.N.E.-E.C.O. en Markdown y JSON
make clean            # Limpia artefactos temporales y reportes generados
```

## 8. Criterios de cierre v1.0

S.N.E.-E.C.O. v1.0 se considera cerrado cuando:

- La suite completa pasa sin errores.
- `make sne-validation` genera Markdown y JSON.
- El reporte incluye estado homeostático y eje intestino-cerebro.
- El README o la documentación apunta al módulo.
- El límite ético/biomédico está explícito.

## 9. Límites éticos y biomédicos

Sistema bioinformático educativo y bioinspirado: S.N.E.-E.C.O. no diagnostica, no interpreta clínicamente, no predice enfermedad y no reemplaza análisis profesional. Sus analogías con mucosa, plexos, microbiota, defensa y eje intestino-cerebro son metáforas arquitectónicas para organizar el flujo de datos.

## 10. Roadmap v1.1

Próximos pasos sugeridos:

1. Integrar `make sne-validation` dentro de `make portfolio-demo`.
2. Crear versión HTML del reporte S.N.E.-E.C.O.
3. Agregar visualización simple del flujo entérico.
4. Permitir lote externo configurable para validación S.N.E.
5. Añadir resumen ejecutivo automático para portafolio.
6. Documentar casos reales/no reales y reglas de uso responsable.

## 11. Resumen final

S.N.E.-E.C.O. v1.0 convierte el argumento entérico del proyecto en una arquitectura comprobable. Ya no es solo una metáfora: es un conjunto de módulos, pruebas, comandos y artefactos que muestran cómo E.C.O. ingiere, filtra, siente, mueve, defiende, recuerda y comunica el estado de sus datos.
