#!/usr/bin/env python3
"""Descarga una muestra real de ClinVar y genera reporte E.C.O.

Este script usa el archivo público variant_summary.txt.gz de ClinVar, extrae
un subconjunto pequeño por genes de interés y lo transforma al formato de
interpretación segura de variantes de E.C.O.

No es diagnóstico médico. Es un reporte bioinformático interpretativo basado en
metadatos públicos de ClinVar.
"""

from __future__ import annotations

import argparse
import csv
import gzip
from pathlib import Path
import shutil
import sys
from typing import Dict, Iterable, List
import urllib.request

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from src.eco_variant_interpretation import VariantRecord, build_report, write_json_report  # noqa: E402
from scripts.run_eco_variant_demo import build_markdown  # noqa: E402

DEFAULT_SOURCE_URL = "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz"
DEFAULT_DATA_DIR = PROJECT_ROOT / "data" / "public" / "clinvar"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "results"
DEFAULT_GENES = ["BRCA1", "BRCA2", "CFTR", "TP53"]
DEFAULT_PREFIX = "eco_clinvar_sample"


def download_file(url: str, destination: Path, force: bool = False) -> str:
    """Descarga archivo con cache local simple."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not force:
        return "cache"

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ECO-genoma-pipeline/0.1 (+https://github.com/CristianGormaz/ECO-genoma-pipeline)"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:  # noqa: S310 - URL pública configurable por CLI
        with destination.open("wb") as handle:
            shutil.copyfileobj(response, handle)
    return "downloaded"


def normalize_gene_list(genes: Iterable[str]) -> set[str]:
    return {gene.strip().upper() for gene in genes if gene.strip()}


def first_non_empty(*values: str) -> str:
    for value in values:
        value = (value or "").strip()
        if value and value not in {"-", "na", "NA", "not provided"}:
            return value
    return "no informado"


def clinvar_row_to_variant_record(row: Dict[str, str]) -> VariantRecord:
    """Convierte una fila de variant_summary.txt a VariantRecord E.C.O."""
    variation_id = first_non_empty(row.get("VariationID", ""), row.get("#AlleleID", ""), row.get("AlleleID", ""))
    gene = first_non_empty(row.get("GeneSymbol", ""), row.get("GeneID", ""))
    variant_name = first_non_empty(row.get("Name", ""), f"ClinVar Variation {variation_id}")
    hgvs = first_non_empty(row.get("Name", ""), row.get("OtherIDs", ""))
    condition = first_non_empty(row.get("PhenotypeList", ""), row.get("PhenotypeIDS", ""))
    clinical_significance = first_non_empty(row.get("ClinicalSignificance", ""), "no classification provided")
    review_status = first_non_empty(row.get("ReviewStatus", ""), "no assertion criteria provided")
    last_evaluated = first_non_empty(row.get("LastEvaluated", ""), "no informado")
    origin = first_non_empty(row.get("Origin", ""), row.get("OriginSimple", ""), "ClinVar")
    source_url = f"https://www.ncbi.nlm.nih.gov/clinvar/variation/{variation_id}/" if variation_id != "no informado" else "https://www.ncbi.nlm.nih.gov/clinvar/"
    notes = (
        f"Tipo={first_non_empty(row.get('Type', ''))}; "
        f"Assembly={first_non_empty(row.get('Assembly', ''))}; "
        f"Chr={first_non_empty(row.get('Chromosome', ''))}; "
        f"Start={first_non_empty(row.get('Start', ''))}; Stop={first_non_empty(row.get('Stop', ''))}"
    )
    return VariantRecord(
        variant_id=f"ClinVar-{variation_id}",
        gene=gene,
        variant_name=variant_name,
        hgvs=hgvs,
        condition=condition,
        clinical_significance=clinical_significance,
        review_status=review_status,
        evidence_origin=origin,
        last_evaluated=last_evaluated,
        source_url=source_url,
        notes=notes,
    )


def iter_clinvar_rows(path: Path) -> Iterable[Dict[str, str]]:
    """Itera filas del variant_summary.txt.gz sin cargar todo el archivo."""
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            yield row


def collect_records(path: Path, genes: List[str], max_records: int) -> List[VariantRecord]:
    """Recolecta registros por genes desde ClinVar."""
    wanted = normalize_gene_list(genes)
    records: List[VariantRecord] = []
    for row in iter_clinvar_rows(path):
        gene = (row.get("GeneSymbol", "") or "").strip().upper()
        if wanted and gene not in wanted:
            continue
        records.append(clinvar_row_to_variant_record(row))
        if len(records) >= max_records:
            break
    return records


def write_tsv(records: List[VariantRecord], output_tsv: Path) -> None:
    output_tsv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "variant_id",
        "gene",
        "variant_name",
        "hgvs",
        "condition",
        "clinical_significance",
        "review_status",
        "evidence_origin",
        "last_evaluated",
        "source_url",
        "notes",
    ]
    with output_tsv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for record in records:
            writer.writerow(record.__dict__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Descarga ClinVar variant_summary y genera una muestra interpretativa E.C.O.")
    parser.add_argument("--source-url", default=DEFAULT_SOURCE_URL, help="URL del variant_summary.txt.gz de ClinVar.")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR, help="Carpeta local para cache de ClinVar.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Carpeta de resultados.")
    parser.add_argument("--prefix", default=DEFAULT_PREFIX, help="Prefijo de salida.")
    parser.add_argument("--genes", nargs="+", default=DEFAULT_GENES, help="Genes a muestrear, por ejemplo BRCA1 BRCA2 CFTR TP53.")
    parser.add_argument("--max-records", type=int, default=20, help="Máximo de variantes a incluir.")
    parser.add_argument("--force-download", action="store_true", help="Descarga ClinVar aunque exista cache local.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.max_records < 1:
        parser.exit(status=1, message="Error: --max-records debe ser mayor que cero.\n")

    clinvar_gz = args.data_dir / "variant_summary.txt.gz"
    output_tsv = args.output_dir / f"{args.prefix}.tsv"
    output_json = args.output_dir / f"{args.prefix}_report.json"
    output_md = args.output_dir / f"{args.prefix}_report.md"

    try:
        download_state = download_file(args.source_url, clinvar_gz, force=args.force_download)
        records = collect_records(clinvar_gz, genes=args.genes, max_records=args.max_records)
        if not records:
            parser.exit(status=1, message="Error: no se encontraron variantes para los genes indicados.\n")

        write_tsv(records, output_tsv)
        report = build_report(records)
        report["source"] = {
            "url": args.source_url,
            "download_state": download_state,
            "genes": args.genes,
            "max_records": args.max_records,
            "tsv_sample": str(output_tsv),
        }
        write_json_report(report, output_json)
        output_md.parent.mkdir(parents=True, exist_ok=True)
        output_md.write_text(build_markdown(report, output_tsv), encoding="utf-8")

        summary = report["summary"]
        print("E.C.O. CLINVAR SAMPLE REPORT")
        print("============================")
        print(f"Fuente: {args.source_url}")
        print(f"Descarga: {download_state}")
        print(f"Genes buscados: {', '.join(args.genes)}")
        print(f"Variantes procesadas: {summary['variants_processed']}")
        print(f"Categorías: {summary['category_counts']}")
        print(f"Evidencia: {summary['evidence_strength_counts']}")
        print(f"Muestra TSV: {output_tsv}")
        print(f"Reporte JSON: {output_json}")
        print(f"Reporte Markdown: {output_md}")
        print("Estado: OK, muestra pública de ClinVar interpretada por E.C.O. sin diagnóstico médico.")
        return 0
    except (OSError, ValueError, KeyError, urllib.error.URLError) as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
