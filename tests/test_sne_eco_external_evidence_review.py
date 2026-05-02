from scripts.run_sne_eco_external_evidence_review import (
    build_evidence_review,
    classify_row,
    to_markdown,
)


def test_external_evidence_review_classifies_expected_patterns():
    rows = [
        {
            "source": "external_absorb",
            "observed_state": "watch",
            "predicted_state": "stable",
            "matched_rule": "digestive_key",
            "final_decision": "absorb",
            "defense": "none/none",
            "correct": False,
        },
        {
            "source": "external_quarantine",
            "observed_state": "watch",
            "predicted_state": "attention",
            "matched_rule": "digestive_key",
            "final_decision": "quarantine",
            "defense": "ambiguous_payload/medium",
            "correct": False,
        },
        {
            "source": "external_reject",
            "observed_state": "watch",
            "predicted_state": "attention",
            "matched_rule": "digestive_key",
            "final_decision": "reject",
            "defense": "invalid_payload/high",
            "correct": False,
        },
        {
            "source": "external_recurrent",
            "observed_state": "watch",
            "predicted_state": "watch",
            "matched_rule": "feature_key",
            "final_decision": "discard_duplicate",
            "defense": "redundant_payload/low",
            "correct": True,
        },
    ]

    categories = [classify_row(row)["category"] for row in rows]

    assert categories == [
        "external_context_boundary",
        "expected_defensive_tension",
        "expected_invalid_payload_tension",
        "expected_external_alignment",
    ]


def test_external_evidence_review_reports_yellow_without_default_state():
    probe_payload = {
        "probe_name": "sne_eco_external_scenario_probe",
        "rows": [
            {
                "source": "external_absorb",
                "observed_state": "watch",
                "predicted_state": "stable",
                "matched_rule": "digestive_key",
                "final_decision": "absorb",
                "defense": "none/none",
                "correct": False,
            },
            {
                "source": "external_recurrent",
                "observed_state": "watch",
                "predicted_state": "watch",
                "matched_rule": "feature_key",
                "final_decision": "discard_duplicate",
                "defense": "redundant_payload/low",
                "correct": True,
            },
        ],
    }

    review = build_evidence_review(probe_payload)

    assert review["status"] == "yellow"
    assert review["external_differences"] == 1
    assert review["default_state_rows"] == 0
    assert review["category_counts"]["external_context_boundary"] == 1
    assert review["category_counts"]["expected_external_alignment"] == 1


def test_external_evidence_review_reports_red_with_default_state():
    probe_payload = {
        "probe_name": "sne_eco_external_scenario_probe",
        "rows": [
            {
                "source": "external_unknown",
                "observed_state": "watch",
                "predicted_state": "stable",
                "matched_rule": "default_state",
                "final_decision": "absorb",
                "defense": "none/none",
                "correct": False,
            }
        ],
    }

    review = build_evidence_review(probe_payload)

    assert review["status"] == "red"
    assert review["default_state_rows"] == 1
    assert review["category_counts"]["coverage_gap_high_priority"] == 1


def test_external_evidence_review_markdown_is_explainable():
    review = build_evidence_review(
        {
            "probe_name": "sne_eco_external_scenario_probe",
            "rows": [
                {
                    "source": "external_recurrent",
                    "observed_state": "watch",
                    "predicted_state": "watch",
                    "matched_rule": "feature_key",
                    "final_decision": "discard_duplicate",
                    "defense": "redundant_payload/low",
                    "correct": True,
                }
            ],
        }
    )
    markdown = to_markdown(review)

    assert "Revisión de evidencia externa S.N.E.-E.C.O." in markdown
    assert "Matriz de revisión" in markdown
    assert "Las diferencias externas no invalidan RC1" in markdown
    assert "expected_external_alignment" in markdown
