from pathlib import Path
import argparse
import importlib.util
import json
import math
import random
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


def get_centroids(model):
    """
    Extrae centroides desde varias estructuras posibles.

    El modelo usado por centroid_train puede venir como:
    - dict directo: {"regulatory": [...], "non_regulatory": [...]}
    - dict con clave "centroids"
    - tuple/list donde uno de los elementos es el dict de centroides
    - objeto con atributo .centroids

    Esta función evita acoplar el router a una sola forma interna del modelo.
    """
    if isinstance(model, dict):
        if "centroids" in model and isinstance(model["centroids"], dict):
            return model["centroids"]

        if model and all(isinstance(v, (list, tuple)) for v in model.values()):
            return model

    if isinstance(model, (tuple, list)):
        for item in model:
            if isinstance(item, dict):
                if "centroids" in item and isinstance(item["centroids"], dict):
                    return item["centroids"]

                if item and all(isinstance(v, (list, tuple)) for v in item.values()):
                    return item

    if hasattr(model, "centroids"):
        centroids = getattr(model, "centroids")
        if isinstance(centroids, dict):
            return centroids

    raise TypeError(
        "No se pudo interpretar la estructura del modelo centroid. "
        f"Tipo={type(model)} Preview={repr(model)[:500]}"
    )


def predict_with_confidence(row, model, feature_fn):
    centroids = get_centroids(model)
    vector = feature_fn(row["sequence"])

    distances = []
    for label, centroid in centroids.items():
        distances.append((label, euclidean(vector, centroid)))

    distances.sort(key=lambda x: x[1])
    pred = distances[0][0]

    if len(distances) < 2:
        return pred, 1.0

    d1 = distances[0][1]
    d2 = distances[1][1]

    confidence = (d2 - d1) / (d2 + 1e-12)
    confidence = max(0.0, min(1.0, confidence))
    return pred, confidence


def stratified_split_by_label(rows, ratio, seed):
    rng = random.Random(seed)
    grouped = {}

    for row in rows:
        grouped.setdefault(row["label"], []).append(row)

    left = []
    right = []

    for _, group in grouped.items():
        group = list(group)
        rng.shuffle(group)
        cut = int(round(len(group) * (1.0 - ratio)))
        cut = max(1, min(len(group) - 1, cut))
        left.extend(group[:cut])
        right.extend(group[cut:])

    rng.shuffle(left)
    rng.shuffle(right)
    return left, right


def metric_pack(eco, y_true, y_pred):
    return {
        "accuracy": eco.accuracy(y_true, y_pred),
        "macro_f1": eco.macro_f1(y_true, y_pred),
    }


def evaluate_threshold(eco, calibration_rows, model_v3, model_semireal, threshold, embedding_k, dimensions):
    y_true = []
    y_router = []

    for row in calibration_rows:
        pred_v3, confidence = predict_with_confidence(row, model_v3, eco.features_baseline_v3)
        pred_semireal = eco.predict(
            row,
            model_semireal,
            lambda seq: eco.features_semireal(seq, embedding_k, dimensions),
        )

        pred_router = pred_v3 if confidence >= threshold else pred_semireal

        y_true.append(row["label"])
        y_router.append(pred_router)

    return eco.macro_f1(y_true, y_router)


def choose_threshold(eco, calibration_rows, model_v3, model_semireal, thresholds, embedding_k, dimensions):
    scored = []

    for threshold in thresholds:
        f1 = evaluate_threshold(
            eco,
            calibration_rows,
            model_v3,
            model_semireal,
            threshold,
            embedding_k,
            dimensions,
        )
        scored.append((threshold, f1))

    scored.sort(key=lambda item: (item[1], -item[0]), reverse=True)
    return scored[0][0], scored


def evaluate_once(eco, rows, seed, args):
    train_cal, test = stratified_split_by_label(rows, args.test_ratio, seed)
    train, calibration = stratified_split_by_label(train_cal, args.calibration_ratio, seed + 10_000)

    model_v3 = eco.centroid_train(train, eco.features_baseline_v3)
    model_semireal = eco.centroid_train(
        train,
        lambda seq: eco.features_semireal(seq, args.embedding_k, args.dimensions),
    )

    thresholds = [round(i * args.threshold_step, 4) for i in range(int(args.threshold_max / args.threshold_step) + 1)]

    selected_threshold, calibration_scores = choose_threshold(
        eco,
        calibration,
        model_v3,
        model_semireal,
        thresholds,
        args.embedding_k,
        args.dimensions,
    )

    y_true = []
    pred_v3_all = []
    pred_semireal_all = []
    pred_router_all = []

    route_counts = {
        "baseline_v3": 0,
        "embedding_semireal": 0,
    }

    for row in test:
        pred_v3, confidence = predict_with_confidence(row, model_v3, eco.features_baseline_v3)
        pred_semireal = eco.predict(
            row,
            model_semireal,
            lambda seq: eco.features_semireal(seq, args.embedding_k, args.dimensions),
        )

        if confidence >= selected_threshold:
            pred_router = pred_v3
            route_counts["baseline_v3"] += 1
        else:
            pred_router = pred_semireal
            route_counts["embedding_semireal"] += 1

        y_true.append(row["label"])
        pred_v3_all.append(pred_v3)
        pred_semireal_all.append(pred_semireal)
        pred_router_all.append(pred_router)

    v3_metrics = metric_pack(eco, y_true, pred_v3_all)
    semireal_metrics = metric_pack(eco, y_true, pred_semireal_all)
    router_metrics = metric_pack(eco, y_true, pred_router_all)

    return {
        "seed": seed,
        "train": len(train),
        "calibration": len(calibration),
        "test": len(test),
        "selected_threshold": selected_threshold,
        "baseline_v3_accuracy": v3_metrics["accuracy"],
        "baseline_v3_macro_f1": v3_metrics["macro_f1"],
        "embedding_semireal_accuracy": semireal_metrics["accuracy"],
        "embedding_semireal_macro_f1": semireal_metrics["macro_f1"],
        "confidence_router_accuracy": router_metrics["accuracy"],
        "confidence_router_macro_f1": router_metrics["macro_f1"],
        "route_baseline_v3": route_counts["baseline_v3"],
        "route_embedding_semireal": route_counts["embedding_semireal"],
        "calibration_scores": calibration_scores,
    }


def summarize(records):
    return {
        "baseline_v3": {
            "accuracy_avg": round(avg([r["baseline_v3_accuracy"] for r in records]), 4),
            "macro_f1_avg": round(avg([r["baseline_v3_macro_f1"] for r in records]), 4),
            "macro_f1_std": round(std([r["baseline_v3_macro_f1"] for r in records]), 4),
        },
        "embedding_semireal": {
            "accuracy_avg": round(avg([r["embedding_semireal_accuracy"] for r in records]), 4),
            "macro_f1_avg": round(avg([r["embedding_semireal_macro_f1"] for r in records]), 4),
            "macro_f1_std": round(std([r["embedding_semireal_macro_f1"] for r in records]), 4),
        },
        "confidence_router_calibrated": {
            "accuracy_avg": round(avg([r["confidence_router_accuracy"] for r in records]), 4),
            "macro_f1_avg": round(avg([r["confidence_router_macro_f1"] for r in records]), 4),
            "macro_f1_std": round(std([r["confidence_router_macro_f1"] for r in records]), 4),
        },
    }


def decide(summary):
    v3 = summary["baseline_v3"]["macro_f1_avg"]
    semireal = summary["embedding_semireal"]["macro_f1_avg"]
    router = summary["confidence_router_calibrated"]["macro_f1_avg"]

    router_std = summary["confidence_router_calibrated"]["macro_f1_std"]
    semireal_std = summary["embedding_semireal"]["macro_f1_std"]

    if router > max(v3, semireal) + 0.01 and router_std <= semireal_std + 0.03:
        return "router_calibrado_prometedor"
    if router >= max(v3, semireal) - 0.01:
        return "router_calibrado_competitivo"
    return "mantener_como_experimento"


def to_markdown(payload):
    config = payload["config"]
    summary = payload["summary"]
    decision = payload["decision"]
    records = payload["records"]

    threshold_values = [r["selected_threshold"] for r in records]
    route_v3 = sum(r["route_baseline_v3"] for r in records)
    route_semireal = sum(r["route_embedding_semireal"] for r in records)

    lines = []
    lines.append("# E.C.O. - Router por confianza calibrado")
    lines.append("")
    lines.append("## Propósito")
    lines.append("")
    lines.append("Este informe evalúa un router sin oráculo que decide entre `baseline_v3` y `embedding_semireal` usando confianza interna.")
    lines.append("")
    lines.append("A diferencia de R8-G.4, el umbral se selecciona en una partición de calibración y luego se evalúa en test separado.")
    lines.append("")
    lines.append("```text")
    lines.append("train       -> entrena modelos")
    lines.append("calibration -> selecciona umbral")
    lines.append("test        -> evalúa router con umbral fijo")
    lines.append("```")
    lines.append("")
    lines.append("## Configuración")
    lines.append("")
    lines.append("| Campo | Valor |")
    lines.append("| --- | --- |")
    lines.append(f"| Dataset | {config['input']} |")
    lines.append(f"| Repeticiones | {config['repeats']} |")
    lines.append(f"| Test ratio | {config['test_ratio']} |")
    lines.append(f"| Calibration ratio sobre train_cal | {config['calibration_ratio']} |")
    lines.append(f"| Seed base | {config['base_seed']} |")
    lines.append(f"| Embedding k | {config['embedding_k']} |")
    lines.append(f"| Dimensiones | {config['dimensions']} |")
    lines.append(f"| Decisión | {decision} |")
    lines.append("")
    lines.append("## Resumen general")
    lines.append("")
    lines.append("| Modelo | Accuracy prom. | Macro F1 prom. | Macro F1 std |")
    lines.append("| --- | ---: | ---: | ---: |")
    for model, row in summary.items():
        lines.append(f"| {model} | {row['accuracy_avg']} | {row['macro_f1_avg']} | {row['macro_f1_std']} |")
    lines.append("")
    lines.append("## Umbrales seleccionados")
    lines.append("")
    lines.append(f"- Umbral promedio: `{round(avg(threshold_values), 4)}`")
    lines.append(f"- Umbral mínimo: `{min(threshold_values)}`")
    lines.append(f"- Umbral máximo: `{max(threshold_values)}`")
    lines.append("")
    lines.append("## Rutas usadas")
    lines.append("")
    lines.append("| Ruta | Veces usada |")
    lines.append("| --- | ---: |")
    lines.append(f"| baseline_v3 | {route_v3} |")
    lines.append(f"| embedding_semireal | {route_semireal} |")
    lines.append("")
    lines.append("## Detalle por repetición")
    lines.append("")
    lines.append("| Seed | Train | Calibration | Test | Umbral | V3 F1 | Semi-real F1 | Router F1 | Usa V3 | Usa Semi-real |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for r in records:
        lines.append(
            f"| {r['seed']} | {r['train']} | {r['calibration']} | {r['test']} | "
            f"{r['selected_threshold']} | {round(r['baseline_v3_macro_f1'], 4)} | "
            f"{round(r['embedding_semireal_macro_f1'], 4)} | "
            f"{round(r['confidence_router_macro_f1'], 4)} | "
            f"{r['route_baseline_v3']} | {r['route_embedding_semireal']} |"
        )
    lines.append("")
    lines.append("## Decisión E.C.O.")
    lines.append("")
    lines.append(f"**Decisión:** `{decision}`")
    lines.append("")
    lines.append("Lectura prudente:")
    lines.append("")
    lines.append("- Si el router calibrado supera a `baseline_v3`, ya existe una señal más honesta que R8-G.4.")
    lines.append("- Si además se acerca al router oracular, E.C.O. gana una válvula adaptativa realista.")
    lines.append("- Si baja frente al router no calibrado, es esperable: se eliminó optimismo por selección de umbral.")
    lines.append("")
    lines.append("## Límite responsable")
    lines.append("")
    lines.append("Este resultado sigue usando dataset demostrativo. No es diagnóstico clínico, no es benchmark científico general y no reemplaza validación externa.")
    lines.append("")
    return "\n".join(lines)


def to_html(markdown):
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>E.C.O. Router calibrado</title>
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
    parser = argparse.ArgumentParser(description="Router por confianza calibrado E.C.O.")
    parser.add_argument("--input", default="examples/eco_labeled_sequences.tsv")
    parser.add_argument("--repeats", type=int, default=50)
    parser.add_argument("--test-ratio", type=float, default=0.3)
    parser.add_argument("--calibration-ratio", type=float, default=0.25)
    parser.add_argument("--base-seed", type=int, default=42)
    parser.add_argument("--embedding-k", type=int, default=4)
    parser.add_argument("--dimensions", type=int, default=128)
    parser.add_argument("--threshold-step", type=float, default=0.05)
    parser.add_argument("--threshold-max", type=float, default=0.8)
    parser.add_argument("--output-json", default="results/eco_confidence_router_calibrated_eval_report.json")
    parser.add_argument("--output-md", default="results/eco_confidence_router_calibrated_eval_report.md")
    parser.add_argument("--output-html", default="results/eco_confidence_router_calibrated_eval_report.html")
    args = parser.parse_args()

    eco = load_difficulty_module()
    rows = eco.read_dataset(args.input)

    Path("results").mkdir(exist_ok=True)

    records = []
    for i in range(args.repeats):
        records.append(evaluate_once(eco, rows, args.base_seed + i, args))

    summary = summarize(records)
    decision = decide(summary)

    payload = {
        "config": vars(args),
        "decision": decision,
        "summary": summary,
        "records": records,
    }

    md = to_markdown(payload)

    Path(args.output_json).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    Path(args.output_md).write_text(md, encoding="utf-8")
    Path(args.output_html).write_text(to_html(md), encoding="utf-8")

    print("E.C.O. CALIBRATED CONFIDENCE ROUTER REPORT")
    print("==========================================")
    print(f"Dataset: {args.input}")
    print(f"Repeticiones: {args.repeats}")
    print(f"Decisión: {decision}")
    for model, row in summary.items():
        print(f"{model}: macro F1={row['macro_f1_avg']} | std={row['macro_f1_std']}")
    print(f"Reporte JSON: {args.output_json}")
    print(f"Reporte Markdown: {args.output_md}")
    print(f"Reporte HTML: {args.output_html}")
    print("Estado: OK, router calibrado evaluado.")


if __name__ == "__main__":
    main()
