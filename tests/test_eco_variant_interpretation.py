from pathlib import Path

from src.eco_variant_interpretation import (
    VariantRecord,
    build_report,
    classify_clinical_significance,
    estimate_evidence_strength,
    parse_variant_tsv,
)


def make_variant(
    variant_id: str,
    gene: str,
    clinical_significance: str,
    review_status: str = "criteria provided, multiple submitters, no conflicts",
) -> VariantRecord:
    return VariantRecord(
        variant_id=variant_id,
        gene=gene,
        variant_name=f"Demo {gene} {variant_id}",
        hgvs=f"{gene}:demo.{variant_id}",
        condition="Demo condition",
        clinical_significance=clinical_significance,
        review_status=review_status,
        evidence_origin="demo",
        last_evaluated="2026-04-29",
        source_url="https://www.ncbi.nlm.nih.gov/clinvar/",
    )


def test_classify_clinical_significance_core_categories():
    assert classify_clinical_significance("Pathogenic") == "alerta_clinica_alta"
    assert classify_clinical_significance("Likely benign") == "probablemente_no_patogenica"
    assert classify_clinical_significance("Uncertain significance") == "incertidumbre_clinica"
    assert classify_clinical_significance("Conflicting classifications") == "evidencia_conflictiva"
    assert classify_clinical_significance("Risk factor") == "factor_de_riesgo_no_determinista"


def test_estimate_evidence_strength_from_review_status():
    assert estimate_evidence_strength("practice guideline") == "muy_alta"
    assert estimate_evidence_strength("reviewed by expert panel") == "alta"
    assert estimate_evidence_strength("criteria provided, multiple submitters, no conflicts") == "moderada"
    assert estimate_evidence_strength("criteria provided, single submitter") == "limitada"
    assert estimate_evidence_strength("criteria provided, conflicting classifications") == "conflictiva"


def test_build_report_keeps_non_diagnostic_limits():
    records = [
        VariantRecord(
            variant_id="DEMO-001",
            gene="BRCA1",
            variant_name="Demo variant",
            hgvs="NM_007294.4:c.5266dupC",
            condition="Hereditary cancer predisposition",
            clinical_significance="Pathogenic",
            review_status="criteria provided, multiple submitters, no conflicts",
            evidence_origin="demo",
            last_evaluated="2026-04-29",
            source_url="https://www.ncbi.nlm.nih.gov/clinvar/",
        )
    ]
    report = build_report(records)
    assert report["summary"]["variants_processed"] == 1
    assert report["summary"]["diagnostic_status"] == "no_diagnostico_resultado_bioinformatico_interpretativo"
    assert report["interpretations"][0]["category"] == "alerta_clinica_alta"
    assert "No es diagnóstico médico." in report["limits"]


def test_build_report_includes_gene_counts_and_gene_category_matrix():
    records = [
        make_variant("DEMO-BRCA1-P", "BRCA1", "Pathogenic"),
        make_variant("DEMO-BRCA1-VUS", "BRCA1", "Uncertain significance"),
        make_variant("DEMO-CFTR-B", "CFTR", "Benign"),
        make_variant("DEMO-CFTR-C", "CFTR", "Conflicting classifications of pathogenicity", "criteria provided, conflicting classifications"),
    ]

    report = build_report(records)
    summary = report["summary"]

    assert summary["gene_counts"] == {"BRCA1": 2, "CFTR": 2}
    assert summary["gene_category_matrix"]["BRCA1"]["alerta_clinica_alta"] == 1
    assert summary["gene_category_matrix"]["BRCA1"]["incertidumbre_clinica"] == 1
    assert summary["gene_category_matrix"]["CFTR"]["probablemente_no_patogenica"] == 1
    assert summary["gene_category_matrix"]["CFTR"]["evidencia_conflictiva"] == 1


def test_parse_variant_demo_dataset():
    records = parse_variant_tsv(Path("examples/clinvar_style_demo_variants.tsv"))
    assert len(records) == 5
    report = build_report(records)
    assert report["summary"]["variants_processed"] == 5
    assert report["summary"]["category_counts"]["alerta_clinica_alta"] == 1
    assert report["summary"]["category_counts"]["incertidumbre_clinica"] == 1
    assert report["summary"]["category_counts"]["probablemente_no_patogenica"] == 1
