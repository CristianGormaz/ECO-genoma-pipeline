from pathlib import Path
import argparse
import importlib.util
import json
from html import escape


def load_module(path, name):
    module_path = Path(path)
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def clean_sequence(seq):
    seq = seq.strip().upper().replace(" ", "").replace("\n", "")
    invalid = sorted(set(seq) - set("ACGTN"))
    if invalid:
        raise SystemExit(f"ERROR: secuencia contiene caracteres no válidos: {', '.join(invalid)}")
    if not seq:
        raise SystemExit("ERROR: secuencia vacía.")
    return seq


def make_markdown(payload):
    lines = []
    lines.append("# E.C.O. - Predicción con router adaptativo")
    lines.append("")
    lines.append("## Propósito")
    lines.append("")
    lines.append("Este reporte ejecuta una predicción individual usando la válvula adaptativa E.C.O.")
    lines.append("")
    lines.append("```text")
    lines.append("si confianza_baseline_v3 >= umbral:")
    lines.append("    usar baseline_v3")
    lines.append("si no:")
    lines.append("    usar embedding_semireal")
    lines.append("```")
    lines.append("")
    lines.append("## Entrada")
    lines.append("")
    lines.append("| Campo | Valor |")
    lines.append("| --- | --- |")
    lines.append(f"| Sequence ID | {payload['sequence_id']} |")
    lines.append(f"| Secuencia | `{payload['sequence']}` |")
    lines.append(f"| Longitud | {payload['length']} |")
    lines.append(f"| Umbral | {payload['threshold']} |")
    lines.append("")
    lines.append("## Resultados internos")
    lines.append("")
    lines.append("| Ruta | Predicción | Confianza |")
    lines.append("| --- | --- | ---: |")
    lines.append(f"| baseline_v3 | {payload['baseline_v3']['prediction']} | {payload['baseline_v3']['confidence']} |")
    lines.append(f"| embedding_semireal | {payload['embedding_semireal']['prediction']} | {payload['embedding_semireal']['confidence']} |")
    lines.append("")
    lines.append("## Decisión adaptativa")
    lines.append("")
    lines.append("| Elemento | Resultado |")
    lines.append("| --- | --- |")
    lines.append(f"| Ruta seleccionada | {payload['selected_route']} |")
    lines.append(f"| Predicción final | {payload['final_prediction']} |")
    lines.append(f"| Motivo | {payload['reason']} |")
    lines.append("")
    lines.append("## Lectura E.C.O.")
    lines.append("")
    lines.append(payload["eco_reading"])
    lines.append("")
    lines.append("## Límite responsable")
    lines.append("")
    lines.append("Este resultado es demostrativo. No es diagnóstico clínico, no es benchmark científico y no reemplaza validación externa.")
    lines.append("")
    return "\n".join(lines)


def make_html(md):
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>E.C.O. Predicción adaptativa</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.5; }}
pre {{ background: #f4f4f4; padding: 12px; overflow-x: auto; }}
</style>
</head>
<body>
<pre>{escape(md)}</pre>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Predicción individual con router adaptativo E.C.O.")
    parser.add_argument("--sequence", required=True)
    parser.add_argument("--sequence-id", default="user_sequence")
    parser.add_argument("--input", default="examples/eco_labeled_sequences.tsv")
    parser.add_argument("--threshold", type=float, default=0.20)
    parser.add_argument("--embedding-k", type=int, default=4)
    parser.add_argument("--dimensions", type=int, default=128)
    parser.add_argument("--output-json", default="results/eco_adaptive_router_prediction.json")
    parser.add_argument("--output-md", default="results/eco_adaptive_router_prediction.md")
    parser.add_argument("--output-html", default="results/eco_adaptive_router_prediction.html")
    args = parser.parse_args()

    eco = load_module("scripts/run_eco_difficulty_eval.py", "eco_difficulty_eval")
    router = load_module("scripts/run_eco_confidence_router_calibrated_eval.py", "eco_confidence_router_calibrated_eval")

    sequence = clean_sequence(args.sequence)
    rows = eco.read_dataset(args.input)

    semireal_features = lambda seq: eco.features_semireal(seq, args.embedding_k, args.dimensions)

    model_v3 = eco.centroid_train(rows, eco.features_baseline_v3)
    model_semireal = eco.centroid_train(rows, semireal_features)

    row = {
        "sequence_id": args.sequence_id,
        "sequence": sequence,
        "label": "unknown",
        "split": "inference",
        "difficulty": "unknown",
    }

    pred_v3, confidence_v3 = router.predict_with_confidence(row, model_v3, eco.features_baseline_v3)
    pred_semireal, confidence_semireal = router.predict_with_confidence(row, model_semireal, semireal_features)

    if confidence_v3 >= args.threshold:
        selected_route = "baseline_v3"
        final_prediction = pred_v3
        reason = "confianza_baseline_v3_supera_umbral"
        eco_reading = "La secuencia fue tratada como un dato relativamente claro. E.C.O. usó la ruta explicable rápida."
    else:
        selected_route = "embedding_semireal"
        final_prediction = pred_semireal
        reason = "confianza_baseline_v3_bajo_umbral"
        eco_reading = "La secuencia fue tratada como un dato incierto. E.C.O. derivó hacia la ruta vectorial semi-real."

    payload = {
        "sequence_id": args.sequence_id,
        "sequence": sequence,
        "length": len(sequence),
        "threshold": args.threshold,
        "baseline_v3": {
            "prediction": pred_v3,
            "confidence": round(confidence_v3, 4),
        },
        "embedding_semireal": {
            "prediction": pred_semireal,
            "confidence": round(confidence_semireal, 4),
        },
        "selected_route": selected_route,
        "final_prediction": final_prediction,
        "reason": reason,
        "eco_reading": eco_reading,
        "limits": [
            "dataset demostrativo",
            "no diagnostico clinico",
            "no benchmark cientifico",
            "umbral basado en R8-G.5",
        ],
    }

    Path("results").mkdir(exist_ok=True)

    md = make_markdown(payload)

    Path(args.output_json).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    Path(args.output_md).write_text(md, encoding="utf-8")
    Path(args.output_html).write_text(make_html(md), encoding="utf-8")

    print("E.C.O. ADAPTIVE ROUTER PREDICTION")
    print("=================================")
    print(f"Sequence ID: {args.sequence_id}")
    print(f"Longitud: {len(sequence)}")
    print(f"baseline_v3: {pred_v3} | confianza={round(confidence_v3, 4)}")
    print(f"embedding_semireal: {pred_semireal} | confianza={round(confidence_semireal, 4)}")
    print(f"Ruta seleccionada: {selected_route}")
    print(f"Predicción final: {final_prediction}")
    print(f"Reporte Markdown: {args.output_md}")
    print(f"Reporte HTML: {args.output_html}")
    print("Estado: OK, predicción adaptativa generada.")


if __name__ == "__main__":
    main()
