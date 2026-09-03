# Arquitectura Propuesta: Motor de Reportes PDF Dinamico

**Fecha:** 2026-09-01
**Estado:** Diseno para revision. NO implementado.

---

## 1. Diagnostico

El sistema tiene DOS caminos de reporte:

1. **Clasico** (`/reportes/generar`): filtros -> datos -> generador con COLUMNAS fijas -> PDF rígido
2. **Constructor** (`/reportes/construir`): wizard -> SQL dinamico -> dataset generico -> preview + export

El constructor ya resuelve el analisis dinamico (GROUP BY, metricas, dimensiones). Pero el PDF clasico sigue amarrado a COLUMNAS hardcoded.

**El problema real:** el usuario no puede decir "quiero este reporte pero con estas 5 columnas y ordenado por X".

---

## 2. Decision central: EVOLUCIONAR el clasico, no reemplazar

```
FLUJO CLASICO ACTUAL
  Filtros -> datos -> generador COLUMNAS fijas -> PDF rigido

                    +--[campo_seleccion]--> generador COLUMNAS dinamicas
                    |
FLUJO CLASICO      +--[agrupacion]------> subtotales
PROPUESTO          |
                    +--[ordenamiento]----> PDF ordenado
                    |
                    +--[orientacion]-----> landscape automatico

FLUJO CONSTRUCTOR (intacto)
  Wizard -> SQL dinamico -> dataset generico -> ConstructorReport
```

**No se toca el flujo del constructor.** Ya funciona. La mejora es solo sobre el clasico.

---

## 3. Nueva arquitectura del flujo clasico

```
USUARIO
  |
  v
[1] Click modulo -> filtros (IGUAL QUE AHORA)
  |
  v
[2] **NUEVO: Panel de campos disponibles** (checkboxes)
  |   -> Cargado desde un dict CAMPOS_DISPONIBLES en Python
  |   -> El usuario selecciona que columnas quiere
  |
  v
[3] Vista Previa (IGUAL QUE AHORA, pero con columnas seleccionadas)
  |
  v
[4] Descargar PDF
  |   -> POST incluye: modulo, filtros, columnas_seleccionadas[], orden, orientacion
  |   -> BaseReportGenerator recibe COLUMNAS dinamicas
  |   -> generate() renderiza con las columnas seleccionadas
  |
  v
[5] PDF generado (IGUAL QUE ANTES en apariencia, pero con campos configurables)
```

---

## 4. Capas de la propuesta

### 4.1 Definicion de campos (nuevo dict en Python)

Ubicacion: `app/helpers/reportes_campos.py` (nuevo archivo, ~200 lineas)

```python
CAMPOS_DISPONIBLES = {
    'guiones': {
        'nombre': {'label': 'Nombre', 'key': 'nombre', 'type': 'texto', 'width': 150, 'order': 1},
        'game': {'label': 'Game', 'key': 'game', 'type': 'entero', 'width': 40, 'order': 2},
        'pregame': {'label': 'Pre-Game', 'key': 'pregame', 'type': 'entero', 'width': 50, 'order': 3},
        'fecha_ejecucion': {'label': 'Ejecucion', 'key': 'fecha_ejecucion', 'type': 'fecha', 'width': 70, 'order': 4},
        'estado': {'label': 'Estado', 'key': 'estado', 'type': 'texto', 'width': 60, 'order': 5},
        'tiempo_total': {'label': 'Tiempo', 'key': 'tiempo_total', 'type': 'duracion', 'width': 60, 'order': 6},
        'creado_en': {'label': 'Creado', 'key': 'creado_en', 'type': 'fecha_hora', 'width': 75, 'order': 7},
        'encargado': {'label': 'Encargado', 'key': 'encargado', 'type': 'texto', 'width': 100, 'order': 8},
    },
    'inventario': {
        'id': {'label': 'ID', 'key': 'id', 'type': 'entero', 'width': 30, 'order': 1},
        'nombre': {'label': 'Nombre', 'key': 'nombre', 'type': 'texto', 'width': 130, 'order': 2},
        'tipo_nombre': {'label': 'Tipo', 'key': 'tipo_nombre', 'type': 'texto', 'width': 80, 'order': 3},
        'estado_nombre': {'label': 'Estado', 'key': 'estado_nombre', 'type': 'texto', 'width': 70, 'order': 4},
        'fecha_compra': {'label': 'Compra', 'key': 'fecha_compra', 'type': 'fecha', 'width': 70, 'order': 5},
        'costo': {'label': 'Costo', 'key': 'costo', 'type': 'moneda', 'width': 70, 'order': 6},
        'descripcion': {'label': 'Descripcion', 'key': 'descripcion', 'type': 'texto_largo', 'width': 150, 'order': 7},
    },
    # ... 10 modulos mas
}

# Columnas por defecto (las que aparecen si el usuario no selecciona nada)
COLUMNAS_DEFAULT = {
    'guiones': ['nombre', 'game', 'pregame', 'fecha_ejecucion', 'estado', 'tiempo_total'],
    'inventario': ['id', 'nombre', 'tipo_nombre', 'estado_nombre', 'fecha_compra'],
    # ...
}
```

### 4.2 Formateadores (nuevo)

Ubicacion: dentro de `reportes_campos.py`

```python
FORMATTERS = {
    'texto': lambda v: str(v) if v else '—',
    'texto_largo': lambda v: str(v)[:50] + '...' if v and len(str(v)) > 50 else (str(v) if v else '—'),
    'entero': lambda v: f"{int(v):,}" if v else '0',
    'moneda': lambda v: f"${float(v):,.2f}" if v else '$0.00',
    'fecha': lambda v: str(v) if v else '—',
    'fecha_hora': lambda v: str(v)[:16] if v else '—',
    'duracion': lambda v: _formatear_tiempo(v) if v else '—',
    'porcentaje': lambda v: f"{float(v):.1f}%" if v else '0%',
    'boolean': lambda v: 'Si' if v else 'No',
}
```

### 4.3 BaseReportGenerator modificado

Cambios MINIMOS en `base_report.py`:

1. `generate()` acepta `columnas_seleccionadas=None` en `opciones`
2. Si se provee, usa esas columnas en vez de `self.COLUMNAS`
3. Calcula anchos dinamicamente segun cantidad de columnas seleccionadas
4. `_build_rows()` recibe las columnas como parametro

```python
def generate(self, datos, filtros=None, kpis=None, opciones=None):
    opciones = opciones or {}
    # ... codigo existente ...

    # Si hay columnas seleccionadas, usarlas
    col_ids = opciones.get('columnas_seleccionadas')
    if col_ids:
        columnas = self._resolver_columnas(col_ids)
    else:
        columnas = self.COLUMNAS  # default = comportamiento actual

    # Calcular anchos dinamicos
    widths = self._calcular_anchos(columnas, opciones.get('orientacion'))

    # Construir tabla con columnas seleccionadas
    header = [Paragraph(c[0], self.style_bold) for c in columnas]
    rows = [header]
    for item in datos:
        rows.append([self._formatear_celda(item, c) for c in columnas])

    story.extend(self._tabla(rows, colWidths=widths))
```

### 4.4 Nuevos parametros en el endpoint

En `reportes_controller.py`, la funcion `generar()` ya acepta `opciones`. Se amplia:

```python
# En generar(), despues de extraer opciones existentes:
columnas_raw = request.form.get('columnas_seleccionadas', '')
if columnas_raw:
    opciones['columnas_seleccionadas'] = [c.strip() for c in columnas_raw.split(',') if c.strip()]

orientacion = request.form.get('orientacion', 'vertical')
if orientacion in ('vertical', 'horizontal'):
    opciones['orientacion'] = orientacion

agrupar_por = request.form.get('agrupar_por', '')
if agrupar_por:
    opciones['agrupar_por'] = agrupar_por
```

### 4.5 Endpoint nuevo: campos disponibles

```python
@bp.route('/campos/<modulo>', methods=['GET'])
def campos_modulo(modulo):
    """Devuelve los campos disponibles para un modulo."""
    if modulo not in CAMPOS_DISPONIBLES:
        return jsonify({'error': 'Modulo no valido'}), 400
    campos = CAMPOS_DISPONIBLES[modulo]
    defaults = COLUMNAS_DEFAULT.get(modulo, [])
    return jsonify({
        'campos': campos,
        'defaults': defaults,
    })
```

### 4.6 Frontend: panel de campos

En `GestionReportes.js`, despues de renderizar filtros, agregar seccion de campos:

```javascript
// Nuevo: panel de seleccion de campos
function renderCampos(modulo, config) {
    fetch(`/reportes/campos/${modulo}`)
        .then(r => r.json())
        .then(data => {
            const container = document.getElementById('campoPanelBody');
            container.innerHTML = '';
            Object.entries(data.campos).forEach(([key, campo]) => {
                const checked = data.defaults.includes(key) ? 'checked' : '';
                container.innerHTML += `
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox"
                               value="${key}" id="campo_${key}" ${checked}>
                        <label class="form-check-label" for="campo_${key}">
                            ${campo.label}
                        </label>
                    </div>`;
            });
        });
}
```

---

## 5. Agrupacion y subtotales

### 5.1 Definicion

```python
# En opciones:
opciones['agrupar_por'] = 'estado'  # key de columna
```

### 5.2 Implementacion en BaseReportGenerator

```python
def _agrupar_datos(self, datos, campo_agrupacion, columnas):
    from collections import OrderedDict
    grupos = OrderedDict()
    for item in datos:
        valor = item.get(campo_agrupacion, 'Sin valor')
        grupos.setdefault(valor, []).append(item)

    rows = []
    totales = {c[1]: 0 for c in columnas if c[2] in ('moneda', 'entero')}

    for grupo_valor, items_grupo in grupos.items():
        # Fila de grupo
        rows.append([Paragraph(f"<b>{grupo_valor}</b>", self.style_bold)] +
                     [''] * (len(columnas) - 1))

        for item in items_grupo:
            rows.append([self._formatear_celda(item, c) for c in columnas])

        # Subtotal del grupo
        subtotal = self._calcular_subtotales(items_grupo, columnas)
        rows.append([Paragraph(f"<b>Subtotal {grupo_valor}</b>", self.style_bold)] +
                     [Paragraph(f"<b>{self._fmt(subtotal[c[1]], c)}</b>", self.style_bold)
                      for c in columnas[1:]])

        # Acumular totales generales
        for k, v in subtotal.items():
            totales[k] = totales.get(k, 0) + v

    # Fila total general
    rows.append([Paragraph("<b>TOTAL GENERAL</b>", self.style_bold)] +
                 [Paragraph(f"<b>{self._fmt(totales.get(c[1], 0), c)}</b>", self.style_bold)
                  for c in columnas[1:]])

    return rows
```

---

## 6. Orientacion dinamica

```python
def _determinar_orientacion(self, columnas_seleccionadas, orientacion_solicitada):
    """Si hay muchas columnas y el usuario pidio vertical, sugerir landscape."""
    if orientacion_solicitada == 'horizontal':
        return landscape(letter)

    total_width = sum(c[2] for c in columnas_seleccionadas)
    if total_width > 500:  # umbral para landscape
        return landscape(letter)
    return letter
```

---

## 7. Resumen visual de cambios

| Componente | Cambio | Archivo |
|------------|--------|---------|
| Definicion de campos | NUEVO dict | `reportes_campos.py` |
| Endpoint campos | NUEVO ruta | `reportes_controller.py` |
| BaseReportGenerator | Ampliar `generate()` y `_build_rows()` | `base_report.py` |
| Generadores existentes | NO cambian (usan defaults) | `*_report.py` |
| Frontend | Nuevo panel de checkboxes de campos | `GestionReportes.js` |
| Dashboard HTML | Nuevo contenedor para campos | `dashboard.html` |
| Preview | Respeta columnas seleccionadas | `reportes_controller.py` |
| OPTIONS endpoint | Nuevo | `reportes_controller.py` |

---

*Documento de diseno. Requiere aprobacion antes de implementar.*
