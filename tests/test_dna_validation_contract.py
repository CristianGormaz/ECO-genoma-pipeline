from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from eco_bed_to_fasta import parse_bed_line, parse_fasta as parse_reference_fasta
from eco_core.validation.dna_validation import (
    FastaRecord,
    fasta_records_to_dict,
    iter_bed_records,
    iter_fasta_lines,
    iter_fasta_records,
    normalize_dna_sequence,
    parse_bed_record,
    parse_bed_records,
    parse_fasta_records,
    validate_dna_sequence,
    validate_fasta_header,
    write_fasta_records,
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


def test_parse_fasta_records_reads_multiple_sequences(tmp_path: Path):
    fasta = tmp_path / "demo.fa"
    fasta.write_text(">seq1\nACGT\nCCAAT\n>seq2\nNNNNTATAAA\n", encoding="utf-8")

    records = parse_fasta_records(fasta)

    assert records[0].sequence_id == "seq1"
    assert records[0].sequence == "ACGTCCAAT"
    assert records[1].sequence_id == "seq2"
    assert records[1].sequence == "NNNNTATAAA"
    assert fasta_records_to_dict(records) == {"seq1": "ACGTCCAAT", "seq2": "NNNNTATAAA"}


def test_parse_fasta_records_rejects_missing_header(tmp_path: Path):
    fasta = tmp_path / "malformed.fa"
    fasta.write_text("ACGT\nTATAAA\n", encoding="utf-8")

    with pytest.raises(ValueError, match="debe comenzar con una cabecera"):
        parse_fasta_records(fasta)


def test_iter_fasta_records_supports_partial_consumption(tmp_path: Path):
    fasta = tmp_path / "partial.fa"
    fasta.write_text(">seq1\nACGT\n>seq2\nACGX\n", encoding="utf-8")

    iterator = iter_fasta_records(fasta, validate_sequences=True)

    first = next(iterator)
    assert first.sequence_id == "seq1"
    assert first.sequence == "ACGT"

    with pytest.raises(ValueError, match="seq2"):
        next(iterator)


def test_parse_bed_record_ignores_comments_and_empty_lines():
    assert parse_bed_record("# comment", 1) is None
    assert parse_bed_record("   ", 2) is None


def test_parse_bed_records_reads_multiple_regions(tmp_path: Path):
    bed = tmp_path / "regions.bed"
    bed.write_text("# comment\nchr1\t0\t4\tfirst\nchr1\t4\t8\tsecond\t0\t+\n", encoding="utf-8")

    records = parse_bed_records(bed)

    assert len(records) == 2
    assert records[0].name == "first"
    assert records[1].strand == "+"


def test_iter_bed_records_supports_partial_consumption(tmp_path: Path):
    bed = tmp_path / "partial.bed"
    bed.write_text("chr1\t0\t4\tfirst\nchr1\t4\twrong\tsecond\n", encoding="utf-8")

    iterator = iter_bed_records(bed)

    first = next(iterator)
    assert first.name == "first"

    with pytest.raises(ValueError, match="start/end deben ser enteros"):
        next(iterator)


def test_iter_fasta_lines_matches_existing_format_contract():
    records = [
        FastaRecord(sequence_id="seq1", sequence="ACGT"),
        FastaRecord(sequence_id="seq2", sequence="TTAA"),
    ]

    assert "".join(iter_fasta_lines(records, line_width=2)) == (
        ">seq1\n"
        "AC\n"
        "GT\n"
        ">seq2\n"
        "TT\n"
        "AA\n"
    )


def test_write_fasta_records_supports_partial_writes(tmp_path: Path):
    output = tmp_path / "partial.fa"

    def records():
        yield FastaRecord(sequence_id="seq1", sequence="ACGT")
        raise ValueError("late failure")

    with pytest.raises(ValueError, match="late failure"):
        write_fasta_records(records(), output, line_width=4)

    assert output.read_text(encoding="utf-8") == ">seq1\nACGT\n"


def test_write_fasta_records_does_not_create_output_before_first_record(tmp_path: Path):
    output = tmp_path / "no_output.fa"

    def records():
        raise ValueError("boom before first record")
        yield  # pragma: no cover

    with pytest.raises(ValueError, match="boom before first record"):
        write_fasta_records(records(), output)

    assert not output.exists()


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
