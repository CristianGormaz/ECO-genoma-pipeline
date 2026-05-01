import json
import subprocess
import sys
from pathlib import Path


def test_run_eco_adaptive_router_predict_exports_reports(tmp_path: Path):
    output_json = tmp_path / "adaptive_prediction.json"
    output_md = tmp_path / "adaptive_prediction.md"
    output_html = tmp_path / "adaptive_prediction.html"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/run_eco_adaptive_router_predict.py",
            "--sequence",
            "ACGTCCAATGGTATAAAGGCGGGCGGAATAAAGTAC",
            "--sequence-id",
            "pytest_adaptive_router",
            "--threshold",
            "0.20",
            "--embedding-k",
            "4",
            "--dimensions",
            "128",
            "--output-json",
            str(output_json),
            "--output-md",
            str(output_md),
            "--output-html",
            str(output_html),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "Estado: OK, predicción adaptativa generada." in result.stdout
    assert "Reflejo entérico:" in result.stdout
    assert output_json.exists()
    assert output_md.exists()
    assert output_html.exists()

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert payload["sequence_id"] == "pytest_adaptive_router"
    assert payload["selected_route"] in {"baseline_v3", "embedding_semireal"}
    assert payload["final_prediction"] in {"regulatory", "non_regulatory"}
    assert "baseline_v3" in payload
    assert "embedding_semireal" in payload
    assert "sensory_profile" in payload
    assert payload["sensory_profile"]["length"] == 36
    assert "enteric_reflex" in payload
    assert payload["enteric_reflex"]["reflex_name"] in {
        "reflejo_explicable_rapido",
        "reflejo_vectorial_de_derivacion",
    }
    assert payload["enteric_reflex"]["caution_level"] in {"normal", "media", "alta"}
    assert "no diagnostico clinico" in payload["limits"]

    markdown = output_md.read_text(encoding="utf-8")
    assert "# E.C.O. - Predicción con router adaptativo" in markdown
    assert "## Sensado entérico" in markdown
    assert "## Decisión adaptativa" in markdown
    assert "## Reflejo entérico del router" in markdown
