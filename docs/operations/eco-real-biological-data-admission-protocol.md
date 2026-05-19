# E.C.O. — Protocolo de Admisión de Datos Reales Biológicos

Este protocolo define una ruta documental previa para evaluar, en fases futuras, una posible solicitud de admisión de datos reales biológicos antes de cualquier procesamiento.

## Estado del documento

- Documental.
- No ejecutable.
- no habilita uso de datos reales.
- no aprueba procesamiento de datos reales por sí mismo.
- no reemplaza revisión humana.
- Pendiente de futuras fases técnicas.

Este documento no admite datos reales, no procesa datos reales, no autoriza ingestión y no convierte una solicitud futura en aprobación operativa.

## Propósito

El propósito de este protocolo es describir una ruta previa para evaluar solicitudes futuras de admisión de datos reales biológicos.

La ruta existe para ordenar revisión humana, evidencia auditable, límites interpretativos y posibilidad de pausa, rollback o rechazo antes de cualquier contacto operativo con datos reales.

## Relación con el Manual de Madurez

Este protocolo se relaciona con docs/operations/eco-real-biological-data-maturity-manual.md.

El manual define el punto de madurez requerido para discutir capacidades futuras relacionadas con datos reales biológicos. Este protocolo define el procedimiento documental previo a una admisión futura.

Ninguno de los dos documentos habilita procesamiento real por sí mismo, aprueba admisión real, autoriza ingestión, reemplaza revisión humana ni declara que E.C.O. esté listo para datos reales.

## Alcance del protocolo

Este protocolo aplica a cualquier intento futuro de usar:

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

La aplicación de este alcance no implica aceptación. Solo establece que cualquier intento dentro de estas categorías debe pasar por evaluación previa, revisión humana y evidencia auditable antes de cualquier fase técnica futura.

## Flujo de admisión documental

El flujo conceptual de evaluación previa debe mantener esta secuencia:

solicitud de admisión
→ identificación de fuente
→ clasificación de sensibilidad
→ revisión de licencia o permiso
→ revisión técnica previa
→ revisión ética
→ revisión interpretativa
→ revisión humana
→ decisión registrada
→ evidencia auditable
→ rollback o rechazo si corresponde

Este flujo no describe procesamiento, transformación, ingestión ni análisis de datos reales. Su función es registrar una ruta de evaluación anterior a cualquier decisión técnica futura.

## Compuertas mínimas

Toda solicitud futura debería quedar detenida hasta documentar, como mínimo:

1. compuerta ética: finalidad declarada, límites responsables y ausencia de uso clínico aplicado.
2. compuerta de fuente: origen, trazabilidad, licencia o permiso y condiciones de uso.
3. compuerta técnica: revisión previa de formato, estructura, tamaño y compatibilidad sin procesar datos reales.
4. compuerta de seguridad: sensibilidad, exposición, acceso, almacenamiento permitido y riesgo operativo.
5. compuerta interpretativa: límites sobre diagnóstico, interpretación clínica, riesgo individual y afirmaciones biomédicas aplicadas.
6. compuerta de revisión humana: decisión humana explícita antes de cualquier avance futuro.
7. compuerta de rollback: ruta para detener, revertir y registrar cualquier intento.
8. compuerta de evidencia: conservación de reporte auditable, decisión, límites y resultado.

## Estados de decisión permitidos

Los estados documentales permitidos son:

- bloqueado;
- pausado;
- requiere revisión humana;
- permitido limitado;
- rechazado.

El estado permitido limitado no equivale a aprobación general. Solo podría describir, en una fase futura separada, una validación técnica limitada bajo revisión humana y evidencia auditable.

## Evidencia mínima requerida

Una solicitud futura no debería avanzar sin evidencia mínima:

- manifiesto de fuente;
- clasificación de sensibilidad;
- licencia o permiso;
- decisión humana;
- reporte auditable;
- registro de rollback;
- límites interpretativos.

La evidencia debe ser suficiente para explicar por qué una solicitud queda bloqueada, pausada, limitada o rechazada.

## Condiciones de rechazo obligatorio

El intento debe rechazarse si falta cualquiera de estos elementos:

- fuente clara;
- licencia o permiso;
- clasificación de sensibilidad;
- revisión humana;
- evidencia auditable;
- límites interpretativos;
- rollback;
- ausencia de finalidad clínica;
- ausencia de identificadores personales.

Estas condiciones priorizan detener la solicitud antes de exposición, ingestión o uso operativo de datos reales.

## Primer uso futuro permitido solo como validación técnica limitada

Si una fase futura llegara a evaluar un primer uso real, solo podría considerarse como validación técnica limitada y debería ser:

- público;
- no humano o de bajo riesgo;
- sin identificadores personales;
- sin finalidad clínica;
- con licencia clara;
- con revisión humana;
- con evidencia auditable;
- solo validación técnica limitada.

Este protocolo no selecciona, recomienda ni sugiere conjuntos de datos reales concretos. Tampoco aprueba una admisión real.

## Límites responsables

Esta fase declara explícitamente:

- sin datos reales en esta fase;
- sin ingestión de datos reales;
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

Solo como horizonte futuro, podrían evaluarse fases separadas:

- Real Biological Data Admission Template;
- Real Biological Data Admission Example;
- Real Biological Data Manifest Schema;
- Real Biological Data Admission Dry-Run Gate;
- Real Biological Data Rollback Report;
- enlace posterior en mapa, índice y capabilities report si corresponde.

Estas fases no quedan aprobadas por este protocolo. Cada una requeriría alcance propio, revisión humana, validaciones independientes y autorización explícita.
