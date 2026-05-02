from scripts.run_sne_eco_neurogastro_context_report import (
    build_neurogastro_context_report,
    to_markdown,
)


def _state_payload(rows):
    return {
        "scenario_set": "test",
        "rows": rows,
    }


def test_neurogastro_context_report_reads_stable_state_without_modifying_core():
    payload = build_neurogastro_context_report(
        state_payload=_state_payload(
            [
                {
                    "source": "valid_sequence",
                    "state_before": "stable",
                    "state_after": "stable",
                    "final_decision": "absorbed",
                    "defense_category": "none",
                    "motility_action": "advance",
                    "microbiota_seen_count": 0,
                    "immune_load_after": 0.0,
                    "quarantine_ratio_after": 0.0,
                    "recurrence_ratio_after": 0.0,
                }
            ]
        ),
        observability_payload={
            "status": "green",
            "confused_routes": 0,
            "confused_recurrence_rows": 0,
            "default_state_confused_routes": 0,
        },
    )

    assert payload["status"] == "stable"
    assert payload["metrics"]["rows_evaluated"] == 1
    assert payload["metrics"]["state_after_counts"] == {"stable": 1}
    assert payload["stability_locks"]["stable_dataset_modified"] is False
    assert payload["stability_locks"]["baseline_modified"] is False
    assert payload["stability_locks"]["rules_modified"] is False
    assert payload["stability_locks"]["report_only"] is True
    assert payload["claim_boundaries"]["clinical_diagnosis"] is False
    assert payload["claim_boundaries"]["bioinspired_architecture"] is True


def test_neurogastro_context_report_escalates_watch_and_attention():
    watch_payload = build_neurogastro_context_report(
        state_payload=_state_payload(
            [
                {
                    "source": "short_sequence",
                    "state_before": "stable",
                    "state_after": "watch",
                    "final_decision": "quarantined",
                    "defense_category": "low_information",
                    "motility_action": "hold",
                }
            ]
        ),
        observability_payload={"status": "green"},
    )
    attention_payload = build_neurogastro_context_report(
        state_payload=_state_payload(
            [
                {
                    "source": "invalid_sequence",
                    "state_before": "watch",
                    "state_after": "attention",
                    "final_decision": "rejected",
                    "defense_category": "invalid_payload",
                    "motility_action": "reject",
                }
            ]
        ),
        observability_payload={"status": "green"},
    )

    assert watch_payload["status"] == "watch"
    assert "vigilancia" in watch_payload["ux_reading"]["state"]
    assert attention_payload["status"] == "attention"
    assert "auditar" in attention_payload["ux_reading"]["suggested_action"]


def test_neurogastro_context_report_markdown_is_safe_and_explainable():
    payload = build_neurogastro_context_report(
        state_payload=_state_payload(
            [
                {
                    "source": "valid_sequence",
                    "state_before": "stable",
                    "state_after": "stable",
                    "final_decision": "absorbed",
                    "defense_category": "none",
                    "motility_action": "advance",
                }
            ]
        ),
        observability_payload={
            "status": "green",
            "confused_routes": 0,
            "confused_recurrence_rows": 0,
            "default_state_confused_routes": 0,
        },
    )

    markdown = to_markdown(payload)

    assert "Reporte neurogastrocomputacional S.N.E.-E.C.O." in markdown
    assert "Lectura UX conversacional" in markdown
    assert "interocepción" in markdown
    assert "señal aferente" in markdown
    assert "Dataset estable modificado: `False`" in markdown
    assert "Baseline modificado: `False`" in markdown
    assert "no diagnostica enfermedades" in markdown
    assert "no reemplaza evaluación médica" in markdown
