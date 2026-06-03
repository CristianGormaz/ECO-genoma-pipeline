import json
from pathlib import Path

import scripts.run_sne_eco_ml_baseline as ml_baseline


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
    )


def synthetic_split(tmp_path: Path) -> tuple[Path, Path]:
    train_rows = [
        {
            "id": "train_absorb_001",
            "input_type": "sequence",
            "source_text": "paquete válido sintético estable para absorción",
            "expected_decision": "absorb",
            "defense_category": "none",
            "responsible_limit": "educational_experimental_not_clinical",
        },
        {
            "id": "train_absorb_002",
            "input_type": "sequence",
            "source_text": "secuencia sintética válida con estructura suficiente",
            "expected_decision": "absorb",
            "defense_category": "none",
            "responsible_limit": "educational_experimental_not_clinical",
        },
        {
            "id": "train_reject_001",
            "input_type": "sequence",
            "source_text": "paquete sintético inválido con formato roto",
            "expected_decision": "reject",
            "defense_category": "invalid_payload",
            "responsible_limit": "educational_experimental_not_clinical",
        },
        {
            "id": "train_reject_002",
            "input_type": "claim",
            "source_text": "reclamo diagnóstico humano prohibido",
            "expected_decision": "reject",
            "defense_category": "forbidden_diagnostic_claim",
            "responsible_limit": "reject_clinical_diagnostic_claim",
        },
        {
            "id": "train_quarantine_001",
            "input_type": "sequence",
            "source_text": "paquete ambiguo sintético para revisión",
            "expected_decision": "quarantine",
            "defense_category": "retained_payload",
            "responsible_limit": "educational_experimental_not_clinical",
        },
        {
            "id": "train_quarantine_002",
            "input_type": "sequence",
            "source_text": "dato breve ambiguo retenido",
            "expected_decision": "quarantine",
            "defense_category": "retained_payload",
            "responsible_limit": "educational_experimental_not_clinical",
        },
        {
            "id": "train_duplicate_001",
            "input_type": "sequence",
            "source_text": "paquete repetido sintético observado antes",
            "expected_decision": "discard_duplicate",
            "defense_category": "redundant_payload",
            "responsible_limit": "educational_experimental_not_clinical",
        },
        {
            "id": "train_duplicate_002",
            "input_type": "sequence",
            "source_text": "secuencia redundante sintética ya vista",
            "expected_decision": "discard_duplicate",
            "defense_category": "redundant_payload",
            "responsible_limit": "educational_experimental_not_clinical",
        },
    ]
    eval_rows = [
        {
            "id": "eval_absorb_001",
            "input_type": "sequence",
            "source_text": "paquete válido sintético para absorción",
            "expected_decision": "absorb",
            "defense_category": "none",
            "responsible_limit": "educational_experimental_not_clinical",
        },
        {
            "id": "eval_reject_001",
            "input_type": "sequence",
            "source_text": "paquete sintético inválido roto",
            "expected_decision": "reject",
            "defense_category": "invalid_payload",
            "responsible_limit": "educational_experimental_not_clinical",
        },
        {
            "id": "eval_quarantine_001",
            "input_type": "sequence",
            "source_text": "paquete ambiguo sintético retenido para revisión",
            "expected_decision": "quarantine",
            "defense_category": "retained_payload",
            "responsible_limit": "educational_experimental_not_clinical",
        },
        {
            "id": "eval_duplicate_001",
            "input_type": "sequence",
            "source_text": "paquete repetido sintético ya observado",
            "expected_decision": "discard_duplicate",
            "defense_category": "redundant_payload",
            "responsible_limit": "educational_experimental_not_clinical",
        },
    ]
    train_path = tmp_path / "train.jsonl"
    eval_path = tmp_path / "eval.jsonl"
    write_jsonl(train_path, train_rows)
    write_jsonl(eval_path, eval_rows)
    return train_path, eval_path


def test_ml_baseline_builds_report_from_tmp_split(tmp_path):
    train_path, eval_path = synthetic_split(tmp_path)
    report = ml_baseline.build_report(train_path=train_path, eval_path=eval_path)

    assert report["status"] in {"green", "attention"}
    assert report["train_count"] > report["eval_count"] > 0
    assert report["total"] == report["eval_count"]
    assert 0.0 <= report["accuracy"] <= 1.0
    assert report["using_embedded_fixture"] is False
    assert report["sanity_check_only"] is True
    assert report["training_allowed"] is False


def test_ml_baseline_generates_predictions_from_tmp_split(tmp_path):
    train_path, eval_path = synthetic_split(tmp_path)
    report = ml_baseline.build_report(train_path=train_path, eval_path=eval_path)

    assert len(report["predictions"]) == report["eval_count"]

    for row in report["predictions"]:
        assert "expected_decision" in row
        assert "predicted_decision" in row
        assert "nearest_train_id" in row
        assert "similarity" in row


def test_ml_baseline_keeps_responsible_limits(tmp_path):
    train_path, eval_path = synthetic_split(tmp_path)
    report = ml_baseline.build_report(train_path=train_path, eval_path=eval_path)
    markdown = ml_baseline.to_markdown(report)

    assert "no clínico" in markdown
    assert "diagnóstico" in markdown
    assert "forense" in markdown
    assert "conciencia humana" in markdown
    assert "no autoriza entrenamiento" in markdown
    assert "no usa datos reales" in markdown
    assert "No modifica reglas, baseline estable ni umbrales" in markdown
    assert report["errors"] == []


def test_ml_baseline_tracks_eval_distribution(tmp_path):
    train_path, eval_path = synthetic_split(tmp_path)
    report = ml_baseline.build_report(train_path=train_path, eval_path=eval_path)

    expected = report["expected_counts"]

    assert "absorb" in expected
    assert "reject" in expected
    assert "quarantine" in expected
    assert "discard_duplicate" in expected


def test_ml_baseline_feature_policy_excludes_defense_category(tmp_path):
    train_path, eval_path = synthetic_split(tmp_path)
    report = ml_baseline.build_report(train_path=train_path, eval_path=eval_path)
    policy = report["feature_policy"]

    assert "defense_category" not in policy["predictive_features"]
    assert "defense_category" in policy["excluded_from_prediction"]
    assert "defense_category" in policy["audit_only_fields"]


def test_predict_decision_does_not_score_defense_category():
    train_rows = [
        {
            "id": "nearest_by_text",
            "input_type": "sequence",
            "source_text": "paquete válido sintético estable para absorción",
            "expected_decision": "absorb",
            "defense_category": "none",
            "responsible_limit": "educational_experimental_not_clinical",
        },
        {
            "id": "same_defense_wrong_text",
            "input_type": "sequence",
            "source_text": "texto sin relación operacional",
            "expected_decision": "reject",
            "defense_category": "forbidden_diagnostic_claim",
            "responsible_limit": "reject_clinical_diagnostic_claim",
        },
    ]
    row = {
        "id": "eval",
        "input_type": "sequence",
        "source_text": "paquete válido sintético para absorción",
        "expected_decision": "absorb",
        "defense_category": "forbidden_diagnostic_claim",
        "responsible_limit": "educational_experimental_not_clinical",
    }

    prediction = ml_baseline.predict_decision(row, train_rows)

    assert prediction["nearest_train_id"] == "nearest_by_text"
    assert prediction["predicted_decision"] == "absorb"


def test_ml_baseline_default_uses_embedded_fixture_when_default_splits_are_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(ml_baseline, "TRAIN_PATH", tmp_path / "missing_train.jsonl")
    monkeypatch.setattr(ml_baseline, "EVAL_PATH", tmp_path / "missing_eval.jsonl")

    report = ml_baseline.build_report()

    assert report["status"] == "attention"
    assert report["using_embedded_fixture"] is True
    assert report["sanity_check_only"] is True
    assert report["training_allowed"] is False
    assert report["train_count"] > report["eval_count"] > 0
    assert report["errors"] == []
    assert any("fixture sintético embebido" in warning for warning in report["warnings"])


def test_makefile_has_ml_baseline_target():
    text = Path("Makefile").read_text(encoding="utf-8")

    assert "sne-ml-baseline:" in text
    assert "scripts/run_sne_eco_ml_baseline.py" in text
