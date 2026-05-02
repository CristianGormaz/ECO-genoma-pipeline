from scripts.run_sne_eco_external_evidence_policy import build_evidence_policy, to_markdown


def sample_review_payload():
    return {
        "review_name": "sne_eco_external_evidence_review",
        "rows": [
            {
                "source": "external_min_valid_boundary",
                "category": "external_context_boundary",
                "observed_state": "watch",
                "predicted_state": "stable",
            },
            {
                "source": "external_short_borderline",
                "category": "expected_defensive_tension",
                "observed_state": "watch",
                "predicted_state": "attention",
            },
            {
                "source": "external_invalid_symbolic",
                "category": "expected_invalid_payload_tension",
                "observed_state": "watch",
                "predicted_state": "attention",
            },
            {
                "source": "external_recurrent_gc_dense",
                "category": "expected_external_alignment",
                "observed_state": "watch",
                "predicted_state": "watch",
            },
        ],
    }


def test_external_evidence_policy_classifies_current_review_as_yellow_without_high_risk():
    policy = build_evidence_policy(sample_review_payload())

    assert policy["status"] == "yellow"
    assert policy["external_rows"] == 4
    assert policy["future_candidate_rows"] == 2
    assert policy["excluded_rows"] == 1
    assert policy["high_risk_rows"] == 0
    assert policy["risk_counts"] == {"medium": 3, "low": 1}


def test_external_evidence_policy_maps_categories_to_dataset_actions():
    policy = build_evidence_policy(sample_review_payload())
    actions_by_source = {row["source"]: row["dataset_action"] for row in policy["rows"]}

    assert actions_by_source["external_min_valid_boundary"] == "candidate_for_future_stable_scenario"
    assert actions_by_source["external_short_borderline"] == "candidate_for_threshold_review"
    assert actions_by_source["external_invalid_symbolic"] == "keep_out_of_stable_dataset"
    assert actions_by_source["external_recurrent_gc_dense"] == "do_not_train_yet"


def test_external_evidence_policy_detects_high_risk_default_state_category():
    review_payload = {
        "review_name": "sne_eco_external_evidence_review",
        "rows": [
            {
                "source": "external_unknown",
                "category": "coverage_gap_high_priority",
                "observed_state": "watch",
                "predicted_state": "stable",
            }
        ],
    }
    policy = build_evidence_policy(review_payload)

    assert policy["status"] == "red"
    assert policy["high_risk_rows"] == 1
    assert policy["rows"][0]["policy_decision"] == "block_until_reviewed"


def test_external_evidence_policy_markdown_is_explainable():
    policy = build_evidence_policy(sample_review_payload())
    markdown = to_markdown(policy)

    assert "Política de evidencia externa S.N.E.-E.C.O." in markdown
    assert "Candidatos futuros" in markdown
    assert "Exclusiones temporales" in markdown
    assert "no decide entrenar todavía" in markdown
