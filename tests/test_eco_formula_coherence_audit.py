from scripts.run_eco_formula_coherence_audit import build_report, to_markdown


def test_formula_coherence_audit_report_contract():
    report = build_report()

    assert report["status"] in {"passed", "attention"}
    assert report["scope"]["kind"] == "technical_coherence_synthetic_audit"
    assert report["scope"]["scientific_claims"] == "not_evaluated"
    assert report["scope"]["biomedical_claims"] == "not_applicable"
    assert report["invariants_evaluated"] >= 8
    assert report["invariants_evaluated"] == len(report["invariants"])

    invariant_ids = {item["invariant_id"] for item in report["invariants"]}
    expected_ids = {
        "laos_score_range",
        "laos_risk_friction_monotonicity",
        "laos_coherence_signal_monotonicity",
        "reject_quarantine_not_absorption_projection",
        "batch_absorb_is_absorption",
        "fallback_effective_is_reported",
        "public_guard_not_real_data_authorization",
        "responsible_limits_are_explicit",
    }
    assert expected_ids.issubset(invariant_ids)


def test_formula_coherence_audit_passes_current_synthetic_baseline():
    report = build_report()
    assert report["status"] == "passed"
    assert report["invariants_failed"] == 0
    assert report["failed_invariant_ids"] == []


def test_formula_coherence_audit_markdown_mentions_limits_and_scope():
    report = build_report()
    markdown = to_markdown(report).lower()

    assert "coherencia técnica interna" in markdown
    assert "afirmaciones científicas" in markdown
    assert "sin datos reales" in markdown
    assert "sin entrenamiento" in markdown
    assert "sin modificación de baseline" in markdown
    assert "sin recalibración de umbrales" in markdown
