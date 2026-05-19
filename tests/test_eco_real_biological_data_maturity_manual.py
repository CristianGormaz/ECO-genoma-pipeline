from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "operations" / "eco-real-biological-data-maturity-manual.md"


def test_real_biological_data_maturity_manual_exists_and_states_status():
    assert DOC.exists()
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "Manual de Madurez para Datos Reales Biológicos",
        "no habilita uso de datos reales",
        "no aprueba procesamiento de datos reales por sí mismo",
        "rechazar, pausar, auditar y explicar",
        "dato real biológico",
    ]

    for token in required_tokens:
        assert token in content


def test_real_biological_data_maturity_manual_defines_real_biological_data():
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "secuencias genéticas",
        "secuencias genómicas",
        "datos moleculares",
        "proteínas",
        "variantes",
        "anotaciones biológicas",
        "metadatos clínicos",
        "metadatos poblacionales",
        "estructuras provenientes de bases científicas reales",
        "organismos, individuos, muestras o sistemas biológicos observados",
    ]

    for token in required_tokens:
        assert token in content


def test_real_biological_data_maturity_manual_defines_maturity_controls():
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "Rojo",
        "Amarillo",
        "Verde",
        "compuerta ética",
        "compuerta de fuente",
        "compuerta técnica",
        "compuerta de seguridad",
        "compuerta interpretativa",
        "compuerta de revisión humana",
        "compuerta de rollback",
        "compuerta de evidencia",
        "bloqueado",
        "pausado",
        "requiere revisión humana",
        "permitido limitado",
        "rechazado",
    ]

    for token in required_tokens:
        assert token in content


def test_real_biological_data_maturity_manual_requires_evidence_and_future_limits():
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "manifiesto de fuente",
        "clasificación de sensibilidad",
        "decisión humana",
        "reporte auditable",
        "registro de rollback",
        "límites interpretativos",
        "público",
        "no humano o de bajo riesgo",
        "licencia clara",
        "sin identificadores personales",
        "sin finalidad clínica",
        "validación técnica limitada",
    ]

    for token in required_tokens:
        assert token in content


def test_real_biological_data_maturity_manual_declares_responsible_limits():
    content = DOC.read_text(encoding="utf-8")

    required_tokens = [
        "sin datos reales en esta fase",
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


def test_real_biological_data_maturity_manual_has_no_executable_code_blocks():
    content = DOC.read_text(encoding="utf-8")

    forbidden_tokens = [
        "```python",
        "```bash",
        "```sh",
        "```sql",
    ]

    for token in forbidden_tokens:
        assert token not in content
