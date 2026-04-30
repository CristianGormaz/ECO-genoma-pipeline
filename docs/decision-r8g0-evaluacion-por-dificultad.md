# E.C.O. - Evaluación por dificultad de casos

## Propósito

Este informe evalúa si `embedding_semireal` mejora frente a `baseline_v3` según dificultad del caso: `easy`, `ambiguous` y `hard`.

## Configuración

| Campo | Valor |
| --- | --- |
| Dataset | examples/eco_labeled_sequences.tsv |
| Repeticiones | 50 |
| Test ratio | 0.4 |
| Seed base | 42 |
| Embedding | kmer_frequency_semireal |
| k | 4 |
| Dimensiones | 128 |
| Decisión | candidato_preoficial_condicional |

## Resumen por dificultad

| Dificultad | V3 F1 prom. | V3 std | Semi-real F1 prom. | Semi-real std | Delta | Gana/Empata/Pierde | Decisión local |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| easy | 0.9356 | 0.081 | 0.7456 | 0.1981 | -0.1899 | 0/16/34 | mixta |
| ambiguous | 0.7621 | 0.2055 | 0.7862 | 0.1332 | 0.0241 | 26/6/18 | favorable |
| hard | 0.742 | 0.2336 | 0.9256 | 0.0973 | 0.1836 | 31/16/3 | favorable |

## Decisión E.C.O.

**Decisión:** `candidato_preoficial_condicional`

Lectura prudente:

- Si la mejora aparece solo en `easy`, no se promueve.
- Si la mejora aparece en `ambiguous` o `hard`, la señal es más útil.
- Si además baja la variabilidad, puede avanzar como candidato pre-oficial condicional.

## Detalle por repetición

| Seed | Dificultad | N | V3 F1 | Semi-real F1 | Delta | Mejor |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 42 | ambiguous | 13 | 0.6061 | 0.8452 | 0.2392 | embedding_semireal |
| 42 | hard | 6 | 0.3333 | 1.0 | 0.6667 | embedding_semireal |
| 42 | easy | 5 | 1.0 | 0.7619 | -0.2381 | baseline_v3 |
| 43 | hard | 8 | 0.5636 | 1.0 | 0.4364 | embedding_semireal |
| 43 | ambiguous | 9 | 0.4156 | 0.8831 | 0.4675 | embedding_semireal |
| 43 | easy | 7 | 1.0 | 1.0 | 0.0 | tie |
| 44 | easy | 8 | 1.0 | 0.7333 | -0.2667 | baseline_v3 |
| 44 | ambiguous | 7 | 0.7083 | 0.8444 | 0.1361 | embedding_semireal |
| 44 | hard | 9 | 0.8831 | 0.8831 | 0.0 | tie |
| 45 | ambiguous | 9 | 1.0 | 0.8889 | -0.1111 | baseline_v3 |
| 45 | hard | 7 | 0.65 | 1.0 | 0.35 | embedding_semireal |
| 45 | easy | 8 | 0.8545 | 0.8545 | 0.0 | tie |
| 46 | easy | 10 | 0.899 | 0.5833 | -0.3157 | baseline_v3 |
| 46 | ambiguous | 7 | 0.8444 | 1.0 | 0.1556 | embedding_semireal |
| 46 | hard | 7 | 1.0 | 0.8444 | -0.1556 | baseline_v3 |
| 47 | ambiguous | 6 | 1.0 | 0.625 | -0.375 | baseline_v3 |
| 47 | easy | 8 | 1.0 | 0.3333 | -0.6667 | baseline_v3 |
| 47 | hard | 10 | 0.7917 | 1.0 | 0.2083 | embedding_semireal |
| 48 | hard | 9 | 0.5 | 0.775 | 0.275 | embedding_semireal |
| 48 | easy | 4 | 1.0 | 1.0 | 0.0 | tie |
| 48 | ambiguous | 11 | 0.6118 | 0.7179 | 0.1062 | embedding_semireal |
| 49 | ambiguous | 7 | 1.0 | 0.7083 | -0.2917 | baseline_v3 |
| 49 | hard | 10 | 0.2857 | 0.899 | 0.6133 | embedding_semireal |
| 49 | easy | 7 | 0.8571 | 0.7083 | -0.1488 | baseline_v3 |
| 50 | ambiguous | 11 | 0.8167 | 0.9091 | 0.0924 | embedding_semireal |
| 50 | easy | 7 | 0.8444 | 0.65 | -0.1944 | baseline_v3 |
| 50 | hard | 6 | 1.0 | 1.0 | 0.0 | tie |
| 51 | hard | 7 | 1.0 | 1.0 | 0.0 | tie |
| 51 | easy | 10 | 0.8901 | 0.7619 | -0.1282 | baseline_v3 |
| 51 | ambiguous | 7 | 1.0 | 1.0 | 0.0 | tie |
| 52 | ambiguous | 8 | 0.873 | 0.7333 | -0.1397 | baseline_v3 |
| 52 | hard | 7 | 0.8444 | 0.8444 | 0.0 | tie |
| 52 | easy | 9 | 0.8889 | 0.775 | -0.1139 | baseline_v3 |
| 53 | easy | 8 | 1.0 | 0.873 | -0.127 | baseline_v3 |
| 53 | ambiguous | 10 | 0.6703 | 0.697 | 0.0266 | embedding_semireal |
| 53 | hard | 6 | 0.8286 | 1.0 | 0.1714 | embedding_semireal |
| 54 | ambiguous | 7 | 0.8444 | 0.7083 | -0.1361 | baseline_v3 |
| 54 | hard | 8 | 0.7333 | 1.0 | 0.2667 | embedding_semireal |
| 54 | easy | 9 | 0.75 | 0.5846 | -0.1654 | baseline_v3 |
| 55 | easy | 7 | 0.8444 | 0.8444 | 0.0 | tie |
| 55 | ambiguous | 11 | 0.8036 | 0.8167 | 0.0131 | embedding_semireal |
| 55 | hard | 6 | 0.8286 | 1.0 | 0.1714 | embedding_semireal |
| 56 | hard | 9 | 1.0 | 0.8889 | -0.1111 | baseline_v3 |
| 56 | easy | 8 | 0.873 | 0.7333 | -0.1397 | baseline_v3 |
| 56 | ambiguous | 7 | 1.0 | 0.8571 | -0.1429 | baseline_v3 |
| 57 | easy | 10 | 0.8 | 0.5833 | -0.2167 | baseline_v3 |
| 57 | ambiguous | 5 | 1.0 | 0.5833 | -0.4167 | baseline_v3 |
| 57 | hard | 9 | 1.0 | 1.0 | 0.0 | tie |
| 58 | easy | 8 | 0.8545 | 0.8545 | 0.0 | tie |
| 58 | ambiguous | 11 | 0.6857 | 0.6071 | -0.0786 | baseline_v3 |
| 58 | hard | 5 | 0.5833 | 0.8 | 0.2167 | embedding_semireal |
| 59 | easy | 7 | 1.0 | 1.0 | 0.0 | tie |
| 59 | hard | 9 | 1.0 | 1.0 | 0.0 | tie |
| 59 | ambiguous | 8 | 0.619 | 0.7333 | 0.1143 | embedding_semireal |
| 60 | ambiguous | 10 | 0.7619 | 0.4949 | -0.267 | baseline_v3 |
| 60 | hard | 10 | 0.5833 | 0.697 | 0.1136 | embedding_semireal |
| 60 | easy | 4 | 1.0 | 1.0 | 0.0 | tie |
| 61 | hard | 8 | 1.0 | 0.873 | -0.127 | baseline_v3 |
| 61 | easy | 9 | 0.8831 | 0.5846 | -0.2985 | baseline_v3 |
| 61 | ambiguous | 7 | 1.0 | 1.0 | 0.0 | tie |
| 62 | easy | 9 | 1.0 | 0.775 | -0.225 | baseline_v3 |
| 62 | hard | 9 | 0.75 | 0.8831 | 0.1331 | embedding_semireal |
| 62 | ambiguous | 6 | 0.7778 | 0.7778 | 0.0 | tie |
| 63 | easy | 8 | 1.0 | 0.7333 | -0.2667 | baseline_v3 |
| 63 | ambiguous | 8 | 0.3651 | 0.75 | 0.3849 | embedding_semireal |
| 63 | hard | 8 | 0.2727 | 0.873 | 0.6003 | embedding_semireal |
| 64 | hard | 12 | 0.4126 | 1.0 | 0.5874 | embedding_semireal |
| 64 | easy | 7 | 1.0 | 0.8444 | -0.1556 | baseline_v3 |
| 64 | ambiguous | 5 | 1.0 | 0.8 | -0.2 | baseline_v3 |
| 65 | hard | 8 | 0.8545 | 0.8545 | 0.0 | tie |
| 65 | easy | 10 | 0.7917 | 0.3333 | -0.4583 | baseline_v3 |
| 65 | ambiguous | 6 | 1.0 | 0.7778 | -0.2222 | baseline_v3 |
| 66 | hard | 10 | 0.4949 | 0.899 | 0.404 | embedding_semireal |
| 66 | easy | 8 | 1.0 | 0.75 | -0.25 | baseline_v3 |
| 66 | ambiguous | 6 | 1.0 | 0.6667 | -0.3333 | baseline_v3 |
| 67 | ambiguous | 11 | 0.3125 | 0.7179 | 0.4054 | embedding_semireal |
| 67 | hard | 7 | 0.7083 | 0.8571 | 0.1488 | embedding_semireal |
| 67 | easy | 6 | 1.0 | 1.0 | 0.0 | tie |
| 68 | easy | 11 | 0.8036 | 0.8036 | 0.0 | tie |
| 68 | hard | 9 | 1.0 | 1.0 | 0.0 | tie |
| 68 | ambiguous | 4 | 1.0 | 1.0 | 0.0 | tie |
| 69 | hard | 9 | 1.0 | 1.0 | 0.0 | tie |
| 69 | easy | 10 | 0.7917 | 0.7917 | 0.0 | tie |
| 69 | ambiguous | 5 | 1.0 | 0.5833 | -0.4167 | baseline_v3 |
| 70 | hard | 10 | 0.7917 | 1.0 | 0.2083 | embedding_semireal |
| 70 | easy | 5 | 1.0 | 1.0 | 0.0 | tie |
| 70 | ambiguous | 9 | 0.3571 | 0.6494 | 0.2922 | embedding_semireal |
| 71 | ambiguous | 8 | 0.619 | 0.8545 | 0.2355 | embedding_semireal |
| 71 | easy | 9 | 0.8889 | 0.775 | -0.1139 | baseline_v3 |
| 71 | hard | 7 | 1.0 | 1.0 | 0.0 | tie |
| 72 | easy | 9 | 0.8889 | 0.3077 | -0.5812 | baseline_v3 |
| 72 | ambiguous | 11 | 1.0 | 0.7179 | -0.2821 | baseline_v3 |
| 72 | hard | 4 | 1.0 | 1.0 | 0.0 | tie |
| 73 | ambiguous | 10 | 0.6 | 0.6703 | 0.0703 | embedding_semireal |
| 73 | hard | 10 | 0.375 | 0.7917 | 0.4167 | embedding_semireal |
| 73 | easy | 4 | 1.0 | 1.0 | 0.0 | tie |
| 74 | ambiguous | 7 | 0.7083 | 0.8444 | 0.1361 | embedding_semireal |
| 74 | hard | 10 | 0.5833 | 1.0 | 0.4167 | embedding_semireal |
| 74 | easy | 7 | 1.0 | 0.7083 | -0.2917 | baseline_v3 |
| 75 | hard | 11 | 0.8167 | 0.8167 | 0.0 | tie |
| 75 | ambiguous | 8 | 0.5636 | 0.6667 | 0.103 | embedding_semireal |
| 75 | easy | 5 | 1.0 | 1.0 | 0.0 | tie |
| 76 | ambiguous | 9 | 0.8831 | 0.775 | -0.1081 | baseline_v3 |
| 76 | hard | 8 | 1.0 | 1.0 | 0.0 | tie |
| 76 | easy | 7 | 1.0 | 0.7083 | -0.2917 | baseline_v3 |
| 77 | ambiguous | 9 | 0.5846 | 0.55 | -0.0346 | baseline_v3 |
| 77 | hard | 8 | 0.619 | 0.873 | 0.254 | embedding_semireal |
| 77 | easy | 7 | 1.0 | 0.7083 | -0.2917 | baseline_v3 |
| 78 | hard | 7 | 0.3636 | 0.65 | 0.2864 | embedding_semireal |
| 78 | ambiguous | 11 | 0.4762 | 0.6333 | 0.1571 | embedding_semireal |
| 78 | easy | 6 | 1.0 | 1.0 | 0.0 | tie |
| 79 | easy | 7 | 1.0 | 0.8571 | -0.1429 | baseline_v3 |
| 79 | ambiguous | 9 | 0.55 | 0.775 | 0.225 | embedding_semireal |
| 79 | hard | 8 | 0.7333 | 1.0 | 0.2667 | embedding_semireal |
| 80 | ambiguous | 10 | 0.8 | 0.8901 | 0.0901 | embedding_semireal |
| 80 | hard | 9 | 0.75 | 1.0 | 0.25 | embedding_semireal |
| 80 | easy | 5 | 1.0 | 0.7619 | -0.2381 | baseline_v3 |
| 81 | hard | 9 | 0.8831 | 0.8831 | 0.0 | tie |
| 81 | easy | 10 | 0.899 | 0.5238 | -0.3752 | baseline_v3 |
| 81 | ambiguous | 5 | 1.0 | 1.0 | 0.0 | tie |
| 82 | hard | 8 | 0.2 | 0.8545 | 0.6545 | embedding_semireal |
| 82 | ambiguous | 11 | 0.4107 | 0.6333 | 0.2226 | embedding_semireal |
| 82 | easy | 5 | 1.0 | 1.0 | 0.0 | tie |
| 83 | ambiguous | 6 | 0.8286 | 0.8286 | 0.0 | tie |
| 83 | hard | 9 | 1.0 | 1.0 | 0.0 | tie |
| 83 | easy | 9 | 1.0 | 0.6667 | -0.3333 | baseline_v3 |
| 84 | hard | 9 | 0.6494 | 0.8889 | 0.2395 | embedding_semireal |
| 84 | easy | 7 | 1.0 | 0.65 | -0.35 | baseline_v3 |
| 84 | ambiguous | 8 | 0.619 | 1.0 | 0.381 | embedding_semireal |
| 85 | ambiguous | 8 | 1.0 | 0.873 | -0.127 | baseline_v3 |
| 85 | hard | 6 | 0.8286 | 1.0 | 0.1714 | embedding_semireal |
| 85 | easy | 10 | 0.7917 | 0.5238 | -0.2679 | baseline_v3 |
| 86 | easy | 7 | 1.0 | 1.0 | 0.0 | tie |
| 86 | ambiguous | 10 | 0.7917 | 0.8 | 0.0083 | embedding_semireal |
| 86 | hard | 7 | 0.3636 | 0.65 | 0.2864 | embedding_semireal |
| 87 | ambiguous | 10 | 0.8 | 1.0 | 0.2 | embedding_semireal |
| 87 | hard | 6 | 0.7778 | 1.0 | 0.2222 | embedding_semireal |
| 87 | easy | 8 | 1.0 | 0.873 | -0.127 | baseline_v3 |
| 88 | ambiguous | 10 | 0.697 | 0.899 | 0.202 | embedding_semireal |
| 88 | hard | 7 | 0.7879 | 1.0 | 0.2121 | embedding_semireal |
| 88 | easy | 7 | 1.0 | 0.2222 | -0.7778 | baseline_v3 |
| 89 | easy | 9 | 0.8831 | 0.5846 | -0.2985 | baseline_v3 |
| 89 | ambiguous | 8 | 0.7333 | 1.0 | 0.2667 | embedding_semireal |
| 89 | hard | 7 | 1.0 | 1.0 | 0.0 | tie |
| 90 | hard | 7 | 0.8444 | 1.0 | 0.1556 | embedding_semireal |
| 90 | ambiguous | 10 | 0.4949 | 0.7917 | 0.2967 | embedding_semireal |
| 90 | easy | 7 | 1.0 | 0.7083 | -0.2917 | baseline_v3 |
| 91 | easy | 10 | 0.8 | 0.4505 | -0.3495 | baseline_v3 |
| 91 | hard | 6 | 0.8286 | 1.0 | 0.1714 | embedding_semireal |
| 91 | ambiguous | 8 | 0.873 | 0.7333 | -0.1397 | baseline_v3 |

## Límites responsables

- Dataset demostrativo pequeño.
- No es DNABERT.
- No es diagnóstico clínico.
- No representa benchmark científico general.
- La decisión debe validarse con datos externos antes de cualquier conclusión fuerte.
