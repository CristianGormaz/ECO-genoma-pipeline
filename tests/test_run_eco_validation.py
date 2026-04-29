import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATION_SCRIPT = ROOT / "scripts" / "run_eco_validation.py"


def test_run_eco_validation_script_succeeds():
    """La validación oficial debe ejecutarse como comando real y terminar OK."""
    result = subprocess.run(
        [sys.executable, str(VALIDATION_SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "E.C.O. VALIDATION REPORT" in result.stdout
    assert "Paquetes procesados: 2" in result.stdout
    assert "Aceptados: 1" in result.stdout
    assert "Rechazados: 1" in result.stdout
    assert "Absorbidos: 1" in result.stdout
    assert "OK: metabolismo informacional mínimo funcionando." in result.stdout
