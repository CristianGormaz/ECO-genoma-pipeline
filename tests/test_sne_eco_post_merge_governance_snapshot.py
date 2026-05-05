from pathlib import Path


DOC = Path("docs/sne-eco-post-merge-governance-snapshot.md")


def test_post_merge_snapshot_exists():
    assert DOC.exists()


def test_post_merge_snapshot_declares_merge_context():
    text = DOC.read_text(encoding="utf-8")

    assert "PR #83" in text
    assert "a8a9275" in text
    assert "main" in text


def test_post_merge_snapshot_keeps_responsible_limits():
    text = DOC.read_text(encoding="utf-8")

    assert "No ingiere datos reales" in text
    assert "No diagnostica personas" in text
    assert "No recalibra umbrales" in text
    assert "No modifica baseline estable" in text
