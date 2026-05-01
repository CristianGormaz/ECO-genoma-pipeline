from pathlib import Path
import argparse
import csv
import importlib.util
import json
from collections import Counter
from html import escape


def load_module(path, name):
    module_path = Path(path)
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_predict_module():
    return load_module("scripts/run_eco_adaptive_router_predict.py", "eco_adaptive_router_predict")


def safe_clean_sequence(seq):
    raw = str(seq or "")
    cleaned = raw.strip().upper().replace(" ", "").replace("\n", "")
    invalid = sorted(set(cleaned) - set("ACGTN"))
    if invalid:
        return None, f"secuencia contiene caracteres no válidos: {', '.join(invalid)}"
    if not cleaned:
        return None, "secuencia vacía"
    return cleaned, None


def read_batch(path):
    batch_path = Path(path)
    if not batch_path.exists():
        raise SystemExit(f"ERROR: no existe el TSV de entrada: {batch_path}")

    with batch_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if not reader.fieldnames or "sequence" not in reader.fieldnames:
            raise SystemExit("ERROR: el TSV debe incluir una columna 'sequence'.")
        rows = []
        for index, row in enumerate(reader, start=1):
            rows.append({
                "row_number": index,
                "sequence_id": row.get("sequence_id") or f"batch_sequence_{index}",
                "sequence": row.get("sequence", ""),
                "description": row.get("description", ""),
            })
    return rows


def predict_one(row, *, eco, router, predict, model_v3, model_semireal, semireal_features, threshold):
    sequence, error = safe_clean_sequence(row["sequence"])
    if error:
        return {
            "row_number": row["row_number"],
            "sequence_id": row["sequence_id"],
            "description": row.get("description", ""),
            "status": "rejected",
            "reason": error,
            "selected_route": "none",
            "final_prediction": "not_available",
            "enteric_reflex": {
                "reflex_name": "reflejo_inmune_de_rechazo",
                "caution_level": "alta",
                "caution_message": "El dato no cumple la barrera mínima de entrada.",
            },
        }

    inference_row = {
        "sequence_id": row["sequence_id"],
        "sequence": sequence,
        "label": "unknown",
        "split": "batch_inference",
        "difficulty": "unknown",
    }

    pred_v3, confidence_v3 = router.predict_with_confidence(inference_row, model_v3, eco.features_baseline_v3)
    pred_semireal, confidence_semireal = router.predict_with_confidence(inference_row, model_semireal, semireal_features)

    if confidence_v3 >= threshold:
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
        "row_number": row["row_number"],
        "sequence_id": row["sequence_id"],
        "description": row.get("description", ""),
        "status": "processed",
        "sequence": sequence,
        "length": len(sequence),
        "threshold": threshold,
        "sensory_profile": predict.sequence_sensory_profile(sequence),
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
    }
    payload["enteric_reflex"] = predict.build_enteric_reflex(payload)
    return payload


def safe_rate(count, total):
    if total == 0:
        return 0.0
    return round(count / total, 4)


def build_batch_homeostasis(total, rejected, contradiction_count, high_caution_count):
    """Construye una lectura UX de estabilidad del lote completo.

    La homeostasis no reemplaza las métricas; las traduce a una señal rápida
    de estado para revisión humana: estable, atención o crítico.
    """
    if total == 0:
        return {
            "state": "idle",
            "risk_score": 0.0,
            "rejection_rate": 0.0,
            "contradiction_rate": 0.0,
            "high_caution_rate": 0.0,
            "triggers": ["No hay secuencias para evaluar."],
            "reading": "Sin flujo informacional para evaluar.",
            "recommendation": "Agregar secuencias al TSV de entrada.",
        }

    rejection_rate = safe_rate(rejected, total)
    contradiction_rate = safe_rate(contradiction_count, total)
    high_caution_rate = safe_rate(high_caution_count, total)
    risk_score = round(
        min(
            1.0,
            rejection_rate * 0.35
            + contradiction_rate * 0.35
            + high_caution_rate * 0.30,
        ),
        4,
    )

    triggers = []
    if rejected:
        triggers.append("barrera_inmune_activa")
    if contradiction_count:
        triggers.append("contradiccion_entre_rutas")
    if high_caution_count:
        triggers.append("cautela_alta")

    if rejection_rate > 0.5 or contradiction_rate > 0.5 or risk_score >= 0.7:
        state = "critico"
        reading = "El lote muestra inestabilidad alta: hay demasiado rechazo, contradicción o cautela acumulada."
        recommendation = "Revisar calidad del TSV, separar casos inválidos y validar manualmente las secuencias conflictivas."
    elif triggers:
        state = "atencion"
        reading = "El lote es procesable, pero requiere revisión: hay señales de rechazo, contradicción o baja separación entre rutas."
        recommendation = "Revisar primero los casos rechazados, luego los casos con contradicción interna y cautela alta."
    else:
        state = "estable"
        reading = "El lote mantiene homeostasis operativa: no hay rechazos, contradicciones ni cautela alta relevante."
        recommendation = "Usar el reporte como salida demostrativa y continuar con validación externa si corresponde."

    return {
        "state": state,
        "risk_score": risk_score,
        "rejection_rate": rejection_rate,
        "contradiction_rate": contradiction_rate,
        "high_caution_rate": high_caution_rate,
        "triggers": triggers or ["sin_alertas"],
        "reading": reading,
        "recommendation": recommendation,
    }


def has_internal_contradiction(item):
    return (
        item.get("status") == "processed"
        and item.get("baseline_v3", {}).get("prediction") != item.get("embedding_semireal", {}).get("prediction")
    )


def caution_level(item):
    return item.get("enteric_reflex", {}).get("caution_level", "unknown")


def build_priority_cases(results):
    """Ordena casos para revisión humana: rechazo, contradicción, cautela alta."""
    priority_cases = []
    for item in results:
        if item.get("status") == "rejected":
            priority_cases.append({
                "priority": 1,
                "category": "rechazo_inmune",
                "sequence_id": item["sequence_id"],
                "row_number": item["row_number"],
                "status": item.get("status"),
                "selected_route": item.get("selected_route", "none"),
                "final_prediction": item.get("final_prediction", "not_available"),
                "caution_level": caution_level(item),
                "reason": item.get("reason", "dato rechazado"),
                "review_action": "Corregir secuencia, revisar caracteres inválidos o excluir del lote.",
            })
        elif has_internal_contradiction(item):
            priority_cases.append({
                "priority": 2,
                "category": "contradiccion_interna",
                "sequence_id": item["sequence_id"],
                "row_number": item["row_number"],
                "status": item.get("status"),
                "selected_route": item.get("selected_route", "none"),
                "final_prediction": item.get("final_prediction", "not_available"),
                "caution_level": caution_level(item),
                "reason": "baseline_v3 y embedding_semireal entregan predicciones distintas.",
                "review_action": "Revisar manualmente señales, confianza y posible empate operativo entre rutas.",
            })
        elif caution_level(item) == "alta":
            priority_cases.append({
                "priority": 3,
                "category": "cautela_alta",
                "sequence_id": item["sequence_id"],
                "row_number": item["row_number"],
                "status": item.get("status"),
                "selected_route": item.get("selected_route", "none"),
                "final_prediction": item.get("final_prediction", "not_available"),
                "caution_level": caution_level(item),
                "reason": "La decisión requiere cautela alta por baja separación de señales.",
                "review_action": "Validar con más datos, más evaluación o una ruta externa antes de usar como conclusión.",
            })

    return sorted(priority_cases, key=lambda case: (case["priority"], case["row_number"]))


def summarize(results):
    total = len(results)
    processed = sum(1 for item in results if item["status"] == "processed")
    rejected = total - processed
    route_counts = Counter(item.get("selected_route", "none") for item in results)
    prediction_counts = Counter(item.get("final_prediction", "not_available") for item in results)
    caution_counts = Counter(item.get("enteric_reflex", {}).get("caution_level", "unknown") for item in results)
    contradiction_count = sum(1 for item in results if has_internal_contradiction(item))
    high_caution_count = caution_counts.get("alta", 0)
    homeostasis = build_batch_homeostasis(total, rejected, contradiction_count, high_caution_count)

    notes = []
    if rejected:
        notes.append("Hay secuencias rechazadas por la barrera inmune informacional.")
    if contradiction_count:
        notes.append("Hay rutas internas con predicciones contradictorias; revisar esos casos con cautela.")
    if high_caution_count:
        notes.append("Hay decisiones con cautela alta; tratarlas como empate operativo o baja separación de señales.")
    if not notes:
        notes.append("Lote procesado sin alertas críticas.")
    notes.append(f"Homeostasis del lote: {homeostasis['state']}.")

    return {
        "total_sequences": total,
        "processed_sequences": processed,
        "rejected_sequences": rejected,
        "route_counts": dict(route_counts),
        "prediction_counts": dict(prediction_counts),
        "caution_counts": dict(caution_counts),
        "contradiction_count": contradiction_count,
        "high_caution_count": high_caution_count,
        "priority_case_count": len(build_priority_cases(results)),
        "homeostasis": homeostasis,
        "notes": notes,
    }


def make_markdown(payload):
    summary = payload["summary"]
    homeostasis = summary["homeostasis"]
    priority_cases = payload.get("priority_cases", [])
    lines = []
    lines.append("# E.C.O. - Inferencia por lote con router adaptativo")
    lines.append("")
    lines.append("## Propósito")
    lines.append("")
    lines.append("Este reporte procesa varias secuencias con el router adaptativo E.C.O. y resume rutas, predicciones, cautela y rechazos.")
    lines.append("")
    lines.append("## Resumen del lote")
    lines.append("")
    lines.append("| Métrica | Valor |")
    lines.append("| --- | ---: |")
    lines.append(f"| Secuencias totales | {summary['total_sequences']} |")
    lines.append(f"| Procesadas | {summary['processed_sequences']} |")
    lines.append(f"| Rechazadas | {summary['rejected_sequences']} |")
    lines.append(f"| Contradicciones internas | {summary['contradiction_count']} |")
    lines.append(f"| Cautela alta | {summary['high_caution_count']} |")
    lines.append(f"| Casos prioritarios | {summary['priority_case_count']} |")
    lines.append("")
    lines.append("## Homeostasis del lote")
    lines.append("")
    lines.append("| Señal | Valor |")
    lines.append("| --- | --- |")
    lines.append(f"| Estado | {homeostasis['state']} |")
    lines.append(f"| Riesgo operativo | {homeostasis['risk_score']} |")
    lines.append(f"| Tasa de rechazo | {homeostasis['rejection_rate']} |")
    lines.append(f"| Tasa de contradicción | {homeostasis['contradiction_rate']} |")
    lines.append(f"| Tasa de cautela alta | {homeostasis['high_caution_rate']} |")
    lines.append(f"| Activadores | {', '.join(homeostasis['triggers'])} |")
    lines.append("")
    lines.append(f"> {homeostasis['reading']}")
    lines.append("")
    lines.append(f"**Recomendación:** {homeostasis['recommendation']}")
    lines.append("")
    lines.append("## Casos prioritarios")
    lines.append("")
    if priority_cases:
        lines.append("E.C.O. ordena automáticamente la revisión: primero rechazos, luego contradicciones internas y finalmente cautela alta.")
        lines.append("")
        lines.append("| Prioridad | ID | Categoría | Ruta | Predicción | Cautela | Acción sugerida |")
        lines.append("| ---: | --- | --- | --- | --- | --- | --- |")
        for case in priority_cases:
            lines.append(
                f"| {case['priority']} | {case['sequence_id']} | {case['category']} | "
                f"{case['selected_route']} | {case['final_prediction']} | {case['caution_level']} | {case['review_action']} |"
            )
    else:
        lines.append("No hay casos prioritarios. El lote no activó rechazos, contradicciones ni cautela alta.")
    lines.append("")
    lines.append("## Conteo de rutas")
    lines.append("")
    lines.append("| Ruta | Conteo |")
    lines.append("| --- | ---: |")
    for route, count in summary["route_counts"].items():
        lines.append(f"| {route} | {count} |")
    lines.append("")
    lines.append("## Detalle")
    lines.append("")
    lines.append("| ID | Estado | Ruta | Predicción | Cautela | Motivo |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for item in payload["results"]:
        caution = caution_level(item)
        lines.append(
            f"| {item['sequence_id']} | {item['status']} | {item.get('selected_route', 'none')} | "
            f"{item.get('final_prediction', 'not_available')} | {caution} | {item.get('reason', '')} |"
        )
    lines.append("")
    lines.append("## Notas E.C.O.")
    lines.append("")
    for note in summary["notes"]:
        lines.append(f"- {note}")
    lines.append("")
    lines.append("## Límite responsable")
    lines.append("")
    lines.append("Este resultado es demostrativo. No es diagnóstico clínico, no es benchmark científico y no reemplaza validación externa.")
    lines.append("")
    return "\n".join(lines)


def metric(label, value):
    return f"<div class='metric'><span>{escape(str(label))}</span><strong>{escape(str(value))}</strong></div>"


def make_html(payload, md):
    summary = payload["summary"]
    homeostasis = summary["homeostasis"]
    priority_cases = payload.get("priority_cases", [])
    rows = []
    for item in payload["results"]:
        caution = caution_level(item)
        rows.append(
            "<tr>"
            f"<td>{escape(str(item['sequence_id']))}</td>"
            f"<td>{escape(str(item['status']))}</td>"
            f"<td>{escape(str(item.get('selected_route', 'none')))}</td>"
            f"<td>{escape(str(item.get('final_prediction', 'not_available')))}</td>"
            f"<td>{escape(str(caution))}</td>"
            f"<td>{escape(str(item.get('reason', '')))}</td>"
            "</tr>"
        )

    priority_rows = []
    for case in priority_cases:
        priority_rows.append(
            "<tr>"
            f"<td>{escape(str(case['priority']))}</td>"
            f"<td>{escape(str(case['sequence_id']))}</td>"
            f"<td>{escape(str(case['category']))}</td>"
            f"<td>{escape(str(case['selected_route']))}</td>"
            f"<td>{escape(str(case['final_prediction']))}</td>"
            f"<td>{escape(str(case['caution_level']))}</td>"
            f"<td>{escape(str(case['review_action']))}</td>"
            "</tr>"
        )
    if not priority_rows:
        priority_rows.append("<tr><td colspan='7'>No hay casos prioritarios.</td></tr>")

    notes = "".join(f"<li>{escape(note)}</li>" for note in summary["notes"])
    triggers = ", ".join(homeostasis["triggers"])

    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>E.C.O. Batch router adaptativo</title>
<style>
body {{ margin: 0; font-family: Arial, sans-serif; background: #f8fafc; color: #0f172a; line-height: 1.5; }}
.hero {{ background: linear-gradient(135deg, #0f172a, #334155); color: white; padding: 40px 28px; }}
.hero h1 {{ margin: 0 0 8px; }}
.wrap {{ max-width: 1120px; margin: 0 auto; padding: 28px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }}
.card {{ background: white; border: 1px solid #e5e7eb; border-radius: 16px; padding: 18px; box-shadow: 0 8px 24px rgba(15,23,42,.06); }}
.metric {{ display: flex; justify-content: space-between; gap: 12px; border-bottom: 1px solid #e5e7eb; padding: 8px 0; }}
.metric:last-child {{ border-bottom: 0; }}
.metric span {{ color: #64748b; }}
.homeostasis {{ border-left: 6px solid #334155; }}
.homeostasis strong {{ font-size: 1.4rem; }}
.priority {{ border-left: 6px solid #7f1d1d; }}
table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 16px; overflow: hidden; }}
th, td {{ border-bottom: 1px solid #e5e7eb; padding: 10px; text-align: left; vertical-align: top; }}
th {{ background: #f1f5f9; }}
pre {{ background: #0b1020; color: #e5e7eb; padding: 16px; border-radius: 14px; overflow-x: auto; }}
details {{ margin-top: 18px; }}
</style>
</head>
<body>
<header class="hero">
  <h1>E.C.O. — Inferencia por lote</h1>
  <p>Router adaptativo aplicado a múltiples secuencias: rutas seleccionadas, predicciones, cautela y rechazos.</p>
</header>
<main class="wrap">
  <section class="grid">
    <article class="card">{metric('Total', summary['total_sequences'])}{metric('Procesadas', summary['processed_sequences'])}{metric('Rechazadas', summary['rejected_sequences'])}</article>
    <article class="card">{metric('Contradicciones internas', summary['contradiction_count'])}{metric('Cautela alta', summary['high_caution_count'])}{metric('Casos prioritarios', summary['priority_case_count'])}</article>
    <article class="card homeostasis"><h2>Homeostasis del lote</h2>{metric('Estado', homeostasis['state'])}{metric('Riesgo operativo', homeostasis['risk_score'])}{metric('Activadores', triggers)}<p>{escape(homeostasis['reading'])}</p><p><strong>Recomendación:</strong> {escape(homeostasis['recommendation'])}</p></article>
    <article class="card"><h2>Notas E.C.O.</h2><ul>{notes}</ul></article>
  </section>
  <section class="card priority" style="margin-top:18px;">
    <h2>Casos prioritarios</h2>
    <p>Orden automático de revisión: rechazos, contradicciones internas y cautela alta.</p>
    <table>
      <thead><tr><th>Prioridad</th><th>ID</th><th>Categoría</th><th>Ruta</th><th>Predicción</th><th>Cautela</th><th>Acción sugerida</th></tr></thead>
      <tbody>{''.join(priority_rows)}</tbody>
    </table>
  </section>
  <section class="card" style="margin-top:18px;">
    <h2>Detalle del lote</h2>
    <table>
      <thead><tr><th>ID</th><th>Estado</th><th>Ruta</th><th>Predicción</th><th>Cautela</th><th>Motivo</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
  </section>
  <details>
    <summary>Ver Markdown técnico completo</summary>
    <pre>{escape(md)}</pre>
  </details>
</main>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Inferencia por lote con router adaptativo E.C.O.")
    parser.add_argument("--batch-input", required=True)
    parser.add_argument("--training-input", default="examples/eco_labeled_sequences.tsv")
    parser.add_argument("--threshold", type=float, default=0.20)
    parser.add_argument("--embedding-k", type=int, default=4)
    parser.add_argument("--dimensions", type=int, default=128)
    parser.add_argument("--output-json", default="results/eco_adaptive_router_batch_report.json")
    parser.add_argument("--output-md", default="results/eco_adaptive_router_batch_report.md")
    parser.add_argument("--output-html", default="results/eco_adaptive_router_batch_report.html")
    args = parser.parse_args()

    eco = load_module("scripts/run_eco_difficulty_eval.py", "eco_difficulty_eval")
    router = load_module("scripts/run_eco_confidence_router_calibrated_eval.py", "eco_confidence_router_calibrated_eval")
    predict = load_predict_module()

    rows = eco.read_dataset(args.training_input)
    semireal_features = lambda seq: eco.features_semireal(seq, args.embedding_k, args.dimensions)
    model_v3 = eco.centroid_train(rows, eco.features_baseline_v3)
    model_semireal = eco.centroid_train(rows, semireal_features)

    batch_rows = read_batch(args.batch_input)
    results = [
        predict_one(
            row,
            eco=eco,
            router=router,
            predict=predict,
            model_v3=model_v3,
            model_semireal=model_semireal,
            semireal_features=semireal_features,
            threshold=args.threshold,
        )
        for row in batch_rows
    ]
    priority_cases = build_priority_cases(results)

    payload = {
        "batch_input": args.batch_input,
        "training_input": args.training_input,
        "threshold": args.threshold,
        "embedding_k": args.embedding_k,
        "dimensions": args.dimensions,
        "summary": summarize(results),
        "priority_cases": priority_cases,
        "results": results,
        "limits": ["dataset demostrativo", "no diagnostico clinico", "no benchmark cientifico"],
    }

    Path("results").mkdir(exist_ok=True)
    md = make_markdown(payload)
    Path(args.output_json).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    Path(args.output_md).write_text(md, encoding="utf-8")
    Path(args.output_html).write_text(make_html(payload, md), encoding="utf-8")

    summary = payload["summary"]
    homeostasis = summary["homeostasis"]
    print("E.C.O. ADAPTIVE ROUTER BATCH")
    print("============================")
    print(f"Entrada batch: {args.batch_input}")
    print(f"Secuencias totales: {summary['total_sequences']}")
    print(f"Procesadas: {summary['processed_sequences']}")
    print(f"Rechazadas: {summary['rejected_sequences']}")
    print(f"Contradicciones internas: {summary['contradiction_count']}")
    print(f"Cautela alta: {summary['high_caution_count']}")
    print(f"Casos prioritarios: {summary['priority_case_count']}")
    print(f"Homeostasis: {homeostasis['state']}")
    print(f"Riesgo operativo: {homeostasis['risk_score']}")
    print(f"Recomendación: {homeostasis['recommendation']}")
    print(f"Reporte Markdown: {args.output_md}")
    print(f"Reporte HTML: {args.output_html}")
    print("Estado: OK, inferencia por lote generada.")


if __name__ == "__main__":
    main()
