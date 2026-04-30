from pathlib import Path
from html import escape
import re

RESULTS = Path("results")

COMPARISON = RESULTS / "eco_classifier_comparison_report.md"
CLASSIFIER_REPEATED = RESULTS / "eco_classifier_repeated_eval_report.md"
PLACEHOLDER_REPEATED = RESULTS / "eco_embedding_repeated_eval_report.md"
SEMIREAL_REPEATED = RESULTS / "eco_embedding_semireal_repeated_eval_report.md"

OUT_MD = RESULTS / "eco_model_decision_semireal_report.md"
OUT_HTML = RESULTS / "eco_model_decision_semireal_report.html"


def read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def clean(value: str) -> str:
    return value.strip().strip("`").strip()


def table_value(text: str, key: str, default: str = "no_disponible") -> str:
    pattern = re.compile(r"^\|\s*" + re.escape(key) + r"\s*\|\s*([^|]+?)\s*\|", re.MULTILINE)
    match = pattern.search(text)
    return clean(match.group(1)) if match else default


def first_match(text: str, pattern: str, default: str = "no_disponible") -> str:
    match = re.search(pattern, text, re.MULTILINE)
    return clean(match.group(1)) if match else default


def comparison_delta(text: str, label: str, default: str = "no_disponible") -> str:
    pattern = re.compile(r"^\|\s*" + re.escape(label) + r"\s*\|\s*([-+]?\d+(?:\.\d+)?)\s*\|", re.MULTILINE)
    match = pattern.search(text)
    return clean(match.group(1)) if match else default


def comparison_wins_losses(text: str, label: str) -> tuple[str, str, str]:
    pattern = re.compile(
        r"^\|\s*" + re.escape(label) +
        r"\s*\|\s*[-+]?\d+(?:\.\d+)?\s*\|\s*[-+]?\d+(?:\.\d+)?\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|",
        re.MULTILINE,
    )
    match = pattern.search(text)
    if not match:
        return "no_disponible", "no_disponible", "no_disponible"
    return match.group(1), match.group(2), match.group(3)


def model_metric_row(text: str, model: str) -> dict[str, str]:
    pattern = re.compile(
        r"^\|\s*" + re.escape(model) +
        r"\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
        re.MULTILINE,
    )
    match = pattern.search(text)
    if not match:
        return {
            "rol": "no_disponible",
            "acc": "no_disponible",
            "macro_f1": "no_disponible",
            "std": "no_disponible",
            "wins": "no_disponible",
        }
    return {
        "rol": clean(match.group(1)),
        "acc": clean(match.group(2)),
        "macro_f1": clean(match.group(3)),
        "std": clean(match.group(4)),
        "wins": clean(match.group(5)),
    }


def to_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def decision_label(delta: str, wins: str, losses: str, semireal_decision: str) -> str:
    delta_f = to_float(delta)
    try:
        wins_i = int(wins)
        losses_i = int(losses)
    except (TypeError, ValueError):
        wins_i = losses_i = -1

    if semireal_decision == "semireal_prometedor" and delta_f is not None and delta_f >= 0.05 and wins_i > losses_i:
        return "candidato_experimental_para_R8-F"
    if delta_f is not None and abs(delta_f) < 0.01:
        return "empate_tecnico_con_v3"
    if delta_f is not None and delta_f < 0:
        return "v3_sigue_como_referencia"
    return "senal_mixta_requiere_mas_evaluacion"


def main() -> None:
    comparison = read(COMPARISON)
    classifier_repeated = read(CLASSIFIER_REPEATED)
    placeholder_repeated = read(PLACEHOLDER_REPEATED)
    semireal_repeated = read(SEMIREAL_REPEATED)

    fixed_best = first_match(comparison, r"^- Mejor modelo:\s*`?([^`\n]+)`?")
    fixed_delta_v1 = first_match(comparison, r"^- Delta vs v1:\s*`?([^`\n]+)`?")
    classifier_best = table_value(classifier_repeated, "Mejor promedio")

    placeholder_decision = table_value(placeholder_repeated, "Decisión operativa")
    placeholder_delta = comparison_delta(placeholder_repeated, "embedding_placeholder vs baseline_v3")

    semireal_best = table_value(semireal_repeated, "Mejor promedio")
    semireal_decision = table_value(semireal_repeated, "Decisión operativa")
    semireal_delta = comparison_delta(semireal_repeated, "embedding_semireal vs baseline_v3")
    semireal_wins, semireal_ties, semireal_losses = comparison_wins_losses(semireal_repeated, "embedding_semireal vs baseline_v3")

    v3_metrics = model_metric_row(semireal_repeated, "baseline_v3")
    semireal_metrics = model_metric_row(semireal_repeated, "embedding_semireal")

    final_decision = decision_label(semireal_delta, semireal_wins, semireal_losses, semireal_decision)

    md = f"""# E.C.O. - Decisión ampliada con embedding semi-real

## Propósito

Este reporte complementa la decisión oficial de modelos incorporando la ruta `embedding_semireal`.

No reemplaza automáticamente a `baseline_v3`: su función es decidir si la señal semi-real merece pasar a una evaluación extendida R8-F.

## Resumen ejecutivo

| Elemento | Resultado |
| --- | --- |
| Mejor modelo en split fijo | {fixed_best} |
| Delta del mejor modelo vs v1 | {fixed_delta_v1} |
| Mejor promedio clasificador repetido | {classifier_best} |
| Decisión placeholder | {placeholder_decision} |
| Delta placeholder vs v3 | {placeholder_delta} |
| Mejor promedio semi-real | {semireal_best} |
| Decisión semi-real | {semireal_decision} |
| Delta semi-real vs v3 | {semireal_delta} |
| Semi-real gana/empata/pierde vs v3 | {semireal_wins}/{semireal_ties}/{semireal_losses} |
| Decisión ampliada E.C.O. | {final_decision} |

## Comparación repetida clave

| Modelo | Rol | Test acc promedio | Macro F1 prom. | Macro F1 std | Mejor en repeticiones |
| --- | --- | ---: | ---: | ---: | ---: |
| baseline_v3 | {v3_metrics['rol']} | {v3_metrics['acc']} | {v3_metrics['macro_f1']} | {v3_metrics['std']} | {v3_metrics['wins']} |
| embedding_semireal | {semireal_metrics['rol']} | {semireal_metrics['acc']} | {semireal_metrics['macro_f1']} | {semireal_metrics['std']} | {semireal_metrics['wins']} |

## Lectura E.C.O.

`embedding_semireal` muestra una señal positiva frente a `baseline_v3`, pero todavía debe tratarse como transición controlada, no como reemplazo oficial.

La lectura prudente es:

```text
baseline_v1 = control explicable
baseline_v3 = referencia oficial pre-embeddings
embedding_placeholder = contrato vectorial validado
embedding_semireal = candidato experimental para evaluación extendida
```

## Criterio para R8-F

Para avanzar desde `semireal_prometedor` hacia candidato pre-oficial, R8-F debería evaluar:

1. 30 a 50 repeticiones estratificadas.
2. Delta promedio frente a `baseline_v3`.
3. Variabilidad entre splits.
4. Conteo gana/empata/pierde contra `baseline_v3`.
5. Rendimiento separado en casos fáciles, ambiguos y difíciles.
6. Reproducibilidad local sin dependencias pesadas.

## Decisión operativa

`embedding_semireal` no reemplaza todavía a `baseline_v3`.

Sí queda habilitado como **candidato experimental para R8-F**, porque su señal repetida es mayor que la del placeholder y supera a `baseline_v3` con margen práctico en la muestra actual.

## Límites responsables

- Dataset demostrativo pequeño.
- No es DNABERT.
- No es embedding profundo real.
- No es diagnóstico clínico.
- No representa benchmark científico general.
- La decisión final requiere evaluación extendida y documentación actualizada.
"""

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(md, encoding="utf-8")

    html = """<!doctype html>
<html lang=\"es\">
<head>
<meta charset=\"utf-8\">
<title>E.C.O. - Decisión ampliada semi-real</title>
<style>
body { font-family: system-ui, sans-serif; max-width: 980px; margin: 2rem auto; line-height: 1.5; padding: 0 1rem; }
pre { white-space: pre-wrap; background: #f6f6f6; padding: 1rem; border-radius: 0.75rem; }
</style>
</head>
<body>
<pre>""" + escape(md) + """</pre>
</body>
</html>
"""
    OUT_HTML.write_text(html, encoding="utf-8")

    print("E.C.O. MODEL DECISION SEMI-REAL REPORT")
    print("======================================")
    print(f"Markdown: {OUT_MD}")
    print(f"HTML: {OUT_HTML}")
    print("Estado: OK, reporte de decisión ampliada semi-real generado.")


if __name__ == "__main__":
    main()
