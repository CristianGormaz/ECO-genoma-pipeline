from pathlib import Path


def test_portfolio_demo_runs_v1_1_comparison():
    text = Path("Makefile").read_text(encoding="utf-8")
    assert "sne-portfolio-demo:" in text
    block = text.split("sne-portfolio-demo:", 1)[1].split("\n\n", 1)[0]
    assert "$(MAKE) sne-neurogastro-pipeline" in block
    assert "$(MAKE) sne-compare-v1-1" in block
    assert "$(MAKE) sne-portfolio-check" in block
