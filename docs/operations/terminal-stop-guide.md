# Guía operativa — Cuándo detenerse en terminal

## Estado

Estado: operativo.

Clasificación: permitido.

Esta guía ayuda a decidir qué hacer cuando la terminal vuelve al prompt del proyecto.

## Señal verde

Puedes detenerte, cerrar la terminal o iniciar un nuevo sprint si se cumplen estas condiciones:

- Estás en main.
- La rama está actualizada con origin/main.
- git status muestra árbol limpio.
- pytest termina con passed.
- El PR anterior fue mergeado.

## Señal amarilla

No inicies otro sprint todavía si:

- Hay un PR abierto con checks pendientes.
- Estás en una rama experimental.
- GitHub aún no confirma checks verdes.

## Señal roja

No hagas commit ni merge si:

- Hay tests fallando.
- git status muestra archivos modificados o no rastreados que no entiendes.
- Estás en main y quieres modificar código directamente.
- Hay conflictos de merge.

## Regla simple

Si ves el prompt de la terminal y el repo está limpio, no estás obligado a hacer nada.

Puedes cerrar la terminal con seguridad cuando:

```text
nada para hacer commit, el árbol de trabajo está limpio
pytest: passed
```

## Límite responsable

Esta guía es operativa. No modifica datos, no ejecuta entrenamiento, no cambia baseline, no recalibra umbrales y no altera resultados del pipeline.

## Comando rápido de estado

Cuando la terminal quede en duda, ejecuta:

make eco-status

Lectura esperada:

- Estado green: puedes detenerte o iniciar un nuevo sprint desde main.
- Estado attention: revisa cambios pendientes antes de seguir.
- Estado unknown o error: no hagas commit ni push hasta diagnosticar.

Este comando solo inspecciona el repositorio. No modifica archivos, no entrena modelos, no cambia baseline y no recalibra umbrales.

