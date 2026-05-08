from pathlib import Path


def test_eco_operational_block_bitacora_documents_pr_131_to_136():
    root = Path(__file__).resolve().parents[1]
    bitacora = root / "docs" / "architecture" / "eco-operational-block-bitacora-131-136.md"
    readme = root / "docs" / "architecture" / "README.md"
    assert bitacora.exists()
    text = bitacora.read_text(encoding="utf-8")
    readme_text = readme.read_text(encoding="utf-8")
    for marker in ("#131", "#132", "#133", "#134", "#135", "#136"):
        assert marker in text
    assert "schema operacional" in text
    assert "reporte operacional" in text
    assert "No usa datos sensibles" in text
    assert "no recalibra umbrales" in text
    assert "eco-operational-block-bitacora-131-136.md" in readme_text
