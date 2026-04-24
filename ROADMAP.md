# E.C.O. Roadmap

E.C.O. — Entérico Codificador Orgánico is an experimental, bioinspired genomic analysis pipeline. The current version is an MVP focused on reading FASTA sequences and detecting simple regulatory motifs. This roadmap defines the next technical stages needed to evolve the project from motif scanning toward a reproducible genomics pipeline.

## Current status

- Python module available at `src/eco_motif_analysis.py`.
- FASTA parsing and sequence validation.
- GC content and ambiguous `N` base calculation.
- Regex-based detection of simple regulatory motifs:
  - TATA box
  - degenerate TATA motif
  - CAAT box
  - GC box
  - polyA signal
  - long homopolymer runs
- JSON and CSV output support.
- Example FASTA file in `examples/`.
- Example output in `results/`.
- Unit tests available in `tests/`.
- GitHub Actions workflow for automated Python tests.

## Phase 1 — Motif analysis MVP

Goal: keep the current module stable, documented and easy to test.

Planned improvements:

- Add more representative FASTA examples.
- Add clearer CLI examples in the README.
- Add optional output summary statistics per motif type.
- Add version information to the command-line interface.
- Keep tests passing on Python 3.10, 3.11 and 3.12.

Status: in progress.

## Phase 2 — BED to FASTA conversion

Goal: allow E.C.O. to process genomic coordinates instead of only raw FASTA files.

Planned improvements:

- Accept BED files as input.
- Validate BED columns: chromosome, start and end.
- Extract real genomic sequences from a reference genome FASTA.
- Add strand handling when available.
- Export extracted sequences to FASTA.
- Add tests with a tiny artificial genome and small BED file.

Expected tools:

- Python implementation for small examples.
- Optional future support for `bedtools getfasta`.

Status: next step.

## Phase 3 — Public regulatory datasets

Goal: test the pipeline with real regulatory annotations.

Candidate datasets:

- ENCODE regulatory regions.
- EnhancerAtlas enhancer annotations.
- Promoter or enhancer regions from public genome browsers.

Planned improvements:

- Add dataset download notes.
- Add preprocessing instructions.
- Add small reproducible samples rather than large raw datasets.
- Document genome build compatibility, such as hg19 or hg38.

Status: planned.

## Phase 4 — Embeddings for DNA sequences

Goal: transform DNA sequences into numerical representations for machine learning.

Planned improvements:

- Add k-mer tokenization.
- Add DNABERT or similar DNA language model embeddings.
- Store embeddings in a reusable format.
- Add dimensionality reduction examples such as PCA or t-SNE.

Status: planned.

## Phase 5 — Classification model

Goal: classify regulatory versus non-regulatory regions.

Planned improvements:

- Build a baseline classifier.
- Compare simple models before using complex models.
- Add train/test split.
- Report precision, recall and F1-score.
- Export predictions as CSV or BED-like tables.

Possible first baseline:

- Logistic regression or random forest using simple sequence features.

Possible later model:

- MLP using DNA embeddings.

Status: planned.

## Phase 6 — Interpretability and biological review

Goal: make predictions understandable and biologically cautious.

Planned improvements:

- Report which motifs contributed to each sequence summary.
- Add motif density calculations.
- Compare motif hits between positive and negative examples.
- Avoid treating motif presence as proof of regulatory activity.
- Document limitations clearly.

Status: planned.

## Phase 7 — Visualization dashboard

Goal: make E.C.O. easier to inspect and explain.

Planned improvements:

- Build a small Streamlit dashboard.
- Load JSON or CSV reports.
- Filter by motif type.
- Visualize GC content and motif counts.
- Display sequence-level summaries.

Status: planned.

## Phase 8 — Workflow orchestration

Goal: move from scripts to a reproducible pipeline.

Planned improvements:

- Add a Nextflow workflow.
- Separate modules for:
  - input validation
  - BED to FASTA conversion
  - motif scanning
  - embedding generation
  - classification
  - report generation
- Add Docker support for reproducible execution.

Status: planned.

## Limitations

- The current MVP detects known motifs using regular expressions.
- Motif presence alone does not prove biological regulatory activity.
- Current examples are demonstrative and not biological evidence.
- Large-scale analysis requires genome-build consistency and curated datasets.
- Machine learning stages are not implemented yet.

## Guiding principle

E.C.O. should remain modular, reproducible and honest about its biological scope. Each stage should transform raw genomic data into a more interpretable form without overstating what the current evidence supports.

## Signature

Cristian Gormaz — Proyecto E.C.O.
