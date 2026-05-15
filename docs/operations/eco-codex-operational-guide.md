# E.C.O. — Guía Operativa para pedir trabajo a Codex

## Cómo pedir tareas a Codex
Solicita tareas con alcance claro:
1. objetivo del sprint;
2. archivos esperados;
3. validaciones obligatorias;
4. límites responsables que deben preservarse;
5. formato de entrega.

## Qué sprint conviene pedir
Preferir sprints:
- pequeños y acotados;
- con outputs verificables (tests/reportes);
- reversibles por commit;
- sin tocar áreas críticas sin aprobación.

## Ejemplos de prompts seguros
- "Crea un reporte sintético en `results/` y su test, sin usar internet ni datos reales."
- "Actualiza Makefile para incluir un target documental y valida que no rompa `eco-check`."
- "Añade guía operativa y checklist de PR con validaciones reproducibles."

## Ejemplos de prompts bloqueados
- "Entrena un modelo con datos clínicos reales ahora mismo."
- "Recalibra umbrales de producción sin revisión humana."
- "Reemplaza baseline actual directamente en main."
- "Conecta fuentes sensibles externas y ejecuta ingestión automática."

## Checklist antes de abrir PR
- [ ] Rama de sprint (no `main`).
- [ ] Cambios pequeños, testeables y reversibles.
- [ ] Sin datos reales, sin entrenamiento, sin tocar baseline ni umbrales.
- [ ] Validaciones ejecutadas y reportadas.
- [ ] Árbol limpio.
- [ ] Resumen técnico + riesgos restantes + siguiente paso.
