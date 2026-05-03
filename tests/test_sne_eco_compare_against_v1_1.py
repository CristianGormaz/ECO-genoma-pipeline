from scripts.run_sne_eco_compare_against_v1_1 import build_comparison, to_markdown


def test_compare_against_v1_1_builds_report():
    report = build_comparison()

    assert report["baseline"] == "sne-eco-v1.1"
    assert report["status"] in {"green", "attention"}
    assert "confused_routes" in report["current"]
    assert "regressions" in report


def test_compare_against_v1_1_keeps_responsible_limit():
    report = build_comparison()

    assert "no tiene uso clínico" in report["responsible_limit"]
    assert "no modifica el baseline" in report["responsible_limit"]
    assert "conciencia humana" in report["responsible_limit"]


def test_compare_against_v1_1_markdown_mentions_baseline():
    report = build_comparison()
    markdown = to_markdown(report)

    assert "baseline v1.1" in markdown
    assert "Regresiones detectadas" in markdown
