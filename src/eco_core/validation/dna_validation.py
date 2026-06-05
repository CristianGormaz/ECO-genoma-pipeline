from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


DNA_ALPHABET = frozenset("ACGTN")
STRICT_DNA_ALPHABET = frozenset("ACGT")


@dataclass(frozen=True)
class ValidationResult:
    normalized_sequence: str
    is_valid: bool
    issues: list[str]
    invalid_characters: list[str]
    allow_n: bool = True


@dataclass(frozen=True)
class FastaRecord:
    sequence_id: str
    sequence: str


@dataclass(frozen=True)
class BedRecord:
    chrom: str
    start: int
    end: int
    name: str
    score: str | None = None
    strand: str | None = None


@dataclass(frozen=True)
class ParseErrorRecord:
    line_number: int
    message: str
    raw_line: str | None = None


def normalize_dna_sequence(sequence: str) -> str:
    return re.sub(r"\s+", "", sequence.upper())


def validate_dna_sequence(sequence: str, allow_n: bool = True) -> ValidationResult:
    normalized = normalize_dna_sequence(sequence)
    allowed = DNA_ALPHABET if allow_n else STRICT_DNA_ALPHABET
    issues: list[str] = []

    if not normalized:
        issues.append("La secuencia está vacía.")

    invalid = sorted(set(normalized) - allowed)
    if invalid:
        issues.append("Caracteres no válidos: " + ", ".join(invalid))

    return ValidationResult(
        normalized_sequence=normalized,
        is_valid=not issues,
        issues=issues,
        invalid_characters=invalid,
        allow_n=allow_n,
    )


def validate_fasta_header(line: str) -> bool:
    stripped = line.strip()
    if not stripped.startswith(">"):
        return False
    return bool(stripped[1:].strip().split())


def parse_fasta_header(line: str) -> str:
    stripped = line.strip()
    if not stripped.startswith(">"):
        raise ValueError("El archivo FASTA debe comenzar con una cabecera '>'.")

    tokens = stripped[1:].strip().split()
    if not tokens:
        raise ValueError("Se encontró una cabecera FASTA sin identificador.")
    return tokens[0]


def parse_fasta_records(path: str | Path) -> list[FastaRecord]:
    fasta_path = Path(path)
    if not fasta_path.exists():
        raise FileNotFoundError(f"No existe el archivo FASTA: {fasta_path}")

    records: dict[str, list[str]] = {}
    current_id: str | None = None

    with fasta_path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith(">"):
                current_id = parse_fasta_header(line)
                records.setdefault(current_id, [])
                continue
            if current_id is None:
                raise ValueError("El archivo FASTA debe comenzar con una cabecera '>'.")
            records[current_id].append(line)

    parsed_records = [
        FastaRecord(sequence_id=sequence_id, sequence=normalize_dna_sequence("".join(parts)))
        for sequence_id, parts in records.items()
    ]
    if not parsed_records:
        raise ValueError(f"El archivo no contiene secuencias FASTA: {fasta_path}")
    return parsed_records


def fasta_records_to_dict(records: Iterable[FastaRecord]) -> dict[str, str]:
    return {record.sequence_id: record.sequence for record in records}


def validate_bed_fields(fields: Sequence[str], line_number: int) -> BedRecord:
    if len(fields) < 3:
        raise ValueError(f"Línea BED {line_number}: se esperaban al menos 3 columnas.")

    chrom = fields[0]
    try:
        start = int(fields[1])
        end = int(fields[2])
    except ValueError as exc:
        raise ValueError(f"Línea BED {line_number}: start/end deben ser enteros.") from exc

    if start < 0:
        raise ValueError(f"Línea BED {line_number}: start no puede ser negativo.")
    if end <= start:
        raise ValueError(f"Línea BED {line_number}: end debe ser mayor que start.")

    name = fields[3] if len(fields) >= 4 else f"{chrom}:{start}-{end}"
    score = fields[4] if len(fields) >= 5 else None
    strand = fields[5] if len(fields) >= 6 else None

    if strand is not None and strand not in {"+", "-", "."}:
        raise ValueError(
            f"Línea BED {line_number}: strand debe ser '+', '-' o '.', no '{strand}'."
        )

    return BedRecord(chrom=chrom, start=start, end=end, name=name, score=score, strand=strand)


def parse_bed_record(line: str, line_number: int) -> BedRecord | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    return validate_bed_fields(stripped.split(), line_number)


def parse_bed_records(path: str | Path) -> list[BedRecord]:
    bed_path = Path(path)
    if not bed_path.exists():
        raise FileNotFoundError(f"No existe el archivo BED: {bed_path}")

    records: list[BedRecord] = []
    with bed_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            record = parse_bed_record(line, line_number)
            if record is not None:
                records.append(record)

    if not records:
        raise ValueError(f"El archivo BED no contiene regiones válidas: {bed_path}")
    return records
