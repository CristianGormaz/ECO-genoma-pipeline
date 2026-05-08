# Onboarding técnico (30 minutos)

Guía rápida para que una persona técnica pueda preparar el entorno, ejecutar una validación mínima, correr una demo y ubicar los módulos núcleo del pipeline E.C.O.

## 1) Preparar entorno (10 min)

```bash
git clone https://github.com/CristianGormaz/ECO-genoma-pipeline.git
cd ECO-genoma-pipeline
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
```

Alternativa activando el entorno virtual:

```bash
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## 2) Ejecutar validación mínima (8 min)

Ejecuta el set mínimo para comprobar que el proyecto está sano en local:

```bash
make check-fast
```

Si prefieres correr comandos directos equivalentes:

```bash
.venv/bin/python -m pytest -q
make sne-validation
make sne-state-confusion
```

Resultado esperado (resumen):

- Tests en verde.
- `Rutas confundidas: 0` en el reporte de confusión de estado.

## 3) Correr script de demo (5 min)

Para una demo rápida del componente S.N.E.-E.C.O. ejecuta:

```bash
.venv/bin/python scripts/run_sne_eco_recurrence_audit.py
```

Artefactos esperados:

- `results/sne_eco_recurrence_audit.md`
- `results/sne_eco_recurrence_audit.json`

## 4) Ubicar módulos núcleo en `src/eco_core` (5 min)

Ruta principal:

```text
src/eco_core/
```

Módulos clave para orientarte:

- `enteric_system.py` → coordinación general del sistema entérico.
- `barrier.py` → barrera/mucosa informacional.
- `sensor_local.py` → sensado submucoso local.
- `motility.py` → tránsito operativo (plexo mientérico).
- `microbiota.py` → memoria adaptativa y recurrencia.
- `defense.py` → defensa inmune informacional.
- `homeostasis.py` → equilibrio operativo.
- `gut_brain_axis.py` → reporte interpretable del estado interno.

## 5) Checklist de PR antes de abrir cambios

- [ ] Corrí `make check-fast` sin errores.
- [ ] Si toqué lógica S.N.E., revisé `make sne-state-confusion`.
- [ ] Si toqué recurrencia, corrí `scripts/run_sne_eco_recurrence_audit.py`.
- [ ] Actualicé documentación relevante (`README`, `docs/`).
- [ ] Incluí contexto técnico claro en el PR (qué cambia, por qué, cómo validé).
