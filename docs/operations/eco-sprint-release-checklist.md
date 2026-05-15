# E.C.O. Sprint Release Checklist

Checklist operativa para cerrar un sprint de forma reproducible y responsable en E.C.O.

## Límites responsables (obligatorios)
- [ ] Sin datos reales.
- [ ] Sin entrenamiento.
- [ ] Sin modificación de baseline.
- [ ] Sin recalibración de umbrales.
- [ ] Sin afirmaciones biomédicas aplicadas.

## 1) Antes de abrir PR
- [ ] Trabajar en rama de sprint (no `main`).
- [ ] Confirmar alcance acotado y reversible.
- [ ] Ejecutar estado operativo:

```bash
make eco-status
```

- [ ] Ejecutar pruebas:

```bash
python3 -m pytest -q
```

- [ ] Confirmar árbol limpio o cambios esperados únicamente:

```bash
git status --short
```

## 2) Antes de mergear
- [ ] PR revisado y aprobado.
- [ ] Sin PR pendiente bloqueante para este sprint.
- [ ] Confirmar pruebas pasando (`pytest passing`).
- [ ] Ejecutar validación integral y limpieza:

```bash
make eco-check-clean
```

- [ ] Confirmar que no quedan outputs temporales en `results/`.

## 3) Después de mergear
- [ ] Volver a `main`:

```bash
git switch main
```

- [ ] Actualizar `main` con fast-forward:

```bash
git pull --ff-only origin main
```

- [ ] Validación final en `main`:

```bash
make eco-status
python3 -m pytest -q
make eco-check-clean
git status --short
```

## 4) Limpieza de ramas locales
- [ ] Listar ramas locales:

```bash
git branch --list
```

- [ ] Eliminar rama de sprint local ya mergeada.

## 5) Limpieza de ramas remotas
- [ ] Limpiar referencias remotas obsoletas:

```bash
git fetch -p
```

- [ ] Eliminar rama remota de sprint ya mergeada.

## 6) Confirmación de sincronización y cierre
- [ ] Confirmar `HEAD = origin/main`.
- [ ] Verificar sincronización exacta:

```bash
git rev-list --left-right --count HEAD...origin/main
```

Resultado esperado: `0\t0`.

- [ ] Confirmar árbol limpio:

```bash
git status --short
```

- [ ] Confirmar explícitamente: no PR pendiente.
- [ ] Confirmar explícitamente: no outputs temporales en `results/`.
