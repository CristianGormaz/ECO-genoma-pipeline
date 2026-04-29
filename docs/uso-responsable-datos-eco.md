# Uso responsable de datos públicos en E.C.O.

Este documento resume las reglas prácticas para usar datos públicos, especialmente ClinVar/NCBI, dentro del proyecto **E.C.O. — Entérico Codificador Orgánico**.

> Este documento no es asesoría legal. Es una guía operativa de uso responsable para reducir riesgos de atribución, privacidad, interpretación y redistribución.

## 1. Fuente de datos

E.C.O. puede usar datos públicos de ClinVar/NCBI para demostraciones bioinformáticas, reportes educativos y validación técnica del pipeline.

Cuando se usen datos de ClinVar, el proyecto debe declarar explícitamente:

- fuente: ClinVar/NCBI;
- archivo o endpoint usado;
- fecha o modo de descarga cuando sea posible;
- que el resultado es interpretativo y no diagnóstico.

Ejemplo recomendado:

```text
Datos públicos obtenidos desde ClinVar/NCBI. Este reporte es una interpretación bioinformática educativa y no constituye diagnóstico médico ni recomendación clínica.
```

## 2. Atribución

Si E.C.O. copia, distribuye o muestra datos derivados de ClinVar, debe reconocer a ClinVar/NCBI como fuente.

Texto recomendado para README, reportes o portafolio:

```text
Este proyecto utiliza datos públicos de ClinVar/NCBI como fuente de registros de variantes. ClinVar debe ser citado como fuente de datos. Las clasificaciones externas pertenecen a los submitters o fuentes declaradas por ClinVar.
```

## 3. No redistribuir bases completas

E.C.O. no debe subir al repositorio descargas completas de bases externas como:

- `variant_summary.txt.gz` completo;
- archivos VCF completos de ClinVar;
- XML completos de ClinVar;
- bases descargadas masivas;
- datos genéticos personales.

El enfoque recomendado es:

```text
descargar localmente → procesar muestra reducida → generar reporte → ignorar resultados locales en Git
```

## 4. Datos personales y privacidad

No se deben subir al repositorio:

- genomas personales;
- archivos VCF personales;
- resultados de pruebas genéticas reales;
- reportes con información identificable;
- capturas con datos sensibles.

Si en el futuro se analiza un archivo real de una persona, ese flujo debe tratarse como información sensible, separada del repositorio público y con consentimiento explícito.

## 5. Límite no diagnóstico

E.C.O. interpreta registros de variantes y evidencia declarada por fuentes externas. No interpreta pacientes.

Por lo tanto, los reportes deben mantener frases como:

```text
Estado diagnóstico: no_diagnostico_resultado_bioinformatico_interpretativo
```

Y deben evitar afirmaciones como:

```text
La persona tiene esta enfermedad.
La persona tiene este riesgo absoluto.
Debe cambiar tratamiento.
Debe tomar una decisión médica.
```

Frase segura:

```text
Esta variante pública está clasificada por la fuente externa como relevante, incierta, benigna, conflictiva o farmacogenómica. Cualquier decisión de salud requiere revisión profesional y contexto clínico.
```

## 6. Uso de artículos, abstracts y terceros

ClinVar puede enlazar literatura, submitters y fuentes externas. Eso no autoriza a copiar textos largos, figuras, tablas o artículos completos.

Regla práctica:

- usar identificadores y enlaces;
- resumir con palabras propias;
- citar fuente;
- no copiar contenido protegido de terceros.

## 7. Buenas prácticas para portafolio

Para mostrar E.C.O. profesionalmente, usar una frase como:

```text
E.C.O. usa una muestra pública de ClinVar/NCBI para demostrar procesamiento bioinformático, clasificación interpretativa y generación de reportes educativos, con atribución explícita y límites de no diagnóstico.
```

## 8. Checklist antes de publicar

Antes de subir cambios o mostrar el proyecto:

- [ ] El README menciona que ClinVar/NCBI es la fuente.
- [ ] Los reportes dicen que no son diagnóstico.
- [ ] No hay datos personales en `results/`, `data/` o capturas.
- [ ] No se subieron bases completas descargadas.
- [ ] Los resultados locales están ignorados por `.gitignore`.
- [ ] Las clasificaciones externas se presentan como información reportada por fuentes externas, no como conclusión propia de E.C.O.
