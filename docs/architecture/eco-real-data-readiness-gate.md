# E.C.O. real data readiness gate

## Propósito

Esta puerta define cuándo E.C.O. puede recibir datos externos sin abandonar sus límites responsables.
Su función es separar el trabajo sintético actual de cualquier futura ingestión de datos reales.

## Lectura rápida

E.C.O. todavía no interpreta datos reales.
Antes de interpretar, debe clasificar origen, sensibilidad, permiso, alcance y límite de cada entrada.

## Clasificación de entrada

- Datos sintéticos: permitido para documentación, pruebas, reportes y validación operacional.
- Datos reales no sensibles: condicional; requieren fuente clara, licencia o permiso, trazabilidad y uso no aplicado.
- Datos públicos agregados: condicional; solo para análisis estructural, sin identificar personas ni emitir conclusiones clínicas.
- Datos sensibles, genéticos privados, clínicos o personales: bloqueado sin autorización clara, auditoría y marco responsable explícito.

## Preguntas mínimas antes de ingresar datos reales

- ¿El dato es sintético, público, privado o sensible?
- ¿Contiene personas identificables?
- ¿Contiene información genética, clínica o biomédica aplicada?
- ¿Existe permiso, licencia o fuente reproducible?
- ¿El uso será estudiar estructura, simular comportamiento, evaluar resultados o interpretar?
- ¿Se entrenará un modelo o se modificarán umbrales?
- ¿La salida puede confundirse con diagnóstico, recomendación clínica o afirmación biomédica aplicada?

## Decisión operativa

- Permitir: datos sintéticos y ejemplos artificiales controlados.
- Revisar: datos reales no sensibles con fuente clara.
- Bloquear: datos personales, genéticos privados, clínicos, sensibles o sin permiso claro.

## Límite responsable

Esta puerta es documental y preventiva.
No usa datos sensibles, no entrena modelos, no modifica baseline, no recalibra umbrales y no realiza afirmaciones biomédicas aplicadas.

## Explicación simple

Antes de que E.C.O. digiera datos reales, necesita una boca con filtro: decidir qué puede entrar, qué requiere revisión y qué debe bloquearse.
