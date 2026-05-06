import json
import subprocess
import sys
from pathlib import Path


DOC = Path("docs/architecture/eco-synthetic-data-contract.md")
SCRIPT = Path("scripts/run_eco_minimal_simulation.py")
RESULT_JSON = Path("results/eco_minimal_simulation_demo.json")


def test_synthetic_data_contract_document_exists_and_sets_limits():
    text = DOC.read_text(encoding="utf-8")

    assert "Contrato de datos sintéticos E.C.O." in text
    assert "Estudiar datos" in text
    assert "Simular comportamiento" in text
    assert "Entrenar modelos" in text
    assert "Evaluar resultados" in text
    assert "Generar hipótesis" in text
    assert "Hacer afirmaciones aplicadas" in text
    assert "synthetic_only" in text
    assert "No debe entrenar modelos" in text
    assert "No debe usar datos sensibles" in text
    assert "No debe modificar baseline" in text
    assert "No debe recalibrar umbrales" in text
    assert "No debe convertir metáforas simbólicas en conclusiones científicas" in text


def test_minimal_simulation_output_matches_synthetic_contract():
    result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)

    assert result.returncode == 0
    assert RESULT_JSON.exists()

    data = json.loads(RESULT_JSON.read_text(encoding="utf-8"))
    summary = data["summary"]

    assert data["title"]
    assert data["scope"]
    assert isinstance(data["trace"], list)
    assert data["trace"]
    assert isinstance(data["limits"], list)

    assert summary["classification"] == "allowed"
    assert summary["data_policy"] == "synthetic_only"
    assert summary["training"] is False
    assert summary["sensitive_data"] is False
    assert summary["baseline_changed"] is False
    assert summary["threshold_recalibrated"] is False
    assert summary["ticks"] == len(data["trace"])
    assert summary["final_state"] == data["trace"][-1]

    required_keys = {"tick", "nutrient", "signal", "waste", "stability", "action"}
    for item in data["trace"]:
        assert required_keys.issubset(item)
        assert isinstance(item["tick"], int)
        assert item["tick"] >= 1
        for key in ["nutrient", "signal", "waste", "stability"]:
            assert isinstance(item[key], int)
            assert item[key] >= 0
        assert item["action"] in {"digest", "rest"}
