from scripts.run_sne_eco_stable_admission_plan import build_stable_admission_plan, to_markdown


def sample_policy_payload():
    return {
        "policy_name": "sne_eco_external_evidence_policy",
        "rows": [
            {
                "source": "external_min_valid_boundary",
                "category": "external_context_boundary",
                "policy_decision": "document_boundary",
                "dataset_action": "candidate_for_future_stable_scenario",
                "risk": "medium",
            },
            {
                "source": "external_short_borderline",
                "category": "expected_defensive_tension",
                "policy_decision": "observe_threshold_candidate",
                "dataset_action": "candidate_for_threshold_review",
                "risk": "medium",
            },
            {
                "source": "external_invalid_symbolic",
                "category": "expected_invalid_payload_tension",
                "policy_decision": "exclude_until_policy_defined",
                "dataset_action": "keep_out_of_stable_dataset",
                "risk": "medium",
            },
            {
                "source": "external_recurrent_gc_dense",
                "category": "expected_external_alignment",
                "policy_decision": "observe_as_control",
                "dataset_action": "do_not_train_yet",
                "risk": "low",
            },
        ],
    }


def test_stable_admission_plan_keeps_admission_locked_and_stability_safe():
    plan = build_stable_admission_plan(sample_policy_payload())

    assert plan["status"] == "yellow"
    assert plan["admission_locked"] is True
    assert plan["stable_dataset_modified"] is False
    assert plan["baseline_modified"] is False
    assert plan["external_rows"] == 4


def test_stable_admission_plan_maps_dataset_actions_to_admission_decisions():
    plan = build_stable_admission_plan(sample_policy_payload())
    decisions_by_source = {row["source"]: row["admission_decision"] for row in plan["rows"]}

    assert decisions_by_source["external_min_valid_boundary"] == "admit_later"
    assert decisions_by_source["external_short_borderline"] == "hold_for_threshold_review"
    assert decisions_by_source["external_invalid_symbolic"] == "exclude_until_policy_defined"
    assert decisions_by_source["external_recurrent_gc_dense"] == "keep_as_observation_control"


def test_stable_admission_plan_blocks_high_risk_or_unknown_actions():
    plan = build_stable_admission_plan(
        {
            "policy_name": "sne_eco_external_evidence_policy",
            "rows": [
                {
                    "source": "external_unknown_default",
                    "category": "coverage_gap_high_priority",
                    "policy_decision": "block_until_reviewed",
                    "dataset_action": "unknown_dataset_action",
                    "risk": "high",
                }
            ],
        }
    )

    assert plan["status"] == "red"
    assert plan["manual_review_rows"] == 1
    assert plan["rows"][0]["admission_decision"] == "manual_review_required"


def test_stable_admission_plan_markdown_explains_admission_without_training():
    plan = build_stable_admission_plan(sample_policy_payload())
    markdown = to_markdown(plan)

    assert "Plan de admisión estable S.N.E.-E.C.O." in markdown
    assert "Aduana de admisión" in markdown
    assert "Dataset estable modificado: `False`" in markdown
    assert "Baseline modificado: `False`" in markdown
    assert "no incorpora todavía escenarios externos" in markdown
