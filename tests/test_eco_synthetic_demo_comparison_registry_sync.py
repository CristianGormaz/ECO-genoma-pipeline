import json
from pathlib import Path


REGISTRY = Path("docs/architecture/eco-synthetic-demo-registry.json")
COMPARISON = Path("docs/architecture/eco-synthetic-demo-comparison.md")


def normalize(value: str) -> str:
    return value.lower().replace("_", " ").replace("-", " ").strip()


def test_comparison_mentions_every_registered_demo():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    comparison_text = normalize(COMPARISON.read_text(encoding="utf-8"))
    demos = registry.get("demos", [])

    assert demos, "El registro debe contener al menos una demo sintética."

    for demo in demos:
        name = demo.get("name") or demo.get("title") or demo.get("id")
        assert name, f"Demo sin nombre identificable: {demo}"
        assert normalize(name) in comparison_text


def test_comparison_mentions_every_registered_demo_runner():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    comparison_text = COMPARISON.read_text(encoding="utf-8")

    for demo in registry.get("demos", []):
        runner = demo.get("runner")
        assert runner, f"Demo sin runner declarado: {demo}"
        assert runner in comparison_text
