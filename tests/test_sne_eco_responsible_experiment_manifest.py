from pathlib import Path

from scripts.run_sne_eco_responsible_experiment_manifest import (
    build_manifest,
    to_markdown,
)


def test_responsible_experiment_manifest_builds_green_report():
    manifest = build_manifest()

    assert manifest["status"] == "green"
    assert manifest["evaluation_allowed"] is True
    assert manifest["decision"] == "allowed_experimental_evaluation"


def test_responsible_experiment_manifest_declares_action_scope():
    manifest = build_manifest()
    scope = manifest["action_scope"]

    assert scope["study_data"] is True
    assert scope["evaluate_results"] is True
    assert scope["train_models"] is False
    assert scope["make_applied_claims"] is False
    assert scope["modify_stable_baseline"] is False
    assert scope["recalibrate_thresholds"] is False


def test_responsible_experiment_manifest_classifies_sensitive_data():
    manifest = build_manifest()
    data = manifest["data_classification"]

    assert "synthetic_examples" in data["allowed"]
    assert "anonymized_or_licensed_research_datasets" in data["conditional"]
    assert "personal_medical_records" in data["blocked"]
    assert "human_consciousness_detection_claims" in data["blocked"]


def test_responsible_experiment_manifest_references_evidence_reports():
    manifest = build_manifest()

    assert "results/sne_eco_governed_ml_evaluation_gate.md" in manifest["input_reports"]
    assert "results/sne_eco_sensitive_governance_summary.md" in manifest["input_reports"]
    assert "results/sne_eco_ml_challenge_eval_report.md" in manifest["input_reports"]


def test_responsible_experiment_manifest_keeps_responsible_limits():
    manifest = build_manifest()
    markdown = to_markdown(manifest)

    assert "no ingiere datos reales" in markdown
    assert "no entrena modelos nuevos" in markdown
    assert "no diagnostica" in markdown
    assert "no tiene uso clínico aplicado" in markdown
    assert "no realiza inferencias forenses" in markdown
    assert "no afirma conciencia humana real" in markdown
    assert "no recalibra umbrales" in markdown
    assert "no modifica baseline estable" in markdown


def test_makefile_has_responsible_experiment_manifest_target():
    text = Path("Makefile").read_text(encoding="utf-8")

    assert "sne-responsible-experiment-manifest:" in text
    assert "scripts/run_sne_eco_responsible_experiment_manifest.py" in text
