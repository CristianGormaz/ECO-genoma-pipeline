import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from eco_motif_analysis import parse_fasta, reports_to_json, scan_sequence, write_csv


def test_scan_sequence_detects_expected_motifs():
    sequence = "ACGTACGTCCAATTTTTTTTATAAAGGGCGGAATAAA"
    report = scan_sequence(sequence, sequence_id="ejemplo_promotor")

    hits = {
        (hit.motif_name, hit.start, hit.end, hit.matched_sequence)
        for hit in report.hits
    }

    assert report.sequence_id == "ejemplo_promotor"
    assert report.length == 37
    assert report.gc_percent == pytest.approx(32.4324)
    assert ("CAAT_box", 9, 13, "CCAAT") in hits
    assert ("homopolimero_T_6_mas", 13, 20, "TTTTTTTT") in hits
    assert ("TATA_box_canonica", 20, 25, "TATAAA") in hits
    assert ("TATA_box_degenerada", 20, 25, "TATAAA") in hits
    assert ("GC_box", 26, 31, "GGGCGG") in hits
    assert ("polyA_signal", 32, 37, "AATAAA") in hits


def test_parse_fasta_supports_multiple_records(tmp_path):
    fasta = tmp_path / "demo.fa"
    fasta.write_text(">seq1\nACGT\nCCAAT\n>seq2\nNNNNTATAAA\n", encoding="utf-8")

    records = parse_fasta(fasta)

    assert records == {"seq1": "ACGTCCAAT", "seq2": "NNNNTATAAA"}


def test_scan_sequence_rejects_invalid_characters():
    with pytest.raises(ValueError, match="caracteres no válidos"):
        scan_sequence("ACGTX")


def test_scan_sequence_strict_mode_rejects_n():
    with pytest.raises(ValueError, match="N"):
        scan_sequence("ACGTN", allow_n=False)


def test_json_and_csv_exports(tmp_path):
    report = scan_sequence("CCAAT", sequence_id="seq")

    json_data = json.loads(reports_to_json([report]))
    assert json_data[0]["sequence_id"] == "seq"
    assert json_data[0]["hits"][0]["motif_name"] == "CAAT_box"

    csv_path = tmp_path / "report.csv"
    write_csv([report], csv_path)
    csv_text = csv_path.read_text(encoding="utf-8")
    assert "CAAT_box" in csv_text
    assert "CCAAT" in csv_text
