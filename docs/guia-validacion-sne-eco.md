# Guía rápida de validación S.N.E.-E.C.O.

Esta guía resume cómo validar que el **Sistema Nervioso Entérico E.C.O.** funciona como arquitectura integrada.

## 1. Objetivo

La validación integral confirma que el pipeline procesa un lote mínimo pasando por las capas principales del S.N.E.-E.C.O.:

1. barrera / mucosa informacional,
2. plexo submucoso / sensado local,
3. plexo mientérico / motilidad,
4. defensa informacional,
5. microbiota / memoria adaptativa,
6. homeostasis,
7. eje intestino-cerebro.

El objetivo no es diagnosticar datos biomédicos. El objetivo es comprobar que la arquitectura bioinspirada está integrada, trazable y estable.

## 2. Validación completa de pruebas

Ejecuta:

```bash
cd ~/Proyectos/ECO-genoma-pipeline
source .venv/bin/activate
python -m pytest -q
```

Resultado esperado actual:

```text
105 passed
```

## 3. Validación integral S.N.E.-E.C.O.

Ejecuta:

```bash
python scripts/run_sne_eco_validation.py
```

El comando debe imprimir un reporte similar a:

```text
S.N.E.-E.C.O. VALIDATION REPORT
processed_packets: 4
state: attention
OK: S.N.E.-E.C.O. integrado funcionando.
```

## 4. Lectura de resultado

- `processed_packets`: paquetes procesados por el intestino informacional.
- `absorbed_packets`: paquetes convertidos en señal útil.
- `rejected_packets`: paquetes rechazados por defensa o barrera.
- `quarantined_packets`: paquetes retenidos por incertidumbre.
- `discarded_packets`: paquetes descartados de forma trazable.
- `duplicate_packets`: recurrencias detectadas por microbiota.
- `defense_alerts`: señales de defensa informacional.
- `state`: estado general de homeostasis.

## 5. Interpretación UX

Si el sistema responde con `OK`, significa que el circuito mínimo está funcionando:

```text
entrada → barrera → sensado → motilidad → defensa → microbiota → homeostasis → reporte
```

Si el estado es `attention`, no significa error. Significa que el lote de prueba incluye datos inválidos, cortos o duplicados para demostrar que la defensa, cuarentena y microbiota reaccionan correctamente.

## 6. Límite biomédico

S.N.E.-E.C.O. es un pipeline bioinformático educativo y bioinspirado. Sus reportes no son diagnóstico médico, no reemplazan evaluación profesional y no deben usarse para decisiones clínicas.
