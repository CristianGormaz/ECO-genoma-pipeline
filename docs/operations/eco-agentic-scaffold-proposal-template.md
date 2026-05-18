# E.C.O. — Agentic Scaffold Proposal Template

## Propósito de la plantilla

Esta plantilla ordena propuestas de nuevas funciones o modulos candidatos para
E.C.O. dentro del marco de Agentic Scaffold. Su uso esperado es que un agente
generativo proponga estructura documental o técnica mínima, trazable y
reversible, siempre bajo revisión humana.

La plantilla no aprueba integración por si misma. Solo organiza una propuesta
para que una persona pueda revisar alcance, límites, archivos sugeridos,
validaciones y decisión final.

## Relación con el protocolo

Referencia obligatoria:
`docs/operations/eco-agentic-scaffold-protocol.md`.

Toda propuesta debe respetar el protocolo de Agentic Scaffold: autodesarrollo
asistido o gobernado significa construcción de plantilla por agente generativo
bajo revisión humana, sin autonomía real, sin conciencia y sin libre albedrío
real.

## Identificación de la propuesta

- Nombre corto:
- Fecha:
- Rama o sprint:
- Agente proponente:
- Revisor humano esperado:
- Estado inicial: borrador / requiere revisión / rechazado / aprobado.

## Propósito operativo

- Problema operativo que ordena:
- Resultado mínimo esperado:
- Beneficio esperado para trazabilidad, validación o gobernanza:
- Lo que queda explícitamente fuera de alcance:

## Módulo o habitación propuesta

- Nombre del módulo o habitación:
- Ubicación esperada dentro del repositorio:
- Relación con capacidades existentes:
- Dependencias nuevas previstas:
- Riesgos de alcance:

## Clasificación inicial

Seleccionar una clasificación inicial y justificarla.

- **permitido**: documentación, contratos de prueba, índices o scaffolds sin
  datos reales, sin entrenamiento, sin modificación de baseline y sin
  recalibración de umbrales.
- **requiere revisión**: nuevas funciones, módulos candidatos, cambios de
  gobernanza operativa, ampliaciones de alcance o dependencias nuevas.
- **bloqueado**: datos reales, entrenamiento, modificación de baseline,
  recalibración de umbrales, afirmaciones biomédicas aplicadas, autonomía real,
  conciencia o libre albedrío real.

Clasificación propuesta:

Justificación:

## Archivos mínimos sugeridos

Listar solo archivos necesarios para una propuesta pequeña, testeable,
reversible y trazable.

- Documento o contrato:
- Test contractual:
- Índice o referencia operacional, si aplica:
- Archivos que no deben tocarse:

## Tests contractuales esperados

- Existencia de documentos o artefactos propuestos.
- Presencia de secciones obligatorias.
- Presencia de límites responsables.
- Presencia de referencia al protocolo de Agentic Scaffold cuando aplique.
- Confirmación de que no se habilitan datos reales, entrenamiento, baseline ni
  recalibración de umbrales.

## Validaciones requeridas

Registrar comandos esperados para validar la propuesta antes de revisión.

```bash
python -m pytest -q
make eco-status
make eco-check-clean
git status --short
```

Resultado esperado:

- Tests relevantes pasando.
- Estado operativo revisado.
- Sin residuos sintéticos no esperados.
- Árbol limpio antes de cierre o entrega.

## Criterios de pausa/revisión humana

Pausar y solicitar revisión humana si la propuesta:

- cambia alcance operativo o gobernanza;
- introduce dependencias nuevas;
- propone nuevas funciones ejecutables;
- toca baseline, umbrales, entrenamiento o datos reales;
- puede inducir afirmaciones biomédicas aplicadas;
- no puede validarse con tests contractuales claros;
- requiere decidir propósito, prioridad o aceptación final.

## Límites responsables

La propuesta debe declarar y preservar todos estos límites:

- sin autonomía real;
- sin conciencia;
- sin libre albedrío real;
- sin datos reales;
- sin entrenamiento;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin afirmaciones biomédicas aplicadas.

## Decisión final humana

- Decisión: aprobado / requiere cambios / pausado / rechazado.
- Responsable humano:
- Fecha de decisión:
- Condiciones de integración:
- Validaciones revisadas:
- Comentarios:

La decisión final siempre corresponde a revisión humana. El agente generativo
puede proponer, ordenar y materializar scaffold permitido, pero no decide
integración, propósito ni cambios críticos por cuenta propia.
