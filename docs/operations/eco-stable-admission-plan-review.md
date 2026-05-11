# Revisión de rama: eco-sne-stable-admission-plan

Este documento resume la inspección segura de la rama antigua `eco-sne-stable-admission-plan`.

## Objetivo

Identificar qué partes de la rama pueden rescatarse sin integrar cambios antiguos en bloque.

## Estado de la revisión

- Tipo de sprint: documental / auditoría.
- Clasificación: permitido.
- Acción realizada: inspección de commits, archivos y diff contra `main`.
- No se hizo merge.
- No se hizo cherry-pick.
- No se modificó baseline.
- No se recalibraron umbrales.
- No se incorporó evidencia externa automáticamente.

## Lectura de la rama

La rama contiene una secuencia amplia de trabajo S.N.E.-E.C.O., incluyendo:

- plan de admisión de escenarios estables;
- pruebas del plan de admisión;
- script de admisión estable;
- política de evidencia externa;
- revisión de evidencia externa;
- expansión de escenarios externos;
- comparación contra RC1;
- dashboard de observabilidad;
- empaquetado de portfolio;
- documentación pública y técnica.

## Riesgo detectado

La rama no debe integrarse completa. El diff contra `main` muestra cambios amplios en workflows, Makefile, README, datos, documentación, scripts, tests y resultados generados.

La rama parece contener trabajo valioso, pero mezclado con piezas antiguas que podrían retroceder el estado actual del repositorio.

## Áreas sensibles

No rescatar sin revisión separada:

- `data/governance/`;
- `data/training/`;
- scripts de evaluación o entrenamiento;
- cambios de CI;
- cambios grandes en Makefile;
- resultados generados en `results/`;
- cualquier pieza que implique baseline, umbral, entrenamiento o evaluación aplicada.

## Piezas potencialmente rescatables

Rescatar solo en PRs pequeños:

1. Documento conceptual del plan de admisión estable.
2. Checklist de admisión de escenarios.
3. Glosario operativo si existe contenido vigente.
4. Resumen público no clínico y no diagnóstico.
5. Test documental aislado si solo valida límites responsables.

## Decisión recomendada

No integrar la rama `eco-sne-stable-admission-plan` como bloque.

El siguiente sprint lógico debería rescatar una sola pieza documental: el plan de admisión estable, si todavía encaja con `main`.

## Comandos seguros de inspección usados

```bash
git log --oneline main..eco-sne-stable-admission-plan
git diff --name-only main..eco-sne-stable-admission-plan
git diff --stat main..eco-sne-stable-admission-plan
```

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas;
- sin incorporación automática de evidencia externa;
- sin integración masiva de ramas antiguas.
