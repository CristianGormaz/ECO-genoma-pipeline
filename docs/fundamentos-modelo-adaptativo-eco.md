# Fundamentos del modelo adaptativo E.C.O.

> E.C.O. — Entérico Codificador Orgánico — como sistema bioinspirado de transición de estados.

## 1. Principio base

El fundamento no es que un alimento o molécula entregue una idea directa a la conciencia. El fundamento computacional más responsable es:

```text
estímulo → interacción local → cambio de estado interno → salida observable
```

En biología, una entrada externa puede modificar señales químicas, nerviosas, inmunes o metabólicas. El sistema nervioso central no recibe "el alimento" como tal; recibe un estado fisiológico transformado.

En E.C.O., un paquete de información cumple el rol de estímulo. El sistema no debe interpretarlo de forma mística ni clínica: debe transformarlo en señales internas medibles.

## 2. Traducción a arquitectura

```text
payload
→ barrera informacional
→ sensado submucoso
→ motilidad mientérica
→ defensa informacional
→ microbiota/memoria
→ homeostasis
→ reporte eje intestino-cerebro
→ traza digestiva
```

La versión adaptativa agrega una capa nueva:

```text
estado previo + señales del paquete → modelo de transición → estado siguiente esperado
```

Eso permite que E.C.O. aprenda patrones de cambio sin afirmar que modela conciencia humana.

## 3. Qué puede aprender Machine Learning

Un modelo de ML puede aprender relaciones como:

```text
features del paquete + estado anterior → estado posterior
```

Ejemplos de variables de entrada:

- barrier_status
- barrier_permeability
- motility_action
- defense_severity
- microbiota_seen_count
- payload_length
- final_decision
- absorption_ratio previo
- immune_load previo
- quarantine_ratio previo

Ejemplo de salida entrenable:

- stable
- watch
- attention

También puede predecir métricas continuas:

- absorption_ratio siguiente
- immune_load siguiente
- quarantine_ratio siguiente
- recurrence_ratio siguiente

## 4. Modelo inicial recomendado

Antes de usar deep learning, E.C.O. debería comenzar con un modelo simple y auditable:

```text
baseline heurístico → regresión logística → árbol/gradient boosting → modelo secuencial experimental
```

La primera versión de ML debe funcionar como comparación contra la regla actual de homeostasis, no como reemplazo automático.

## 5. Dataset mínimo propuesto

Cada fila de entrenamiento podría representar una transición:

```text
packet_trace + homeostasis_before + homeostasis_after
```

Columnas sugeridas:

```text
packet_id
source
payload_length
barrier_status
barrier_permeability
motility_action
defense_category
defense_severity
final_decision
microbiota_seen_count
state_before
state_after
absorption_ratio_before
absorption_ratio_after
immune_load_before
immune_load_after
quarantine_ratio_before
quarantine_ratio_after
```

## 6. Límite responsable

Este módulo no debe:

- inducir estados mentales;
- simular consumo de sustancias;
- entregar recomendaciones biomédicas;
- diagnosticar personas;
- interpretar experiencias subjetivas como hechos clínicos.

Sí puede:

- modelar transiciones internas del pipeline;
- mejorar observabilidad;
- comparar reglas heurísticas contra modelos aprendidos;
- explicar por qué un estado cambia de stable a watch o attention;
- generar artefactos técnicos para portafolio y validación.

## 7. Formulación segura

La frase técnica recomendada es:

```text
E.C.O. modela transiciones de estado informacional inspiradas en el eje intestino-cerebro, usando señales internas del pipeline como entrada y estados de homeostasis como salida.
```

No se debe presentar como modelo de conciencia humana. Se debe presentar como arquitectura bioinspirada, educativa y experimental.

## 8. Próximo sprint técnico

Nombre sugerido:

```text
eco-adaptive-state-dataset
```

Objetivo:

```text
generar un dataset JSON/TSV con packet_trace + homeostasis_before + homeostasis_after
```

Criterio de cierre:

```text
python -m pytest -q
python scripts/run_sne_eco_state_dataset.py --output-json results/sne_eco_state_dataset.json --output-tsv results/sne_eco_state_dataset.tsv
```

Esto dejaría lista la base para un modelo ML auditable en una fase posterior.
