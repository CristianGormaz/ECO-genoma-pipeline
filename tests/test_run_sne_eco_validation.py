import subprocess
import sys


def test_run_sne_eco_validation_script_outputs_integrated_report():
    result = subprocess.run(
        [sys.executable, "scripts/run_sne_eco_validation.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "S.N.E.-E.C.O. VALIDATION REPORT" in result.stdout
    assert "processed_packets: 4" in result.stdout
    assert "absorbed_packets: 1" in result.stdout
    assert "rejected_packets: 1" in result.stdout
    assert "quarantined_packets: 1" in result.stdout
    assert "duplicate_packets: 1" in result.stdout
    assert "Reporte eje intestino-cerebro E.C.O." in result.stdout
    assert "OK: S.N.E.-E.C.O. integrado funcionando." in result.stdout
