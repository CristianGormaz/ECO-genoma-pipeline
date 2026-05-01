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


def sequence_sensory_profile(sequence):
    informative = [base for base in sequence if base in "ACGT"]
    gc_count = sum(1 for base in informative if base in "GC")
    n_count = sequence.count("N")
    gc_percent = round((gc_count / len(informative)) * 100, 4) if informative else 0.0
    n_percent = round((n_count / len(sequence)) * 100, 4) if sequence else 0.0
    return {
        "length": len(sequence),
        "gc_percent": gc_percent,
        "n_percent": n_percent,
        "contains_ambiguous_n": n_count > 0,
        "ambiguous_n_count": n_count,
    }


def build_enteric_reflex(payload):
    baseline_confidence = payload["baseline_v3"]["confidence"]
    embedding_confidence = payload["embedding_semireal"]["confidence"]
    threshold = payload["threshold"]
    selected_route = payload["selected_route"]

    confidence_gap = round(abs(baseline_confidence - embedding_confidence), 4)
    sensory_profile = payload["sensory_profile"]

    if selected_route == "baseline_v3":
        reflex_name = "reflejo_explicable_rapido"
        biological_analogy = "plexo submucoso: absorción directa de una señal suficientemente clara"
        ux_summary = "E.C.O. eligió la ruta explicable porque la confianza del baseline superó el umbral operativo."
    else:
        reflex_name = "reflejo_vectorial_de_derivacion"
        biological_analogy = "plexo mientérico: redirección del flujo cuando la señal local no es suficiente"
        ux_summary = "E.C.O. derivó la secuencia hacia la ruta vectorial porque el baseline no alcanzó el umbral de confianza."

    if confidence_gap < 0.02:
        caution_level = "alta"
        caution_message = "Las rutas están muy cercanas; tratar como empate operativo y no como decisión fuerte."
    elif max(baseline_confidence, embedding_confidence) < threshold:
        caution_level = "media"
        caution_message = "La confianza general es baja; conviene revisar con más datos o evaluación externa."
    else:
        caution_level = "normal"
        caution_message = "La decisión es aceptable dentro del marco demostrativo del proyecto."

    return {
        "reflex_name": reflex_name,
        "selected_route": selected_route,
        "threshold": threshold,
        "confidence_gap": confidence_gap,
        "biological_analogy": biological_analogy,
        "ux_summary": ux_summary,
        "caution_level": caution_level,
        "caution_message": caution_message,
        "sensory_interpretation": {
            "length": sensory_profile["length"],
            "gc_percent": sensory_profile["gc_percent"],
            "n_percent": sensory_profile["n_percent"],
            "reading": "Perfil sensorial básico usado para contextualizar la decisión del router.",
        },
    }


def make_markdown(payload):
    reflex = payload["enteric_reflex"]
    sensory = payload["sensory_profile"]

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
    lines.append("## Sensado entérico")
    lines.append("")
    lines.append("| Señal | Valor |")
    lines.append("| --- | ---: |")
    lines.append(f"| Longitud | {sensory['length']} |")
    lines.append(f"| GC % | {sensory['gc_percent']} |")
    lines.append(f"| N ambiguas % | {sensory['n_percent']} |")
    lines.append(f"| Conteo N | {sensory['ambiguous_n_count']} |")
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
    lines.append("## Reflejo entérico del router")
    lines.append("")
    lines.append("| Elemento | Lectura |")
    lines.append("| --- | --- |")
    lines.append(f"| Reflejo activado | {reflex['reflex_name']} |")
    lines.append(f"| Analogía biológica | {reflex['biological_analogy']} |")
    lines.append(f"| Brecha de confianza | {reflex['confidence_gap']} |")
    lines.append(f"| Nivel de cautela | {reflex['caution_level']} |")
    lines.append(f"| Mensaje de cautela | {reflex['caution_message']} |")
    lines.append("")
    lines.append(reflex["ux_summary"])
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


def badge_class(caution_level):
    if caution_level == "alta":
        return "badge badge-high"
    if caution_level == "media":
        return "badge badge-medium"
    return "badge badge-normal"


def make_metric(label, value):
    return f"""
    <div class="metric">
      <span>{escape(str(label))}</span>
      <strong>{escape(str(value))}</strong>
    </div>
    """


def make_html(payload, md):
    sensory = payload["sensory_profile"]
    reflex = payload["enteric_reflex"]
    sequence = escape(payload["sequence"])
    caution_class = badge_class(reflex["caution_level"])

    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>E.C.O. Predicción adaptativa</title>
<style>
:root {{
  --bg: #0f172a;
  --panel: #111827;
  --card: #ffffff;
  --muted: #64748b;
  --line: #e5e7eb;
  --ink: #0f172a;
  --soft: #f8fafc;
}}
body {{
  margin: 0;
  font-family: Arial, sans-serif;
  background: var(--soft);
  color: var(--ink);
  line-height: 1.5;
}}
.hero {{
  background: linear-gradient(135deg, #0f172a, #1e293b);
  color: white;
  padding: 44px 32px;
}}
.hero h1 {{ margin: 0 0 8px; font-size: 32px; }}
.hero p {{ margin: 0; max-width: 920px; color: #cbd5e1; }}
.wrap {{ max-width: 1120px; margin: 0 auto; padding: 28px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 18px; }}
.card {{
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
}}
.card h2 {{ margin-top: 0; font-size: 19px; }}
.metric {{ display: flex; justify-content: space-between; gap: 18px; border-bottom: 1px solid var(--line); padding: 9px 0; }}
.metric:last-child {{ border-bottom: 0; }}
.metric span {{ color: var(--muted); }}
.metric strong {{ text-align: right; }}
.sequence {{
  word-break: break-all;
  background: #f1f5f9;
  border-radius: 10px;
  padding: 12px;
  font-family: monospace;
}}
.badge {{ display: inline-block; padding: 6px 10px; border-radius: 999px; font-weight: 700; }}
.badge-high {{ background: #fee2e2; color: #991b1b; }}
.badge-medium {{ background: #fef3c7; color: #92400e; }}
.badge-normal {{ background: #dcfce7; color: #166534; }}
.route {{ font-size: 28px; margin: 10px 0 0; }}
.callout {{ border-left: 5px solid #334155; background: #f8fafc; padding: 14px 16px; border-radius: 12px; }}
details {{ margin-top: 18px; }}
summary {{ cursor: pointer; font-weight: 700; }}
pre {{ background: #0b1020; color: #e5e7eb; padding: 16px; border-radius: 14px; overflow-x: auto; }}
.footer {{ color: var(--muted); font-size: 14px; margin-top: 18px; }}
</style>
</head>
<body>
<header class="hero">
  <h1>E.C.O. — Predicción adaptativa</h1>
  <p>Vista UX del router adaptativo: sensado de secuencia, comparación de rutas, decisión final y reflejo entérico responsable.</p>
</header>
<main class="wrap">
  <section class="grid">
    <article class="card" data-section="input-card">
      <h2>Entrada</h2>
      {make_metric('Sequence ID', payload['sequence_id'])}
      {make_metric('Longitud', payload['length'])}
      {make_metric('Umbral', payload['threshold'])}
      <p class="sequence">{sequence}</p>
    </article>

    <article class="card" data-section="sensory-card">
      <h2>Sensado entérico</h2>
      {make_metric('GC %', sensory['gc_percent'])}
      {make_metric('N ambiguas %', sensory['n_percent'])}
      {make_metric('Conteo N', sensory['ambiguous_n_count'])}
      {make_metric('Contiene N', sensory['contains_ambiguous_n'])}
    </article>

    <article class="card" data-section="route-card">
      <h2>Rutas internas</h2>
      {make_metric('baseline_v3', payload['baseline_v3']['prediction'])}
      {make_metric('Confianza baseline', payload['baseline_v3']['confidence'])}
      {make_metric('embedding_semireal', payload['embedding_semireal']['prediction'])}
      {make_metric('Confianza embedding', payload['embedding_semireal']['confidence'])}
    </article>

    <article class="card" data-section="decision-card">
      <h2>Decisión final</h2>
      <div class="route">{escape(payload['final_prediction'])}</div>
      {make_metric('Ruta seleccionada', payload['selected_route'])}
      {make_metric('Motivo', payload['reason'])}
    </article>
  </section>

  <section class="card" data-section="enteric-reflex-card" style="margin-top:18px;">
    <h2>Reflejo entérico del router</h2>
    <p><span class="{caution_class}">Cautela: {escape(reflex['caution_level'])}</span></p>
    {make_metric('Reflejo activado', reflex['reflex_name'])}
    {make_metric('Brecha de confianza', reflex['confidence_gap'])}
    {make_metric('Analogía biológica', reflex['biological_analogy'])}
    <div class="callout">
      <strong>Lectura UX:</strong> {escape(reflex['ux_summary'])}<br>
      <strong>Mensaje de cautela:</strong> {escape(reflex['caution_message'])}
    </div>
  </section>

  <section class="card" data-section="responsible-limit-card" style="margin-top:18px;">
    <h2>Límite responsable</h2>
    <p>Este resultado es demostrativo. No es diagnóstico clínico, no es benchmark científico y no reemplaza validación externa.</p>
    <p class="footer">Lectura E.C.O.: {escape(payload['eco_reading'])}</p>
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
        "sensory_profile": sequence_sensory_profile(sequence),
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
    payload["enteric_reflex"] = build_enteric_reflex(payload)

    Path("results").mkdir(exist_ok=True)

    md = make_markdown(payload)

    Path(args.output_json).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    Path(args.output_md).write_text(md, encoding="utf-8")
    Path(args.output_html).write_text(make_html(payload, md), encoding="utf-8")

    print("E.C.O. ADAPTIVE ROUTER PREDICTION")
    print("=================================")
    print(f"Sequence ID: {args.sequence_id}")
    print(f"Longitud: {len(sequence)}")
    print(f"baseline_v3: {pred_v3} | confianza={round(confidence_v3, 4)}")
    print(f"embedding_semireal: {pred_semireal} | confianza={round(confidence_semireal, 4)}")
    print(f"Ruta seleccionada: {selected_route}")
    print(f"Predicción final: {final_prediction}")
    print(f"Reflejo entérico: {payload['enteric_reflex']['reflex_name']}")
    print(f"Cautela: {payload['enteric_reflex']['caution_level']}")
    print(f"Reporte Markdown: {args.output_md}")
    print(f"Reporte HTML: {args.output_html}")
    print("Estado: OK, predicción adaptativa generada.")


if __name__ == "__main__":
    main()
