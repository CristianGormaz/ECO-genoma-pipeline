import json
import subprocess
import sys
import os
from pathlib import Path
import pytest

SCRIPT = "scripts/run_eco_synthetic_operational_dashboard.py"
GOVERNED_CYCLE_OUTPUT = Path("results/eco_governed_experimental_cycle.json")
DASHBOARD_OUTPUT = Path("results/eco_synthetic_operational_dashboard.json")

def test_dashboard_recomputes_governed_cycle_if_missing():
    # Ensure results folder exists but cycle output is missing
    GOVERNED_CYCLE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    if GOVERNED_CYCLE_OUTPUT.exists():
        GOVERNED_CYCLE_OUTPUT.unlink()
    
    # Run dashboard
    result = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True, check=False)
    assert result.returncode == 0
    
    # Check that cycle output was recreated
    assert GOVERNED_CYCLE_OUTPUT.exists()
    
    # Check dashboard payload
    payload = json.loads(DASHBOARD_OUTPUT.read_text(encoding="utf-8"))
    assert payload["governed_experimental_cycle"]["status"] in {"passed", "attention", "red"}
    assert payload["governed_experimental_cycle"]["status"] != "missing"

def test_dashboard_handles_governed_cycle_failure_gracefully():
    # Make the governed cycle script fail by introducing a syntax error (temporary)
    script_path = Path("scripts/run_eco_governed_experimental_cycle.py")
    original_content = script_path.read_text()
    
    try:
        script_path.write_text("import sys; sys.exit(1)")
        
        # Run dashboard
        result = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True, check=False)
        assert result.returncode == 0 # Dashboard itself should still run
        
        # Check dashboard payload
        payload = json.loads(DASHBOARD_OUTPUT.read_text(encoding="utf-8"))
        assert payload["governed_experimental_cycle"]["status"] == "red"
        assert "error" in payload["governed_experimental_cycle"]
        
        # The component list should also show it as red
        comp = next(c for c in payload["components"] if c["id"] == "governed_experimental_cycle")
        assert comp["status"] == "red"
        
    finally:
        # Restore original script
        script_path.write_text(original_content)

if __name__ == "__main__":
    pytest.main([__file__])
