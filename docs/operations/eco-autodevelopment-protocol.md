# E.C.O. — Protocolo de Autodesarrollo Gobernado

## Qué significa autodesarrollo gobernado
En E.C.O., **autodesarrollo gobernado** significa mejorar artefactos, procesos y cobertura documental/técnica bajo límites explícitos, auditoría reproducible y control humano. El sistema puede asistir la evolución del proyecto, pero no opera como autonomía sin supervisión.

## Qué puede proponer E.C.O.
E.C.O. puede proponer:
- mejoras de documentación, trazabilidad y observabilidad;
- nuevos reportes sintéticos;
- hipótesis técnicas para evaluar en entornos controlados;
- ampliaciones de tests y validadores.

## Qué puede ejecutar Codex
Codex puede ejecutar:
- cambios de bajo riesgo y reversibles en código/documentación;
- scripts sintéticos sin datos reales ni internet;
- validaciones automáticas existentes.

Codex **no** puede habilitar por sí mismo cambios críticos de gobernanza.

## Qué requiere revisión humana
Se requiere revisión/aprobación humana previa para:
- habilitar ingestión de datos reales;
- habilitar o modificar entrenamiento;
- modificar baseline vigente;
- recalibrar umbrales de decisión.

## Gates obligatorios antes de cambios críticos
Antes de cualquier transición hacia cambios críticos, deben cumplirse gates explícitos:
1. **Gate de datos reales**: evidencia documental, alcance y minimización de riesgo.
2. **Gate de entrenamiento**: plan experimental y criterios de rollback.
3. **Gate de baseline**: impacto esperado, comparación y justificación.
4. **Gate de umbrales**: análisis de sensibilidad y revisión humana.

## Productividad con control
E.C.O. puede ser más productivo sin autonomía irrestricta porque:
- acelera tareas repetitivas y verificables;
- mantiene separación entre simulación y afirmación aplicada;
- reduce riesgo operativo mediante controles previos;
- facilita auditoría y reversibilidad por sprint.
