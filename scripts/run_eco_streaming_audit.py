from __future__ import annotations

import argparse
import ast
import json
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = "eco_massification_readiness_audit_v1"
SEVERITY_ORDER = [
    "critical",
    "high",
    "medium",
    "low",
    "false_positive",
    "intentional_demo",
]
LONG_RUN_ENTRYPOINTS = [
    Path("scripts/run_eco_demo_pipeline.py"),
    Path("scripts/run_sne_eco_state_dataset.py"),
    Path("scripts/run_sne_eco_sensitive_source_registry.py"),
    Path("scripts/run_sne_eco_empirical_train_eval_split.py"),
]
RESPONSIBLE_LIMITS = [
    "No refactor todavia: primero auditar y estabilizar el baseline operativo.",
    "No tocar parsers FASTA/BED ni ingestion.py en este sprint de auditoria.",
    "No tocar EntericSystem.processed_packets ni EcoPacket en esta fase.",
    "No mover validadores ni crear checkpoint real todavia.",
    "No usar datos reales, no entrenar modelos, no modificar baseline ni recalibrar umbrales.",
]
MICRO_SPRINTS = [
    "Micro-sprint 1: auditoria anti-streaming reproducible y reporte de hallazgos.",
    "Micro-sprint 2: centralizacion de validacion ADN/FASTA/BED.",
    "Micro-sprint 3: migracion de parsers a generadores.",
    "Micro-sprint 4: procesamiento batch por chunks e incremental writers.",
    "Micro-sprint 5: politica de memoria para EntericSystem.",
    "Micro-sprint 6: checkpoint.json + JSONL incremental + resume.",
    "Micro-sprint 7: limpieza final de contratos e imports auxiliares.",
]
CODE_PATHS = [Path("src"), Path("scripts")]


@dataclass(frozen=True)
class Finding:
    severity: str
    rule_id: str
    path: str
    line: int | None
    summary: str
    evidence: str
    recommendation: str


def iter_python_files(root: Path, *top_levels: str) -> Iterable[Path]:
    for name in top_levels:
        base = root / name
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.py")):
            yield path


def is_demo_path(relative_path: Path) -> bool:
    if relative_path.parts[:1] != ("scripts",):
        return False
    demo_tokens = ("demo", "synthetic")
    return any(token in relative_path.name for token in demo_tokens)


def relative(path: Path) -> Path:
    return path.relative_to(ROOT)


def summarize_samples(matches: list[tuple[Path, int]]) -> str:
    samples = ", ".join(f"{path}:{line}" for path, line in matches[:5])
    if len(matches) > 5:
        return f"{samples}, +{len(matches) - 5} mas"
    return samples


def parse_module(path: Path) -> ast.AST:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def find_call_sites(path: Path, attrs: set[str]) -> list[tuple[int, str]]:
    tree = parse_module(path)
    source = path.read_text(encoding="utf-8")
    matches: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in attrs:
            segment = ast.get_source_segment(source, node) or source.splitlines()[node.lineno - 1].strip()
            matches.append((node.lineno, segment))
    return matches


def find_function_line(path: Path, function_name: str) -> int | None:
    tree = parse_module(path)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return node.lineno
    return None


def collect_read_findings() -> list[Finding]:
    findings: list[Finding] = []
    false_positive_matches: list[tuple[Path, int]] = []
    intentional_demo_matches: list[tuple[Path, int]] = []

    for path in iter_python_files(ROOT, "src", "scripts", "tests"):
        rel = relative(path)
        for line, segment in find_call_sites(path, {"read_text", "read_bytes"}):
            top_level = rel.parts[0]
            if top_level == "tests":
                false_positive_matches.append((rel, line))
                continue
            if top_level == "docs":
                false_positive_matches.append((rel, line))
                continue
            if is_demo_path(rel):
                intentional_demo_matches.append((rel, line))
                continue
            if rel == Path("src/eco_core/ingestion.py"):
                findings.append(
                    Finding(
                        severity="critical",
                        rule_id="read_text_full_file_ingest",
                        path=str(rel),
                        line=line,
                        summary="La ingesta central lee el archivo completo en memoria antes de construir el paquete.",
                        evidence=segment,
                        recommendation="Migrar a lectura incremental o derivar a parsers streaming en un sprint separado.",
                    )
                )
                continue
            if ".splitlines()" in segment and rel.parts[:1] == ("scripts",):
                findings.append(
                    Finding(
                        severity="high",
                        rule_id="read_text_splitlines_full_materialization",
                        path=str(rel),
                        line=line,
                        summary="El script materializa el archivo completo antes de iterar linea por linea.",
                        evidence=segment,
                        recommendation="Reemplazar por iterador de lineas o lector JSONL incremental en un sprint posterior.",
                    )
                )

    if false_positive_matches:
        findings.append(
            Finding(
                severity="false_positive",
                rule_id="tests_and_docs_read_text_are_not_massification_blockers",
                path="tests/",
                line=None,
                summary="Hay lecturas completas en tests/documentacion, pero no pertenecen al flujo productivo.",
                evidence=summarize_samples(false_positive_matches),
                recommendation="Mantenerlas fuera del alcance productivo y no tratarlas como bloqueadores de streaming.",
            )
        )
    if intentional_demo_matches:
        findings.append(
            Finding(
                severity="intentional_demo",
                rule_id="demo_scripts_may_materialize_small_payloads",
                path="scripts/",
                line=None,
                summary="Existen demos sinteticas que materializan contenido completo por simplicidad.",
                evidence=summarize_samples(intentional_demo_matches),
                recommendation="Documentar estas rutas como demo-only y no reutilizarlas como pipeline productivo.",
            )
        )
    return findings


def collect_list_materialization_findings() -> list[Finding]:
    findings: list[Finding] = []
    keywords = ("packet", "trace", "row", "record", "region", "sequence", "report", "line")

    for path in iter_python_files(ROOT, "src", "scripts"):
        rel = relative(path)
        if is_demo_path(rel):
            continue
        tree = parse_module(path)
        source = path.read_text(encoding="utf-8")
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Name) or node.func.id != "list" or len(node.args) != 1:
                continue
            argument = ast.get_source_segment(source, node.args[0]) or ""
            lowered = argument.lower()
            if not any(keyword in lowered for keyword in keywords):
                continue
            if rel == Path("src/eco_core/homeostasis.py"):
                findings.append(
                    Finding(
                        severity="high",
                        rule_id="homeostasis_materializes_all_packets",
                        path=str(rel),
                        line=node.lineno,
                        summary="La snapshot homeostatica convierte todo el iterable de paquetes a lista.",
                        evidence=argument,
                        recommendation="Aceptar iteradores y agregar contadores streaming en un sprint dedicado.",
                    )
                )
            elif rel == Path("src/eco_core/feedback.py"):
                findings.append(
                    Finding(
                        severity="high",
                        rule_id="feedback_materializes_all_packets",
                        path=str(rel),
                        line=node.lineno,
                        summary="El resumen de feedback materializa todos los paquetes antes de resumir.",
                        evidence=argument,
                        recommendation="Construir el resumen con acumuladores incrementales.",
                    )
                )
            elif rel == Path("src/eco_core/packet_trace.py"):
                findings.append(
                    Finding(
                        severity="medium",
                        rule_id="packet_trace_materializes_all_traces",
                        path=str(rel),
                        line=node.lineno,
                        summary="La exportacion de trazas exige tener la coleccion completa en memoria.",
                        evidence=argument,
                        recommendation="Agregar un escritor incremental JSONL/Markdown en un sprint posterior.",
                    )
                )
            elif rel == Path("src/eco_core/adaptive_state_dataset.py"):
                findings.append(
                    Finding(
                        severity="medium",
                        rule_id="adaptive_state_rows_materialized_for_rendering",
                        path=str(rel),
                        line=node.lineno,
                        summary="El dataset adaptativo convierte filas a lista completa para renderizar.",
                        evidence=argument,
                        recommendation="Separar construccion del dataset de la renderizacion final.",
                    )
                )
    return findings


def collect_processed_packets_findings() -> list[Finding]:
    path = ROOT / "src/eco_core/enteric_orchestrator.py"
    content = path.read_text(encoding="utf-8")
    rel = relative(path)
    assignment_line = None
    append_line = None
    for index, line in enumerate(content.splitlines(), start=1):
        if "self.processed_packets" in line and "=" in line and assignment_line is None:
            assignment_line = index
        if "self.processed_packets.append(" in line:
            append_line = index
    if assignment_line is None or append_line is None:
        return []
    if "max_processed_packets" in content or "trace_exporter" in content:
        return []
    return [
        Finding(
            severity="high",
            rule_id="processed_packets_without_memory_policy",
            path=str(rel),
            line=assignment_line,
            summary="EntericSystem conserva processed_packets sin una politica explicita de memoria o flush.",
            evidence=f"Inicializacion en linea {assignment_line}; append en linea {append_line}.",
            recommendation="Definir modo demo vs batch, buffer acotado y exportacion incremental de trazas.",
        )
    ]


def collect_streaming_candidate_findings() -> list[Finding]:
    configured = {
        Path("src/eco_bed_to_fasta.py"): {
            "parse_fasta": (
                "high",
                "FASTA completo se carga en un diccionario antes de procesar regiones.",
                "Migrar a iter_fasta_records(path) en un sprint posterior.",
            ),
            "parse_bed": (
                "high",
                "BED completo se carga en una lista antes de generar FASTA.",
                "Migrar a iter_bed_records(path) y escribir FASTA incrementalmente.",
            ),
            "bed_to_fasta": (
                "medium",
                "La conversion BED->FASTA devuelve una lista completa de registros.",
                "Permitir escritor incremental de FASTA o batch por chunks.",
            ),
        },
        Path("src/eco_motif_analysis.py"): {
            "parse_fasta": (
                "high",
                "El analisis de motivos requiere todo el FASTA en memoria.",
                "Separar parser iterativo del calculo por secuencia.",
            ),
        },
        Path("src/eco_sequence_classifier.py"): {
            "parse_labeled_sequences_tsv": (
                "high",
                "El clasificador lee todas las secuencias etiquetadas a una lista.",
                "Agregar iterador TSV y feature extraction por lotes/chunks.",
            ),
            "extract_feature_map": (
                "medium",
                "El mapa completo de features se materializa antes del uso posterior.",
                "Permitir recorrido incremental o chunked para evaluaciones largas.",
            ),
        },
        Path("src/eco_core/adaptive_state_dataset.py"): {
            "build_adaptive_state_rows": (
                "medium",
                "El dataset adaptativo se construye como lista completa de filas.",
                "Separar recoleccion incremental y exportacion final.",
            ),
        },
        Path("scripts/run_eco_demo_pipeline.py"): {
            "run_demo_pipeline": (
                "intentional_demo",
                "El pipeline demo materializa referencia, regiones, FASTA y paquetes por simplicidad.",
                "Mantenerlo como demo-only y no reutilizarlo como base de masificacion productiva.",
            ),
        },
    }
    findings: list[Finding] = []
    for relative_path, functions in configured.items():
        path = ROOT / relative_path
        for function_name, (severity, summary, recommendation) in functions.items():
            line = find_function_line(path, function_name)
            if line is None:
                continue
            findings.append(
                Finding(
                    severity=severity,
                    rule_id=f"streaming_candidate::{function_name}",
                    path=str(relative_path),
                    line=line,
                    summary=summary,
                    evidence=f"Funcion detectada: {function_name}",
                    recommendation=recommendation,
                )
            )
    return findings


def collect_checkpoint_findings() -> list[Finding]:
    required_tokens = ("checkpoint", "resume", "last_processed_record", "run_id")
    missing_paths: list[str] = []
    for relative_path in LONG_RUN_ENTRYPOINTS:
        content = (ROOT / relative_path).read_text(encoding="utf-8").lower()
        if not any(token in content for token in required_tokens):
            missing_paths.append(str(relative_path))
    if not missing_paths:
        return []
    return [
        Finding(
            severity="high",
            rule_id="missing_resume_checkpoint_contract",
            path=missing_paths[0],
            line=1,
            summary="No hay contrato explicito de checkpoint/resume en los entrypoints de corrida larga auditados.",
            evidence=", ".join(missing_paths),
            recommendation="Agregar checkpoint.json, JSONL incremental y resume en un micro-sprint dedicado.",
        )
    ]


def dedupe_findings(findings: Iterable[Finding]) -> list[Finding]:
    unique: dict[tuple[str, str, str, int | None], Finding] = {}
    for finding in findings:
        key = (finding.severity, finding.rule_id, finding.path, finding.line)
        unique[key] = finding
    ordered = list(unique.values())
    severity_rank = {severity: index for index, severity in enumerate(SEVERITY_ORDER)}
    ordered.sort(key=lambda item: (severity_rank[item.severity], item.path, item.line or 0, item.rule_id))
    return ordered


def build_report() -> dict:
    findings = dedupe_findings(
        [
            *collect_read_findings(),
            *collect_list_materialization_findings(),
            *collect_processed_packets_findings(),
            *collect_streaming_candidate_findings(),
            *collect_checkpoint_findings(),
        ]
    )
    counts = Counter(finding.severity for finding in findings)
    summary = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_findings": len(findings),
        "by_severity": {severity: counts.get(severity, 0) for severity in SEVERITY_ORDER},
        "baseline_gate": "No refactor todavia: make check-fast debe mantenerse verde antes de cambiar streaming.",
        "scope": "audit_only",
        "touches_pipeline_semantics": False,
    }
    return {
        "title": "E.C.O. massification readiness audit",
        "summary": summary,
        "responsible_limits": RESPONSIBLE_LIMITS,
        "micro_sprints": MICRO_SPRINTS,
        "findings": [asdict(finding) for finding in findings],
    }


def render_markdown(report: dict) -> str:
    summary = report["summary"]
    lines = [
        "# E.C.O. massification readiness audit",
        "",
        "Estado: audit_only.",
        "",
        "## Gate operativo",
        "",
        "- No refactor todavia: make check-fast debe permanecer verde antes de tocar streaming.",
        "- Este reporte no cambia semantica de pipeline, no mueve validadores y no introduce checkpoint real.",
        "",
        "## Resumen",
        "",
        f"- schema_version: `{summary['schema_version']}`",
        f"- generated_at: `{summary['generated_at']}`",
        f"- total_findings: `{summary['total_findings']}`",
    ]
    for severity in SEVERITY_ORDER:
        lines.append(f"- {severity}: `{summary['by_severity'][severity]}`")
    lines.extend(
        [
            "",
            "## Hallazgos",
            "",
            "| severity | rule_id | path | line | summary |",
            "|---|---|---|---|---|",
        ]
    )
    for finding in report["findings"]:
        line = finding["line"] if finding["line"] is not None else "-"
        summary_text = finding["summary"].replace("|", "/")
        lines.append(
            f"| {finding['severity']} | {finding['rule_id']} | {finding['path']} | {line} | {summary_text} |"
        )
        lines.append(f"  Evidencia: {finding['evidence']}")
        lines.append(f"  Recomendacion: {finding['recommendation']}")
    lines.extend(
        [
            "",
            "## Micro-sprints recomendados",
            "",
            *[f"- {item}" for item in report["micro_sprints"]],
            "",
            "## Limites responsables",
            "",
            *[f"- {item}" for item in report["responsible_limits"]],
            "",
            "## Comando sugerido",
            "",
            "`python scripts/run_eco_streaming_audit.py --output-json /tmp/eco_streaming_audit.json --output-md docs/operations/eco-massification-readiness-audit.md`",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audita riesgos anti-streaming de E.C.O. sin refactorizar el pipeline.")
    parser.add_argument("--output-json", type=Path, default=None, help="Ruta opcional para guardar el reporte JSON.")
    parser.add_argument("--output-md", type=Path, default=None, help="Ruta opcional para guardar el reporte Markdown.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report()
    markdown = render_markdown(report)

    if args.output_json is not None:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.output_md is not None:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.write_text(markdown, encoding="utf-8")

    print("# E.C.O. massification readiness audit")
    print(f"Hallazgos: {report['summary']['total_findings']}")
    print(report["summary"]["baseline_gate"])
    if args.output_json is not None:
        print(f"JSON: {args.output_json}")
    if args.output_md is not None:
        print(f"Markdown: {args.output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
