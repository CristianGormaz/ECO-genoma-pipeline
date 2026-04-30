"""Clasificador baseline de secuencias para Proyecto E.C.O.

Baseline transparente y sin dependencias externas. Sirve como paso previo a
modelos de embeddings: extrae features simples, calcula centroides por clase y
predice por distancia al centroide más cercano.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple
import csv
import json
import math

from src.eco_motif_analysis import scan_sequence

FeatureVector = Dict[str, float]
FeatureScaler = Dict[str, Dict[str, float]]
VALID_FEATURE_MODES = {"motif", "motif_kmer"}
DNA_ALPHABET = "ACGT"


@dataclass(frozen=True)
class LabeledSequence:
    sequence_id: str
    sequence: str
    label: str
    split: str = "train"


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
                    split=(row.get("split") or "train").strip().lower(),
                )
            )
    if not records:
        raise ValueError(f"No hay secuencias etiquetadas en {path}")
    return records


def split_train_test(records: Sequence[LabeledSequence]) -> Tuple[List[LabeledSequence], List[LabeledSequence]]:
    train = [record for record in records if record.split == "train"]
    test = [record for record in records if record.split == "test"]
    if not train or not test:
        raise ValueError("El dataset debe incluir split=train y split=test para evaluación explícita.")
    return train, test


def all_kmers(k: int = 2) -> List[str]:
    if k <= 0:
        raise ValueError("k debe ser mayor que cero.")
    kmers = [""]
    for _ in range(k):
        kmers = [prefix + base for prefix in kmers for base in DNA_ALPHABET]
    return kmers


def kmer_frequencies(sequence: str, k: int = 2) -> FeatureVector:
    sequence = sequence.upper()
    keys = all_kmers(k)
    counts = {f"kmer_{k}_{key}": 0.0 for key in keys}
    valid_windows = 0
    for index in range(0, max(len(sequence) - k + 1, 0)):
        window = sequence[index : index + k]
        if len(window) == k and all(base in DNA_ALPHABET for base in window):
            counts[f"kmer_{k}_{window}"] += 1.0
            valid_windows += 1
    if valid_windows:
        for key in counts:
            counts[key] = round(counts[key] / valid_windows, 4)
    return counts


def extract_motif_features(sequence: str) -> FeatureVector:
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


def extract_features(sequence: str, feature_mode: str = "motif", kmer_k: int = 2) -> FeatureVector:
    if feature_mode not in VALID_FEATURE_MODES:
        raise ValueError(f"feature_mode inválido: {feature_mode}. Usa: {', '.join(sorted(VALID_FEATURE_MODES))}")
    features = extract_motif_features(sequence)
    if feature_mode == "motif_kmer":
        features.update(kmer_frequencies(sequence, k=kmer_k))
    return features


def extract_feature_map(
    records: Sequence[LabeledSequence], feature_mode: str = "motif", kmer_k: int = 2
) -> Dict[str, FeatureVector]:
    return {record.sequence_id: extract_features(record.sequence, feature_mode, kmer_k) for record in records}


def fit_minmax_scaler(vectors: Sequence[FeatureVector]) -> FeatureScaler:
    if not vectors:
        raise ValueError("No hay vectores para ajustar normalización.")
    keys = sorted(set().union(*(vector.keys() for vector in vectors)))
    scaler: FeatureScaler = {}
    for key in keys:
        values = [vector.get(key, 0.0) for vector in vectors]
        scaler[key] = {"min": min(values), "max": max(values)}
    return scaler


def scale_vector(vector: FeatureVector, scaler: FeatureScaler) -> FeatureVector:
    scaled: FeatureVector = {}
    for key, limits in scaler.items():
        minimum = limits["min"]
        maximum = limits["max"]
        value = vector.get(key, 0.0)
        if maximum == minimum:
            scaled[key] = 0.0
        else:
            scaled[key] = round((value - minimum) / (maximum - minimum), 6)
    return scaled


def scale_feature_map(feature_map: Dict[str, FeatureVector], scaler: FeatureScaler) -> Dict[str, FeatureVector]:
    return {sequence_id: scale_vector(vector, scaler) for sequence_id, vector in feature_map.items()}


def average_vectors(vectors: Sequence[FeatureVector]) -> FeatureVector:
    keys = sorted(vectors[0].keys())
    return {key: sum(vector[key] for vector in vectors) / len(vectors) for key in keys}


def train_centroid_classifier_from_features(
    records: Sequence[LabeledSequence], feature_map: Dict[str, FeatureVector]
) -> Dict[str, FeatureVector]:
    grouped: Dict[str, List[FeatureVector]] = {}
    for record in records:
        grouped.setdefault(record.label, []).append(feature_map[record.sequence_id])
    if len(grouped) < 2:
        raise ValueError("Se requieren al menos dos clases.")
    return {label: average_vectors(vectors) for label, vectors in sorted(grouped.items())}


def train_centroid_classifier(
    records: Sequence[LabeledSequence], feature_mode: str = "motif", kmer_k: int = 2
) -> Dict[str, FeatureVector]:
    feature_map = extract_feature_map(records, feature_mode, kmer_k)
    return train_centroid_classifier_from_features(records, feature_map)


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


def prediction_from_features(record: LabeledSequence, features: FeatureVector, centroids: Dict[str, FeatureVector]) -> Prediction:
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


def predict(
    record: LabeledSequence, centroids: Dict[str, FeatureVector], feature_mode: str = "motif", kmer_k: int = 2
) -> Prediction:
    features = extract_features(record.sequence, feature_mode, kmer_k)
    return prediction_from_features(record, features, centroids)


def safe_divide(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def build_classification_metrics(labels: Sequence[str], matrix: Dict[str, Dict[str, int]]) -> Dict[str, object]:
    per_class: Dict[str, Dict[str, float | int]] = {}
    total_support = 0
    macro_precision = 0.0
    macro_recall = 0.0
    macro_f1 = 0.0
    weighted_precision = 0.0
    weighted_recall = 0.0
    weighted_f1 = 0.0

    for label in labels:
        tp = matrix[label].get(label, 0)
        fp = sum(matrix[true_label].get(label, 0) for true_label in labels if true_label != label)
        fn = sum(matrix[label].get(pred_label, 0) for pred_label in labels if pred_label != label)
        support = sum(matrix[label].values())
        precision = safe_divide(tp, tp + fp)
        recall = safe_divide(tp, tp + fn)
        f1 = safe_divide(2 * precision * recall, precision + recall)

        total_support += support
        macro_precision += precision
        macro_recall += recall
        macro_f1 += f1
        weighted_precision += precision * support
        weighted_recall += recall * support
        weighted_f1 += f1 * support
        per_class[label] = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "support": support,
        }

    label_count = len(labels) or 1
    return {
        "per_class": per_class,
        "macro_avg": {
            "precision": round(macro_precision / label_count, 4),
            "recall": round(macro_recall / label_count, 4),
            "f1": round(macro_f1 / label_count, 4),
            "support": total_support,
        },
        "weighted_avg": {
            "precision": round(safe_divide(weighted_precision, total_support), 4),
            "recall": round(safe_divide(weighted_recall, total_support), 4),
            "f1": round(safe_divide(weighted_f1, total_support), 4),
            "support": total_support,
        },
    }


def evaluate_with_feature_map(
    records: Sequence[LabeledSequence], centroids: Dict[str, FeatureVector], feature_map: Dict[str, FeatureVector]
) -> Dict[str, object]:
    predictions = [prediction_from_features(record, feature_map[record.sequence_id], centroids) for record in records]
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
        "classification_metrics": build_classification_metrics(labels, matrix),
        "predictions": [asdict(prediction) for prediction in predictions],
    }


def evaluate(
    records: Sequence[LabeledSequence], centroids: Dict[str, FeatureVector], feature_mode: str = "motif", kmer_k: int = 2
) -> Dict[str, object]:
    feature_map = extract_feature_map(records, feature_mode, kmer_k)
    return evaluate_with_feature_map(records, centroids, feature_map)


def build_classifier_report(
    records: Sequence[LabeledSequence], feature_mode: str = "motif", kmer_k: int = 2, normalize_features: bool = False
) -> Dict[str, object]:
    train_records, test_records = split_train_test(records)
    train_features = extract_feature_map(train_records, feature_mode, kmer_k)
    test_features = extract_feature_map(test_records, feature_mode, kmer_k)
    scaler = None

    if normalize_features:
        scaler = fit_minmax_scaler(list(train_features.values()))
        train_features = scale_feature_map(train_features, scaler)
        test_features = scale_feature_map(test_features, scaler)

    centroids = train_centroid_classifier_from_features(train_records, train_features)
    train_evaluation = evaluate_with_feature_map(train_records, centroids, train_features)
    test_evaluation = evaluate_with_feature_map(test_records, centroids, test_features)

    if feature_mode == "motif_kmer" and normalize_features:
        model_label = "centroid_baseline_motif_kmer_minmax"
    elif feature_mode == "motif_kmer":
        model_label = "centroid_baseline_motif_kmer"
    else:
        model_label = "centroid_baseline_explicable"

    return {
        "model_type": model_label,
        "feature_mode": feature_mode,
        "kmer_k": kmer_k if feature_mode == "motif_kmer" else None,
        "normalize_features": normalize_features,
        "feature_scaling": "minmax_train" if normalize_features else "none",
        "feature_scaler": scaler,
        "purpose": "baseline_pre_embeddings_para_clasificacion_de_secuencias",
        "data_split": {
            "train": len(train_records),
            "test": len(test_records),
            "note": "Entrena con split=train y evalúa desempeño reportable en split=test.",
        },
        "centroids": centroids,
        "train_evaluation": train_evaluation,
        "test_evaluation": test_evaluation,
        "limits": [
            "Baseline pequeño y demostrativo.",
            "La separación train/test evita reportar solo desempeño de entrenamiento.",
            "No representa desempeño general sobre datasets reales grandes.",
            "Las features dependen de motivos simples del MVP y, opcionalmente, frecuencias k-mer.",
            "La normalización, si está activa, se ajusta solo con train para evitar fuga de información desde test.",
        ],
    }


def write_json_report(payload: Dict[str, object], output_path: str | Path) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
