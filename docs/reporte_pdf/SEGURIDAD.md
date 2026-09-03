# Seguridad: Analisis del Motor de Reportes

**Fecha:** 2026-09-01

---

## 1. Principios de seguridad existentes

1. **Whitelist de filtros** (`FILTROS_PERMITIDOS`): solo claves conocidas pasan al backend
2. **Parametros SQL siempre `%s`**: nunca interpolacion de valores
3. **Identificadores desde catalogo**: dimensiones, metricas, fuentes son constantes
4. **Permisos**: `@permiso_requerido('reportes.dashboard')` en todo el blueprint
5. **CSRF**: Flask-WTF protege todos los POST
6. **Soft-delete**: cada fuente tiene su WHERE fijo

---

## 2. Riesgos del motor dinamico

### 2.1 Seleccion de campos

**Riesgo:** Un usuario podria enviar keys de campos que no deberia ver.

**Mitigacion:** Whitelist de campos por modulo en `CAMPOS_DISPONIBLES`. Solo campos declarados son validos. Keys desconocidas se descartan silenciosamente.

```python
def _validar_campos(modulo, campos_seleccionados):
    disponibles = set(CAMPOS_DISPONIBLES.get(modulo, {}).keys())
    return [c for c in campos_seleccionados if c in disponibles]
```

### 2.2 Agrupacion

**Riesgo:** Agrupar por campo sensible (ej: usuario) podria revelar informacion.

**Mitigacion:** Solo campos con `groupable: True` en la definicion. Campos sensibles como `detalle` o `email` no son groupables.

### 2.3 Ordenamiento

**Riesgo:** Ninguno significativo. El ordenamiento es sobre datos ya filtrados por permisos.

### 2.4 SQL Injection

**Riesgo:** El motor constructor ya construye SQL dinamico.

**Mitigacion:** Ya implementada en `reportes_constructor.py`:
- Identificadores desde catalogo (no del cliente)
- Valores via `%s` parametrizados
- `ConstructorError` para invalidos

El flujo clasico NO construye SQL dinamico (usa modelos existentes).

### 2.5 Exposicion de datos

**Riesgo:** Campos como `password_hash`, `cedula`, `ip_address` no deberian aparecer en reportes.

**Mitigacion:** `CAMPOS_DISPONIBLES` solo incluye campos seguros. `COLUMNAS_TECNICAS` en `reportes_data.py` ya excluye campos sensibles del sanitizado.

---

## 3. Controles existentes que se preservan

| Control | Estado | Como se preserva |
|---------|--------|-----------------|
| `FILTROS_PERMITIDOS` | Activo | Se amplia con `CAMPOS_DISPONIBLES` |
| SQL parametrizado | Activo | Sin cambios en flujo clasico |
| Permisos por ruta | Activo | Sin cambios |
| CSRF | Activo | Sin cambios |
| Whitelist de opciones | Activo | Se amplia con `columnas_seleccionadas` |
| Soft-delete | Activo | Sin cambios |

---

## 4. Nuevos controles necesarios

### 4.1 Validacion de campos seleccionados

```python
# En generar():
campos_raw = request.form.get('columnas_seleccionadas', '')
if campos_raw:
    campos = [c.strip() for c in campos_raw.split(',') if c.strip()]
    opciones['columnas_seleccionadas'] = _validar_campos(modulo, campos)
else:
    opciones['columnas_seleccionadas'] = None  # usar defaults
```

### 4.2 Validacion de orientacion

```python
orientacion = request.form.get('orientacion', 'vertical')
if orientacion not in ('vertical', 'horizontal'):
    orientacion = 'vertical'
opciones['orientacion'] = orientacion
```

### 4.3 Validacion de agrupacion

```python
agrupar_por = request.form.get('agrupar_por', '')
if agrupar_por:
    from app.helpers.reportes_campos import CAMPOS_DISPONIBLES
    campos_mod = CAMPOS_DISPONIBLES.get(modulo, {})
    if agrupar_por not in campos_mod or not campos_mod[agrupar_por].get('groupable'):
        agrupar_por = ''  # descartar
opciones['agrupar_por'] = agrupar_por
```

### 4.4 Limite de columnas

```python
if len(opciones.get('columnas_seleccionadas') or []) > 25:
    opciones['columnas_seleccionadas'] = opciones['columnas_seleccionadas'][:25]
    # Nota: se truncara silenciosamente, el usuario vera max 25 columnas
```

---

## 5. Auditoria

Los PDFs generados ya se registran en `reportes_generados` con:
- `usuario_id`
- `modulo`
- `filtros` (JSON)
- `archivo_ruta`
- `creado_en`

**Ampliacion propuesta:** incluir en `filtros` las columnas seleccionadas y opciones usadas:

```python
filtros_completos = {
    'filtros': filtros,
    'columnas_seleccionadas': opciones.get('columnas_seleccionadas'),
    'orientacion': opciones.get('orientacion'),
    'agrupar_por': opciones.get('agrupar_por'),
}
reportes_model.registrar(usuario_id, modulo, 'PDF', json.dumps(filtros_completos), ...)
```

---

## 6. Resumen

| Area | Riesgo | Control |
|------|--------|---------|
| Campos | Ver campos no autorizados | Whitelist CAMPOS_DISPONIBLES |
| Agrupacion | Revelear datos sensibles | groupable: True en definicion |
| SQL | Injection | Ya resuelto (parametros + catalogo) |
| Permisos | Acceso no autorizado | Ya resuelto (@permiso_requerido) |
| Datos | Exposicion de hash/IP/cedula | COLUMNAS_TECNICAS + CAMPOS_DISPONIBLES |
| Auditoria | Sin registro | reportes_generados + ampliacion propuesta |

---

*Documento de analisis de seguridad.*
