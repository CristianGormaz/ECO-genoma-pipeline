from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = (
    ROOT
    / "docs"
    / "operations"
    / "eco-real-biological-data-admission-protocol.md"
)


def test_real_biological_data_admission_protocol_exists_and_states_status():
    assert DOC.exists()
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "Protocolo de Admisión de Datos Reales Biológicos",
        "no habilita uso de datos reales",
        "no aprueba procesamiento de datos reales por sí mismo",
        "no reemplaza revisión humana",
    ]

    for token in required_tokens:
        assert token in content


def test_real_biological_data_admission_protocol_relates_to_maturity_manual():
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "docs/operations/eco-real-biological-data-maturity-manual.md",
        "punto de madurez",
        "procedimiento documental previo",
    ]

    for token in required_tokens:
        assert token in content


def test_real_biological_data_admission_protocol_defines_documental_flow():
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "solicitud de admisión",
        "identificación de fuente",
        "clasificación de sensibilidad",
        "revisión de licencia o permiso",
        "revisión técnica previa",
        "revisión ética",
        "revisión interpretativa",
        "revisión humana",
        "decisión registrada",
        "evidencia auditable",
        "rollback",
        "rechazo",
    ]

    for token in required_tokens:
        assert token in content


def test_real_biological_data_admission_protocol_defines_minimum_gates():
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "compuerta ética",
        "compuerta de fuente",
        "compuerta técnica",
        "compuerta de seguridad",
        "compuerta interpretativa",
        "compuerta de revisión humana",
        "compuerta de rollback",
        "compuerta de evidencia",
    ]

    for token in required_tokens:
        assert token in content


def test_real_biological_data_admission_protocol_defines_decision_states():
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "bloqueado",
        "pausado",
        "requiere revisión humana",
        "permitido limitado",
        "rechazado",
    ]

    for token in required_tokens:
        assert token in content


def test_real_biological_data_admission_protocol_requires_minimum_evidence():
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "manifiesto de fuente",
        "clasificación de sensibilidad",
        "licencia o permiso",
        "decisión humana",
        "reporte auditable",
        "registro de rollback",
        "límites interpretativos",
    ]

    for token in required_tokens:
        assert token in content


def test_real_biological_data_admission_protocol_requires_mandatory_rejection():
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "fuente clara",
        "licencia o permiso",
        "clasificación de sensibilidad",
        "revisión humana",
        "evidencia auditable",
        "límites interpretativos",
        "rollback",
        "ausencia de finalidad clínica",
        "ausencia de identificadores personales",
    ]

    for token in required_tokens:
        assert token in content


def test_real_biological_data_admission_protocol_limits_future_first_use():
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "público",
        "no humano o de bajo riesgo",
        "sin identificadores personales",
        "sin finalidad clínica",
        "licencia clara",
        "validación técnica limitada",
    ]

    for token in required_tokens:
        assert token in content


def test_real_biological_data_admission_protocol_declares_responsible_limits():
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "sin datos reales en esta fase",
        "sin ingestión de datos reales",
        "sin entrenamiento",
        "sin modificación de baseline",
        "sin recalibración de umbrales",
        "sin diagnóstico",
        "sin interpretación clínica",
        "sin riesgo genético individual",
        "sin afirmaciones biomédicas aplicadas",
        "sin autonomía real",
        "sin conciencia",
        "sin libre albedrío real",
    ]

    for token in required_tokens:
        assert token in content


def test_real_biological_data_admission_protocol_has_no_executable_code_blocks():
    content = DOC.read_text(encoding="utf-8")

    forbidden_tokens = [
        "```python",
        "```bash",
        "```sh",
        "```sql",
    ]

    for token in forbidden_tokens:
        assert token not in content
