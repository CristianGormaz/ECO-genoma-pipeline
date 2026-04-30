from pathlib import Path
import re
from html import escape

RESULTS = Path("results")

COMPARISON = RESULTS / "eco_classifier_comparison_report.md"
CLASSIFIER_REPEATED = RESULTS / "eco_classifier_repeated_eval_report.md"
EMBEDDING_REPEATED = RESULTS / "eco_embedding_repeated_eval_report.md"

OUT_MD = RESULTS / "eco_model_decision_report.md"
OUT_HTML = RESULTS / "eco_model_decision_report.html"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def grab(pattern: str, text: str, default: str = "no_disponible") -> str:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else default


def grab_table_value(label: str, text: str, default: str = "no_disponible") -> str:
    pattern = r"\| " + re.escape(label) + r" \| ([^|]+) \|"
    return grab(pattern, text, default)


def grab_embedding_delta(text: str, default: str = "no_disponible") -> str:
    """Extract the practical delta between embedding_placeholder and baseline_v3.

    The source report may expose this value in different forms:
    - console-style sentence copied into Markdown;
    - comparison table row;
    - narrative sentence.
    Keeping these fallbacks makes the decision report robust while the reports evolve.
    """
    patterns = [
        r"Delta embedding vs v3 macro F1 promedio: ([0-9.\-]+)",
        r"\| embedding_placeholder vs baseline_v3 \| ([0-9.\-]+) \|",
        r"delta promedio es ([0-9.\-]+)",
    ]
    for pattern in patterns:
        value = grab(pattern, text, "")
        if value:
            return value
    return default


def main() -> None:
    comparison = read(COMPARISON)
    classifier_repeated = read(CLASSIFIER_REPEATED)
    embedding_repeated = read(EMBEDDING_REPEATED)

    fixed_best = grab(r"Mejor modelo: `([^`]+)`", comparison)
    fixed_delta = grab(r"Delta vs v1: `([^`]+)`", comparison)
    classifier_best = grab_table_value("Mejor promedio", classifier_repeated)
    embedding_best = grab_table_value("Mejor promedio", embedding_repeated)
    embedding_decision = grab_table_value("Decisión operativa", embedding_repeated)
    embedding_delta = grab_embedding_delta(embedding_repeated)

    md = f"""# E.C.O. - Reporte de decisión de modelos

## Propósito

Este reporte resume la decisión operativa actual del pipeline E.C.O. antes de avanzar hacia embeddings reales o modelos más pesados.

## Resumen ejecutivo

| Elemento | Resultado |
| --- | --- |
| Mejor modelo en split fijo | {fixed_best} |
| Delta del mejor modelo vs v1 | {fixed_delta} |
| Mejor promedio en evaluación repetida del clasificador | {classifier_best} |
| Mejor promedio en evaluación repetida embedding | {embedding_best} |
| Decisión operativa embedding | {embedding_decision} |
| Delta embedding vs v3 | {embedding_delta} |

## Decisión E.C.O.

| Modelo | Rol operativo | Decisión |
| --- | --- | --- |
| baseline_v1 | Control explicable | Se mantiene como referencia mínima por transparencia. |
| baseline_v2 | Variante exploratoria | No queda como candidato principal. |
| baseline_v3 | Candidato principal pre-embeddings | Se mantiene como baseline fuerte antes de modelos más complejos. |
| embedding_placeholder | Contrato vectorial experimental | Valida arquitectura, pero no reemplaza a v3 por empate técnico. |

## Lectura técnica

baseline_v3 queda como candidato principal pre-embeddings porque combina motivos, k-mers de tamaño 3 y normalización minmax_train.

embedding_placeholder cumple una función arquitectónica importante: prueba que E.C.O. ya puede ejecutar el flujo:

```text
secuencia -> embedding -> clasificador -> comparación -> reporte
```

Pero como su diferencia frente a baseline_v3 es mínima, se interpreta como empate técnico y no como superioridad real.

## Regla para avanzar a embeddings reales

Un embedding real, como DNABERT u otro modelo vectorial, debería demostrar al menos una de estas mejoras:

1. Mejor macro F1 promedio frente a baseline_v3.
2. Menor variabilidad entre splits.
3. Mejor desempeño en casos ambiguos o difíciles.
4. Mejor explicación complementaria sin romper trazabilidad.
5. Reproducibilidad razonable en el equipo o entorno elegido.

## Límites responsables

- Dataset demostrativo pequeño.
- No es benchmark científico general.
- No hay diagnóstico clínico.
- Las métricas son internas del MVP.
- El embedding placeholder no es DNABERT.
- Cualquier mejora futura debe compararse contra baseline_v1 y baseline_v3.

## Próximo paso recomendado

Preparar una ruta experimental de embedding real o semi-real, manteniendo:

```text
baseline_v1 = control explicable
baseline_v3 = candidato principal pre-embeddings
embedding_placeholder = contrato vectorial validado
```
"""

    OUT_MD.write_text(md, encoding="utf-8")

    html_doc = f"""<!doctype html>
<html lang=\"es\">
<head>
<meta charset=\"utf-8\">
<title>E.C.O. - Reporte de decisión de modelos</title>
<style>
body {{
  font-family: system-ui, sans-serif;
  max-width: 980px;
  margin: 40px auto;
  line-height: 1.55;
  padding: 0 20px;
}}
pre {{
  white-space: pre-wrap;
  background: #f7f7f7;
  padding: 18px;
  border-radius: 12px;
}}
</style>
</head>
<body>
<pre>{escape(md)}</pre>
</body>
</html>
"""

    OUT_HTML.write_text(html_doc, encoding="utf-8")

    print("E.C.O. MODEL DECISION REPORT")
    print("============================")
    print(f"Markdown: {OUT_MD}")
    print(f"HTML: {OUT_HTML}")
    print("Estado: OK, reporte de decisión de modelos generado.")


if __name__ == "__main__":
    main()
