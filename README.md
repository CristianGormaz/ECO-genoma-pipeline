# E.C.O. — Entérico Codificador Orgánico

![E.C.O. Validation](https://github.com/CristianGormaz/ECO-genoma-pipeline/actions/workflows/eco-validation.yml/badge.svg)

**E.C.O. — Entérico Codificador Orgánico** es un pipeline experimental, educativo y bioinspirado para organizar, validar y reportar flujos de datos genómicos, sintéticos y operativos de forma trazable.

El proyecto usa la analogía funcional del sistema digestivo y del **Sistema Nervioso Entérico** como arquitectura de software: ingesta, barrera, sensado local, motilidad, defensa, memoria, homeostasis, absorción, descarte, rollback, gobernanza y reporte.

E.C.O. no es un sistema clínico. No diagnostica, no interpreta pacientes, no calcula riesgo genético individual, no reemplaza evaluación profesional y no modela conciencia humana. Sus salidas son educativas, bioinformáticas, sintéticas u operativas según el flujo ejecutado.

## Estado actual

E.C.O. mantiene una base post-RC1 con validación automatizada, dashboard sintético fresco, Operational Gauntlet v1, gates de gobernanza y límites responsables.

S.N.E.-E.C.O. v1.2 añade observabilidad distribuida por plexos y micro-trazas, sin alterar el flujo canónico v1.0/v1.1.

Validación rápida recomendada:

```bash
make check-fast
```

Validación operativa amplia:

```bash
make eco-check
```

Estado operativo del repositorio:

```bash
make eco-status
```

La cantidad exacta de tests puede cambiar por sprint. La condición esperada es que la suite pase, el árbol esté limpio y `HEAD` esté sincronizado con `origin/main`.

## Qué hace E.C.O.

E.C.O. trabaja actualmente con rutas controladas:

1. **Secuencias y regiones.** BED/FASTA → análisis de motivos → reporte reproducible.
2. **Variantes públicas demostrativas.** TSV estilo ClinVar → lectura prudente → reporte JSON/Markdown/HTML. Esta ruta es educativa y bioinformática; no entrega diagnóstico ni conclusión clínica.
3. **Clasificación baseline.** Dataset demostrativo → modelos simples → comparación formal → reportes de métricas.
4. **Embeddings experimentales.** Contratos vectoriales placeholder/semireales para preparar comparación futura con embeddings reales.
5. **S.N.E.-E.C.O.** Arquitectura entérica computacional para trazabilidad, defensa informacional, homeostasis, decisión adaptativa y auditoría de rutas.
6. **Gobernanza operacional.** Gates, snapshots, score de madurez, auditorías de coherencia, admisión gobernada y paneles sintéticos de decisión.
7. **Observabilidad distribuida (v1.2).** Trazas por plexos, micro-trazas internas y exportación Mermaid.
8. **Operational Gauntlet v1.** Batería sintética de regresión para bordes críticos.
9. **Dashboard sintético fresco.** Recompone el governed experimental cycle durante su ejecución.

## Límites responsables

E.C.O. mantiene límites explícitos:

- sin datos genéticos personales;
- sin datos sensibles;
- sin diagnóstico;
- sin interpretación clínica individual;
- sin riesgo genético personal;
- sin entrenamiento productivo con datos sensibles;
- sin modificación de baseline sin revisión;
- sin recalibración de umbrales sin auditoría;
- sin afirmaciones biomédicas aplicadas;
- sin conciencia;
- sin libre albedrío real.

La bioinspiración S.N.E. se usa como arquitectura funcional, no como afirmación biológica literal. E.C.O. no "piensa" ni "siente"; procesa, valida, reporta y gobierna flujos experimentales.

## Quickstart

```bash
git clone https://github.com/CristianGormaz/ECO-genoma-pipeline.git
cd ECO-genoma-pipeline

python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt

make check-fast
```

Si ya tienes el entorno creado:

```bash
source .venv/bin/activate
make eco-status
make check-fast
```

En Linux, si `python` no existe fuera del entorno virtual, usa `python3` o `.venv/bin/python`.

## Comandos principales

```bash
make eco-status                  # Estado operativo del repositorio
make test                        # Suite pytest
make observability-v1-2          # Generar reportes de observabilidad v1.2
.venv/bin/python scripts/run_eco_operational_gauntlet.py  # Ejecutar Gauntlet Operacional v1
make eco-synthetic-operational-dashboard  # Dashboard operacional sintético fresco
make check-fast                  # Validación rápida local
make eco-check                   # Chequeo operativo amplio con validación global de demos sintéticas
make eco-check-clean             # Chequeo operativo + limpieza de artefactos
make sne-validation              # Validación S.N.E.-E.C.O.
make sne-state-confusion         # Auditoría de rutas confundidas
make sne-admission-governance    # Gobernanza de admisión S.N.E.-E.C.O.
```

Para el índice completo de comandos y estados:

```text
docs/operations/eco-operational-panel-index.md
```

## S.N.E.-E.C.O.

**S.N.E.-E.C.O.** convierte la metáfora del Sistema Nervioso Entérico en una arquitectura computacional verificable.

- **S.N.E.-E.C.O. v1.0/v1.1:** Flujo entérico canónico, homeostasis, defensa, rutas y reportes.
- **v1.2:** Observabilidad distribuida por plexos, micro-trazas y diagramas Mermaid.

El sistema utiliza plexos como analogía funcional para segmentar la lógica:
- **mucosa epitelial:** Ingestión, barrera física, filtrado y absorción.
- **plexo submucoso:** Sensado local y perfil sensorial.
- **plexo mientérico:** Motilidad operativa y reflejos locales.
- **sistema inmune entérico:** Señales de defensa y riesgo técnico.

### Operational Gauntlet v1

Batería de 8 checks críticos para asegurar la integridad del pipeline:
- `classifier_exact_tie_confidence`
- `classifier_raw_distance_prediction`
- `motif_rejects_plain_text_fasta`
- `homeostasis_public_paths_consistent`
- `readiness_report_does_not_claim_live_green`
- `eco_status_green_requires_clean_main_synced`
- `governed_admission_blocks_on_relevant_gates`
- `responsible_limits_not_tautological`

Documentos clave:

```text
docs/sne-eco-v1-indice-demo.md
docs/sne-eco-architecture-map.md
docs/sne-eco-claims-and-limits.md
docs/sne-eco-empirical-narrative.md
```

Reportes principales:

```text
results/sne_eco_validation_report.md
results/sne_eco_validation_report.json
```

## Gobernanza y madurez operacional

E.C.O. incluye controles para que el avance sea trazable y verificable:

- `public-source-url-admission-guard`: valida URLs públicas antes de descargar fuentes externas.
- `real-biological-data-admission-gate`: frontera futura para admisión gobernada de datos reales biológicos.
- auditoría sintética de coherencia de fórmulas y reglas de decisión;
- score de madurez operativa v1;
- panel operacional end-to-end con decisión `advance | pause | review | reject`;
- snapshots operativos y límites responsables.

### Gobernanza de admisión posterior a RC1

Comando principal:

```bash
make sne-admission-governance
```

Este comando ejecuta la cadena completa de gobernanza de admisión S.N.E.-E.C.O. posterior a `sne-eco-v1.0-rc1`: observabilidad, sonda de escenarios externos, revisión de evidencia externa, política de evidencia externa, plan de admisión estable, dry-run de admisión y comparación contra RC1.

Lectura esperada:

- Estado: yellow
- Dataset estable modificado: False
- Baseline modificado: False
- Reglas modificadas: False
- Umbrales modificados: False
- Solo dry-run: True

yellow no representa falla. `yellow` indica que existen observaciones externas retenidas por gobernanza y que ninguna evidencia externa se admite todavía al dataset estable.

Documentos recomendados:

```text
docs/operations/eco-operational-maturity-score.md
docs/operations/eco-current-capabilities-map.md
docs/operations/eco-operational-panel-index.md
docs/operations/eco-governance-evidence-review.md
docs/operations/project-map.md
docs/operations/terminal-stop-guide.md
```

## Datos sintéticos y fuentes públicas

E.C.O. diferencia entre:

```text
datos sintéticos
datos públicos demostrativos
datos reales biológicos
datos sensibles
```

El **Contrato de datos sintéticos E.C.O.** está documentado en:

```text
docs/architecture/eco-synthetic-data-contract.md
```

El uso de fuentes públicas debe mantener trazabilidad, licencia o permiso, límites interpretativos y ausencia de finalidad clínica. Las descargas configurables pasan por guardias de admisión de URL pública cuando corresponde.

## Demos y reportes

Validación global de demos sintéticas E.C.O.:

```bash
make eco-validate-synthetic-demos
```

Registro de demos sintéticas E.C.O.:

```text
docs/architecture/eco-synthetic-demo-registry.md
docs/architecture/eco-synthetic-demo-registry.json
```

Índice de demos sintéticas E.C.O.:

```text
docs/architecture/eco-synthetic-demos-index.md
```

Reporte de suite sintética:

```bash
make eco-synthetic-demos-suite-report
```

Fuente del reporte:

```text
scripts/run_eco_synthetic_demos_suite_report.py
docs/architecture/eco-synthetic-demo-registry.json
docs/operations/eco-synthetic-demos-suite-report-guide.md
```

Reporte comparativo de demos sintéticas:

```bash
make eco-synthetic-demo-comparison-report
```

Dashboard operacional sintético:

```bash
make eco-synthetic-operational-dashboard
```

Guía para agregar nuevas demos sintéticas:

```text
docs/operations/eco-add-synthetic-demo-guide.md
```

Los artefactos generados se escriben en `results/` y pueden limpiarse con:

```bash
make eco-clean-results
```

La limpieza no elimina código, documentación, tests, baseline ni umbrales. Para validar y limpiar en un solo flujo:

```bash
make eco-check-clean
```

## Operación segura del repositorio

Antes de iniciar, cerrar o retomar un sprint:

```bash
make eco-status
```

Lectura rápida:

```text
Estado green     → puedes detenerte aquí. Para iniciar un nuevo sprint, crea una rama nueva desde main antes de modificar archivos.
Estado attention → hay cambios, rama no final o desincronización; revisar antes de continuar.
Estado unknown   → no hagas commit ni push hasta diagnosticar.
Estado error     → prioriza recuperación.
```

Flujo recomendado:

```text
main limpio
→ pull --ff-only
→ rama de sprint
→ cambio acotado
→ test específico
→ suite
→ eco-check-clean
→ commit
→ PR
→ checks
→ merge
→ main
→ pull --ff-only
→ validación final
```

Documentos operativos:

```text
docs/operations/terminal-stop-guide.md
docs/operations/project-map.md
docs/operations/eco-operational-panel-index.md
docs/operations/eco-branch-decision-matrix.md
docs/operations/eco-branch-rescue-index.md
docs/operations/eco-adaptive-dataset-index.md
```

Mapa operativo del proyecto:

```text
docs/operations/project-map.md
```

## Roadmap inmediato

1. Cerrar y publicar **S.N.E.-E.C.O. v1.2** (Observabilidad Distribuida).
2. Revisar notebook Colab rastreado antes de difusión pública.
3. Fortalecer el **release checklist** y preparar changelog/tag para v1.2.
4. Planificar **v1.3 Observabilidad Temporal** (fase futura).

## Publicación responsable

El proyecto puede compartirse como arquitectura experimental y educativa. No debe presentarse como herramienta clínica, diagnóstico genético, interpretación de pacientes ni sistema biológico/consciente.

## Autoría

Proyecto desarrollado por **Cristian Gormaz**.

E.C.O. es un proyecto experimental de aprendizaje, arquitectura bioinspirada, bioinformática educativa, gobernanza operativa y trazabilidad responsable.
