import json
import importlib.util
import pytest
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_report_module():
    module_path = ROOT / "scripts" / "run_eco_adaptive_dataset_report.py"
    spec = importlib.util.spec_from_file_location("run_eco_adaptive_dataset_report", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _valid_limits():
    return {
        "synthetic_only": True,
        "no_real_data": True,
        "no_sensitive_data": True,
        "no_private_genetic_data": True,
        "no_training": True,
        "no_baseline_change": True,
        "no_threshold_recalibration": True,
        "no_biomedical_claims": True,
    }


def _valid_markdown():
    return """
# Ejemplo sintético de dataset adaptativo E.C.O.

- No contiene datos reales.
- No contiene datos sensibles.
- No contiene datos genéticos privados.
- No entrena modelos.
- No modifica baseline.
- No recalibra umbrales.
- No genera afirmaciones biomédicas aplicadas.
"""



def test_adaptive_dataset_report_script_generates_outputs():
    subprocess.run(
        [sys.executable, "scripts/run_eco_adaptive_dataset_report.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    output_json = ROOT / "results" / "eco_adaptive_dataset_report.json"
    output_md = ROOT / "results" / "eco_adaptive_dataset_report.md"

    assert output_json.exists()
    assert output_md.exists()

    report = json.loads(output_json.read_text(encoding="utf-8"))
    markdown = output_md.read_text(encoding="utf-8")

    assert report["status"] == "passed"
    assert report["classification"] == "permitted"
    assert report["synthetic_records"] >= 1
    assert "sin datos reales" in report["responsible_limits"]
    assert "sin entrenamiento" in report["responsible_limits"]
    assert "sin modificación de baseline" in report["responsible_limits"]
    assert "sin recalibración de umbrales" in report["responsible_limits"]
    assert "sin datos reales" in report["source_responsible_limits"]
    assert "sin datos reales" in report["declared_responsible_limits"]
    assert "sin entrenamiento" in report["declared_responsible_limits"]
    assert "sin modificación de baseline" in report["declared_responsible_limits"]
    assert "sin recalibración de umbrales" in report["declared_responsible_limits"]
    assert "E.C.O. adaptive dataset operational report" in markdown
    assert "Límites responsables detectados en fuente" in markdown
    assert "Límites responsables declarados en Markdown" in markdown


def test_makefile_exposes_adaptive_dataset_report_target():
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")

    assert "eco-adaptive-dataset-report:" in makefile
    assert "scripts/run_eco_adaptive_dataset_report.py" in makefile
    assert "eco_adaptive_dataset_report.json" in makefile


def test_adaptive_dataset_report_rejects_missing_markdown(tmp_path, monkeypatch):
    module = _load_report_module()

    source_json = tmp_path / "example.json"
    source_json.write_text(json.dumps({
        "classification": "permitido",
        "limits": _valid_limits(),
        "records": [{"record_id": "synthetic-1"}],
    }), encoding="utf-8")

    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "SOURCE_JSON", source_json)
    monkeypatch.setattr(module, "SOURCE_MD", tmp_path / "missing.md")

    with pytest.raises(SystemExit, match="no existe"):
        module.build_report()


def test_adaptive_dataset_report_rejects_empty_records(tmp_path, monkeypatch):
    module = _load_report_module()

    source_json = tmp_path / "example.json"
    source_md = tmp_path / "example.md"

    source_json.write_text(json.dumps({
        "classification": "permitido",
        "limits": _valid_limits(),
        "records": [],
    }), encoding="utf-8")
    source_md.write_text(_valid_markdown(), encoding="utf-8")

    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "SOURCE_JSON", source_json)
    monkeypatch.setattr(module, "SOURCE_MD", source_md)

    with pytest.raises(SystemExit, match="registros"):
        module.build_report()


def test_adaptive_dataset_report_rejects_non_permitted_classification(tmp_path, monkeypatch):
    module = _load_report_module()

    source_json = tmp_path / "example.json"
    source_md = tmp_path / "example.md"

    source_json.write_text(json.dumps({
        "classification": "bloqueado",
        "limits": _valid_limits(),
        "records": [{"record_id": "synthetic-1"}],
    }), encoding="utf-8")
    source_md.write_text(_valid_markdown(), encoding="utf-8")

    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "SOURCE_JSON", source_json)
    monkeypatch.setattr(module, "SOURCE_MD", source_md)

    with pytest.raises(SystemExit, match="clasificación"):
        module.build_report()


def test_adaptive_dataset_report_detects_markdown_limit_aliases():
    module = _load_report_module()

    declared = module._detect_declared_limits(_valid_markdown())

    assert declared == module.RESPONSIBLE_LIMITS

