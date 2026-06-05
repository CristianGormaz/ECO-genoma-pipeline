"""Contratos compartidos de validacion para E.C.O."""

from .dna_validation import (
    BedRecord,
    FastaRecord,
    ParseErrorRecord,
    ValidationResult,
    fasta_records_to_dict,
    iter_bed_records,
    iter_fasta_records,
    normalize_dna_sequence,
    parse_bed_record,
    parse_bed_records,
    parse_fasta_header,
    parse_fasta_records,
    validate_bed_fields,
    validate_dna_sequence,
    validate_fasta_header,
)

__all__ = [
    "BedRecord",
    "FastaRecord",
    "ParseErrorRecord",
    "ValidationResult",
    "fasta_records_to_dict",
    "iter_bed_records",
    "iter_fasta_records",
    "normalize_dna_sequence",
    "parse_bed_record",
    "parse_bed_records",
    "parse_fasta_header",
    "parse_fasta_records",
    "validate_bed_fields",
    "validate_dna_sequence",
    "validate_fasta_header",
]
