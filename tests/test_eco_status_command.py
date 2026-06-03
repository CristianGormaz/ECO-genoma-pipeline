import importlib.util
import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/run_eco_status.py")
MAKEFILE = Path("Makefile")


def load_eco_status_module():
    spec = importlib.util.spec_from_file_location("run_eco_status", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_eco_status_script_exists():
    assert SCRIPT.exists()


def test_eco_status_outputs_operational_state():
    result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)
    assert result.returncode == 0
    assert "E.C.O. status operativo" in result.stdout
    assert "Rama actual:" in result.stdout
    assert "Árbol limpio:" in result.stdout
    assert "Sincronizado con origin/main:" in result.stdout
    assert "Límite operativo" in result.stdout


def test_compute_operational_state_is_green_only_when_clean_main_and_synced():
    module = load_eco_status_module()

    assert module.compute_operational_state(clean=True, on_main=True, synced=True) == "green"
    assert module.compute_operational_state(clean=True, on_main=False, synced=True) == "attention"
    assert module.compute_operational_state(clean=True, on_main=True, synced=False) == "attention"
    assert module.compute_operational_state(clean=False, on_main=True, synced=True) == "attention"


def test_eco_status_guides_new_sprint_from_clean_main_via_branch_creation():
    module = load_eco_status_module()
    reading = module.build_quick_reading(clean=True, on_main=True, synced=True)
    assert "Semáforo verde: puedes detenerte aquí." in reading
    assert "crea una rama nueva desde main antes de modificar archivos" in reading


def test_eco_status_warns_when_clean_but_not_on_main():
    module = load_eco_status_module()

    reading = module.build_quick_reading(clean=True, on_main=False, synced=True)

    assert "no estás en main" in reading
    assert "Cierra o integra la rama" in reading


def test_eco_status_warns_when_main_is_not_synced_with_origin():
    module = load_eco_status_module()

    reading = module.build_quick_reading(clean=True, on_main=True, synced=False)

    assert "HEAD no coincide con origin/main" in reading
    assert "Sincroniza antes de declarar estado green" in reading


def test_eco_status_does_not_modify_git_state():
    before = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True,
        text=True,
        check=False,
    )
    result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True, check=False)
    after = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert before.stdout == after.stdout


def test_eco_status_make_target_exists():
    text = MAKEFILE.read_text(encoding="utf-8")
    assert ".PHONY: eco-status" in text
    assert "eco-status:" in text
    assert "scripts/run_eco_status.py" in text
