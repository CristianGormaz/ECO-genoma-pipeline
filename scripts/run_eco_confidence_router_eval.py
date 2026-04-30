from pathlib import Path
import argparse
import importlib.util
import json
import math
import statistics
from html import escape


def load_difficulty_module():
    module_path = Path(__file__).with_name("run_eco_difficulty_eval.py")
    spec = importlib.util.spec_from_file_location("eco_difficulty_eval", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def avg(values):
    return sum(values) / len(values) if values else 0.0


def std(values):
    return statistics.pstdev(values) if len(values) > 1 else 0.0


def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def mean_vector(vectors):
    if not vectors:
        return []
    n = len(vectors)
    dim = len(vectors[0])
    return [sum(v[i] for v in vectors) / n for i in range(dim)]


def train_centroids(rows, feature_fn):
    grouped = {}
    for row in rows:
        label = row["label"]
        grouped.setdefault(label, []).append(feature_fn(row["sequence"]))

    return {
        label: mean_vector(vectors)
        for label, vectors in grouped.items()
    }


def predict_with_confidence(row, model, feature_fn):
    vector = feature_fn(row["sequence"])

    distances = []
    for label, centroid in model.items():
        distances.append((label, euclidean(vector, centroid)))

    distances.sort(key=lambda item: item[1])

    best_label, best_dist = distances[0]

    if len(distances) == 1:
        return best_label, 1.0

    second_dist = distances[1][1]

    # Confianza por margen: si la mejor clase está muy separada de la segunda,
    # el modelo está más seguro. Si están cerca, hay incertidumbre.
    confidence = (second_dist - best_dist) / (second_dist + 1e-9)
    confidence = max(0.0, min(1.0, confidence))

    return best_label, confidence


def summarize(records, prefix):
    acc_values = [r[f"{prefix}_acc"] for r in records]
    f1_values = [r[f"{prefix}_f1"] for r in records]

    return {
        "accuracy_avg": round(avg(acc_values), 4),
        "accuracy_std": round(std(acc_values), 4),
        "macro_f1_avg": round(avg(f1_values), 4),
        "macro_f1_std": round(std(f1_values), 4),
    }


def evaluate_threshold(args, threshold):
    eco = load_difficulty_module()
    rows = eco.read_dataset(args.input)

    records = []
    route_counts = {
        "baseline_v3": 0,
        "embedding_semireal": 0,
    }

    for offset in range(args.repeats):
        seed = args.base_seed + offset
        train, test = eco.stratified_split(rows, args.test_ratio, seed)

        feature_v3 = eco.features_baseline_v3
        feature_semireal = lambda seq: eco.features_semireal(
            seq,
            args.embedding_k,
            args.dimensions,
        )

        model_v3 = train_centroids(train, feature_v3)
        model_semireal = train_centroids(train, feature_semireal)

        y_true = []
        pred_v3_all = []
        pred_semireal_all = []
        pred_router_all = []
        confidence_values = []

        for row in test:
            label = row["label"]

            pred_v3, confidence = predict_with_confidence(row, model_v3, feature_v3)
            pred_semireal, _ = predict_with_confidence(row, model_semireal, feature_semireal)

            if confidence >= threshold:
                pred_router = pred_v3
                route_counts["baseline_v3"] += 1
            else:
                pred_router = pred_semireal
                route_counts["embedding_semireal"] += 1

            y_true.append(label)
            pred_v3_all.append(pred_v3)
            pred_semireal_all.append(pred_semireal)
            pred_router_all.append(pred_router)
            confidence_values.append(confidence)

        records.append({
            "seed": seed,
            "threshold": threshold,
            "confidence_avg": round(avg(confidence_values), 4),
            "baseline_v3_acc": eco.accuracy(y_true, pred_v3_all),
            "baseline_v3_f1": eco.macro_f1(y_true, pred_v3_all),
            "embedding_semireal_acc": eco.accuracy(y_true, pred_semireal_all),
            "embedding_semireal_f1": eco.macro_f1(y_true, pred_semireal_all),
            "confidence_router_acc": eco.accuracy(y_true, pred_router_all),
            "confidence_router_f1": eco.macro_f1(y_true, pred_router_all),
        })

    summary = {
        "threshold": threshold,
        "baseline_v3": summarize(records, "baseline_v3"),
        "embedding_semireal": summarize(records, "embedding_semireal"),
        "confidence_router": summarize(records, "confidence_router"),
        "route_counts": route_counts,
        "records": records,
    }

    return summary


def decide(best_summary):
    v3 = best_summary["baseline_v3"]["macro_f1_avg"]
    semireal = best_summary["embedding_semireal"]["macro_f1_avg"]
    router = best_summary["confidence_router"]["macro_f1_avg"]

    router_std = best_summary["confidence_router"]["macro_f1_std"]
    semireal_std = best_summary["embedding_semireal"]["macro_f1_std"]

    if router > semireal + 0.01 and router_std <= semireal_std + 0.02:
        return "router_confianza_prometedor"

    if router > v3 + 0.01:
        return "router_confianza_competitivo"

    return "mantener_como_experimento"


def run(args):
    thresholds = [
        round(x * args.threshold_step, 4)
        for x in range(0, int(args.threshold_max / args.threshold_step) + 1)
    ]

    threshold_summaries = [
        evaluate_threshold(args, threshold)
        for threshold in thresholds
    ]

    best = sorted(
        threshold_summaries,
        key=lambda item: (
            item["confidence_router"]["macro_f1_avg"],
            -item["confidence_router"]["macro_f1_std"],
        ),
        reverse=True,
    )[0]

    decision = decide(best)

    return {
        "config": vars(args),
        "decision": decision,
        "best_threshold": best["threshold"],
        "best_summary": best,
        "threshold_summaries": threshold_summaries,
    }


def to_markdown(payload):
    config = payload["config"]
    best = payload["best_summary"]

    lines = []
    lines.append("# E.C.O. - Router sin oráculo por confianza")
    lines.append("")
    lines.append("## Propósito")
    lines.append("")
    lines.append("Este informe evalúa un router que decide entre `baseline_v3` y `embedding_semireal` sin usar la etiqueta real de dificultad.")
    lines.append("")
    lines.append("La regla evaluada es:")
    lines.append("")
    lines.append("```text")
    lines.append("si confianza_baseline_v3 >= umbral:")
    lines.append("    usar baseline_v3")
    lines.append("si no:")
    lines.append("    usar embedding_semireal")
    lines.append("```")
    lines.append("")
    lines.append("## Configuración")
    lines.append("")
    lines.append("| Campo | Valor |")
    lines.append("| --- | --- |")
    lines.append(f"| Dataset | {config['input']} |")
    lines.append(f"| Repeticiones | {config['repeats']} |")
    lines.append(f"| Test ratio | {config['test_ratio']} |")
    lines.append(f"| Seed base | {config['base_seed']} |")
    lines.append(f"| Embedding k | {config['embedding_k']} |")
    lines.append(f"| Dimensiones | {config['dimensions']} |")
    lines.append(f"| Mejor umbral | {payload['best_threshold']} |")
    lines.append(f"| Decisión | {payload['decision']} |")
    lines.append("")
    lines.append("## Mejor resultado")
    lines.append("")
    lines.append("| Modelo | Accuracy prom. | Accuracy std | Macro F1 prom. | Macro F1 std |")
    lines.append("| --- | ---: | ---: | ---: | ---: |")
    for model in ["baseline_v3", "embedding_semireal", "confidence_router"]:
        row = best[model]
        lines.append(
            f"| {model} | {row['accuracy_avg']} | {row['accuracy_std']} | "
            f"{row['macro_f1_avg']} | {row['macro_f1_std']} |"
        )
    lines.append("")
    lines.append("## Rutas usadas por el router")
    lines.append("")
    lines.append("| Ruta | Veces usada |")
    lines.append("| --- | ---: |")
    for route, count in best["route_counts"].items():
        lines.append(f"| {route} | {count} |")
    lines.append("")
    lines.append("## Barrido de umbrales")
    lines.append("")
    lines.append("| Umbral | Router F1 prom. | Router std | V3 F1 prom. | Semi-real F1 prom. | Usa V3 | Usa Semi-real |")
    lines.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: |")

    for item in payload["threshold_summaries"]:
        lines.append(
            f"| {item['threshold']} | "
            f"{item['confidence_router']['macro_f1_avg']} | "
            f"{item['confidence_router']['macro_f1_std']} | "
            f"{item['baseline_v3']['macro_f1_avg']} | "
            f"{item['embedding_semireal']['macro_f1_avg']} | "
            f"{item['route_counts']['baseline_v3']} | "
            f"{item['route_counts']['embedding_semireal']} |"
        )

    lines.append("")
    lines.append("## Decisión E.C.O.")
    lines.append("")
    lines.append(f"**Decisión:** `{payload['decision']}`")
    lines.append("")
    lines.append("Lectura prudente:")
    lines.append("")
    lines.append("- Este router ya no usa `easy`, `ambiguous` ni `hard` para decidir.")
    lines.append("- Si mejora frente a `baseline_v3`, demuestra una ruta más realista que el router oracular.")
    lines.append("- Si no supera al router oracular, es normal: el oracular usa información privilegiada.")
    lines.append("- El siguiente paso sería calibrar el umbral con un conjunto de validación separado.")
    lines.append("")
    lines.append("## Límite responsable")
    lines.append("")
    lines.append("Este resultado sigue siendo demostrativo. No es diagnóstico clínico, no es benchmark científico general y no reemplaza validación externa.")
    lines.append("")
    return "\n".join(lines)


def to_html(markdown):
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>E.C.O. Router sin oráculo</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.5; }}
pre {{ background: #f4f4f4; padding: 12px; overflow-x: auto; white-space: pre-wrap; }}
</style>
</head>
<body>
<pre>{escape(markdown)}</pre>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Router sin oráculo por confianza E.C.O.")
    parser.add_argument("--input", default="examples/eco_labeled_sequences.tsv")
    parser.add_argument("--repeats", type=int, default=50)
    parser.add_argument("--test-ratio", type=float, default=0.4)
    parser.add_argument("--base-seed", type=int, default=42)
    parser.add_argument("--embedding-k", type=int, default=4)
    parser.add_argument("--dimensions", type=int, default=128)
    parser.add_argument("--threshold-max", type=float, default=0.8)
    parser.add_argument("--threshold-step", type=float, default=0.05)
    parser.add_argument("--output-json", default="results/eco_confidence_router_eval_report.json")
    parser.add_argument("--output-md", default="results/eco_confidence_router_eval_report.md")
    parser.add_argument("--output-html", default="results/eco_confidence_router_eval_report.html")
    args = parser.parse_args()

    Path("results").mkdir(exist_ok=True)

    payload = run(args)
    md = to_markdown(payload)

    Path(args.output_json).write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    Path(args.output_md).write_text(md, encoding="utf-8")
    Path(args.output_html).write_text(to_html(md), encoding="utf-8")

    best = payload["best_summary"]

    print("E.C.O. CONFIDENCE ROUTER EVALUATION REPORT")
    print("==========================================")
    print(f"Dataset: {args.input}")
    print(f"Repeticiones: {args.repeats}")
    print(f"Mejor umbral: {payload['best_threshold']}")
    print(f"Decisión: {payload['decision']}")
    print(f"baseline_v3 macro F1: {best['baseline_v3']['macro_f1_avg']}")
    print(f"embedding_semireal macro F1: {best['embedding_semireal']['macro_f1_avg']}")
    print(f"confidence_router macro F1: {best['confidence_router']['macro_f1_avg']}")
    print(f"confidence_router std: {best['confidence_router']['macro_f1_std']}")
    print(f"Reporte JSON: {args.output_json}")
    print(f"Reporte Markdown: {args.output_md}")
    print(f"Reporte HTML: {args.output_html}")
    print("Estado: OK, router sin oráculo evaluado.")


if __name__ == "__main__":
    main()
