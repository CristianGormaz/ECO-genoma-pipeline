import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENTERIC_DEMO_SCRIPT = ROOT / "scripts" / "run_eco_enteric_demo.py"


def test_run_eco_enteric_demo_script_succeeds():
    """La demo entérica debe ejecutarse como comando real y terminar OK."""
    result = subprocess.run(
        [sys.executable, str(ENTERIC_DEMO_SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "E.C.O. ENTERIC SYSTEM REPORT" in result.stdout
    assert "Acción: absorb" in result.stdout
    assert "Acción: reject" in result.stdout
    assert "Acción: quarantine" in result.stdout
    assert "Acción: discard_duplicate" in result.stdout
    assert "Paquetes procesados: 4" in result.stdout
    assert "Absorbidos: 1" in result.stdout
    assert "Cuarentena: 1" in result.stdout
    assert "Descartados: 2" in result.stdout
    assert "Duplicados: 1" in result.stdout
    assert "OK: sistema entérico integrado funcionando." in result.stdout
