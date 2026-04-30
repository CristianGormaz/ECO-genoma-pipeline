# Nota técnica: ruta de embeddings placeholder

## Propósito

Esta nota documenta la ruta experimental `embedding-placeholder` de **E.C.O. — Entérico Codificador Orgánico**.

Su objetivo no es reemplazar a DNABERT ni declarar un modelo avanzado. Su función es preparar el contrato arquitectónico que permitirá comparar embeddings reales contra baselines ya existentes.

## Contexto

E.C.O. ya cuenta con tres referencias internas:

```text
baseline_v1 = control mínimo explicable
baseline_v2 = variante exploratoria no principal
baseline_v3 = candidato principal pre-embeddings
```

Antes de incorporar modelos pesados, conviene crear una ruta liviana que pruebe el flujo completo:

```text
secuencia
→ vector/embedding
→ normalización
→ clasificador
→ comparación contra v1/v3
→ reporte JSON/Markdown/HTML
```

## Qué hace el placeholder

El script:

```text
scripts/run_eco_embedding_placeholder.py
```

convierte cada secuencia en un vector determinista basado en frecuencias k-mer agrupadas en dimensiones fijas.

Configuración actual:

```text
embedding_type = kmer_frequency_placeholder
embedding_k = 3
embedding_dimensions = 64
feature_scaling = minmax_train
```

Esto permite validar el flujo vectorial sin descargar modelos externos ni agregar dependencias pesadas.

## Comandos

```bash
make embedding-placeholder
make open-embedding-placeholder
```

Salidas:

```text
results/eco_embedding_placeholder_report.json
results/eco_embedding_placeholder_report.md
results/eco_embedding_placeholder_report.html
```

## Comparación esperada

El reporte compara tres rutas:

| Modelo | Rol | Lectura |
|---|---|---|
| baseline_v1 | Control explicable | Referencia mínima simple. |
| baseline_v3 | Candidato pre-embeddings | Mejor baseline actual con k=3. |
| embedding_placeholder | Contrato vectorial | Ruta experimental para futura conexión con embeddings reales. |

## Decisión arquitectónica

```text
v1 y v3 siguen siendo las referencias principales.
embedding-placeholder valida el enchufe técnico para una ruta DNABERT futura.
```

Si un embedding real se integra más adelante, debe demostrar mejora frente a:

```text
baseline_v1
baseline_v3
```

## Límites

- No es DNABERT.
- No usa modelo profundo.
- No descarga pesos externos.
- No representa benchmark científico.
- No entrega interpretación clínica.
- No reemplaza validación externa.

## Próximo paso lógico

Mantener esta ruta como capa estable de comparación y luego crear una variante futura, por ejemplo:

```text
scripts/run_eco_embedding_real.py
```

Esa variante debería reutilizar el mismo contrato de salida para que la comparación sea limpia, medible y trazable.
