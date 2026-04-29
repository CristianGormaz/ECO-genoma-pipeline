#!/usr/bin/env python3
"""
Reporte público E.C.O. con hg38/chrM
===================================

Descarga una referencia pública pequeña desde UCSC, genera regiones BED a partir
 de motivos detectados y ejecuta el pipeline E.C.O. para producir un informe
interpretativo estilo laboratorio.

Uso recomendado desde la raíz del repositorio:

    python3 scripts/run_eco_public_chrM_report.py

Nota: este script usa una referencia pública, no datos privados de una persona.
El informe es bioinformático/educativo y no constituye diagnóstico médico.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import json
from pathlib import Path
import shutil
import sys
from typing import Any, Dict, Iterable, List, Tuple
import urllib.request

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from run_eco_demo_pipeline import run_demo_pipeline  # noqa: E402
from src.eco_motif_analysis import MotifHit, parse_fasta, scan_sequence  # noqa: E402

DEFAULT_SOURCE_URL = "https://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/chrM.fa.gz"
DEFAULT_DATA_DIR = PROJECT_ROOT / "data" / "public" / "ucsc_hg38_chrM"
DEFAULT_RESULTS_DIR = PROJECT_ROOT / "results"
DEFAULT_PREFIX = "eco_public_chrM"

MOTIF_PRIORITY = [
    "TATA_box_canonica",
    "TATA_box_degenerada",
    "CAAT_box",
    "GC_box",
    "polyA_signal",
    "homopolimero_A_6_mas",
    "homopolimero_T_6_mas",
    "homopolimero_C_6_mas",
    "homopolimero_G_6_mas",
]


def download_file(url: str, destination: Path, force: bool = False) -> str:
    """Descarga un archivo externo con cache local simple."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not force:
        return "cache"

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ECO-genoma-pipeline/0.1 (+https://github.com/CristianGormaz/ECO-genoma-pipeline)"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310 - URL controlada por CLI/usuario
        with destination.open("wb") as handle:
            shutil.copyfileobj(response, handle)
    return "downloaded"


def decompress_gzip(source_gz: Path, destination_fasta: Path, force: bool = False) -> str:
    """Descomprime un FASTA .gz a FASTA plano."""
    destination_fasta.parent.mkdir(parents=True, exist_ok=True)
    if destination_fasta.exists() and not force:
        return "cache"

    with gzip.open(source_gz, "rb") as compressed:
        with destination_fasta.open("wb") as output:
            shutil.copyfileobj(compressed, output)
    return "decompressed"


def load_single_sequence(fasta_path: Path) -> Tuple[str, str]:
    """Carga una referencia FASTA de un solo registro o toma el primero."""
    records = parse_fasta(fasta_path)
    sequence_id = next(iter(records))
    return sequence_id, records[sequence_id]


def group_hits_by_motif(hits: Iterable[MotifHit]) -> Dict[str, List[MotifHit]]:
    """Agrupa coincidencias por nombre de motivo."""
    grouped: Dict[str, List[MotifHit]] = defaultdict(list)
    for hit in hits:
        grouped[hit.motif_name].append(hit)
    return grouped


def select_interpretable_regions(
    chrom: str,
    sequence: str,
    max_regions: int = 12,
    flank: int = 12,
) -> List[Tuple[str, int, int, str, str]]:
    """Selecciona regiones BED pequeñas alrededor de motivos detectados.

    Devuelve tuplas: chrom, start0, end0, name, strand.
    Las coordenadas BED son 0-based y semiabiertas.
    """
    whole_report = scan_sequence(sequence, sequence_id=chrom)
    grouped_hits = group_hits_by_motif(whole_report.hits)
    selected: List[Tuple[str, int, int, str, str]] = []
    seen_intervals = set()

    for motif_name in MOTIF_PRIORITY:
        for hit in grouped_hits.get(motif_name, [])[:3]:
            start0 = max(0, hit.start - 1 - flank)
            end0 = min(len(sequence), hit.end + flank)
            interval_key = (start0, end0, motif_name)
            if end0 <= start0 or interval_key in seen_intervals:
                continue
            seen_intervals.add(interval_key)
            region_name = f"{motif_name}_{hit.start}_{hit.end}"
            selected.append((chrom, start0, end0, region_name, "+"))
            if len(selected) >= max_regions:
                return selected

    if selected:
        return selected

    # Fallback defensivo: si no aparecen motivos, analiza ventanas fijas.
    window = min(120, len(sequence))
    step = max(1, window)
    for index, start0 in enumerate(range(0, len(sequence), step), start=1):
        end0 = min(len(sequence), start0 + window)
        selected.append((chrom, start0, end0, f"ventana_control_{index}", "+"))
        if len(selected) >= max_regions:
            break
    return selected


def write_bed(regions: Iterable[Tuple[str, int, int, str, str]], bed_path: Path) -> None:
    """Escribe regiones seleccionadas en formato BED6."""
    bed_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{chrom}\t{start}\t{end}\t{name}\t0\t{strand}" for chrom, start, end, name, strand in regions]
    bed_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def motif_counter(report: Dict[str, Any]) -> Counter:
    """Cuenta motivos detectados en el reporte integrado."""
    counts: Counter = Counter()
    for entry in report.get("sequences", []):
        motif_report = entry.get("motif_report") or {}
        for hit in motif_report.get("hits", []):
            counts[hit.get("motif_name", "motivo_desconocido")] += 1
    return counts


def table(headers: List[str], rows: Iterable[List[Any]]) -> List[str]:
    """Construye una tabla Markdown simple."""
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        safe_row = [str(value).replace("|", "\\|").replace("\n", " ") for value in row]
        lines.append("| " + " | ".join(safe_row) + " |")
    return lines


def entry_motif_names(entry: Dict[str, Any]) -> str:
    """Devuelve nombres de motivos por región."""
    motif_report = entry.get("motif_report") or {}
    hits = motif_report.get("hits") or []
    if not hits:
        return "sin motivos"
    return ", ".join(hit.get("motif_name", "motivo_desconocido") for hit in hits)


def build_interpretive_markdown(report: Dict[str, Any], source_url: str, fasta_path: Path, bed_path: Path) -> str:
    """Construye un informe interpretativo estilo laboratorio, no diagnóstico."""
    summary = report["summary"]
    feedback = summary["feedback"]
    counts = motif_counter(report)
    status_ok = feedback["rejected_packets"] == 0 and feedback["absorbed_packets"] == summary["regions_processed"]
    status = "OK: digestión informacional completa" if status_ok else "REVISAR: hubo rechazos o absorción incompleta"

    sequence_rows = []
    for entry in report.get("sequences", []):
        features = entry.get("metadata", {}).get("absorbed_features", {})
        sequence_rows.append(
            [
                entry.get("sequence_id", "n/a"),
                f"{features.get('length', 'n/a')} bp",
                f"{features.get('gc_percent', 'n/a')}%",
                f"{features.get('n_percent', 'n/a')}%",
                entry_motif_names(entry),
            ]
        )

    motif_rows = [[name, count] for name, count in counts.most_common()]
    if not motif_rows:
        motif_rows = [["sin motivos detectados", 0]]

    lines: List[str] = [
        "# Informe interpretativo E.C.O. – análisis público hg38/chrM",
        "",
        "## 1. Identificación de la muestra",
        "",
        *table(
            ["Campo", "Valor"],
            [
                ["Tipo de dato", "Referencia genómica pública"],
                ["Fuente", source_url],
                ["Archivo FASTA local", fasta_path],
                ["BED generado", bed_path],
                ["Alcance", "Validación bioinformática del pipeline E.C.O.; no es muestra clínica personal"],
            ],
        ),
        "",
        "## 2. Resultado ejecutivo",
        "",
        *table(
            ["Métrica", "Resultado"],
            [
                ["Estado general", status],
                ["Regiones procesadas", summary["regions_processed"]],
                ["Motivos encontrados", summary["total_motif_hits"]],
                ["Paquetes aceptados", feedback["accepted_packets"]],
                ["Paquetes rechazados", feedback["rejected_packets"]],
                ["Paquetes absorbidos", feedback["absorbed_packets"]],
                ["Tasa de rechazo", f"{feedback['rejection_rate']}%"],
                ["Tasa de absorción", f"{feedback['absorbed_rate']}%"],
            ],
        ),
        "",
        "## 3. Lectura tipo laboratorio",
        "",
        "El sistema logró ingerir, filtrar y absorber las regiones seleccionadas desde una referencia pública. "
        "Cuando no aparecen rechazos, la lectura técnica es que las secuencias extraídas son compatibles con el alfabeto ADN esperado por E.C.O. y pudieron avanzar por el metabolismo informacional completo.",
        "",
        "La presencia de motivos como TATA, CAAT, GC o señal de poliadenilación debe interpretarse como una coincidencia de patrones cortos dentro de la secuencia. "
        "Estos patrones son biológicamente relevantes como elementos regulatorios conocidos, pero su presencia aislada no demuestra actividad funcional, expresión génica ni efecto clínico.",
        "",
        "## 4. Hallazgos por región",
        "",
        *table(["Región", "Longitud", "GC", "N ambiguas", "Motivos detectados"], sequence_rows),
        "",
        "## 5. Resumen de motivos detectados",
        "",
        *table(["Motivo", "Cantidad"], motif_rows),
        "",
        "## 6. Interpretación empírica y límites",
        "",
        "- **Calidad de entrada:** la tasa de rechazo indica cuántas regiones fallaron por caracteres no válidos o problemas de calidad.",
        "- **GC%:** resume composición básica de la secuencia; valores extremos pueden orientar preguntas, pero no son conclusión clínica por sí mismos.",
        "- **Motivos regulatorios:** TATA, CAAT y GC box son elementos conocidos en promotores eucariontes; una coincidencia local es una señal exploratoria, no una prueba funcional definitiva.",
        "- **Referencia pública:** este análisis usa una secuencia de referencia, no el genoma de un paciente ni una muestra privada.",
        "- **No diagnóstico:** E.C.O. todavía no interpreta variantes, enfermedades, riesgo genético, patogenicidad, expresión, conservación, metilación ni evidencia clínica curada.",
        "",
        "## 7. Próxima mejora sugerida",
        "",
        "El siguiente salto empírico es usar regiones regulatorias reales anotadas, por ejemplo datos reducidos de ENCODE/EnhancerAtlas, y comparar el resultado contra evidencia externa. "
        "Ahí E.C.O. dejaría de buscar solo patrones simples y empezaría a contrastar contexto biológico.",
        "",
    ]
    return "\n".join(lines)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Descarga hg38/chrM desde UCSC y genera un informe interpretativo E.C.O."
    )
    parser.add_argument("--source-url", default=DEFAULT_SOURCE_URL, help="URL del FASTA .gz público a descargar.")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR, help="Carpeta local para datos descargados.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_RESULTS_DIR, help="Carpeta para resultados.")
    parser.add_argument("--prefix", default=DEFAULT_PREFIX, help="Prefijo para archivos generados.")
    parser.add_argument("--max-regions", type=int, default=12, help="Número máximo de regiones BED generadas.")
    parser.add_argument("--flank", type=int, default=12, help="Bases alrededor del motivo al crear regiones BED.")
    parser.add_argument("--force-download", action="store_true", help="Descarga y descomprime aunque existan archivos locales.")
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    gz_path = args.data_dir / "chrM.fa.gz"
    fasta_path = args.data_dir / "chrM.fa"
    bed_path = args.data_dir / f"{args.prefix}_regions.bed"
    output_fasta = args.output_dir / f"{args.prefix}.fa"
    output_json = args.output_dir / f"{args.prefix}_report.json"
    output_markdown = args.output_dir / f"{args.prefix}_interpretive_report.md"

    try:
        download_state = download_file(args.source_url, gz_path, force=args.force_download)
        decompress_state = decompress_gzip(gz_path, fasta_path, force=args.force_download)
        chrom, sequence = load_single_sequence(fasta_path)
        regions = select_interpretable_regions(chrom, sequence, max_regions=args.max_regions, flank=args.flank)
        write_bed(regions, bed_path)

        report = run_demo_pipeline(
            bed_path=bed_path,
            reference_path=fasta_path,
            output_fasta=output_fasta,
            output_json=output_json,
        )
        report["source"] = {
            "url": args.source_url,
            "download_state": download_state,
            "decompress_state": decompress_state,
            "generated_bed": str(bed_path),
        }
        output_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

        markdown = build_interpretive_markdown(report, args.source_url, fasta_path, bed_path)
        output_markdown.parent.mkdir(parents=True, exist_ok=True)
        output_markdown.write_text(markdown, encoding="utf-8")

        feedback = report["summary"]["feedback"]
        print("E.C.O. PUBLIC CHRM INTERPRETIVE REPORT")
        print("======================================")
        print(f"Fuente: {args.source_url}")
        print(f"Descarga: {download_state}")
        print(f"Descompresión: {decompress_state}")
        print(f"Cromosoma/registro: {chrom}")
        print(f"Longitud referencia: {len(sequence)} bp")
        print(f"Regiones BED generadas: {len(regions)}")
        print(f"Motivos encontrados: {report['summary']['total_motif_hits']}")
        print(f"Aceptados: {feedback['accepted_packets']}")
        print(f"Rechazados: {feedback['rejected_packets']}")
        print(f"Absorbidos: {feedback['absorbed_packets']}")
        print(f"Reporte JSON: {output_json}")
        print(f"Informe interpretativo Markdown: {output_markdown}")
        if feedback["rejected_packets"] == 0:
            print("Estado: OK, archivo público descargado y digerido por E.C.O.")
            return 0
        print("Estado: REVISAR, hubo rechazos durante la digestión informacional.")
        return 1
    except (OSError, ValueError, KeyError, urllib.error.URLError) as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
