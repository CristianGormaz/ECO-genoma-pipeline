# E.C.O. — Real Biological Data Admission Dry-Run Gate

## Qué es

La compuerta dry-run de admisión para datos reales biológicos evalúa manifiestos descriptivos de intención antes de cualquier procesamiento.

Su función es verificar si E.C.O. puede rechazar, pausar, auditar y explicar un intento de uso antes de exponer el sistema a datos reales.

## Qué evalúa

- manifiesto de fuente;
- clasificación de sensibilidad;
- licencia o permiso;
- decisión humana;
- límites interpretativos;
- rollback;
- evidencia auditable;
- criterios estrictos para una validación técnica limitada futura.

## Qué NO hace

- No lee datos reales.
- No descarga URLs.
- No abre archivos de secuencias, variantes, BED, FASTA o VCF.
- No parsea contenido biológico.
- No interpreta variantes.
- No entrena modelos.
- No modifica baseline.
- No recalibra umbrales.
- No habilita uso clínico.

## Relación con el Manual de Madurez

Esta compuerta implementa una primera fase técnica limitada derivada del Manual de Madurez para Datos Reales Biológicos.

El manual define el principio: E.C.O. no está maduro cuando puede leer datos reales; E.C.O. está maduro cuando puede rechazar, pausar, auditar y explicar cualquier intento de uso antes de procesarlo.

El dry-run no reemplaza revisión humana, no autoriza procesamiento por sí mismo y no declara que E.C.O. esté listo para datos reales.

## Estados de decisión

- `blocked`: existe una condición que impide avanzar.
- `paused`: falta evidencia crítica no humana.
- `requires_human_review`: falta revisión o decisión humana.
- `limited_allowed`: el manifiesto cumple criterios de validación técnica limitada futura.
- `rejected`: falta base mínima de manifiesto o el manifiesto no es válido.

## Evidencia mínima

- manifiesto de fuente;
- clasificación de sensibilidad;
- licencia o permiso;
- decisión humana;
- límites interpretativos;
- rollback;
- evidencia auditable.

## Criterios para `limited_allowed`

`limited_allowed` solo puede aparecer si el manifiesto declara:

- fuente pública;
- no humano o de bajo riesgo;
- licencia clara;
- sin identificadores personales;
- sin finalidad clínica;
- revisión humana;
- rollback;
- límites interpretativos;
- validación técnica limitada;
- evidencia auditable.

Esta decisión no autoriza uso clínico, interpretación biomédica aplicada, entrenamiento ni procesamiento general de datos reales.

## Límites responsables

- sin datos reales;
- sin entrenamiento;
- sin datos sensibles;
- sin diagnóstico;
- sin interpretación clínica;
- sin riesgo genético individual;
- sin baseline changes;
- sin threshold recalibration;
- sin conciencia;
- sin libre albedrío real.

## Siguiente fase futura posible

Una fase futura podría conectar este dry-run con un schema de manifiesto más estricto o con reportes operativos adicionales.

Esa fase futura seguiría sin habilitar datos reales por sí misma y requeriría revisión humana, evidencia auditable y rollback.
