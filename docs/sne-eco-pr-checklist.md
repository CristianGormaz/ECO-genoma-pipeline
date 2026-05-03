# Checklist de Pull Request — S.N.E.-E.C.O.

Antes de fusionar cambios a `main`, revisar:

## 1. Validación técnica

```bash
make sne-portfolio-demo
```

Resultado esperado:

```text
S.N.E.-E.C.O. portfolio demo ready
```

Y pruebas pasando:

```text
passed
```

## 2. Documentación

- El README sigue enlazando documentos principales.
- El índice de portafolio sigue actualizado.
- La guía de demo sigue siendo entendible para usuarios no técnicos.

## 3. Límites responsables

Confirmar que el cambio mantiene explícito que E.C.O.:

- no diagnostica;
- no tiene uso clínico;
- no tiene uso forense;
- no modela conciencia humana;
- funciona como arquitectura experimental y educativa.

## 4. Artefactos esperados

Verificar que el pipeline puede generar reportes en:

```text
results/
```

Principalmente:

```text
results/sne_eco_neurogastro_pipeline_summary.json
results/sne_eco_neurogastro_context_report.json
results/sne_eco_compare_against_rc1.json
results/sne_eco_portfolio_check.json
```

## 5. Criterio de fusión

Solo fusionar si:

```text
pipeline demo OK
tests OK
documentación OK
límites responsables OK
```
