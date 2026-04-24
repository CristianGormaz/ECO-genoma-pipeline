import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from eco_bed_to_fasta import (
    BedRegion,
    bed_to_fasta,
    extract_region,
    format_fasta,
    parse_bed,
    parse_bed_line,
    parse_fasta,
    reverse_complement,
)


def test_parse_bed_line_supports_bed6():
    region = parse_bed_line("chr1\t4\t10\tregion_a\t0\t-", 1)

    assert region == BedRegion(
        chrom="chr1",
        start=4,
        end=10,
        name="region_a",
        score="0",
        strand="-",
    )


def test_parse_bed_line_rejects_invalid_coordinates():
    with pytest.raises(ValueError, match="end debe ser mayor"):
        parse_bed_line("chr1\t10\t4", 1)


def test_parse_fasta_reads_reference(tmp_path):
    fasta = tmp_path / "reference.fa"
    fasta.write_text(">chr1\nACGT\nACGT\n>chr2\nNNNN\n", encoding="utf-8")

    records = parse_fasta(fasta)

    assert records == {"chr1": "ACGTACGT", "chr2": "NNNN"}


def test_extract_region_uses_zero_based_half_open_coordinates():
    reference = {"chr1": "ACGTACGTACGT"}
    region = BedRegion(chrom="chr1", start=4, end=10, name="region_a")

    record = extract_region(reference, region)

    assert record.sequence_id == "region_a|chr1:4-10(.)"
    assert record.sequence == "ACGTAC"


def test_extract_region_reverse_complement_for_negative_strand():
    reference = {"chr1": "AAAACCCCGGGGTTTT"}
    region = BedRegion(chrom="chr1", start=4, end=8, name="neg", strand="-")

    record = extract_region(reference, region)

    assert record.sequence == "GGGG"


def test_bed_to_fasta_and_format_output():
    reference = {"chr1": "ACGTACGTACGT"}
    regions = [
        BedRegion(chrom="chr1", start=0, end=4, name="first"),
        BedRegion(chrom="chr1", start=4, end=8, name="second"),
    ]

    records = bed_to_fasta(reference, regions)
    fasta_text = format_fasta(records, line_width=4)

    assert fasta_text == (
        ">first|chr1:0-4(.)\n"
        "ACGT\n"
        ">second|chr1:4-8(.)\n"
        "ACGT\n"
    )


def test_parse_bed_reads_multiple_regions(tmp_path):
    bed = tmp_path / "regions.bed"
    bed.write_text("chr1\t0\t4\tfirst\nchr1\t4\t8\tsecond\t0\t+\n", encoding="utf-8")

    regions = parse_bed(bed)

    assert len(regions) == 2
    assert regions[0].name == "first"
    assert regions[1].strand == "+"


def test_extract_region_rejects_missing_chromosome():
    with pytest.raises(ValueError, match="no existe"):
        extract_region({"chr1": "ACGT"}, BedRegion("chrX", 0, 2, "missing"))


def test_extract_region_rejects_out_of_bounds():
    with pytest.raises(ValueError, match="excede"):
        extract_region({"chr1": "ACGT"}, BedRegion("chr1", 0, 10, "too_long"))
