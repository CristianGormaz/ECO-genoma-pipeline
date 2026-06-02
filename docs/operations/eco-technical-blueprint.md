# E.C.O. — Plano Técnico

## Estado del documento

- Documento técnico de orientación.
- No ejecutable.
- No modifica arquitectura por sí mismo.
- no habilita datos reales.
- No reemplaza tests, reportes ni dashboard.

## Propósito

Este plano muestra cómo está construido E.C.O. y cómo se relacionan sus piezas principales. Sirve para leer la arquitectura, ubicar capas, entender responsabilidades y distinguir qué pertenece al plano técnico frente al plano operativo.

## Definición breve de E.C.O.

E.C.O. — Entérico Codificador Orgánico — es un sistema bioinspirado de digestión de información. Su objetivo es recibir información cruda, fragmentarla, filtrarla, transformarla, evaluarla, absorber conocimiento útil, descartar ruido y generar retroalimentación verificable.

## Principio bioinspirado

E.C.O. usa una inspiración funcional en el Sistema Nervioso Entérico para organizar flujos de información.

Esta inspiración no debe leerse como afirmación biológica literal. E.C.O. no es un organismo biológico, no modela conciencia, no afirma autonomía real y no afirma libre albedrío real. El sistema debe presentarse como arquitectura experimental, documental y verificable.

## Capas técnicas mínimas

- Ingesta: entrada controlada de información o manifiestos descriptivos.
- Fragmentación: separación conceptual de entradas en unidades revisables.
- Filtrado: descarte o retención según reglas y límites declarados.
- Transformación: conversión de entradas en señales, reportes o estructuras auditables.
- Evaluación: revisión de estado, riesgo, evidencia, consistencia y límites.
- Absorción: retención de conocimiento útil dentro del alcance permitido.
- Retroalimentación: generación de reportes, métricas y recomendaciones verificables.
- Descarte: rechazo de ruido, redundancia, residuos informacionales o entradas fuera de alcance.

## Mapa funcional SNE → E.C.O.

- Plexo de Auerbach: referencia para flujo, tránsito y coordinación del pipeline.
- Plexo de Meissner: referencia para evaluación, secreción, preparación y regulación local.
- Sistema inmune intestinal: referencia para detección de anomalías, sesgos, entradas peligrosas o corrupción.
- Eje intestino-cerebro: referencia para telemetría, métricas, reportes y control global.
- Desecho: referencia para descarte de ruido, redundancia y residuos informacionales.

## Componentes técnicos actuales

Componentes detectados en el repositorio:

- Documentos de gobernanza en `docs/operations/`, incluyendo manuales, protocolos, registros, snapshots, matrices y guías de revisión.
- Reportes generados en `results/` cuando se ejecutan validaciones o demos sintéticas.
- Dashboard sintético operacional existente, asociado a `scripts/run_eco_synthetic_operational_dashboard.py`.
- Tests contractuales en `tests/`, orientados a asegurar estructura documental, límites responsables y comportamiento de scripts.
- Validaciones operativas existentes mediante pytest, `eco-status`, `eco-check-clean` y validadores de manifiestos o contratos sintéticos.
- Scripts existentes en `scripts/`, incluyendo inspección de estado, validadores, reportes, dashboard sintético, ciclo experimental gobernado y dry-run documental de admisión.
- Mapas e índices existentes en `docs/operations/`, como `project-map.md`, `eco-operational-panel-index.md` y `eco-current-capabilities-map.md`.

Este plano no inventa módulos nuevos ni declara capacidades fuera de las que ya están presentes en el repositorio.

## Límites técnicos

- no procesar datos reales en este sprint;
- no entrenar modelos;
- no modificar baseline;
- no recalibrar umbrales;
- no crear compuertas funcionales nuevas;
- no crear scripts;
- no afirmar preparación para datos reales;
- no afirmar uso clínico;
- no afirmar interpretación biomédica aplicada.

## Cómo leer este plano

El plano técnico sirve para entender la construcción de E.C.O.: capas, analogías, componentes, límites y relaciones principales. No es una guía paso a paso para operar el repositorio, ejecutar validaciones o cerrar un sprint.

## Relación con el plano operativo

El plano operativo es el documento complementario para saber cómo entrar, avanzar, pausar, validar y cerrar ciclos sin romper el sistema. Este plano explica la construcción; el plano operativo explica cómo trabajar con esa construcción.
