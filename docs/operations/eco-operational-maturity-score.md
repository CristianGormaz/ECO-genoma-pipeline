# E.C.O. Operational Maturity Score v1

## Propósito
Traducir gobernanza, madurez experimental y operación completa de E.C.O. a un marco verificable y trazable, sin introducir nuevas capacidades funcionales.

## Alcance
- Auditoría técnica-operativa sintética.
- Evidencia documental y de scripts existentes.
- Decisión global de estado: `passed` o `attention`.

## Qué no evalúa
- No evalúa validez científica aplicada.
- No evalúa efectividad clínica o biomédica.
- No habilita uso de datos reales por sí mismo.

## Dimensiones evaluadas (v1)
1. Gobernanza integrada.
2. Gates de decisión.
3. Score de madurez.
4. Panel end-to-end.
5. Madurez por fase.
6. Simulación robusta.
7. Comparación de resultados.
8. Rollback visible.
9. Admisión gobernada.

Cada dimensión debe declarar:
- nombre;
- propósito;
- evidencia esperada;
- estado (`passed | attention | missing | future`);
- explicación breve;
- límite responsable asociado.

## Criterio de decisión global
- `passed`: todas las dimensiones en `passed`.
- `attention`: al menos una dimensión en `attention`, `missing` o `future`.

## Lectura responsable
Este score es un indicador de coherencia técnica y madurez operativa documental/sintética. No equivale a autorización para admisión de datos reales ni a validación biomédica aplicada.

## Límite responsable
- Sin datos reales.
- Sin entrenamiento.
- Sin modificación de baseline.
- Sin recalibración de umbrales.
- Sin diagnóstico.
- Sin interpretación clínica.
- Sin afirmaciones biomédicas aplicadas.
- Sin autonomía humana real.
- Sin conciencia.
