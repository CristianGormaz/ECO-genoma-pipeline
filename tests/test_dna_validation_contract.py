from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from eco_bed_to_fasta import parse_bed_line, parse_fasta as parse_reference_fasta
from eco_core.validation.dna_validation import (
    normalize_dna_sequence,
    validate_dna_sequence,
    validate_fasta_header,
)
from eco_motif_analysis import scan_sequence
from src.eco_sequence_classifier import extract_features, kmer_frequencies


def test_normalize_dna_sequence_uppercases_and_strips_whitespace():
    assert normalize_dna_sequence(" acg t\nn ") == "ACGTN"


def test_validate_dna_sequence_rejects_invalid_characters():
    result = validate_dna_sequence("ACGTX")

    assert result.is_valid is False
    assert result.invalid_characters == ["X"]
    assert "Caracteres no válidos: X" in result.issues


def test_validate_dna_sequence_accepts_n_when_allowed():
    result = validate_dna_sequence("ACGTN", allow_n=True)

    assert result.is_valid is True
    assert result.issues == []


def test_validate_dna_sequence_rejects_empty_sequence():
    result = validate_dna_sequence(" \n\t ")

    assert result.is_valid is False
    assert result.issues == ["La secuencia está vacía."]


def test_validate_fasta_header_accepts_leading_marker():
    assert validate_fasta_header(">seq1 descripcion") is True


def test_validate_fasta_header_rejects_missing_marker():
    assert validate_fasta_header("seq1 descripcion") is False


def test_motif_analysis_keeps_previous_invalid_character_behavior():
    with pytest.raises(ValueError, match="caracteres no válidos"):
        scan_sequence("ACGTX")


def test_sequence_classifier_kmers_share_normalization_contract():
    features = kmer_frequencies("ac gt", k=2)

    assert features["kmer_2_AC"] == 0.3333
    assert features["kmer_2_CG"] == 0.3333
    assert features["kmer_2_GT"] == 0.3333


def test_sequence_classifier_extract_features_remains_compatible():
    features = extract_features("ACGTCCAATTTTTTTTATAAAGGGCGGAATAAA")

    assert features["has_tata"] == 1.0
    assert features["has_caat"] == 1.0


def test_bed_to_fasta_header_and_bed_validation_remain_compatible(tmp_path: Path):
    fasta = tmp_path / "reference.fa"
    fasta.write_text(">chr1\nACGT\n", encoding="utf-8")

    assert parse_reference_fasta(fasta) == {"chr1": "ACGT"}
    assert parse_bed_line("chr1\t0\t4\tregion", 1) is not None
