#!/usr/bin/env python3
"""
E.C.O. - Análisis de motivos regulatorios en ADN
=================================================

Este módulo forma parte del proyecto E.C.O. (Entérico Codificador Orgánico),
un pipeline bioinspirado que interpreta datos genómicos como si fueran
"alimento" informacional: entrada de secuencias, digestión computacional y
salida interpretativa.

Funcionalidad principal:
- Leer secuencias desde archivos FASTA.
- Normalizar y validar ADN.
- Calcular longitud y porcentaje GC.
- Buscar motivos regulatorios clásicos:
  - TATA box canónica: TATAAA
  - TATA box degenerada: TATA[AT][AT]
  - CAAT box: CCAAT
  - GC box: GGGCGG
  - Señal de poliadenilación: AATAAA
  - Repeticiones homopoliméricas largas, como AAAAAA, TTTTTT, etc.
- Reportar posiciones en base 1 para lectura biológica más intuitiva.
- Exportar resultados en JSON o CSV.

Firma conceptual:
Cristian Gormaz - Proyecto E.C.O.
Actualización asistida por ChatGPT.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Pattern

DNA_ALPHABET = set("ACGTN")

DEFAULT_MOTIFS: Dict[str, str] = {
    "TATA_box_canonica": r"TATAAA",
    "TATA_box_degenerada": r"TATA[AT][AT]",
    "CAAT_box": r"CCAAT",
    "GC_box": r"GGGCGG",
    "polyA_signal": r"AATAAA",
    "homopolimero_A_6_mas": r"A{6,}",
    "homopolimero_T_6_mas": r"T{6,}",
    "homopolimero_C_6_mas": r"C{6,}",
    "homopolimero_G_6_mas": r"G{6,}",
}


@dataclass(frozen=True)
class MotifHit:
    """Representa una coincidencia de motivo en una secuencia."""

    motif_name: str
    pattern: str
    start: int
    end: int
    matched_sequence: str


@dataclass(frozen=True)
class SequenceReport:
    """Resumen del análisis de una secuencia."""

    sequence_id: str
    length: int
    gc_percent: float
    n_percent: float
    hits: List[MotifHit]


def parse_fasta(path: str | Path) -> Dict[str, str]:
    """Lee uno o más registros FASTA.

    Args:
        path: Ruta al archivo FASTA.

    Returns:
        Diccionario {id_secuencia: secuencia}.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si el archivo no contiene secuencias.
    """
    fasta_path = Path(path)
    if not fasta_path.exists():
        raise FileNotFoundError(f"No existe el archivo FASTA: {fasta_path}")

    records: Dict[str, List[str]] = {}
    current_id: Optional[str] = None

    with fasta_path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith(">"):
                current_id = line[1:].split()[0] or f"sequence_{len(records) + 1}"
                records.setdefault(current_id, [])
                continue
            if current_id is None:
                current_id = "sequence_1"
                records.setdefault(current_id, [])
            records[current_id].append(line)

    sequences = {seq_id: normalize_sequence("".join(parts)) for seq_id, parts in records.items()}
    if not sequences:
        raise ValueError(f"El archivo no contiene secuencias FASTA: {fasta_path}")
    return sequences


def normalize_sequence(sequence: str) -> str:
    """Normaliza una secuencia de ADN.

    Convierte a mayúsculas y elimina espacios, saltos de línea y caracteres
    comunes de separación.
    """
    return re.sub(r"\s+", "", sequence.upper())


def validate_sequence(sequence: str, allow_n: bool = True) -> None:
    """Valida que la secuencia contenga bases esperadas.

    Args:
        sequence: Secuencia normalizada.
        allow_n: Permite N como base ambigua.

    Raises:
        ValueError: Si aparecen caracteres no válidos.
    """
    allowed = DNA_ALPHABET if allow_n else set("ACGT")
    invalid = sorted(set(sequence) - allowed)
    if invalid:
        raise ValueError(
            "La secuencia contiene caracteres no válidos: " + ", ".join(invalid)
        )


def gc_percent(sequence: str) -> float:
    """Calcula el porcentaje GC ignorando N en el denominador efectivo."""
    informative_bases = [base for base in sequence if base in "ACGT"]
    if not informative_bases:
        return 0.0
    gc_count = sum(1 for base in informative_bases if base in "GC")
    return round((gc_count / len(informative_bases)) * 100, 4)


def n_percent(sequence: str) -> float:
    """Calcula el porcentaje de bases ambiguas N."""
    if not sequence:
        return 0.0
    return round((sequence.count("N") / len(sequence)) * 100, 4)


def compile_motifs(motifs: Dict[str, str]) -> Dict[str, Pattern[str]]:
    """Compila patrones regex para búsqueda eficiente."""
    return {name: re.compile(pattern) for name, pattern in motifs.items()}


def scan_sequence(
    sequence: str,
    sequence_id: str = "sequence_1",
    motifs: Optional[Dict[str, str]] = None,
    allow_n: bool = True,
) -> SequenceReport:
    """Analiza una secuencia y devuelve un reporte estructurado.

    Las posiciones se entregan en base 1 e incluyen ambos extremos.
    """
    seq = normalize_sequence(sequence)
    validate_sequence(seq, allow_n=allow_n)

    motif_patterns = motifs or DEFAULT_MOTIFS
    compiled = compile_motifs(motif_patterns)

    hits: List[MotifHit] = []
    for motif_name, regex in compiled.items():
        pattern = motif_patterns[motif_name]
        for match in regex.finditer(seq):
            hits.append(
                MotifHit(
                    motif_name=motif_name,
                    pattern=pattern,
                    start=match.start() + 1,
                    end=match.end(),
                    matched_sequence=match.group(0),
                )
            )

    hits.sort(key=lambda item: (item.start, item.end, item.motif_name))

    return SequenceReport(
        sequence_id=sequence_id,
        length=len(seq),
        gc_percent=gc_percent(seq),
        n_percent=n_percent(seq),
        hits=hits,
    )


def reports_to_json(reports: Iterable[SequenceReport]) -> str:
    """Convierte reportes a JSON legible."""
    return json.dumps([asdict(report) for report in reports], ensure_ascii=False, indent=2)


def write_csv(reports: Iterable[SequenceReport], output_path: str | Path) -> None:
    """Exporta coincidencias de motivos a CSV."""
    fieldnames = [
        "sequence_id",
        "length",
        "gc_percent",
        "n_percent",
        "motif_name",
        "pattern",
        "start",
        "end",
        "matched_sequence",
    ]
    with Path(output_path).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for report in reports:
            if not report.hits:
                writer.writerow(
                    {
                        "sequence_id": report.sequence_id,
                        "length": report.length,
                        "gc_percent": report.gc_percent,
                        "n_percent": report.n_percent,
                        "motif_name": "",
                        "pattern": "",
                        "start": "",
                        "end": "",
                        "matched_sequence": "",
                    }
                )
                continue
            for hit in report.hits:
                writer.writerow(
                    {
                        "sequence_id": report.sequence_id,
                        "length": report.length,
                        "gc_percent": report.gc_percent,
                        "n_percent": report.n_percent,
                        **asdict(hit),
                    }
                )


def print_human_report(reports: Iterable[SequenceReport]) -> None:
    """Imprime un resumen claro para uso en terminal."""
    for report in reports:
        print(f"\nSecuencia: {report.sequence_id}")
        print(f"Longitud: {report.length} bp")
        print(f"GC: {report.gc_percent:.2f}%")
        print(f"N ambiguas: {report.n_percent:.2f}%")

        if not report.hits:
            print("Motivos encontrados: 0")
            continue

        print(f"Motivos encontrados: {len(report.hits)}")
        for hit in report.hits:
            print(
                f"- {hit.motif_name} ({hit.matched_sequence}) "
                f"posiciones {hit.start}-{hit.end}"
            )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analiza motivos regulatorios clásicos en secuencias FASTA para el proyecto E.C.O."
    )
    parser.add_argument("--fasta", required=True, help="Ruta al archivo FASTA de entrada.")
    parser.add_argument(
        "--json",
        dest="json_output",
        help="Ruta opcional para guardar el reporte JSON.",
    )
    parser.add_argument(
        "--csv",
        dest="csv_output",
        help="Ruta opcional para guardar el reporte CSV.",
    )
    parser.add_argument(
        "--strict-acgt",
        action="store_true",
        help="Rechaza secuencias con N. Por defecto se permite N como base ambigua.",
    )
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    try:
        sequences = parse_fasta(args.fasta)
        reports = [
            scan_sequence(seq, sequence_id=seq_id, allow_n=not args.strict_acgt)
            for seq_id, seq in sequences.items()
        ]

        print_human_report(reports)

        if args.json_output:
            Path(args.json_output).write_text(reports_to_json(reports), encoding="utf-8")
            print(f"\nReporte JSON guardado en: {args.json_output}")

        if args.csv_output:
            write_csv(reports, args.csv_output)
            print(f"Reporte CSV guardado en: {args.csv_output}")
    except (FileNotFoundError, ValueError) as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")


if __name__ == "__main__":
    main()
