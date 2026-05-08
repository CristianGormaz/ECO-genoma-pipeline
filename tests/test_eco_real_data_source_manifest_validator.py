import subprocess
from pathlib import Path


def test_eco_real_data_source_manifest_validator_passes_contract():
    root = Path(__file__).resolve().parents[1]
    script = root / "scripts" / "validate_eco_real_data_source_manifest.py"
    doc = root / "docs" / "architecture" / "eco-real-data-source-manifest-validator.md"
    readme = root / "docs" / "architecture" / "README.md"

    assert script.exists()
    assert doc.exists()

    result = subprocess.run(["make", "eco-validate-real-data-source-manifest"], cwd=root, text=True, capture_output=True, check=False)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Estado: passed" in result.stdout
    assert "Schema validado:" in result.stdout
    assert "Manifiestos candidatos:" in result.stdout
    assert "sin datos sensibles" in result.stdout

    doc_text = doc.read_text(encoding="utf-8")
    readme_text = readme.read_text(encoding="utf-8")
    assert "no ingiere datos reales" in doc_text
    assert "no entrena modelos" in doc_text
    assert "eco-real-data-source-manifest-validator.md" in readme_text
