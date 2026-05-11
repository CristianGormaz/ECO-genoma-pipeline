# Plantilla de revisión de admisión estable E.C.O.

Esta plantilla sirve para revisar una pieza candidata antes de integrarla a `main`.

## Objetivo

Asegurar que cada rescate, documento, script, demo o pieza operativa sea comprensible, verificable y compatible con los límites responsables del proyecto.

## Identificación de la pieza

- Nombre de la pieza:
- Rama o archivo origen:
- Tipo de pieza: documentación / script / test / demo / reporte / índice / otro.
- Estado propuesto: draft / review_needed / candidate / accepted / blocked.
- Responsable de revisión:

## Clasificación responsable

- Permitido:
- Condicional:
- Bloqueado:

Marcar como bloqueado si incluye datos sensibles, entrenamiento no autorizado, modificación de baseline, recalibración de umbrales o afirmaciones biomédicas aplicadas.

## Preguntas de admisión

1. ¿La pieza tiene un propósito claro?
2. ¿Se entiende sin depender de contexto perdido?
3. ¿Puede validarse con comandos simples?
4. ¿Respeta los límites responsables del proyecto?
5. ¿Evita integrar ramas antiguas en bloque?
6. ¿No modifica baseline ni umbrales?
7. ¿No incorpora datos sensibles?
8. ¿No convierte metáforas bioinspiradas en conclusiones clínicas?
9. ¿Tiene test, checklist o validación mínima?
10. ¿Encaja con el estado actual de `main`?

## Decisión

- Resultado: accepted / candidate / review_needed / blocked.
- Motivo:
- Próximo paso:

## Validación mínima sugerida

```bash
make eco-status
.venv/bin/python -m pytest -q
make eco-check-clean
git status --short
git rev-list --left-right --count HEAD...origin/main
```

## Límites responsables

- sin entrenamiento;
- sin datos sensibles;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas;
- sin incorporación automática de evidencia externa;
- sin integración masiva de ramas antiguas.
