# E.C.O. — Plano Operativo

## Estado del documento

- Documento operativo de orientación.
- No ejecutable.
- No reemplaza validaciones reales.
- No autoriza cambios directos en main.
- No habilita datos reales.

## Propósito

Este plano ayuda a entrar al repo, ubicarse, avanzar, pausar, validar, recuperar y cerrar ciclos de trabajo sin romper E.C.O. Está pensado para uso diario del repositorio, no para explicar todos los detalles internos de arquitectura.

## Principio operativo

Antes de avanzar, verificar estado real: rama, árbol, HEAD vs origin/main, último commit, eco-status, tests relevantes y PR abiertos.

El estado real manda sobre cualquier suposición previa.

## Cómo entrar al repo

Entrada conceptual recomendada:

- entrar al directorio del repo;
- activar entorno virtual si existe;
- verificar rama;
- verificar árbol;
- verificar sincronización con origin/main;
- revisar PR abiertos si gh está disponible;
- revisar eco-status.

## Cómo entender el estado

- green: estado operativo apto para continuar o cerrar.
- árbol sucio: hay cambios locales; revisar antes de cambiar de tarea.
- rama incorrecta: no avanzar hasta volver a la rama esperada o crear la rama de sprint correcta.
- HEAD desfasado: revisar relación local contra origin/main antes de continuar.
- PR abierto: no iniciar otro objetivo sin decidir qué hacer con ese PR.
- tests fallando: pausar avance funcional y diagnosticar.
- entorno roto: revisar Python, entorno virtual y dependencias antes de culpar al repo.
- terminal interrumpida: recuperar control antes de ejecutar comandos nuevos.
- archivos accidentales: identificar origen antes de borrar o commitear.

## Cómo avanzar

Flujo operativo seguro:

- no trabajar directo en main;
- crear rama desde main limpio;
- hacer un cambio acotado;
- ejecutar test específico;
- ejecutar suite completa;
- ejecutar make eco-check-clean si existe;
- crear commit;
- hacer push;
- abrir PR;
- esperar checks;
- mergear cuando corresponda;
- volver a main;
- actualizar con pull --ff-only;
- ejecutar validación final.

## Cómo pausar

Criterios de pausa:

- árbol sucio no entendido;
- tests fallando;
- make fallando sin diagnóstico;
- entorno virtual no activo;
- terminal esperando “>”;
- terminal en “(END)”;
- resultados inesperados;
- datos reales biológicos;
- cambios fuera de alcance;
- intento de modificar baseline o umbrales sin autorización.

## Cómo validar

Validaciones operativas frecuentes:

- make eco-status;
- test específico;
- python -m pytest -q;
- make eco-check-clean si existe;
- git status --short;
- git rev-list --left-right --count HEAD...origin/main;
- gh pr list --state open --limit 10 si gh está disponible.

## Cómo no romper el sistema

- no usar git reset sin revisión;
- no usar git clean sin revisión;
- no borrar ramas con -D sin verificar;
- no tocar scripts si el sprint es documental;
- no ampliar alcance;
- no mezclar sprints;
- no abrir datos reales;
- no entrenar modelos;
- no modificar baseline;
- no recalibrar umbrales.

## Recuperación básica

- si aparece “(END)”, presionar q;
- si aparece “>”, presionar Ctrl+C;
- si hay árbol sucio, revisar git status --short antes de limpiar;
- si hay archivos nuevos, identificar origen antes de borrar;
- si pytest no existe, revisar entorno virtual antes de asumir fallo del repo;
- si make no existe en Windows, validar con Python directo y reportar limitación.

## Cierre seguro

Condición de cierre recomendada:

- main activo;
- HEAD = origin/main;
- árbol limpio;
- tests pasando;
- eco-status green;
- eco-check-clean OK si existe;
- sin PR abiertos pendientes;
- ramas de sprint mergeadas limpiadas solo tras verificar.

## Relación con el plano técnico

El plano técnico explica la construcción y el plano operativo explica cómo trabajar con esa construcción sin dañarla. Si necesitas comprender capas, analogías y componentes, lee el plano técnico. Si necesitas ejecutar un ciclo de trabajo seguro, usa este plano operativo.
