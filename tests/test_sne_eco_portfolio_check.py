from scripts.run_sne_eco_portfolio_check import to_markdown


def sample_payload(status="green"):
    return {
        "status": status,
        "required_files": [
            {"path": "README.md", "exists": True, "size_bytes": 100},
            {"path": "docs/sne-eco-portfolio-index.md", "exists": True, "size_bytes": 100},
            {"path": "docs/case-study-sne-eco-neurogastro-pipeline.md", "exists": True, "size_bytes": 100},
        ],
        "readme_checks": [
            {"text": "Para lectura rapida de portafolio S.N.E.-E.C.O.", "present": True},
            {"text": "docs/sne-eco-portfolio-index.md", "present": True},
            {"text": "docs/case-study-sne-eco-neurogastro-pipeline.md", "present": True},
        ],
        "recommended_reports": [
            {"path": "results/sne_eco_neurogastro_pipeline_summary.json", "exists": True, "size_bytes": 100},
            {"path": "results/sne_eco_compare_against_rc1.json", "exists": True, "size_bytes": 100},
        ],
        "responsible_limit": "Chequeo operativo de materiales de portafolio.",
    }


def test_portfolio_check_markdown_green():
    markdown = to_markdown(sample_payload("green"))

    assert "Chequeo de portafolio S.N.E.-E.C.O." in markdown
    assert "Estado: 🟢 `green`" in markdown
    assert "Portafolio técnico completo" in markdown
    assert "README.md" in markdown
    assert "docs/sne-eco-portfolio-index.md" in markdown


def test_portfolio_check_markdown_yellow_suggests_pipeline():
    markdown = to_markdown(sample_payload("yellow"))

    assert "Estado: 🟡 `yellow`" in markdown
    assert "make sne-neurogastro-pipeline" in markdown


def test_portfolio_check_markdown_red_suggests_review():
    markdown = to_markdown(sample_payload("red"))

    assert "Estado: 🔴 `red`" in markdown
    assert "Revisar README y docs" in markdown
