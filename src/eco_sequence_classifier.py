"""Clasificador baseline de secuencias para Proyecto E.C.O.

Baseline transparente y sin dependencias externas. Sirve como paso previo a
modelos de embeddings: extrae features simples, calcula centroides por clase y
predice por distancia al centroide más cercano.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Sequence
import csv
import json
import math

from src.eco_motif_analysis import scan_sequence

FeatureVector = Dict[str, float]


@dataclass(frozen=True)
class LabeledSequence:
    sequence_id: str
    sequence: str
    label: str


@dataclass(frozen=True)
class Prediction:
    sequence_id: str
    true_label: str
    predicted_label: str
    confidence: float
    distances: Dict[str, float]
    features: FeatureVector


def parse_labeled_sequences_tsv(path: str | Path) -> List[LabeledSequence]:
    records: List[LabeledSequence] = []
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        required = {"sequence_id", "sequence", "label"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError("Faltan columnas: " + ", ".join(sorted(missing)))
        for row in reader:
            records.append(
                LabeledSequence(
                    sequence_id=row["sequence_id"].strip(),
                    sequence=row["sequence"].strip(),
                    label=row["label"].strip(),
                )
            )
    if not records:
        raise ValueError(f"No hay secuencias etiquetadas en {path}")
    return records


def extract_features(sequence: str) -> FeatureVector:
    report = scan_sequence(sequence)
    motif_names = [hit.motif_name for hit in report.hits]
    length = max(report.length, 1)
    return {
        "length": float(report.length),
        "gc_percent": report.gc_percent,
        "n_percent": report.n_percent,
        "motif_count": float(len(report.hits)),
        "motif_density_per_100bp": round((len(report.hits) / length) * 100, 4),
        "has_tata": 1.0 if "TATA_box_canonica" in motif_names or "TATA_box_degenerada" in motif_names else 0.0,
        "has_caat": 1.0 if "CAAT_box" in motif_names else 0.0,
        "has_gc_box": 1.0 if "GC_box" in motif_names else 0.0,
        "has_polya": 1.0 if "polyA_signal" in motif_names else 0.0,
        "has_homopolymer": 1.0 if any(name.startswith("homopolimero") for name in motif_names) else 0.0,
    }


def average_vectors(vectors: Sequence[FeatureVector]) -> FeatureVector:
    keys = sorted(vectors[0].keys())
    return {key: sum(vector[key] for vector in vectors) / len(vectors) for key in keys}


def train_centroid_classifier(records: Sequence[LabeledSequence]) -> Dict[str, FeatureVector]:
    grouped: Dict[str, List[FeatureVector]] = {}
    for record in records:
        grouped.setdefault(record.label, []).append(extract_features(record.sequence))
    if len(grouped) < 2:
        raise ValueError("Se requieren al menos dos clases.")
    return {label: average_vectors(vectors) for label, vectors in sorted(grouped.items())}


def euclidean_distance(left: FeatureVector, right: FeatureVector) -> float:
    keys = sorted(set(left) | set(right))
    return math.sqrt(sum((left.get(key, 0.0) - right.get(key, 0.0)) ** 2 for key in keys))


def confidence_from_distances(distances: Dict[str, float]) -> float:
    ordered = sorted(distances.values())
    if len(ordered) < 2:
        return 1.0
    best, second = ordered[0], ordered[1]
    if second == 0:
        return 1.0
    return round(min(max((second - best) / second, 0.0), 1.0), 4)


def predict(record: LabeledSequence, centroids: Dict[str, FeatureVector]) -> Prediction:
    features = extract_features(record.sequence)
    distances = {label: round(euclidean_distance(features, centroid), 4) for label, centroid in centroids.items()}
    predicted_label = min(distances, key=distances.get)
    return Prediction(
        sequence_id=record.sequence_id,
        true_label=record.label,
        predicted_label=predicted_label,
        confidence=confidence_from_distances(distances),
        distances=distances,
        features=features,
    )


def evaluate(records: Sequence[LabeledSequence], centroids: Dict[str, FeatureVector]) -> Dict[str, object]:
    predictions = [predict(record, centroids) for record in records]
    labels = sorted({record.label for record in records} | set(centroids))
    matrix: Dict[str, Dict[str, int]] = {true: {pred: 0 for pred in labels} for true in labels}
    correct = 0
    for item in predictions:
        matrix[item.true_label][item.predicted_label] += 1
        correct += int(item.true_label == item.predicted_label)
    total = len(predictions)
    return {
        "total": total,
        "correct": correct,
        "accuracy": round(correct / total, 4) if total else 0.0,
        "labels": labels,
        "confusion_matrix": matrix,
        "predictions": [asdict(prediction) for prediction in predictions],
    }


def build_classifier_report(records: Sequence[LabeledSequence]) -> Dict[str, object]:
    centroids = train_centroid_classifier(records)
    evaluation = evaluate(records, centroids)
    return {
        "model_type": "centroid_baseline_explicable",
        "purpose": "baseline_pre_embeddings_para_clasificacion_de_secuencias",
        "centroids": centroids,
        "evaluation": evaluation,
        "limits": [
            "Baseline pequeño y demostrativo.",
            "No representa desempeño general sobre datasets reales grandes.",
            "Las features dependen de motivos simples del MVP.",
        ],
    }


def write_json_report(payload: Dict[str, object], output_path: str | Path) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
