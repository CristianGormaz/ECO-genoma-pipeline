#!/usr/bin/env python3
"""Genera un panel sintético/documental de gobernanza E.C.O."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class GovernancePanel:
    panel_name: str
    generated_at_utc: str
    mode: str
    internet_required: bool
    uses_real_data: bool
    training_enabled: bool
    baseline_modified: bool
    threshold_recalibration_enabled: bool
    human_review_required_for_critical_changes: bool
    operational_status: str
    external_sources_paused: bool
    responsible_limits: list[str]
    gates: dict[str, str]
    recommendation: str


def build_panel() -> GovernancePanel:
    return GovernancePanel(
        panel_name="E.C.O. Governance Panel",
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        mode="synthetic_documentary",
        internet_required=False,
        uses_real_data=False,
        training_enabled=False,
        baseline_modified=False,
        threshold_recalibration_enabled=False,
        human_review_required_for_critical_changes=True,
        operational_status="governed_operational_state",
        external_sources_paused=True,
        responsible_limits=[
            "no_real_data",
            "no_training",
            "no_baseline_changes",
            "no_threshold_recalibration",
            "no_sensitive_data",
            "no_biomedical_applied_claims",
        ],
        gates={
            "real_data_gate": "human_review_required",
            "training_gate": "human_review_required",
            "baseline_gate": "human_review_required",
            "threshold_gate": "human_review_required",
        },
        recommendation=(
            "Mantener operación sintética/documental y ampliar validaciones "
            "de gobernanza antes de habilitar cualquier gate crítico."
        ),
    )


def render_markdown(panel: GovernancePanel) -> str:
    return "\n".join(
        [
            "# E.C.O. Governance Panel",
            "",
            f"- Generated at (UTC): {panel.generated_at_utc}",
            f"- Mode: {panel.mode}",
            f"- Operational status: {panel.operational_status}",
            "",
            "## Responsible limits",
            *[f"- {item}" for item in panel.responsible_limits],
            "",
            "## Critical gates",
            *[f"- {name}: {status}" for name, status in panel.gates.items()],
            "",
            "## Enforcement flags",
            f"- internet_required: {panel.internet_required}",
            f"- uses_real_data: {panel.uses_real_data}",
            f"- training_enabled: {panel.training_enabled}",
            f"- baseline_modified: {panel.baseline_modified}",
            f"- threshold_recalibration_enabled: {panel.threshold_recalibration_enabled}",
            f"- human_review_required_for_critical_changes: {panel.human_review_required_for_critical_changes}",
            f"- external_sources_paused: {panel.external_sources_paused}",
            "",
            "## Operational recommendation",
            f"{panel.recommendation}",
            "",
        ]
    )


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    results_dir = root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    panel = build_panel()
    panel_json = results_dir / "eco_governance_panel.json"
    panel_md = results_dir / "eco_governance_panel.md"

    panel_json.write_text(json.dumps(asdict(panel), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    panel_md.write_text(render_markdown(panel), encoding="utf-8")

    print(f"Generated: {panel_json}")
    print(f"Generated: {panel_md}")


if __name__ == "__main__":
    main()
