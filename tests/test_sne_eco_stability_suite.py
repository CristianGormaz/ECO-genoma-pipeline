import json
import subprocess
import sys

from src.eco_core import (
    EXTENDED_TRANSITION_PACKETS,
    analyze_confused_routes,
    build_adaptive_state_rows,
    evaluate_state_transition_holdout,
)


def test_sne_eco_extended_holdout_has_no_confused_routes():
    rows = build_adaptive_state_rows(EXTENDED_TRANSITION_PACKETS)
    report = analyze_confused_routes(rows)

    assert report.test_rows >= 6
    assert report.confused_routes == ()
    assert report.suggested_focus == ()
    assert "no representa desempeño general" in report.responsible_limit


def test_sne_eco_holdout_avoids_default_state_and_incorrect_predictions():
    rows = build_adaptive_state_rows(EXTENDED_TRANSITION_PACKETS)
    evaluation = evaluate_state_transition_holdout(rows)

    assert evaluation.test_rows >= 6
    assert all(prediction.matched_rule != "default_state" for prediction in evaluation.predictions)
    assert all(prediction.correct for prediction in evaluation.predictions)
    assert evaluation.accuracy_holdout == 1.0


def test_sne_eco_recurrence_audit_stays_clean():
    result = subprocess.run(
        [sys.executable, "scripts/run_sne_eco_recurrence_audit.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "OK: auditoría de recurrencia S.N.E.-E.C.O. generada." in result.stdout

    with open("results/sne_eco_recurrence_audit.json", encoding="utf-8") as handle:
        payload = json.load(handle)

    assert payload["recurrence_rows"] >= 7
    assert payload["confused_recurrence_rows"] == 0
    assert all(not row["is_confused"] for row in payload["rows"])
