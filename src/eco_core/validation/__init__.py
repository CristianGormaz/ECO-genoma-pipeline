"""Contratos compartidos de validacion para E.C.O."""

from .dna_validation import (
    BedRecord,
    FastaRecord,
    ParseErrorRecord,
    ValidationResult,
    normalize_dna_sequence,
    parse_fasta_header,
    validate_bed_fields,
    validate_dna_sequence,
    validate_fasta_header,
)

__all__ = [
    "BedRecord",
    "FastaRecord",
    "ParseErrorRecord",
    "ValidationResult",
    "normalize_dna_sequence",
    "parse_fasta_header",
    "validate_bed_fields",
    "validate_dna_sequence",
    "validate_fasta_header",
]
