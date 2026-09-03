# Riesgos del Proyecto

**Fecha:** 2026-09-01

---

## 1. Riesgos criticos

### R1: Regresion en PDFs existentes

**Riesgo:** Modificar `BaseReportGenerator.generate()` podria romper los 12 generadores actuales.

**Probabilidad:** MEDIA (si no se testea correctamente)
**Impacto:** ALTO (todos los reportes se rompen)

**Mitigacion:**
- Sin `columnas_seleccionadas` en opciones, el comportamiento DEBE ser identico
- Tests de regresion: PDF generado sin opciones = byte-a-byte identico
- Los 12 generadores existentes NO se modifican

**Estado del plan:** Mitigado por diseno. `generate()` solo usa columnas dinamicas si `opciones['columnas_seleccionadas']` existe.

---

### R2: Complejidad del panel de campos

**Riesgo:** El usuario se confunde con demasiados checkboxes y no sabe que seleccionar.

**Probabilidad:** MEDIA
**Impacto:** MEDIO (mala UX, no rompe nada)

**Mitigacion:**
- Defaults sensatos (las mismas columnas de hoy)
- Organizar campos por categoria visual
- Checkbox "Seleccionar todo" / "Limpiar"
- Tooltip con descripcion de cada campo

**Estado del plan:** Mitigado por diseno. Defaults = comportamiento actual.

---

## 2. Riesgos medios

### R3: Rendimiento con muchos campos

**Riesgo:** 20+ columnas en un PDF lenta la generacion o produce un PDF ilegible.

**Probabilidad:** MEDIA
**Impacto:** MEDIO (PDF lento o feo)

**Mitigacion:**
- Limite de 25 columnas maximo
- Deteccion automatica de landscape
- Reduccion de fuente para muchas columnas
- Aviso al usuario

**Estado del plan:** Mitigado. Limites claros en el diseno.

---

### R4: Agrupacion con subtotales incorrectos

**Riesgo:** Los subtotales suman columnas que no deberian sumarse (ej: campos de texto).

**Probabilidad:** BAJA
**Impacto:** MEDIO (datos incorrectos en PDF)

**Mitigacion:**
- Solo columnas con `aggregate: True` se suman
- Los campos de texto muestran vacio en subtotal
- Tests de validacion de subtotales

**Estado del plan:** Mitigado por diseno. `aggregate` es explicito por campo.

---

### R5: Duplicacion de configuracion

**Riesgo:** `CAMPOS_DISPONIBLES` duplica informacion de `COLUMNAS` en generadores y `columns` en MODULE_CONFIG.

**Probabilidad:** ALTA (ya existe este problema)
**Impacto:** BAJO (no rompe nada, solo mantenimiento)

**Mitigacion:**
- `CAMPOS_DISPONIBLES` se convierte en la fuente unica de verdad
- Los generadores existentes leen de ahi
- `MODULE_CONFIG.columns` se genera desde el backend
- Migracion gradual

**Estado del plan:** Aceptado como deuda tecnica conocida. Se ataca en refactor futuro.

---

## 3. Riesgos bajos

### R6: CSS rompe con muchos campos

**Riesgo:** El layout del dashboard se desborda con el panel de campos abierto.

**Probabilidad:** BAJA
**Impacto:** BAJO

**Mitigacion:** Panel de campos con scroll propio, max-height fijo.

---

### R7: Compatibilidad con constructor

**Riesgo:** Los cambios al flujo clasico interfieren con el constructor.

**Probabilidad:** BAJA
**Impacto:** MEDIO

**Mitigacion:** Los flujos son completamente paralelos. No comparten estado.

---

### R8: Permisos insuficientes

**Riesgo:** Un usuario ve campos que no deberia ver.

**Probabilidad:** BAJA
**Impacto:** ALTO

**Mitigacion:** `CAMPOS_DISPONIBLES` solo incluye campos seguros. Los permisos ya estan en el blueprint.

---

## 4. Riesgos eliminados

| Riesgo | Por que se elimino |
|--------|-------------------|
| SQL injection | El flujo clasico NO construye SQL dinamico |
| Dependencias nuevas | Solo se usa reportlab (ya instalado) |
| Cambios en BD | No se modifican tablas existentes |
| Cambios en modelos | No se modifican modelos existentes |
| Cambios en SocketIO | No aplica a reportes |

---

## 5. Matriz de riesgos

| # | Riesgo | Probabilidad | Impacto | Mitigacion |
|---|--------|-------------|---------|------------|
| R1 | Regresion PDFs | MEDIA | ALTO | Tests byte-a-byte |
| R2 | Complejidad UX | MEDIA | MEDIO | Defaults sensatos |
| R3 | Rendimiento | MEDIA | MEDIO | Limites claros |
| R4 | Subtotales | BAJA | MEDIO | aggregate explicito |
| R5 | Duplicacion config | ALTA | BAJO | Fuente unica futura |
| R6 | CSS | BAJA | BAJO | Panel con scroll |
| R7 | Constructor | BAJA | MEDIO | Flujos paralelos |
| R8 | Permisos | BAJA | ALTO | Campos seguros |

---

*Documento de analisis de riesgos.*
