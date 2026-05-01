# Guía de lectura — Reporte Entérico E.C.O.

## Propósito

El reporte entérico muestra cómo la capa `EntericSystem` convierte la metáfora digestiva de E.C.O. en una arquitectura operativa verificable.

La idea central es simple:

```text
dato crudo
→ barrera epitelial informacional
→ sensado local
→ reflejo entérico
→ absorción / cuarentena / descarte
→ memoria microbiota
→ homeostasis
```

Esto permite explicar E.C.O. como un pipeline que no trata todos los datos igual. Primero evalúa el estado del dato, decide una ruta y deja trazabilidad.

---

## Archivos generados

Al ejecutar:

```bash
python scripts/run_eco_enteric_report.py
python scripts/export_eco_enteric_html.py
```

Se generan:

```text
results/eco_enteric_system_report.json
results/eco_enteric_system_report.md
results/eco_enteric_system_report.html
```

- **JSON:** evidencia estructurada para auditoría técnica.
- **Markdown:** lectura rápida para documentación.
- **HTML:** pieza visual para portafolio, presentación o entrevista.

---

## Qué demuestra cada caso

| Caso | Acción esperada | Lectura E.C.O. |
|---|---|---|
| Secuencia válida | `absorb` | El dato supera la barrera y se transforma en nutrientes informacionales. |
| Secuencia inválida | `reject` | El sistema inmune informacional detecta caracteres no válidos. |
| Secuencia corta | `quarantine` | El dato no es basura, pero requiere revisión antes de absorberse. |
| Secuencia duplicada | `discard_duplicate` | La microbiota informacional evita absorber redundancia como conocimiento nuevo. |

---

## Cómo leer la homeostasis

El bloque de homeostasis resume el estado del flujo:

- **Procesados:** paquetes evaluados por la capa entérica.
- **Absorbidos:** paquetes convertidos en features útiles.
- **Cuarentena:** paquetes conservados para revisión.
- **Descartados:** paquetes eliminados de forma auditable.
- **Rechazados:** paquetes bloqueados por problemas de calidad.
- **Duplicados:** paquetes detectados por memoria microbiota mínima.
- **Estado:** lectura general del sistema: `stable`, `attention` o `idle`.

La homeostasis es importante porque E.C.O. no solo busca procesar mucho. Busca mantener equilibrio entre absorción, defensa, trazabilidad y limpieza.

---

## Lectura arquitectónica

La capa entérica representa una evolución desde pipeline lineal hacia pipeline distribuido.

Antes:

```text
entrada → filtro → salida
```

Ahora:

```text
entrada → sensado → microdecisión → ruta adaptativa → reporte trazable
```

Esto permite defender el proyecto con una frase precisa:

> E.C.O. no afirma que el software esté vivo; usa principios del Sistema Nervioso Entérico como inspiración arquitectónica para crear un pipeline más distribuido, trazable y resiliente.

---

## Uso en portafolio

Este reporte puede presentarse como una pieza del proyecto bajo el título:

> Sistema Entérico Integrado para digestión informacional de secuencias.

Explicación breve:

> Diseñé una capa bioinspirada que evalúa secuencias antes de procesarlas. El sistema distingue entradas válidas, inválidas, insuficientes y duplicadas mediante una lógica de sensado local, reflejo autónomo, memoria mínima y reporte homeostático.

Competencias demostradas:

- arquitectura modular;
- trazabilidad de datos;
- validación automatizada;
- diseño bioinspirado;
- pensamiento sistémico;
- documentación técnica;
- UX de reportes para lectura humana.

---

## Comandos recomendados

```bash
python -m pytest -q
python scripts/run_eco_enteric_report.py
python scripts/export_eco_enteric_html.py
xdg-open results/eco_enteric_system_report.html
```

Si `xdg-open` no abre el archivo, revisar directamente:

```text
results/eco_enteric_system_report.html
```

---

## Límite responsable

La analogía con el Sistema Nervioso Entérico es arquitectónica y funcional. No debe presentarse como afirmación biológica literal ni como diagnóstico médico.

E.C.O. toma inspiración en patrones del SNE: autonomía local, filtrado, absorción, defensa, memoria contextual y homeostasis. Estos principios se traducen a software como reglas, trazas, métricas y decisiones verificables.
