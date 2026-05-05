import subprocess
import sys
from pathlib import Path


def test_ml_challenge_eval_runs_as_direct_script():
    subprocess.run(
        [sys.executable, "scripts/run_sne_eco_empirical_train_eval_split.py"],
        check=True,
        text=True,
        capture_output=True,
    )

    result = subprocess.run(
        [sys.executable, "scripts/run_sne_eco_ml_challenge_eval.py"],
        check=True,
        text=True,
        capture_output=True,
    )

    assert "OK: evaluación de desafío ML S.N.E.-E.C.O. generada." in result.stdout
    assert Path("results/sne_eco_ml_challenge_eval_report.json").exists()
    assert Path("results/sne_eco_ml_challenge_eval_report.md").exists()
