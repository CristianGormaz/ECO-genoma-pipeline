from scripts.run_sne_eco_empirical_seed_report import build_report, to_markdown


def test_empirical_seed_report_builds_green_report():
    report = build_report()

    assert report["status"] == "green"
    assert report["row_count"] >= 6
    assert report["errors"] == []


def test_empirical_seed_report_has_expected_decision_distribution():
    report = build_report()
    decisions = report["counts"]["expected_decision"]

    assert decisions["absorb"] >= 1
    assert decisions["reject"] >= 1
    assert decisions["quarantine"] >= 1
    assert decisions["discard_duplicate"] >= 1


def test_empirical_seed_report_detects_restricted_claim_rows():
    report = build_report()

    assert "seed_claim_limit_001" in report["restricted_claim_rows"]
    assert "seed_consciousness_limit_001" in report["restricted_claim_rows"]


def test_empirical_seed_report_keeps_responsible_limit():
    report = build_report()
    markdown = to_markdown(report)

    assert "no tiene uso clínico" in report["responsible_limit"]
    assert "no modela conciencia humana" in report["responsible_limit"]
    assert "Reporte de calidad empírica" in markdown
