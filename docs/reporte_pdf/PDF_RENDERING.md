# PDF Rendering: Estrategia de Generacion Dinamica

**Fecha:** 2026-09-01

---

## 1. Estrategia actual

```python
# base_report.py
class BaseReportGenerator:
    COLUMNAS = []  # Fijo por generador

    def generate(self, datos, filtros, kpis, opciones):
        story = []
        story.extend(self._header(filtros))
        story.extend(self._seccion_kpis(kpis))
        story.extend(self._secciones_analisis(kpis, opciones))

        # TABLA CON COLUMNAS FIJAS
        header = [Paragraph(c[0], self.style_bold) for c in self.COLUMNAS]
        rows = [header]
        for item in datos:
            rows.append([self._formatear(item, c) for c in self.COLUMNAS])
        story.extend(self._tabla(rows))

        doc.build(story)
```

**Problema:** `COLUMNAS` es tupla fija `(label, key, width)`. No hay seleccion.

---

## 2. Estrategia propuesta

### 2.1 Resolucion de columnas

```python
def _obtener_columnas(self, opciones):
    """Resuelve que columnas usar para el reporte."""
    col_ids = opciones.get('columnas_seleccionadas')

    if not col_ids:
        return self.COLUMNAS  # Default = comportamiento actual

    # Importar CAMPOS_DISPONIBLES
    from app.helpers.reportes_campos import CAMPOS_DISPONIBLES, FORMATTERS

    campos = CAMPOS_DISPONIBLES.get(self.MODULO, {})
    columnas = []
    for key in col_ids:
        if key in campos:
            campo = campos[key]
            columnas.append((campo['label'], campo['key'], campo['width']))

    return columnas if columnas else self.COLUMNAS
```

### 2.2 Calculo de anchos dinamicos

```python
def _calcular_anchos(self, columnas, orientacion):
    """Anchos proporcionales que caben en la pagina."""
    from reportlab.lib.pagesizes import letter, landscape

    if orientacion == 'horizontal':
        disponible = 712  # landscape - margenes
    else:
        disponible = 532  # portrait - margenes

    anchos_sugeridos = [c[2] for c in columnas]
    total = sum(anchos_sugeridos)

    if total <= disponible:
        return anchos_sugeridos

    factor = disponible / total
    return [max(30, int(a * factor)) for a in anchos_sugeridos]
```

### 2.3 Renderizado de celdas

```python
def _formatear_celda(self, item, columna, tipo_campo):
    """Formatea un valor segun tipo de campo."""
    key = columna[1]
    value = item.get(key)

    from app.helpers.reportes_campos import FORMATTERS
    formatter = FORMATTERS.get(tipo_campo, FORMATTERS['texto'])
    texto = formatter(value)

    # Truncar si excede el ancho de columna
    max_chars = max(10, columna[2] // 5)
    if len(texto) > max_chars:
        texto = texto[:max_chars - 2] + '..'

    return Paragraph(texto, self.style_normal)
```

---

## 3. Modificaciones a BaseReportGenerator

### 3.1 generate() ampliado

```python
def generate(self, datos, filtros=None, kpis=None, opciones=None):
    opciones = opciones or {}
    story = []

    # Header (igual que ahora)
    story.extend(self._header(filtros))

    # KPIs (igual que ahora)
    story.extend(self._seccion_kpis(kpis))

    # Analisis (igual que ahora: resumen, top_n, comparativa)
    story.extend(self._secciones_analisis(kpis, opciones))

    # NUEVO: Resolver columnas
    columnas = self._obtener_columnas(opciones)
    orientacion = opciones.get('orientacion', 'vertical')
    pagina = self._determinar_pagina(columnas, orientacion)

    # NUEVO: Ajustar estilos si hay muchas columnas
    self._ajustar_estilo_segun_columnas(len(columnas))

    # TABLA DINAMICA
    header = [Paragraph(c[0], self.style_bold) for c in columnas]
    rows = [header]

    # NUEVO: Agrupacion
    agrupar_por = opciones.get('agrupar_por')
    if agrupar_por and any(c[1] == agrupar_por for c in columnas):
        rows = self._construir_tabla_agrupada(datos, columnas, agrupar_por)
    else:
        for item in datos:
            rows.append([self._formatear_celda(item, c, self._tipo_campo(c[1]))
                         for c in columnas])

    anchos = self._calcular_anchos(columnas, orientacion)
    story.extend(self._tabla(rows, colWidths=anchos))

    # Footer (igual que ahora)
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=0.5,
                             color=colors.HexColor('#cbd5e1')))

    doc = SimpleDocTemplate(buffer, pagesize=pagina, ...)
    doc.build(story)
```

### 3.2 Tabla agrupada

```python
def _construir_tabla_agrupada(self, datos, columnas, campo_agrupacion):
    """Construye tabla con grupos, subtotales y total general."""
    from collections import OrderedDict
    from app.helpers.reportes_campos import CAMPOS_DISPONIBLES

    grupos = OrderedDict()
    for item in datos:
        valor = item.get(campo_agrupacion, 'Sin valor')
        grupos.setdefault(valor, []).append(item)

    rows = []
    campos_mod = CAMPOS_DISPONIBLES.get(self.MODULO, {})
    numeric_keys = [c[1] for c in columnas
                    if campos_mod.get(c[1], {}).get('aggregate')]

    total_general = {k: 0 for k in numeric_keys}

    for grupo_valor, items in grupos.items():
        # Encabezado de grupo
        rows.append([
            Paragraph(f"<b>{grupo_valor}</b>", self.style_bold)
        ] + [''] * (len(columnas) - 1))

        # Filas del grupo
        for item in items:
            rows.append([self._formatear_celda(item, c, self._tipo_campo(c[1]))
                         for c in columnas])

        # Subtotal
        subtotales = {}
        for k in numeric_keys:
            subtotales[k] = sum(float(i.get(k, 0) or 0) for i in items)
            total_general[k] += subtotales[k]

        subtotal_row = [Paragraph(f"<b>Subtotal</b>", self.style_bold)]
        for c in columnas[1:]:
            val = subtotales.get(c[1])
            subtotal_row.append(
                Paragraph(f"<b>{self._fmt_celda(val, c)}</b>", self.style_bold)
                if val is not None else '')
        rows.append(subtotal_row)

    # Total general
    total_row = [Paragraph("<b>TOTAL GENERAL</b>", self.style_bold)]
    for c in columnas[1:]:
        val = total_general.get(c[1])
        total_row.append(
            Paragraph(f"<b>{self._fmt_celda(val, c)}</b>", self.style_bold)
            if val is not None else '')
    rows.append(total_row)

    return rows
```

---

## 4. Paginacion

### 4.1 Como funciona hoy

`SimpleDocTemplate` de reportlab maneja paginacion automatica:
- Si el contenido excede una pagina, crea paginas nuevas
- `onPage` callback puede repetir encabezados

### 4.2 Mejora: encabezados repetidos

```python
def _header_callback(self, doc, columnas):
    """Repite encabezados de columna en cada pagina."""
    header = [Paragraph(f"<b>{c[0]}</b>", self.style_bold) for c in columnas]
    t = Table([header], colWidths=doc._colWidths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ]))
    t.wrapOn(doc, doc.width, doc.topMargin)
    t.drawOn(doc, doc.leftMargin, doc.height + doc.topMargin - 20)

# En generate():
doc.build(story, onFirstPage=lambda d: self._header_callback(d, columnas),
          onLaterPages=lambda d: self._header_callback(d, columnas))
```

---

## 5. Manejo de texto largo

```python
def _formatear_celda(self, item, columna, tipo_campo):
    key = columna[1]
    value = item.get(key)

    # Para textos largos, usar WrappedParagraph
    if tipo_campo == 'texto_largo':
        max_width = columna[2]
        texto = str(value) if value else '—'
        # reportlab Paragraph ajusta automaticamente
        return Paragraph(texto, self.style_small)

    # Para demas tipos, truncar
    formatter = FORMATTERS.get(tipo_campo, FORMATTERS['texto'])
    texto = formatter(value)
    max_chars = max(10, columna[2] // 5)
    if len(texto) > max_chars:
        texto = texto[:max_chars - 2] + '..'
    return Paragraph(texto, self.style_normal)
```

---

## 6. Imagenes y logos

### 6.1 Logo actual

El header ya incluye el logo del estadio (`base_report.py:_header()`). No cambia.

### 6.2 Logo por modulo (futuro)

```python
# En opciones:
opciones['logo'] = 'static/img/logos/contratos.png'

# En generate():
if opciones.get('logo'):
    story.insert(0, Image(opciones['logo'], width=50, height=50))
```

Diferido: el logo actual del estadio es suficiente.

---

## 7. Metadatos del PDF

```python
# En save() o generate():
from reportlab.lib.units import inch

doc = SimpleDocTemplate(buffer, ...)
doc.title = f"{self.TITULO} - {datetime.now().strftime('%Y-%m-%d')}"
doc.author = self.usuario.nombre if self.usuario else 'Sistema'
doc.subject = f"Reporte de {self.MODULO}"
```

---

*Documento de diseno de renderizado PDF.*
