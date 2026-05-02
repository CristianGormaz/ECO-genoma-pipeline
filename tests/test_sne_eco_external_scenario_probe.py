from scripts.run_sne_eco_external_scenario_probe import build_external_probe, to_markdown


def test_external_scenario_probe_runs_without_changing_stable_baseline():
    payload = build_external_probe()

    assert payload["training_rows"] == 28
    assert payload["external_rows"] >= 8
    assert payload["status"] in {"green", "yellow", "red"}
    assert "no modifica dataset estable" in payload["responsible_limit"]
    assert all("source" in row for row in payload["rows"])
    assert all("matched_rule" in row for row in payload["rows"])


def test_external_scenario_probe_avoids_default_state_for_current_probe_set():
    payload = build_external_probe()

    assert payload["default_state_rows"] == 0
    assert all(row["matched_rule"] != "default_state" for row in payload["rows"])


def test_external_scenario_probe_markdown_is_explainable():
    payload = build_external_probe()
    markdown = to_markdown(payload)

    assert "Sonda de escenarios externos S.N.E.-E.C.O." in markdown
    assert "Expansión externa en modo observación" in markdown
    assert "Escenarios externos" in markdown
    assert "Una confusión externa no invalida RC1" in markdown
