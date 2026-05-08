# E.C.O. real data candidate review checklist

## Propósito

Esta checklist define cómo revisar una fuente candidata antes de crear un manifiesto de datos reales para E.C.O.
Su función es evitar que una fuente externa avance por intuición sin revisar origen, permiso, sensibilidad, alcance y límites responsables.

## Lectura rápida

Antes de que una fuente real entre al pipeline, debe pasar por una revisión mínima.
La revisión no ingiere datos, no interpreta resultados y no convierte la fuente en dato usable automáticamente.

## Resultado posible

- Aceptar para manifiesto: la fuente parece pública, no sensible, trazable y limitada.
- Revisar antes de avanzar: falta permiso, licencia, alcance, formato o claridad de uso.
- Bloquear: contiene datos sensibles, personales, clínicos, genéticos privados o riesgo aplicado.

## Checklist de revisión

### 1. Identidad de la fuente

- Nombre de la fuente identificado.
- URL, referencia o ubicación reproducible disponible.
- Responsable, institución o publicador identificable.
- Fecha de acceso o versión registrable.

### 2. Permiso y trazabilidad

- Licencia, permiso o condición de uso revisable.
- Fuente pública o autorizada.
- Uso compatible con análisis estructural no aplicado.
- Sin obligación de aceptar términos incompatibles con el proyecto.

### 3. Sensibilidad

- No contiene personas identificables.
- No contiene datos personales privados.
- No contiene datos clínicos.
- No contiene datos genéticos humanos privados.
- No contiene datos biomédicos aplicados.
- No permite inferir salud, identidad, conducta individual ni riesgo personal.

### 4. Alcance permitido

- El uso previsto es describir estructura, campos, formato o consistencia.
- No se usará para diagnóstico.
- No se usará para recomendación clínica.
- No se usará para entrenar modelos.
- No se usará para recalibrar umbrales.
- No se usará para modificar baseline.

### 5. Forma técnica

- Puede describirse como CSV, JSON, tabla o recurso documental.
- Tiene campos o columnas comprensibles.
- Puede registrarse en un manifiesto antes de cualquier ingestión.
- Puede validarse sin descargar el dataset completo.

### 6. Compatibilidad con el primer candidato seguro

- Preferentemente ambiental, público, agregado y no sensible.
- Tamaño pequeño o revisable.
- Sin datos individuales.
- Sin interpretación biomédica aplicada.

## Decisión operativa

- Si todos los criterios críticos pasan, crear un manifiesto descriptivo.
- Si falta claridad, detener y documentar revisión pendiente.
- Si aparece sensibilidad o riesgo aplicado, bloquear la fuente.

## Límite responsable

Esta checklist es documental y preventiva.
No ingiere datos reales, no usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no realiza afirmaciones biomédicas aplicadas.

## Explicación simple

Esta checklist es el control de entrada: antes de que E.C.O. pruebe una fuente real, revisa si la fuente puede entrar, si necesita revisión o si debe bloquearse.
