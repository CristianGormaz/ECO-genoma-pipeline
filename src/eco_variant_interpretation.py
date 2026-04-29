"""Interpretación bioinformática segura de variantes para E.C.O.

Este módulo convierte registros de variantes estilo ClinVar en un reporte
interpretativo legible. No diagnostica, no calcula riesgo personal y no reemplaza
la evaluación de un profesional de genética clínica.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List
import csv
import json


@dataclass(frozen=True)
class VariantRecord:
    """Registro mínimo de variante para reporte E.C.O."""

    variant_id: str
    gene: str
    variant_name: str
    hgvs: str
    condition: str
    clinical_significance: str
    review_status: str
    evidence_origin: str
    last_evaluated: str
    source_url: str
    notes: str = ""


@dataclass(frozen=True)
class VariantInterpretation:
    """Interpretación estructurada y no diagnóstica de una variante."""

    variant: VariantRecord
    category: str
    evidence_strength: str
    patient_level_warning: str
    practical_reading: str
    recommended_next_step: str

    def to_dict(self) -> Dict[str, object]:
        payload = asdict(self)
        return payload


PATHOGENIC_TERMS = {"pathogenic", "likely pathogenic", "pathogenic/likely pathogenic"}
BENIGN_TERMS = {"benign", "likely benign", "benign/likely benign"}
VUS_TERMS = {"uncertain significance", "vus", "uncertain", "variant of uncertain significance"}
CONFLICT_TERMS = {"conflicting classifications", "conflicting interpretations of pathogenicity"}
RISK_TERMS = {"risk factor", "association", "protective"}
DRUG_TERMS = {"drug response", "affects"}


def normalize_text(value: str) -> str:
    return " ".join((value or "").strip().lower().replace("_", " ").split())


def classify_clinical_significance(clinical_significance: str) -> str:
    """Clasifica el significado clínico declarado por una fuente externa."""
    normalized = normalize_text(clinical_significance)
    if normalized in PATHOGENIC_TERMS or "pathogenic" in normalized and "conflicting" not in normalized:
        return "alerta_clinica_alta"
    if normalized in BENIGN_TERMS or "benign" in normalized:
        return "probablemente_no_patogenica"
    if normalized in VUS_TERMS or "uncertain" in normalized:
        return "incertidumbre_clinica"
    if normalized in CONFLICT_TERMS or "conflicting" in normalized:
        return "evidencia_conflictiva"
    if normalized in RISK_TERMS or "risk" in normalized:
        return "factor_de_riesgo_no_determinista"
    if normalized in DRUG_TERMS or "drug" in normalized:
        return "farmacogenomica_o_respuesta_a_farmacos"
    return "clasificacion_no_estandarizada"


def estimate_evidence_strength(review_status: str) -> str:
    """Estima fuerza de evidencia usando el estado de revisión estilo ClinVar."""
    normalized = normalize_text(review_status)
    if "practice guideline" in normalized:
        return "muy_alta"
    if "expert panel" in normalized or "reviewed by expert panel" in normalized:
        return "alta"
    if "multiple submitters" in normalized and "no conflicts" in normalized:
        return "moderada"
    if "single submitter" in normalized and "criteria provided" in normalized:
        return "limitada"
    if "conflicting" in normalized:
        return "conflictiva"
    if "no assertion" in normalized or "no classification" in normalized:
        return "baja_o_no_informada"
    return "no_determinada"


def build_practical_reading(record: VariantRecord, category: str, evidence_strength: str) -> str:
    """Genera una lectura comprensible sin convertirla en diagnóstico."""
    if category == "alerta_clinica_alta":
        return (
            f"La fuente externa clasifica esta variante en {record.gene} como {record.clinical_significance}. "
            "Esto puede ser clínicamente relevante, pero debe confirmarse con historia personal/familiar, método de laboratorio, zigosidad y evaluación genética profesional."
        )
    if category == "incertidumbre_clinica":
        return (
            "La variante está clasificada como de significado incierto. En genética clínica, una VUS no debe usarse por sí sola para decisiones médicas."
        )
    if category == "probablemente_no_patogenica":
        return (
            "La clasificación externa sugiere que la variante es benigna o probablemente benigna para la condición reportada. Esto no descarta otros riesgos genéticos no evaluados."
        )
    if category == "evidencia_conflictiva":
        return (
            "Existen interpretaciones conflictivas entre fuentes o submitters. El resultado requiere revisión cuidadosa de evidencia, fecha de evaluación y criterios usados."
        )
    if category == "factor_de_riesgo_no_determinista":
        return (
            "La variante se presenta como factor de riesgo o asociación. Esto no significa enfermedad asegurada; el efecto depende de penetrancia, ambiente y otros factores genéticos."
        )
    if category == "farmacogenomica_o_respuesta_a_farmacos":
        return (
            "La variante puede estar relacionada con respuesta a fármacos. No debe cambiarse ningún tratamiento sin evaluación clínica."
        )
    return (
        f"La clasificación '{record.clinical_significance}' no fue reconocida como categoría estándar por E.C.O. "
        f"La fuerza de evidencia estimada fue {evidence_strength}."
    )


def recommended_next_step(category: str) -> str:
    if category == "alerta_clinica_alta":
        return "Validar en fuente clínica actualizada y consultar genética clínica antes de cualquier decisión."
    if category == "incertidumbre_clinica":
        return "No usar para decisiones médicas; monitorear reclasificaciones y revisar evidencia familiar/funcional."
    if category == "probablemente_no_patogenica":
        return "Registrar como hallazgo probablemente no patogénico para esa condición; no sobredimensionar."
    if category == "evidencia_conflictiva":
        return "Revisar submitters, fecha, criterio ACMG/AMP y evidencia primaria antes de concluir."
    if category == "factor_de_riesgo_no_determinista":
        return "Interpretar como riesgo probabilístico, no como diagnóstico; requiere contexto clínico y poblacional."
    if category == "farmacogenomica_o_respuesta_a_farmacos":
        return "Consultar guía farmacogenética y equipo médico antes de modificar tratamientos."
    return "Revisar manualmente la fuente original y normalizar la clasificación."


def interpret_variant(record: VariantRecord) -> VariantInterpretation:
    category = classify_clinical_significance(record.clinical_significance)
    strength = estimate_evidence_strength(record.review_status)
    return VariantInterpretation(
        variant=record,
        category=category,
        evidence_strength=strength,
        patient_level_warning=(
            "Interpretación de variante, no interpretación de paciente. No incorpora síntomas, antecedentes, zigosidad, penetrancia, etnia, edad, sexo, laboratorio ni consentimiento clínico."
        ),
        practical_reading=build_practical_reading(record, category, strength),
        recommended_next_step=recommended_next_step(category),
    )


def parse_variant_tsv(path: Path) -> List[VariantRecord]:
    """Lee un TSV con columnas estilo ClinVar reducido."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        records = []
        for row in reader:
            records.append(
                VariantRecord(
                    variant_id=row.get("variant_id", "").strip(),
                    gene=row.get("gene", "").strip(),
                    variant_name=row.get("variant_name", "").strip(),
                    hgvs=row.get("hgvs", "").strip(),
                    condition=row.get("condition", "").strip(),
                    clinical_significance=row.get("clinical_significance", "").strip(),
                    review_status=row.get("review_status", "").strip(),
                    evidence_origin=row.get("evidence_origin", "").strip(),
                    last_evaluated=row.get("last_evaluated", "").strip(),
                    source_url=row.get("source_url", "").strip(),
                    notes=row.get("notes", "").strip(),
                )
            )
    return records


def summarize_interpretations(interpretations: Iterable[VariantInterpretation]) -> Dict[str, object]:
    interpretations = list(interpretations)
    category_counts: Dict[str, int] = {}
    evidence_counts: Dict[str, int] = {}
    for item in interpretations:
        category_counts[item.category] = category_counts.get(item.category, 0) + 1
        evidence_counts[item.evidence_strength] = evidence_counts.get(item.evidence_strength, 0) + 1
    return {
        "variants_processed": len(interpretations),
        "category_counts": category_counts,
        "evidence_strength_counts": evidence_counts,
        "diagnostic_status": "no_diagnostico_resultado_bioinformatico_interpretativo",
    }


def build_report(records: List[VariantRecord]) -> Dict[str, object]:
    interpretations = [interpret_variant(record) for record in records]
    return {
        "summary": summarize_interpretations(interpretations),
        "interpretations": [item.to_dict() for item in interpretations],
        "limits": [
            "No es diagnóstico médico.",
            "No calcula riesgo personal absoluto.",
            "No reemplaza consejería genética ni validación clínica.",
            "Depende de la calidad, fecha y revisión de la fuente externa.",
        ],
    }


def write_json_report(report: Dict[str, object], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
