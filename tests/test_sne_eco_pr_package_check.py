from pathlib import Path

from scripts.run_sne_eco_pr_package_check import build_report, to_markdown


def test_pr_package_doc_exists():
    assert Path("docs/sne-eco-pr-package.md").exists()


def test_pr_package_check_builds_green_report():
    report = build_report()

    assert report["status"] == "green"
    assert report["errors"] == []
    assert report["missing_phrases"] == []


def test_pr_package_declares_responsible_limits():
    text = Path("docs/sne-eco-pr-package.md").read_text(encoding="utf-8")

    assert "No ingiere datos reales" in text
    assert "No diagnostica personas" in text
    assert "No tiene uso clínico aplicado" in text
    assert "No realiza inferencias forenses aplicadas" in text
    assert "No afirma conciencia humana real" in text
    assert "No recalibra umbrales estables" in text
    assert "No modifica baseline estable sin comparación" in text


def test_pr_package_declares_data_classes():
    text = Path("docs/sne-eco-pr-package.md").read_text(encoding="utf-8")

    assert "Permitido" in text
    assert "Condicional" in text
    assert "Bloqueado" in text


def test_pr_package_markdown_mentions_no_training_or_threshold_changes():
    report = build_report()
    markdown = to_markdown(report)

    assert "No ejecuta entrenamiento" in markdown
    assert "No modifica reglas, baseline ni umbrales" in markdown


def test_makefile_has_pr_package_target():
    text = Path("Makefile").read_text(encoding="utf-8")

    assert "sne-pr-package-check:" in text
    assert "scripts/run_sne_eco_pr_package_check.py" in text
