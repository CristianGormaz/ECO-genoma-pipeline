from pathlib import Path
import argparse
import csv
import hashlib
import html
import itertools
import json
import math
import random
import statistics
from collections import defaultdict, Counter

LABELS = ["non_regulatory", "regulatory"]
RESULTS = Path("results")

MOTIFS = [
    ("CAAT_box", "CCAAT"),
    ("TATA_box_canonica", "TATAAA"),
    ("TATA_box_degenerada", "TATA"),
    ("GC_box", "GGGCGG"),
    ("polyA_signal", "AATAAA"),
]


def read_dataset(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            row["difficulty"] = infer_difficulty(row["sequence_id"])
            rows.append(row)
    return rows


def infer_difficulty(sequence_id):
    if "_easy_" in sequence_id:
        return "easy"
    if "_amb_" in sequence_id:
        return "ambiguous"
    if "_hard_" in sequence_id:
        return "hard"
    return "unknown"


def all_kmers(k):
    return ["".join(p) for p in itertools.product("ACGT", repeat=k)]


def motif_features(seq):
    return [seq.count(pattern) for _, pattern in MOTIFS]


def kmer_features_vocab(seq, k):
    vocab = all_kmers(k)
    counts = Counter(seq[i:i+k] for i in range(max(0, len(seq) - k + 1)))
    total = sum(counts[kmer] for kmer in vocab) or 1
    return [counts[kmer] / total for kmer in vocab]


def hashed_kmer_features(seq, k, dimensions):
    vec = [0.0] * dimensions
    total = 0
    for i in range(max(0, len(seq) - k + 1)):
        kmer = seq[i:i+k]
        if any(ch not in "ACGT" for ch in kmer):
            continue
        digest = hashlib.md5(kmer.encode("utf-8")).hexdigest()
        idx = int(digest, 16) % dimensions
        vec[idx] += 1.0
        total += 1
    if total:
        vec = [x / total for x in vec]
    return vec


def features_baseline_v3(seq):
    return motif_features(seq) + kmer_features_vocab(seq, 3)


def features_semireal(seq, embedding_k=4, dimensions=128):
    return hashed_kmer_features(seq, embedding_k, dimensions)


def stratified_split(rows, test_ratio, seed):
    rng = random.Random(seed)
    by_label = defaultdict(list)
    for row in rows:
        by_label[row["label"]].append(row)

    train, test = [], []
    for label, group in by_label.items():
        group = list(group)
        rng.shuffle(group)
        n_test = max(1, round(len(group) * test_ratio))
        test.extend(group[:n_test])
        train.extend(group[n_test:])

    return train, test


def fit_minmax(matrix):
    if not matrix:
        return [], []
    n = len(matrix[0])
    mins = [min(row[i] for row in matrix) for i in range(n)]
    maxs = [max(row[i] for row in matrix) for i in range(n)]
    return mins, maxs


def apply_minmax(vec, mins, maxs):
    out = []
    for x, mn, mx in zip(vec, mins, maxs):
        if mx == mn:
            out.append(0.0)
        else:
            out.append((x - mn) / (mx - mn))
    return out


def centroid_train(rows, feature_fn):
    raw_x = [feature_fn(row["sequence"]) for row in rows]
    mins, maxs = fit_minmax(raw_x)
    scaled = [apply_minmax(x, mins, maxs) for x in raw_x]

    by_label = defaultdict(list)
    for row, vec in zip(rows, scaled):
        by_label[row["label"]].append(vec)

    centroids = {}
    for label, vectors in by_label.items():
        n = len(vectors[0])
        centroids[label] = [
            sum(vec[i] for vec in vectors) / len(vectors)
            for i in range(n)
        ]

    return centroids, mins, maxs


def distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def predict(row, model, feature_fn):
    centroids, mins, maxs = model
    vec = apply_minmax(feature_fn(row["sequence"]), mins, maxs)
    return min(centroids, key=lambda label: distance(vec, centroids[label]))


def macro_f1(y_true, y_pred):
    scores = []
    for label in LABELS:
        tp = sum(1 for a, b in zip(y_true, y_pred) if a == label and b == label)
        fp = sum(1 for a, b in zip(y_true, y_pred) if a != label and b == label)
        fn = sum(1 for a, b in zip(y_true, y_pred) if a == label and b != label)
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        scores.append(f1)
    return sum(scores) / len(scores)


def accuracy(y_true, y_pred):
    return sum(1 for a, b in zip(y_true, y_pred) if a == b) / len(y_true) if y_true else 0.0


def avg(values):
    return sum(values) / len(values) if values else 0.0


def std(values):
    return statistics.pstdev(values) if len(values) > 1 else 0.0


def evaluate(rows, repeats, test_ratio, base_seed, embedding_k, dimensions):
    per_difficulty = defaultdict(lambda: {
        "v3_f1": [],
        "semireal_f1": [],
        "v3_acc": [],
        "semireal_acc": [],
        "wins": 0,
        "ties": 0,
        "losses": 0,
        "n_tests": [],
    })

    details = []

    for offset in range(repeats):
        seed = base_seed + offset
        train, test = stratified_split(rows, test_ratio, seed)

        model_v3 = centroid_train(train, features_baseline_v3)
        model_semireal = centroid_train(
            train,
            lambda seq: features_semireal(seq, embedding_k, dimensions),
        )

        grouped = defaultdict(list)
        for row in test:
            grouped[row["difficulty"]].append(row)

        for difficulty, group in grouped.items():
            y_true = [row["label"] for row in group]
            pred_v3 = [predict(row, model_v3, features_baseline_v3) for row in group]
            pred_semireal = [
                predict(
                    row,
                    model_semireal,
                    lambda seq: features_semireal(seq, embedding_k, dimensions),
                )
                for row in group
            ]

            f1_v3 = macro_f1(y_true, pred_v3)
            f1_semireal = macro_f1(y_true, pred_semireal)
            acc_v3 = accuracy(y_true, pred_v3)
            acc_semireal = accuracy(y_true, pred_semireal)
            delta = f1_semireal - f1_v3

            bucket = per_difficulty[difficulty]
            bucket["v3_f1"].append(f1_v3)
            bucket["semireal_f1"].append(f1_semireal)
            bucket["v3_acc"].append(acc_v3)
            bucket["semireal_acc"].append(acc_semireal)
            bucket["n_tests"].append(len(group))

            if delta > 0.000001:
                bucket["wins"] += 1
                winner = "embedding_semireal"
            elif delta < -0.000001:
                bucket["losses"] += 1
                winner = "baseline_v3"
            else:
                bucket["ties"] += 1
                winner = "tie"

            details.append({
                "seed": seed,
                "difficulty": difficulty,
                "n": len(group),
                "v3_macro_f1": round(f1_v3, 4),
                "semireal_macro_f1": round(f1_semireal, 4),
                "delta": round(delta, 4),
                "winner": winner,
            })

    summary = {}
    for difficulty, data in sorted(per_difficulty.items()):
        delta_values = [
            b - a for a, b in zip(data["v3_f1"], data["semireal_f1"])
        ]
        summary[difficulty] = {
            "repetitions_seen": len(data["v3_f1"]),
            "avg_test_items": round(avg(data["n_tests"]), 2),
            "baseline_v3_macro_f1_avg": round(avg(data["v3_f1"]), 4),
            "baseline_v3_macro_f1_std": round(std(data["v3_f1"]), 4),
            "semireal_macro_f1_avg": round(avg(data["semireal_f1"]), 4),
            "semireal_macro_f1_std": round(std(data["semireal_f1"]), 4),
            "delta_avg": round(avg(delta_values), 4),
            "delta_std": round(std(delta_values), 4),
            "wins": data["wins"],
            "ties": data["ties"],
            "losses": data["losses"],
        }

    return summary, details


def decision(summary):
    amb = summary.get("ambiguous", {})
    hard = summary.get("hard", {})
    easy = summary.get("easy", {})

    amb_ok = amb.get("delta_avg", 0) > 0.01 and amb.get("wins", 0) >= amb.get("losses", 0)
    hard_ok = hard.get("delta_avg", 0) > 0.01 and hard.get("wins", 0) >= hard.get("losses", 0)
    easy_only = easy.get("delta_avg", 0) > 0.01 and not (amb_ok or hard_ok)

    if amb_ok and hard_ok:
        return "candidato_preoficial_condicional"
    if amb_ok or hard_ok:
        return "candidato_experimental_con_senal_util"
    if easy_only:
        return "no_promover_mejora_concentrada_en_easy"
    return "mantener_como_experimental"


def to_markdown(config, summary, details, final_decision):
    lines = []
    lines.append("# E.C.O. - Evaluación por dificultad de casos")
    lines.append("")
    lines.append("## Propósito")
    lines.append("")
    lines.append("Este informe evalúa si `embedding_semireal` mejora frente a `baseline_v3` según dificultad del caso: `easy`, `ambiguous` y `hard`.")
    lines.append("")
    lines.append("## Configuración")
    lines.append("")
    lines.append("| Campo | Valor |")
    lines.append("| --- | --- |")
    for k, v in config.items():
        lines.append(f"| {k} | {v} |")
    lines.append("")
    lines.append("## Resumen por dificultad")
    lines.append("")
    lines.append("| Dificultad | V3 F1 prom. | V3 std | Semi-real F1 prom. | Semi-real std | Delta | Gana/Empata/Pierde | Decisión local |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |")

    for diff in ["easy", "ambiguous", "hard", "unknown"]:
        if diff not in summary:
            continue
        row = summary[diff]
        local = "favorable" if row["delta_avg"] > 0.01 and row["wins"] >= row["losses"] else "mixta"
        lines.append(
            f"| {diff} | {row['baseline_v3_macro_f1_avg']} | {row['baseline_v3_macro_f1_std']} | "
            f"{row['semireal_macro_f1_avg']} | {row['semireal_macro_f1_std']} | {row['delta_avg']} | "
            f"{row['wins']}/{row['ties']}/{row['losses']} | {local} |"
        )

    lines.append("")
    lines.append("## Decisión E.C.O.")
    lines.append("")
    lines.append(f"**Decisión:** `{final_decision}`")
    lines.append("")
    lines.append("Lectura prudente:")
    lines.append("")
    lines.append("- Si la mejora aparece solo en `easy`, no se promueve.")
    lines.append("- Si la mejora aparece en `ambiguous` o `hard`, la señal es más útil.")
    lines.append("- Si además baja la variabilidad, puede avanzar como candidato pre-oficial condicional.")
    lines.append("")
    lines.append("## Detalle por repetición")
    lines.append("")
    lines.append("| Seed | Dificultad | N | V3 F1 | Semi-real F1 | Delta | Mejor |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | --- |")
    for item in details:
        lines.append(
            f"| {item['seed']} | {item['difficulty']} | {item['n']} | "
            f"{item['v3_macro_f1']} | {item['semireal_macro_f1']} | {item['delta']} | {item['winner']} |"
        )

    lines.append("")
    lines.append("## Límites responsables")
    lines.append("")
    lines.append("- Dataset demostrativo pequeño.")
    lines.append("- No es DNABERT.")
    lines.append("- No es diagnóstico clínico.")
    lines.append("- No representa benchmark científico general.")
    lines.append("- La decisión debe validarse con datos externos antes de cualquier conclusión fuerte.")
    lines.append("")
    return "\n".join(lines)


def to_html(markdown):
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>E.C.O. Evaluación por dificultad</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.5; }}
pre {{ background: #f4f4f4; padding: 12px; overflow-x: auto; }}
table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
th, td {{ border: 1px solid #ddd; padding: 8px; }}
th {{ background: #f2f2f2; }}
</style>
</head>
<body>
<pre>{html.escape(markdown)}</pre>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Evaluación E.C.O. por dificultad de casos.")
    parser.add_argument("--input", default="examples/eco_labeled_sequences.tsv")
    parser.add_argument("--repeats", type=int, default=50)
    parser.add_argument("--test-ratio", type=float, default=0.4)
    parser.add_argument("--base-seed", type=int, default=42)
    parser.add_argument("--embedding-k", type=int, default=4)
    parser.add_argument("--dimensions", type=int, default=128)
    parser.add_argument("--output-json", default="results/eco_difficulty_eval_report.json")
    parser.add_argument("--output-md", default="results/eco_difficulty_eval_report.md")
    parser.add_argument("--output-html", default="results/eco_difficulty_eval_report.html")
    args = parser.parse_args()

    RESULTS.mkdir(exist_ok=True)

    rows = read_dataset(args.input)
    summary, details = evaluate(
        rows=rows,
        repeats=args.repeats,
        test_ratio=args.test_ratio,
        base_seed=args.base_seed,
        embedding_k=args.embedding_k,
        dimensions=args.dimensions,
    )

    final_decision = decision(summary)

    payload = {
        "config": vars(args),
        "summary": summary,
        "decision": final_decision,
        "details": details,
    }

    Path(args.output_json).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    config = {
        "Dataset": args.input,
        "Repeticiones": args.repeats,
        "Test ratio": args.test_ratio,
        "Seed base": args.base_seed,
        "Embedding": "kmer_frequency_semireal",
        "k": args.embedding_k,
        "Dimensiones": args.dimensions,
        "Decisión": final_decision,
    }

    md = to_markdown(config, summary, details, final_decision)
    Path(args.output_md).write_text(md, encoding="utf-8")
    Path(args.output_html).write_text(to_html(md), encoding="utf-8")

    print("E.C.O. DIFFICULTY EVALUATION REPORT")
    print("===================================")
    print(f"Dataset: {args.input}")
    print(f"Repeticiones: {args.repeats}")
    print(f"Decisión: {final_decision}")
    for diff, row in summary.items():
        print(
            f"{diff}: v3={row['baseline_v3_macro_f1_avg']} | "
            f"semireal={row['semireal_macro_f1_avg']} | "
            f"delta={row['delta_avg']} | "
            f"G/E/P={row['wins']}/{row['ties']}/{row['losses']}"
        )
    print(f"Reporte JSON: {args.output_json}")
    print(f"Reporte Markdown: {args.output_md}")
    print(f"Reporte HTML: {args.output_html}")
    print("Estado: OK, evaluación por dificultad generada.")


if __name__ == "__main__":
    main()
