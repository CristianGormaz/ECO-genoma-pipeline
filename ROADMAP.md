# E.C.O. Roadmap

E.C.O. — Entérico Codificador Orgánico is an experimental, bioinspired genomic analysis pipeline.

**Current Maturity State (v1.0 RC1):**
- **Technical MVP:** 85% - 90% (Governance, gauntlet, admission gates, and strict green state are solid).
- **Experimental Governed:** 70% - 75% (Base organism functional and protected; needs better observability).
- **Full Ideal Project:** 45% - 50% (Long-term vision for real data admission with human-in-the-loop).

## Phase 1 — Motif analysis MVP
Goal: keep the current module stable, documented and easy to test.
- Status: **Completed & Endured.** Core regex-based detection and FASTA parsing are stable.

## Phase 2 — BED to FASTA conversion
Goal: allow E.C.O. to process genomic coordinates.
- Status: **Completed.** `eco_bed_to_fasta.py` is functional and tested.

## Phase 3 — Public regulatory datasets
Goal: test the pipeline with real regulatory annotations.
- Status: **In Progress / Endured.** Integration via `source_admission_decision_summary` and public source guards is active.

## Phase 4 — Embeddings for DNA sequences
Goal: transform DNA sequences into numerical representations.
- Status: **Initial Implementation.** Placeholder and semireal embeddings are active for interface testing.

## Phase 5 — Classification model
Goal: classify regulatory versus non-regulatory regions.
- Status: **Active Baseline.** `eco_sequence_classifier.py` and `adaptive_state_baseline.py` are functional.

## Phase 6 — Interpretability and biological review
Goal: make predictions understandable and biologically cautious.
- Status: **Core Feature.** Homeostasis, defense signals, and gut-brain axis reports are active.

## Phase 7 — Visualization dashboard
Goal: make E.C.O. easier to inspect and explain.
- Status: **Operational Dashboard v1.** `run_eco_synthetic_operational_dashboard.py` is active.

## Phase 8 — S.N.E.-E.C.O. v1.2 — Observabilidad Distribuida (Next Step)
Goal: enhance the "organism's" self-awareness and reporting capabilities.
- Add internal module traces (distributed tracing analog).
- Flow visualization between plexos entéricos.
- Extreme synthetic scenario expansion (edge cases).
- Documentation of internal flow decision trees.

## Phase 9 — Workflow orchestration
Goal: move from scripts to a reproducible pipeline.
- Status: **Partial.** `Makefile` and `run_eco_pipeline.py` provide basic orchestration.

## Limitations
- E.C.O. is not a clinical system.
- Real biological data admission requires explicit human review and manifest governance.
- Bioinspiration is a software architecture, not a biological claim.

## Guiding principle
E.C.O. should remain modular, reproducible and honest about its biological scope. Its readiness is measured by its maturity to reject, pause, audit, and rollback rather than its ability to simply ingest data.

## Signature
Cristian Gormaz — Proyecto E.C.O.
