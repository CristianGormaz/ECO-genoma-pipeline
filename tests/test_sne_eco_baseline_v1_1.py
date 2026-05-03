from pathlib import Path
import json

def test_baseline_v1_1_exists():
    path = Path("baselines/sne-eco-v1.1-snapshot.json")
    assert path.exists()

def test_baseline_v1_1_values():
    data = json.loads(Path("baselines/sne-eco-v1.1-snapshot.json").read_text())
    assert data["confused_routes"] == 0
    assert data["clinical_use"] is False
    assert data["models_human_consciousness"] is False
    assert data["tests_passed"] == 211
