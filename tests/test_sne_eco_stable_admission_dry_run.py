from scripts.run_sne_eco_stable_admission_dry_run import build_dry_run, to_markdown


def test_stable_admission_dry_run_never_admits_now():
    payload = {
        "rows": [
            {
                "source": "external_a",
                "admission_decision": "admit_later",
                "gate": "requires_repeated_external_observation",
                "risk": "medium",
            },
            {
                "source": "external_b",
                "admission_decision": "hold_for_threshold_review",
                "gate": "requires_threshold_review",
                "risk": "medium",
            },
            {
                "source": "external_c",
                "admission_decision": "keep_as_observation_control",
                "gate": "control_only",
                "risk": "low",
            },
        ]
    }

    result = build_dry_run(payload)

    assert result["metrics"]["external_rows_evaluated"] == 3
    assert result["metrics"]["simulated_admissions_now"] == 0
    assert result["stability_locks"]["stable_dataset_modified"] is False
    assert result["stability_locks"]["baseline_modified"] is False
    assert result["stability_locks"]["dry_run_only"] is True
    assert all(row["admission_allowed_now"] is False for row in result["rows"])


def test_stable_admission_dry_run_markdown_is_operational():
    result = build_dry_run(
        {
            "rows": [
                {
                    "source": "external_a",
                    "admission_decision": "admit_later",
                    "gate": "requires_repeated_external_observation",
                    "risk": "medium",
                }
            ]
        }
    )

    markdown = to_markdown(result)

    assert "Dry-run de admisión estable S.N.E.-E.C.O." in markdown
    assert "Dataset estable modificado: `False`" in markdown
    assert "Baseline modificado: `False`" in markdown
    assert "admission_allowed_now" in markdown
