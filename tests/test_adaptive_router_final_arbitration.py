import json
import subprocess
import sys
from pathlib import Path

from scripts import run_eco_difficulty_eval as difficulty_eval


KNOWN_SEQUENCE = "GCCCAGTAACCA"
KNOWN_SEQUENCE_ID = "known_arbitration_sequence"
TRAINING_INPUT = "examples/eco_labeled_sequences.tsv"
EXPECTED_LABEL = "regulatory"


def build_inference_row(sequence: str = KNOWN_SEQUENCE) -> dict[str, str]:
    return {
        "sequence_id": KNOWN_SEQUENCE_ID,
        "sequence": sequence,
        "label": "unknown",
        "split": "inference",
        "difficulty": "unknown",
    }


def train_baseline_v3_model():
    rows = difficulty_eval.read_dataset(TRAINING_INPUT)
    return difficulty_eval.centroid_train(rows, difficulty_eval.features_baseline_v3)


def run_predict_cli(tmp_path: Path, *, threshold: float = 0.20):
    output_json = tmp_path / "adaptive_prediction.json"
    output_md = tmp_path / "adaptive_prediction.md"
    output_html = tmp_path / "adaptive_prediction.html"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_eco_adaptive_router_predict.py",
            "--sequence",
            KNOWN_SEQUENCE,
            "--sequence-id",
            KNOWN_SEQUENCE_ID,
            "--threshold",
            str(threshold),
            "--embedding-k",
            "4",
            "--dimensions",
            "128",
            "--output-json",
            str(output_json),
            "--output-md",
            str(output_md),
            "--output-html",
            str(output_html),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(output_json.read_text(encoding="utf-8"))
    return payload, result


def run_batch_cli(tmp_path: Path, *, threshold: float = 0.20):
    batch_input = tmp_path / "known_sequence_batch.tsv"
    output_json = tmp_path / "batch_report.json"
    output_md = tmp_path / "batch_report.md"
    output_html = tmp_path / "batch_report.html"

    batch_input.write_text(
        "sequence_id\tsequence\tdescription\n"
        f"{KNOWN_SEQUENCE_ID}\t{KNOWN_SEQUENCE}\tknown arbitration regression\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_eco_adaptive_router_batch.py",
            "--batch-input",
            str(batch_input),
            "--training-input",
            TRAINING_INPUT,
            "--threshold",
            str(threshold),
            "--embedding-k",
            "4",
            "--dimensions",
            "128",
            "--output-json",
            str(output_json),
            "--output-md",
            str(output_md),
            "--output-html",
            str(output_html),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert len(payload["results"]) == 1
    return payload["results"][0], result


def test_adaptive_router_final_prediction_matches_base_for_known_sequence(tmp_path: Path):
    row = build_inference_row()
    model = train_baseline_v3_model()
    base_prediction = difficulty_eval.predict(row, model, difficulty_eval.features_baseline_v3)

    payload, _result = run_predict_cli(tmp_path)

    assert base_prediction == EXPECTED_LABEL
    assert payload["baseline_v3"]["prediction"] == base_prediction
    assert payload["final_prediction"] == base_prediction


def test_adaptive_router_does_not_select_lower_confidence_conflicting_route_without_reason(tmp_path: Path):
    payload, _result = run_predict_cli(tmp_path)

    assert payload["baseline_v3"]["prediction"] != payload["embedding_semireal"]["prediction"]
    assert payload["baseline_v3"]["confidence"] > payload["embedding_semireal"]["confidence"]
    assert payload["selected_route"] == "baseline_v3"
    assert payload["final_prediction"] == payload["baseline_v3"]["prediction"]
    assert payload["arbitration_reason"].startswith("conflict_resolved_by_higher_confidence")


def test_adaptive_router_output_exposes_arbitration_reason(tmp_path: Path):
    payload, result = run_predict_cli(tmp_path)

    assert payload["selected_route"] == "baseline_v3"
    assert payload["final_prediction"] == EXPECTED_LABEL
    assert payload["route_confidences"] == {
        "baseline_v3": payload["baseline_v3"]["confidence"],
        "embedding_semireal": payload["embedding_semireal"]["confidence"],
    }
    assert payload["arbitration_reason"]
    assert payload["conflicting_routes"] == ["baseline_v3", "embedding_semireal"]
    assert payload["confidence_policy"]
    assert "Arbitraje:" in result.stdout
    assert "Politica de confianza:" in result.stdout
    assert "Rutas en conflicto:" in result.stdout


def test_adaptive_router_batch_final_prediction_matches_base_for_known_sequence(tmp_path: Path):
    item, _result = run_batch_cli(tmp_path)

    assert item["status"] == "processed"
    assert item["baseline_v3"]["prediction"] == EXPECTED_LABEL
    assert item["embedding_semireal"]["prediction"] == "non_regulatory"
    assert item["baseline_v3"]["confidence"] > item["embedding_semireal"]["confidence"]
    assert item["selected_route"] == "baseline_v3"
    assert item["final_prediction"] == EXPECTED_LABEL
    assert item["arbitration_reason"].startswith("conflict_resolved_by_higher_confidence")
