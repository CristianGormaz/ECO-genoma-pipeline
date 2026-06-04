import json
import subprocess
import sys
from pathlib import Path

from scripts import run_eco_confidence_router_calibrated_eval as confidence_router
from scripts import run_eco_difficulty_eval as difficulty_eval


KNOWN_SEQUENCE = "GCCCAGTAACCA"
KNOWN_SEQUENCE_ID = "known_scaling_contract_sequence"
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


def scaled_space_prediction(row: dict[str, str], model) -> str:
    centroids, mins, maxs = model
    vector = difficulty_eval.apply_minmax(
        difficulty_eval.features_baseline_v3(row["sequence"]),
        mins,
        maxs,
    )
    return min(centroids, key=lambda label: confidence_router.euclidean(vector, centroids[label]))


def test_confidence_router_applies_training_scaler():
    row = build_inference_row()
    model = train_baseline_v3_model()

    expected_prediction = scaled_space_prediction(row, model)
    predicted_label, confidence, details = confidence_router.predict_with_confidence(
        row,
        model,
        difficulty_eval.features_baseline_v3,
        feature_names=difficulty_eval.feature_names_baseline_v3(),
        return_details=True,
    )

    assert expected_prediction == EXPECTED_LABEL
    assert predicted_label == expected_prediction
    assert 0.0 <= confidence <= 1.0
    assert details["feature_space"] == "minmax"
    assert details["scaler_applied"] is True
    assert len(details["feature_names"]) == len(details["feature_min"]) == len(details["feature_max"])


def test_predict_with_confidence_matches_base_predictor_for_known_sequence():
    row = build_inference_row()
    model = train_baseline_v3_model()

    base_prediction = difficulty_eval.predict(row, model, difficulty_eval.features_baseline_v3)
    predicted_label, _confidence = confidence_router.predict_with_confidence(
        row,
        model,
        difficulty_eval.features_baseline_v3,
    )

    assert base_prediction == EXPECTED_LABEL
    assert predicted_label == base_prediction


def test_adaptive_router_predict_matches_base_logic_for_known_sequence(tmp_path: Path):
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
            "0.0",
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

    assert payload["baseline_v3"]["prediction"] == EXPECTED_LABEL
    assert payload["selected_route"] == "baseline_v3"
    assert payload["final_prediction"] == EXPECTED_LABEL
    assert payload["baseline_v3"]["feature_space"] == "minmax"
    assert payload["baseline_v3"]["scaler_applied"] is True
    assert payload["baseline_v3"]["feature_names"]


def test_adaptive_router_batch_matches_base_logic_for_known_sequence(tmp_path: Path):
    batch_input = tmp_path / "known_sequence_batch.tsv"
    output_json = tmp_path / "batch_report.json"
    output_md = tmp_path / "batch_report.md"
    output_html = tmp_path / "batch_report.html"

    batch_input.write_text(
        "sequence_id\tsequence\tdescription\n"
        f"{KNOWN_SEQUENCE_ID}\t{KNOWN_SEQUENCE}\tknown scaling contract regression\n",
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
            "0.0",
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

    item = payload["results"][0]
    assert item["status"] == "processed"
    assert item["baseline_v3"]["prediction"] == EXPECTED_LABEL
    assert item["selected_route"] == "baseline_v3"
    assert item["final_prediction"] == EXPECTED_LABEL
    assert item["baseline_v3"]["feature_space"] == "minmax"
    assert item["baseline_v3"]["scaler_applied"] is True
    assert item["baseline_v3"]["feature_names"]
