# AGENTS — E.C.O. (Entérico Codificador Orgánico)

## Rol del agente Codex
- Actuar como agente técnico-operativo para el repositorio E.C.O.
- Proponer e implementar cambios pequeños, testeables y reversibles.
- Mantener trazabilidad de comandos, validaciones y resultados.

## Política de ramas
- No trabajar ni integrar cambios directamente en `main`.
- Usar ramas limpias por sprint o tarea.
- Mantener commits atómicos y descriptivos.

## Validaciones obligatorias antes de finalizar
- Ejecutar validaciones técnicas y pruebas relevantes del sprint.
- Reportar comandos ejecutados y su estado (éxito/fallo/advertencia).
- Confirmar que el árbol queda limpio (`git status --short`).

## Límites responsables (obligatorios)
- No ingerir datos reales.
- No habilitar entrenamiento.
- No modificar baseline.
- No recalibrar umbrales.
- No usar datos sensibles.
- No generar afirmaciones biomédicas aplicadas.
- Mantener separación clara entre estudiar, simular, evaluar, generar hipótesis y afirmar resultados aplicados.

## Restricciones de cambios críticos
Sin autorización humana explícita, no tocar:
- baseline;
- umbrales;
- entrenamiento;
- datos reales.

## Cierre de entrega
- Dejar árbol limpio.
- Entregar resumen de cambios, comandos ejecutados y tests.
