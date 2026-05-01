# Módulo S.N.E.-E.C.O. — Sistema Nervioso Entérico para el pipeline E.C.O.

## 1. Propósito

El módulo **S.N.E.-E.C.O.** convierte el Sistema E.C.O. — Entérico Codificador Orgánico — en una arquitectura computacional inspirada en el sistema nervioso entérico real.

La idea no es afirmar que el software esté vivo. La idea técnica es más precisa:

> El sistema nervioso entérico muestra cómo una red distribuida puede tomar microdecisiones locales, coordinar flujo, proteger barreras, transformar entradas y reportar estados sin depender de un único centro de control.

En E.C.O., eso se traduce en un pipeline que no solo procesa datos, sino que los **siente, filtra, mueve, transforma, absorbe, rechaza, recuerda y reporta**.

---

## 2. Argumento empírico base

### 2.1 Sistema nervioso entérico

El sistema nervioso entérico coordina funciones sensoriales y motoras del tracto gastrointestinal. Se organiza en redes distribuidas capaces de regular motilidad, secreción, reflejos locales y comunicación con el sistema nervioso central.

**Traducción E.C.O.:**

- No todo debe decidirlo un módulo central.
- Cada paquete puede recibir una microdecisión local.
- El pipeline puede comportarse como una red de reflejos trazables.

### 2.2 Plexo mientérico

El plexo mientérico regula el movimiento del contenido intestinal.

**Traducción E.C.O.:**

- Decide si el dato avanza, se detiene, se procesa por lote, se deriva o se descarta.
- Equivale al motor de tránsito del pipeline.

### 2.3 Plexo submucoso

El plexo submucoso se relaciona con el sensado local, secreción, microambiente y regulación fina.

**Traducción E.C.O.:**

- Mide calidad del dato, ambigüedad, tamaño, señales internas y riesgo.
- Genera un perfil sensorial antes de decidir.

### 2.4 Mucosa y barrera intestinal

La mucosa intestinal no es solo un muro. Es una interfaz selectiva que permite, limita o bloquea intercambios.

**Traducción E.C.O.:**

- Validación de formato.
- Control de caracteres inválidos.
- Control de datos vacíos.
- Detección de paquetes ambiguos.
- Separación entre dato útil, dato incierto y dato riesgoso.

### 2.5 Microbiota

La microbiota transforma compuestos, produce señales y participa en inmunidad, metabolismo y comunicación con el huésped.

**Traducción E.C.O.:**

- Módulos auxiliares que enriquecen el dato.
- Memoria adaptativa de secuencias vistas.
- Detección de duplicados.
- Normalización, clasificación y apoyo contextual.

### 2.6 Peristalsis y segmentación

El intestino no solo empuja. También mezcla, regula velocidad y expone contenido a zonas de absorción.

**Traducción E.C.O.:**

- El dato no debe moverse siempre igual.
- Secuencias válidas avanzan.
- Secuencias cortas o ambiguas quedan en cuarentena.
- Secuencias grandes pueden marcarse para procesamiento por lotes.

### 2.7 Sistema inmune informacional

El intestino distingue entre nutriente, señal, comensal, amenaza y residuo.

**Traducción E.C.O.:**

- Rechazo de entradas inválidas.
- Descarte trazable.
- Alertas por alta tasa de rechazo.
- Prevención de absorción de ruido como conocimiento.

### 2.8 Eje intestino-cerebro

El eje intestino-cerebro integra señales locales, barreras, microbiota y comunicación bidireccional.

**Traducción E.C.O.:**

- El pipeline genera reportes finales para el usuario o sistema superior.
- El reporte no solo entrega resultado; entrega estado, razón y límites.

---

## 3. Traducción a arquitectura

| Fundamento entérico | Módulo E.C.O. | Pregunta computacional |
|---|---|---|
| Lumen | Ingesta | ¿Qué dato entró? |
| Mucosa | Barrera | ¿Puede entrar sin dañar el sistema? |
| Plexo submucoso | Sensor local | ¿Qué señales trae? |
| Plexo mientérico | Motilidad | ¿Hacia dónde debe moverse? |
| Microbiota | Memoria/módulos auxiliares | ¿Ya vimos esto? ¿Se puede enriquecer? |
| Absorción | Extracción de features | ¿Qué nutriente informacional deja? |
| Sistema inmune | Rechazo/cuarentena | ¿Hay riesgo, ruido o invalidez? |
| Homeostasis | Métricas internas | ¿El sistema está estable? |
| Eje intestino-cerebro | Reporte | ¿Qué debe saber el usuario/sistema superior? |

---

## 4. Módulos de software sugeridos

La base actual ya existe en `src/eco_core/enteric_system.py`. La evolución sugerida es separar responsabilidades sin romper compatibilidad:

```text
src/eco_core/
  enteric_system.py        # Orquestador actual
  sne_eco.py               # Contratos conceptuales del S.N.E.-E.C.O.
  barrier.py               # Barrera epitelial informacional
  motility.py              # Movimiento, retención, batch, descarte
  microbiota.py            # Memoria adaptativa y enriquecimiento
  immune.py                # Respuesta inmune informacional
  homeostasis.py           # Métricas de equilibrio
```

Primera regla de ingeniería:

> No reemplazar lo que ya funciona. Encapsularlo, nombrarlo mejor y hacerlo medible.

---

## 5. Métricas de validación

| Métrica | Descripción | Uso |
|---|---|---|
| `total_packets` | Total de paquetes procesados | Carga del sistema |
| `absorbed_packets` | Paquetes convertidos en features útiles | Nutrición informacional |
| `rejected_packets` | Paquetes rechazados por invalidez | Respuesta inmune |
| `quarantined_packets` | Paquetes retenidos por incertidumbre | Gestión de ambigüedad |
| `discarded_packets` | Paquetes descartados con razón | Excreción trazable |
| `duplicate_packets` | Paquetes repetidos detectados | Memoria microbiota |
| `absorption_ratio` | Absorbidos / total | Eficiencia de absorción |
| `immune_load` | Rechazados / total | Nivel de defensa activada |
| `quarantine_ratio` | Cuarentena / total | Nivel de incertidumbre |
| `homeostasis_state` | `idle`, `stable`, `attention` | Estado general |

---

## 6. Primer paso de implementación

La primera pieza concreta debe ser un contrato liviano llamado `sne_eco.py`.

Su función:

- Definir nombres estables para las capas entéricas.
- Convertir reportes internos en métricas entendibles.
- Mantener compatibilidad con `EntericSystem`.
- Preparar una futura separación en módulos especializados.

Uso esperado:

```python
from src.eco_core import EntericSystem
from src.eco_core.sne_eco import build_sne_metrics

system = EntericSystem()
system.process_dna_sequence("ACGTCCAATGGTATAAA")
report = system.homeostasis_report()
metrics = build_sne_metrics(report)
print(metrics.homeostasis_state)
```

---

## 7. Límites éticos y biomédicos

1. E.C.O. puede inspirarse en sistemas biológicos, pero no debe presentarse como organismo vivo.
2. E.C.O. puede analizar datos genómicos de forma educativa o exploratoria, pero no debe entregar diagnóstico médico.
3. Las clasificaciones de variantes deben citar fuentes, fecha y límites de interpretación.
4. Toda decisión automatizada debe ser trazable.
5. Los datos sensibles deben tratarse con privacidad, minimización y consentimiento.
6. La analogía entérica debe usarse como arquitectura de procesamiento, no como afirmación biológica literal.
7. Los reportes deben distinguir claramente entre:
   - dato observado,
   - inferencia del sistema,
   - hipótesis,
   - recomendación técnica,
   - límite biomédico.

---

## 8. Definición corta para explicar a otra persona

> S.N.E.-E.C.O. es una capa de software bioinspirada en el sistema nervioso entérico. Su función es permitir que un pipeline de datos actúe como un intestino informacional: recibe datos, detecta calidad, decide rutas, absorbe señales útiles, rechaza ruido, recuerda patrones y reporta su estado de forma trazable.
