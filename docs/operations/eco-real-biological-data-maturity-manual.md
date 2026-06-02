# E.C.O. — Manual de Madurez para Datos Reales Biológicos

Este manual define un criterio documental de madurez para evaluar cuándo E.C.O. podría estar preparado para diseñar reglas de admisión de datos reales biológicos.

## Estado del documento

- Documental.
- No ejecutable.
- no habilita uso de datos reales.
- no aprueba procesamiento de datos reales por sí mismo.
- Pendiente de futuras fases técnicas.
- No incluye instrucciones para procesar datos reales.
- No sugiere datasets reales concretos.
- No crea endpoints, scripts, schemas ni validadores funcionales.

## Propósito

El propósito de este manual es fijar el punto de madurez requerido antes de implementar reglas de admisión para datos reales biológicos.

Este documento no activa procesamiento, ingestión, validación funcional ni uso operativo de datos reales. Su función es delimitar criterios de preparación, revisión y gobernanza antes de cualquier fase técnica futura.

## Principio de madurez

E.C.O. no está maduro cuando puede leer datos reales.

E.C.O. está maduro cuando puede rechazar, pausar, auditar y explicar cualquier intento de usar datos reales antes de procesarlos.

La madurez se mide por la capacidad de detener el flujo antes de la exposición, no por la capacidad de interpretar o transformar contenido biológico real.

## Definición de dato real biológico

Para este manual, "dato real biológico" incluye, como mínimo:

- secuencias genéticas;
- secuencias genómicas;
- datos moleculares;
- proteínas;
- variantes;
- anotaciones biológicas;
- metadatos clínicos;
- metadatos poblacionales;
- estructuras provenientes de bases científicas reales;
- archivos que representen organismos, individuos, muestras o sistemas biológicos observados.

La categoría aplica aunque el dato sea público, agregado, parcialmente anonimizado, derivado, resumido o presentado como ejemplo externo. La existencia de licencia o acceso público no elimina la necesidad de control previo.

## Horizonte de E.C.O.

E.C.O. busca ser un sistema bioinspirado de digestión de información: puede estudiar señales, simular decisiones, evaluar límites y generar hipótesis bajo condiciones controladas.

El paso hacia datos reales biológicos requiere reglas estrictas porque cambia el tipo de riesgo: fuente, sensibilidad, interpretación, trazabilidad, rollback y revisión humana deben estar definidos antes de cualquier procesamiento.

## Semáforo de madurez

| Estado | Criterio | Decisión |
|---|---|---|
| Rojo | E.C.O. no tiene controles documentados, evidencia mínima ni ruta de auditoría suficiente. | no implementar reglas reales todavía. |
| Amarillo | E.C.O. puede definir y probar reglas de admisión sin tocar datos reales. | implementar reglas de admisión, pero sin procesar datos reales. |
| Verde | E.C.O. cuenta con control previo, revisión humana, límites interpretativos y rollback verificable. | permitir solo validación técnica limitada de primer dato real de bajo riesgo, si corresponde. |

El estado verde no equivale a aprobación general de datos reales. Solo habilitaría una discusión técnica acotada para una validación limitada, bajo revisión humana explícita.

## Ocho compuertas de madurez

Antes de cualquier regla de admisión futura, E.C.O. debe poder expresar y auditar estas ocho compuertas:

1. compuerta ética: confirma finalidad, límites, ausencia de uso clínico y compatibilidad con los límites responsables del proyecto.
2. compuerta de fuente: exige origen, licencia, trazabilidad y condiciones de uso verificables.
3. compuerta técnica: evalúa formato, tamaño, estructura y compatibilidad sin procesar contenido real.
4. compuerta de seguridad: identifica sensibilidad, exposición, acceso, almacenamiento y riesgo operativo.
5. compuerta interpretativa: impide diagnóstico, interpretación clínica, riesgo individual y afirmaciones biomédicas aplicadas.
6. compuerta de revisión humana: requiere decisión humana explícita antes de avanzar a cualquier validación limitada.
7. compuerta de rollback: define cómo detener, revertir y registrar cualquier intento de admisión.
8. compuerta de evidencia: conserva reporte auditable, límites declarados y resultado de decisión.

## Estados de decisión permitidos

Las reglas futuras solo deberían producir estados explícitos y auditables:

- bloqueado;
- pausado;
- requiere revisión humana;
- permitido limitado;
- rechazado.

Ningún estado debe implicar aprobación automática, entrenamiento, recalibración o interpretación biomédica aplicada.

## Evidencia mínima obligatoria

Antes de considerar cualquier admisión futura, E.C.O. debería exigir evidencia mínima:

- manifiesto de fuente;
- clasificación de sensibilidad;
- decisión humana;
- reporte auditable;
- registro de rollback;
- límites interpretativos.

La falta de cualquiera de estos elementos debe mantener el intento en estado bloqueado, pausado o rechazado.

## Primer dato real permitido en el futuro

Si algún día corresponde evaluar un primer dato real, debe cumplir como mínimo:

- público;
- no humano o de bajo riesgo;
- con licencia clara;
- sin identificadores personales;
- sin finalidad clínica;
- solo para validación técnica limitada.

Este manual no selecciona, recomienda ni sugiere conjuntos de datos concretos. El primer dato real, si alguna vez se evalúa, deberá existir dentro de una fase técnica posterior con revisión humana y evidencia auditable.

## Límites responsables

Esta fase queda limitada por las siguientes restricciones:

- sin datos reales en esta fase;
- sin entrenamiento;
- sin modificación de baseline;
- sin recalibración de umbrales;
- sin diagnóstico;
- sin interpretación clínica;
- sin riesgo genético individual;
- sin afirmaciones biomédicas aplicadas;
- sin autonomía real;
- sin conciencia;
- sin libre albedrío real.

Estos límites separan estudiar, simular, evaluar y generar hipótesis de afirmar resultados aplicados sobre sistemas biológicos reales.

## Próximas fases sugeridas

Solo como horizonte futuro, podrían evaluarse fases documentales o técnicas separadas:

- Real Biological Data Manifest Schema;
- Real Biological Data Admission Dry-Run Gate;
- Real Biological Data Rollback Report;
- integración posterior a reportes/dashboard si corresponde.

Estas fases no quedan aprobadas por este documento. Cada una requeriría alcance propio, revisión humana, pruebas y validaciones independientes.
