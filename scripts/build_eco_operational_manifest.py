#!/usr/bin/env python3
"""Construye un manifiesto operativo para una corrida E.C.O.

El manifiesto resume artefactos generados, hashes, tamaños y métricas
detectables desde reportes JSON. Es una capa puente entre el pipeline técnico
y una futura UX conversacional auditable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS_DIR = PROJECT_ROOT / "results"
DEFAULT_OUTPUT_JSON = DEFAULT_RESULTS_DIR / "eco_operational_manifest.json"
DEFAULT_OUTPUT_MD = DEFAULT_RESULTS_DIR / "eco_operational_manifest.md"

ARTIFACT_PATTERNS: Sequence[str] = ("*.json", "*.md", "*.html", "*.fa", "*.tsv", "*.svg")
SELF_ARTIFACT_NAMES = {"eco_operational_manifest.json", "eco_operational_manifest.md"}

EXPECTED_CORE_ARTIFACTS = (
    "eco_demo_pipeline_report.json",
    "eco_demo_pipeline_report.md",
    "eco_custom_demo_report.json",
    "eco_custom_demo_report.md",
    "eco_variant_demo_report.json",
    "eco_variant_demo_report.md",
    "eco_dataset_audit_report.json",
    "eco_dataset_audit_report.md",
    "eco_classifier_baseline_v3_report.json",
    "eco_classifier_comparison_report.md",
    "eco_embedding_repeated_eval_report.json",
    "eco_model_decision_report.md",
)


def utc_now_iso() -> str:
    """Devuelve la hora UTC en formato ISO-8601."""
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    """Calcula SHA-256 de un archivo sin cargarlo completo en memoria."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_load_json(path: Path) -> Optional[Any]:
    """Carga JSON si es válido; si no, devuelve None para no romper el manifiesto."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def read_path(data: Any, path: Sequence[str]) -> Optional[Any]:
    """Lee una ruta anidada dentro de un dict."""
    current = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def compact_value(value: Any) -> Any:
    """Normaliza valores para el manifiesto sin perder trazabilidad."""
    if isinstance(value, float):
        return round(value, 4)
    return value


def detect_metrics(data: Any) -> Dict[str, Any]:
    """Extrae métricas frecuentes de los reportes E.C.O. sin acoplarse a un único script."""
    if not isinstance(data, dict):
        return {}

    metric_paths = {
        "feature_mode": ("feature_mode",),
        "kmer_k": ("kmer_k",),
        "feature_scaling": ("feature_scaling",),
        "train_size": ("data_split", "train"),
        "test_size": ("data_split", "test"),
        "train_accuracy": ("train_evaluation", "accuracy"),
        "test_accuracy": ("test_evaluation", "accuracy"),
        "test_macro_f1": (
            "test_evaluation",
            "classification_metrics",
            "macro_avg",
            "f1",
        ),
        "best_model": ("best_model",),
        "best_average_model": ("best_average_model",),
        "operational_decision": ("operational_decision",),
        "decision": ("decision",),
        "processed": ("feedback", "processed"),
        "accepted": ("feedback", "accepted"),
        "rejected": ("feedback", "rejected"),
        "absorbed": ("feedback", "absorbed"),
        "rejection_rate": ("feedback", "rejection_rate"),
        "absorption_rate": ("feedback", "absorption_rate"),
    }

    metrics: Dict[str, Any] = {}
    for label, path in metric_paths.items():
        value = read_path(data, path)
        if value is not None:
            metrics[label] = compact_value(value)

    # Fallbacks simples para reportes con estructura "summary" o "resumen".
    for summary_key in ("summary", "resumen", "digestive_summary"):
        summary = data.get(summary_key)
        if isinstance(summary, dict):
            for key, value in summary.items():
                normalized_key = str(key).lower().replace(" ", "_")
                if normalized_key in {
                    "total",
                    "processed",
                    "accepted",
                    "rejected",
                    "absorbed",
                    "motifs_found",
                    "variants_processed",
                    "test_macro_f1",
                }:
                    metrics.setdefault(normalized_key, compact_value(value))

    return metrics


def iter_artifacts(results_dir: Path, excluded_names: Iterable[str]) -> List[Path]:
    """Lista artefactos relevantes dentro de results/ de manera estable."""
    excluded = set(excluded_names)
    paths: List[Path] = []
    if not results_dir.exists():
        return paths

    for pattern in ARTIFACT_PATTERNS:
        for path in results_dir.rglob(pattern):
            if path.is_file() and path.name not in excluded:
                paths.append(path)

    return sorted(set(paths), key=lambda item: item.relative_to(results_dir).as_posix())


def artifact_record(path: Path, results_dir: Path) -> Dict[str, Any]:
    """Construye el registro auditable de un artefacto."""
    stat = path.stat()
    relative = path.relative_to(results_dir).as_posix()
    return {
        "path": relative,
        "extension": path.suffix.lower().lstrip(".") or "sin_extension",
        "size_bytes": stat.st_size,
        "sha256": sha256_file(path),
    }


def build_manifest(results_dir: Path, run_label: str = "eco_local_run") -> Dict[str, Any]:
    """Construye el manifiesto operativo desde el directorio de resultados."""
    artifacts = [artifact_record(path, results_dir) for path in iter_artifacts(results_dir, SELF_ARTIFACT_NAMES)]
    artifacts_by_extension: Dict[str, int] = {}
    for artifact in artifacts:
        extension = artifact["extension"]
        artifacts_by_extension[extension] = artifacts_by_extension.get(extension, 0) + 1

    artifact_names = {artifact["path"] for artifact in artifacts}
    missing_expected = [name for name in EXPECTED_CORE_ARTIFACTS if name not in artifact_names]

    report_summaries: List[Dict[str, Any]] = []
    for artifact in artifacts:
        if artifact["extension"] != "json":
            continue
        data = safe_load_json(results_dir / artifact["path"])
        metrics = detect_metrics(data)
        if metrics:
            report_summaries.append({"path": artifact["path"], "metrics": metrics})

    status = "ok" if artifacts else "sin_artefactos"
    if missing_expected and artifacts:
        status = "ok_con_artefactos_pendientes"

    return {
        "manifest_type": "eco_operational_manifest",
        "schema_version": "0.1",
        "run_label": run_label,
        "generated_at": utc_now_iso(),
        "results_dir": str(results_dir),
        "status": status,
        "artifact_count": len(artifacts),
        "artifacts_by_extension": dict(sorted(artifacts_by_extension.items())),
        "expected_core_artifacts": list(EXPECTED_CORE_ARTIFACTS),
        "missing_expected_core_artifacts": missing_expected,
        "report_summaries": report_summaries,
        "artifacts": artifacts,
        "responsible_use": {
            "scope": "bioinformatico_educativo_y_de_portafolio",
            "medical_diagnosis": False,
            "requires_human_review_for_sensitive_use": True,
        },
    }


def markdown_table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> List[str]:
    """Crea una tabla Markdown simple."""
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return lines


def build_markdown(manifest: Dict[str, Any]) -> str:
    """Convierte el manifiesto operativo a Markdown legible."""
    extension_rows = [
        [extension, count]
        for extension, count in manifest["artifacts_by_extension"].items()
    ] or [["sin_artefactos", 0]]

    artifact_rows = [
        [
            artifact["path"],
            artifact["extension"],
            artifact["size_bytes"],
            artifact["sha256"][:12],
        ]
        for artifact in manifest["artifacts"]
    ]

    summary_rows = []
    for summary in manifest["report_summaries"]:
        metrics = ", ".join(f"{key}={value}" for key, value in summary["metrics"].items())
        summary_rows.append([summary["path"], metrics])

    missing = manifest["missing_expected_core_artifacts"]
    missing_lines = [f"- {item}" for item in missing] if missing else ["- Ninguno."]

    lines = [
        "# E.C.O. - Manifiesto operativo de corrida",
        "",
        "## Propósito",
        "",
        "Este manifiesto funciona como acta digestiva del pipeline: registra qué artefactos existen, "
        "qué métricas principales se detectaron y qué piezas esperadas siguen pendientes.",
        "",
        "## Estado general",
        "",
        *markdown_table(
            ["Campo", "Valor"],
            [
                ["Tipo", manifest["manifest_type"]],
                ["Versión de esquema", manifest["schema_version"]],
                ["Etiqueta de corrida", manifest["run_label"]],
                ["Generado UTC", manifest["generated_at"]],
                ["Estado", manifest["status"]],
                ["Artefactos detectados", manifest["artifact_count"]],
            ],
        ),
        "",
        "## Artefactos por extensión",
        "",
        *markdown_table(["Extensión", "Cantidad"], extension_rows),
        "",
        "## Artefactos esperados pendientes",
        "",
        *missing_lines,
        "",
        "## Métricas detectadas en JSON",
        "",
    ]

    if summary_rows:
        lines.extend(markdown_table(["Reporte", "Métricas"], summary_rows))
    else:
        lines.append("No se detectaron métricas resumibles en los JSON disponibles.")

    lines.extend(
        [
            "",
            "## Inventario de artefactos",
            "",
        ]
    )

    if artifact_rows:
        lines.extend(markdown_table(["Ruta", "Tipo", "Bytes", "SHA-256 corto"], artifact_rows))
    else:
        lines.append("No hay artefactos disponibles.")

    lines.extend(
        [
            "",
            "## Uso responsable",
            "",
            "- Alcance: bioinformático, educativo y de portafolio.",
            "- No entrega diagnóstico médico.",
            "- Cualquier uso sensible requiere revisión humana y contexto explícito.",
            "",
            "## Lectura E.C.O.",
            "",
            "Esta capa convierte una ejecución dispersa en memoria operacional. "
            "La futura UX conversacional debería responder citando este manifiesto, "
            "no improvisando desde archivos sueltos.",
            "",
        ]
    )

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Genera el manifiesto operativo del pipeline E.C.O.")
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--run-label", default="eco_local_run")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manifest = build_manifest(args.results_dir, run_label=args.run_label)

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(build_markdown(manifest), encoding="utf-8")

    print("E.C.O. OPERATIONAL MANIFEST")
    print("==========================")
    print(f"Resultados revisados: {args.results_dir}")
    print(f"Artefactos detectados: {manifest['artifact_count']}")
    print(f"Estado: {manifest['status']}")
    print(f"Manifiesto JSON: {args.output_json}")
    print(f"Manifiesto Markdown: {args.output_md}")
    print("Estado: OK, manifiesto operativo generado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
