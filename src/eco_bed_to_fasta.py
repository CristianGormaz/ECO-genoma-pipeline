#!/usr/bin/env python3
"""
E.C.O. - Conversión BED a FASTA
===============================

Este módulo convierte coordenadas genómicas en formato BED hacia secuencias
FASTA usando un genoma de referencia local.

Contexto biológico:
- BED usa coordenadas 0-based, semiabiertas: start incluido, end excluido.
- FASTA se reporta como secuencia biológica legible.
- Si el BED incluye hebra en la columna 6, se puede extraer la reverse complement
  para regiones anotadas en hebra negativa.

Firma conceptual:
Cristian Gormaz - Proyecto E.C.O.
Actualización asistida por ChatGPT.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional

try:
    from eco_core.validation.dna_validation import (
        fasta_records_to_dict,
        iter_fasta_lines,
        iter_bed_records,
        iter_fasta_records,
        normalize_dna_sequence,
        parse_bed_record,
        validate_dna_sequence as shared_validate_dna_sequence,
        write_fasta_records,
    )
except ImportError:  # pragma: no cover - compatibilidad cuando se importa como src.eco_bed_to_fasta
    from src.eco_core.validation.dna_validation import (
        fasta_records_to_dict,
        iter_fasta_lines,
        iter_bed_records,
        iter_fasta_records,
        normalize_dna_sequence,
        parse_bed_record,
        validate_dna_sequence as shared_validate_dna_sequence,
        write_fasta_records,
    )

COMPLEMENT_TABLE = str.maketrans("ACGTNacgtn", "TGCANtgcan")


@dataclass(frozen=True)
class BedRegion:
    """Representa una región BED mínima."""

    chrom: str
    start: int
    end: int
    name: str
    score: Optional[str] = None
    strand: Optional[str] = None

    @property
    def length(self) -> int:
        return self.end - self.start


@dataclass(frozen=True)
class FastaRecord:
    """Representa una secuencia FASTA extraída desde una región BED."""

    sequence_id: str
    sequence: str


def normalize_sequence(sequence: str) -> str:
    """Normaliza una secuencia de ADN."""
    return normalize_dna_sequence(sequence)


def validate_reference_sequence(sequence: str, sequence_id: str) -> None:
    """Valida que una secuencia de referencia contenga bases esperadas."""
    result = shared_validate_dna_sequence(sequence, allow_n=True)
    if result.invalid_characters:
        raise ValueError(
            f"La secuencia de referencia '{sequence_id}' contiene caracteres no válidos: "
            + ", ".join(result.invalid_characters)
        )


def parse_fasta(path: str | Path) -> Dict[str, str]:
    """Lee un archivo FASTA de referencia.

    Args:
        path: Ruta al archivo FASTA.

    Returns:
        Diccionario {id_contig: secuencia}.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si no contiene registros o contiene bases inválidas.
    """
    fasta_path = Path(path)
    if not fasta_path.exists():
        raise FileNotFoundError(f"No existe el archivo FASTA de referencia: {fasta_path}")

    sequences = fasta_records_to_dict(iter_fasta_records(fasta_path))
    if not sequences:
        raise ValueError(f"El archivo no contiene secuencias FASTA: {fasta_path}")

    for seq_id, sequence in sequences.items():
        validate_reference_sequence(sequence, seq_id)

    return sequences


def parse_bed_line(line: str, line_number: int) -> Optional[BedRegion]:
    """Convierte una línea BED en BedRegion.

    Se aceptan BED3, BED4, BED5 y BED6. Las líneas vacías o comentarios se omiten.
    """
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None

    record = parse_bed_record(stripped, line_number)
    if record is None:
        return None
    return BedRegion(
        chrom=record.chrom,
        start=record.start,
        end=record.end,
        name=record.name,
        score=record.score,
        strand=record.strand,
    )


def parse_bed(path: str | Path) -> List[BedRegion]:
    """Lee un archivo BED y devuelve regiones validadas."""
    bed_path = Path(path)
    if not bed_path.exists():
        raise FileNotFoundError(f"No existe el archivo BED: {bed_path}")

    regions = list(iter_bed_regions(bed_path))

    if not regions:
        raise ValueError(f"El archivo BED no contiene regiones válidas: {bed_path}")
    return regions


def iter_bed_regions(path: str | Path) -> Iterator[BedRegion]:
    """Adapta BedRecord -> BedRegion sin materializar toda la entrada BED."""
    for record in iter_bed_records(path):
        yield BedRegion(
            chrom=record.chrom,
            start=record.start,
            end=record.end,
            name=record.name,
            score=record.score,
            strand=record.strand,
        )


def reverse_complement(sequence: str) -> str:
    """Devuelve la reverse complement de una secuencia de ADN."""
    return sequence.translate(COMPLEMENT_TABLE)[::-1].upper()


def build_fasta_header(region: BedRegion) -> str:
    """Construye una cabecera FASTA trazable desde una región BED."""
    strand = region.strand if region.strand else "."
    return f"{region.name}|{region.chrom}:{region.start}-{region.end}({strand})"


def extract_region(reference: Dict[str, str], region: BedRegion) -> FastaRecord:
    """Extrae una región BED desde el genoma de referencia."""
    if region.chrom not in reference:
        raise ValueError(f"El cromosoma/contig '{region.chrom}' no existe en el FASTA.")

    chrom_sequence = reference[region.chrom]
    if region.end > len(chrom_sequence):
        raise ValueError(
            f"La región {region.chrom}:{region.start}-{region.end} excede el largo "
            f"del contig ({len(chrom_sequence)} bp)."
        )

    sequence = chrom_sequence[region.start : region.end]
    if region.strand == "-":
        sequence = reverse_complement(sequence)

    return FastaRecord(sequence_id=build_fasta_header(region), sequence=sequence)


def bed_to_fasta(reference: Dict[str, str], regions: Iterable[BedRegion]) -> List[FastaRecord]:
    """Convierte regiones BED en registros FASTA."""
    return [extract_region(reference, region) for region in regions]


def format_fasta(records: Iterable[FastaRecord], line_width: int = 60) -> str:
    """Formatea registros FASTA con ancho de línea configurable."""
    return "".join(iter_fasta_lines(records, line_width=line_width))


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convierte coordenadas BED a FASTA usando un genoma de referencia local."
    )
    parser.add_argument("--bed", required=True, help="Ruta al archivo BED de entrada.")
    parser.add_argument(
        "--reference",
        required=True,
        help="Ruta al FASTA de referencia local.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Ruta donde guardar el FASTA extraído.",
    )
    parser.add_argument(
        "--line-width",
        type=int,
        default=60,
        help="Ancho de línea para el FASTA de salida. Por defecto: 60.",
    )
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    try:
        reference = parse_fasta(args.reference)
        output_path = Path(args.output)
        written = write_fasta_records(
            (extract_region(reference, region) for region in iter_bed_regions(args.bed)),
            output_path,
            line_width=args.line_width,
        )

        print(f"Regiones procesadas: {written}")
        print(f"FASTA guardado en: {output_path}")
    except (FileNotFoundError, ValueError) as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")


if __name__ == "__main__":
    main()
