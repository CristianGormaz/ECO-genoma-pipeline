# E.C.O. Operational Readiness Panel v1

## Propósito

Este panel resume si E.C.O. — Entérico Codificador Orgánico — está listo para operar en modo sintético seguro.

Su alcance es técnico-operativo, documental y verificable dentro del repositorio. No define preparación clínica, biológica aplicada ni productiva externa.

## Estado operativo esperado

E.C.O. se considera listo para un ciclo sintético seguro cuando cumple estas condiciones mínimas:

- rama de trabajo creada desde `main`;
- `HEAD` sincronizado con `origin/main` antes de iniciar el sprint;
- árbol de trabajo limpio antes de modificar archivos;
- `make eco-status` en estado `green`;
- suite completa de `pytest` pasando;
- sin PR abierto pendiente para el mismo objetivo;
- sin datos reales;
- sin entrenamiento de modelos;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas.

## Qué tiene E.C.O.

E.C.O. cuenta con una base operativa compuesta por:

- documentación de gobernanza;
- criterios responsables de uso;
- validaciones automatizadas;
- pruebas de contrato;
- snapshots operativos;
- comandos de estado;
- flujo Git/PR verificable;
- separación entre simulación, evaluación, documentación y afirmaciones aplicadas.

## Qué valida

El panel reconoce como validaciones principales:

- estado de rama;
- sincronización entre `HEAD` y `origin/main`;
- limpieza del árbol de trabajo;
- ejecución de `make eco-status`;
- ejecución de la suite completa de `pytest`;
- revisión de cambios antes de commit;
- revisión de checks antes de merge;
- validación final post-merge.

## Qué bloquea

E.C.O. debe pausar avances cuando aparezca cualquiera de estas condiciones:

- árbol de trabajo sucio sin explicación;
- tests fallando;
- `eco-status` distinto de `green`;
- PR abierto pendiente del mismo flujo;
- intento de modificar baseline sin auditoría;
- intento de recalibrar umbrales sin justificación;
- uso de datos sensibles o reales no autorizados;
- afirmaciones clínicas, diagnósticas o biomédicas aplicadas;
- lenguaje que presente una metáfora bioinspirada como conclusión científica.

## Qué reporta

El panel debe permitir responder rápidamente:

- rama actual;
- último commit;
- relación entre `HEAD` y `origin/main`;
- estado del árbol de trabajo;
- resultado de `make eco-status`;
- resultado de `pytest`;
- archivos tocados en el sprint;
- riesgos restantes;
- estado de PR y checks;
- decisión operativa: detenerse, recuperar, continuar o abrir PR.

## Qué falta

Este panel no reemplaza módulos funcionales futuros. E.C.O. todavía requiere consolidar progresivamente:

- flujo central de ejecución;
- reportes finales consolidados;
- interfaz de uso clara;
- datos sintéticos mejor organizados;
- criterios de aceptación por versión;
- demo estable;
- documentación de usuario;
- validación empírica más fuerte para afirmaciones técnicas específicas.

## Decisión operativa

Si todas las validaciones están en verde, la decisión recomendada es:

```text
continuar con sprint panel o micro-sprint controlado
```

Si alguna validación falla, la decisión recomendada es:

```text
pausar y entrar en modo recuperación
```

## Límite responsable

Este panel es permitido porque trabaja con documentación, trazabilidad, validación sintética y control operativo.

No autoriza:

- diagnóstico clínico;
- uso de datos genéticos privados;
- entrenamiento con datos sensibles;
- modificación de baseline sin comparación;
- recalibración de umbrales estables sin auditoría;
- conversión de metáforas simbólicas en conclusiones científicas;
- afirmaciones biomédicas aplicadas.

## Fórmula simple del panel

```text
Listo para operar sintéticamente =
repo limpio
+ eco-status green
+ pytest passing
+ límites responsables respetados
+ objetivo del sprint acotado
```

## Lectura simple

E.C.O. está listo para operar en modo sintético seguro cuando puede demostrar qué tiene, qué valida, qué bloquea, qué reporta y qué falta, sin depender de memoria externa ni de supuestos no verificados.
