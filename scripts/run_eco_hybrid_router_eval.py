from pathlib import Path
import argparse
import importlib.util
import json
import statistics
from collections import defaultdict
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


def summarize(records, model):
    f1_values = [r[f"{model}_f1"] for r in records]
    acc_values = [r[f"{model}_acc"] for r in records]
    return {
        "accuracy_avg": round(avg(acc_values), 4),
        "accuracy_std": round(std(acc_values), 4),
        "macro_f1_avg": round(avg(f1_values), 4),
        "macro_f1_std": round(std(f1_values), 4),
    }


def decide(overall_summary):
    v3 = overall_summary["baseline_v3"]["macro_f1_avg"]
    semireal = overall_summary["embedding_semireal"]["macro_f1_avg"]
    hybrid = overall_summary["hybrid_router"]["macro_f1_avg"]

    hybrid_std = overall_summary["hybrid_router"]["macro_f1_std"]
    semireal_std = overall_summary["embedding_semireal"]["macro_f1_std"]

    if hybrid > max(v3, semireal) + 0.01 and hybrid_std <= semireal_std:
        return "router_hibrido_prometedor"
    if hybrid >= max(v3, semireal) - 0.01:
        return "router_hibrido_competitivo"
    return "mantener_como_experimento"


def evaluate(args):
    eco = load_difficulty_module()
    rows = eco.read_dataset(args.input)

    overall_records = []
    difficulty_records = defaultdict(list)

    for offset in range(args.repeats):
        seed = args.base_seed + offset
        train, test = eco.stratified_split(rows, args.test_ratio, seed)

        model_v3 = eco.centroid_train(train, eco.features_baseline_v3)
        model_semireal = eco.centroid_train(
            train,
            lambda seq: eco.features_semireal(seq, args.embedding_k, args.dimensions),
        )

        y_true_all = []
        pred_v3_all = []
        pred_semireal_all = []
        pred_hybrid_all = []

        grouped = defaultdict(lambda: {
            "y_true": [],
            "v3": [],
            "semireal": [],
            "hybrid": [],
        })

        for row in test:
            y_true = row["label"]
            difficulty = row["difficulty"]

            pred_v3 = eco.predict(row, model_v3, eco.features_baseline_v3)
            pred_semireal = eco.predict(
                row,
                model_semireal,
                lambda seq: eco.features_semireal(seq, args.embedding_k, args.dimensions),
            )

            if difficulty == "easy":
                pred_hybrid = pred_v3
            else:
                pred_hybrid = pred_semireal

            y_true_all.append(y_true)
            pred_v3_all.append(pred_v3)
            pred_semireal_all.append(pred_semireal)
            pred_hybrid_all.append(pred_hybrid)

            grouped[difficulty]["y_true"].append(y_true)
            grouped[difficulty]["v3"].append(pred_v3)
            grouped[difficulty]["semireal"].append(pred_semireal)
            grouped[difficulty]["hybrid"].append(pred_hybrid)

        overall_record = {
            "seed": seed,
            "baseline_v3_acc": eco.accuracy(y_true_all, pred_v3_all),
            "baseline_v3_f1": eco.macro_f1(y_true_all, pred_v3_all),
            "embedding_semireal_acc": eco.accuracy(y_true_all, pred_semireal_all),
            "embedding_semireal_f1": eco.macro_f1(y_true_all, pred_semireal_all),
            "hybrid_router_acc": eco.accuracy(y_true_all, pred_hybrid_all),
            "hybrid_router_f1": eco.macro_f1(y_true_all, pred_hybrid_all),
        }
        overall_records.append(overall_record)

        for difficulty, data in grouped.items():
            difficulty_records[difficulty].append({
                "seed": seed,
                "n": len(data["y_true"]),
                "baseline_v3_acc": eco.accuracy(data["y_true"], data["v3"]),
                "baseline_v3_f1": eco.macro_f1(data["y_true"], data["v3"]),
                "embedding_semireal_acc": eco.accuracy(data["y_true"], data["semireal"]),
                "embedding_semireal_f1": eco.macro_f1(data["y_true"], data["semireal"]),
                "hybrid_router_acc": eco.accuracy(data["y_true"], data["hybrid"]),
                "hybrid_router_f1": eco.macro_f1(data["y_true"], data["hybrid"]),
            })

    overall_summary = {
        "baseline_v3": summarize(overall_records, "baseline_v3"),
        "embedding_semireal": summarize(overall_records, "embedding_semireal"),
        "hybrid_router": summarize(overall_records, "hybrid_router"),
    }

    difficulty_summary = {}
    for difficulty, records in sorted(difficulty_records.items()):
        difficulty_summary[difficulty] = {
            "baseline_v3": summarize(records, "baseline_v3"),
            "embedding_semireal": summarize(records, "embedding_semireal"),
            "hybrid_router": summarize(records, "hybrid_router"),
        }

    final_decision = decide(overall_summary)

    return {
        "config": vars(args),
        "decision": final_decision,
        "overall_summary": overall_summary,
        "difficulty_summary": difficulty_summary,
        "overall_records": overall_records,
        "difficulty_records": difficulty_records,
    }


def to_markdown(payload):
    config = payload["config"]
    decision = payload["decision"]
    overall = payload["overall_summary"]
    by_difficulty = payload["difficulty_summary"]

    lines = []
    lines.append("# E.C.O. - Evaluación de router híbrido por dificultad")
    lines.append("")
    lines.append("## Propósito")
    lines.append("")
    lines.append("Este informe prueba una regla híbrida:")
    lines.append("")
    lines.append("```text")
    lines.append("easy      -> baseline_v3")
    lines.append("ambiguous -> embedding_semireal")
    lines.append("hard      -> embedding_semireal")
    lines.append("```")
    lines.append("")
    lines.append("La hipótesis es que `baseline_v3` conserva mejor los casos fáciles, mientras `embedding_semireal` aporta más valor en casos ambiguos y difíciles.")
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
    lines.append(f"| Decisión | {decision} |")
    lines.append("")
    lines.append("## Resumen general")
    lines.append("")
    lines.append("| Modelo | Accuracy prom. | Accuracy std | Macro F1 prom. | Macro F1 std |")
    lines.append("| --- | ---: | ---: | ---: | ---: |")
    for model, row in overall.items():
        lines.append(
            f"| {model} | {row['accuracy_avg']} | {row['accuracy_std']} | "
            f"{row['macro_f1_avg']} | {row['macro_f1_std']} |"
        )

    lines.append("")
    lines.append("## Resumen por dificultad")
    lines.append("")
    for difficulty, models in by_difficulty.items():
        lines.append(f"### {difficulty}")
        lines.append("")
        lines.append("| Modelo | Accuracy prom. | Macro F1 prom. | Macro F1 std |")
        lines.append("| --- | ---: | ---: | ---: |")
        for model, row in models.items():
            lines.append(
                f"| {model} | {row['accuracy_avg']} | {row['macro_f1_avg']} | {row['macro_f1_std']} |"
            )
        lines.append("")

    lines.append("## Decisión E.C.O.")
    lines.append("")
    lines.append(f"**Decisión:** `{decision}`")
    lines.append("")
    lines.append("Lectura prudente:")
    lines.append("")
    lines.append("- Si el router mejora el promedio sin aumentar la variabilidad, puede pasar a candidato pre-oficial condicional.")
    lines.append("- Si solo empata, se mantiene como experimento arquitectónico.")
    lines.append("- Este router todavía usa etiquetas de dificultad conocidas; en datos reales habría que inferir dificultad automáticamente.")
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
<title>E.C.O. Router híbrido</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.5; }}
pre {{ background: #f4f4f4; padding: 12px; overflow-x: auto; }}
</style>
</head>
<body>
<pre>{escape(markdown)}</pre>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Evaluación de router híbrido E.C.O.")
    parser.add_argument("--input", default="examples/eco_labeled_sequences.tsv")
    parser.add_argument("--repeats", type=int, default=50)
    parser.add_argument("--test-ratio", type=float, default=0.4)
    parser.add_argument("--base-seed", type=int, default=42)
    parser.add_argument("--embedding-k", type=int, default=4)
    parser.add_argument("--dimensions", type=int, default=128)
    parser.add_argument("--output-json", default="results/eco_hybrid_router_eval_report.json")
    parser.add_argument("--output-md", default="results/eco_hybrid_router_eval_report.md")
    parser.add_argument("--output-html", default="results/eco_hybrid_router_eval_report.html")
    args = parser.parse_args()

    Path("results").mkdir(exist_ok=True)

    payload = evaluate(args)
    md = to_markdown(payload)

    Path(args.output_json).write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=list), encoding="utf-8")
    Path(args.output_md).write_text(md, encoding="utf-8")
    Path(args.output_html).write_text(to_html(md), encoding="utf-8")

    print("E.C.O. HYBRID ROUTER EVALUATION REPORT")
    print("======================================")
    print(f"Dataset: {args.input}")
    print(f"Repeticiones: {args.repeats}")
    print(f"Decisión: {payload['decision']}")
    for model, row in payload["overall_summary"].items():
        print(f"{model}: macro F1={row['macro_f1_avg']} | std={row['macro_f1_std']}")
    print(f"Reporte JSON: {args.output_json}")
    print(f"Reporte Markdown: {args.output_md}")
    print(f"Reporte HTML: {args.output_html}")
    print("Estado: OK, router híbrido evaluado.")


if __name__ == "__main__":
    main()
