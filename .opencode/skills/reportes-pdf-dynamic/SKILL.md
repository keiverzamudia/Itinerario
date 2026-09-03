# Skill: reportes-pdf-dynamic

# PDF Dinamico con Columnas Configurables — Itinerario

Motor de reportes PDF con columnas seleccionables por el usuario, anchos proporcionales, agrupacion con subtotales y orientacion automatica. Usa exclusivamente reportlab (ya instalado).

## Reglas duras

1. **Sin dependencias nuevas.** Solo reportlab nativo (`reportlab.lib`, `reportlab.platypus`, `reportlab.graphics`).
2. **Sin opciones = mismo PDF.** Si `opciones` no tiene `columnas_seleccionadas`, el output es byte-a-byte identico al anterior.
3. **Whitelist server-side.** Solo campos en `CAMPOS_DISPONIBLES` son validos. Keys desconocidas se descartan.
4. **Anchos proporcionales.** Nunca recortar columnas; escalar proporcionalmente al espacio disponible.
5. **Texto siempre legible.** Truncar con `..` si excede, nunca cortar a mitad de palabra.

## Calculo de anchos dinamicos

```python
def _calcular_anchos(columnas, orientacion='vertical'):
    """Anchos proporcionales que caben en la pagina."""
    from reportlab.lib.pagesizes import letter, landscape

    disponible = 712 if orientacion == 'horizontal' else 532  # letter - margenes
    anchos_sugeridos = [c[2] for c in columnas]  # tupla: (label, key, width)
    total = sum(anchos_sugeridos)

    if total <= disponible:
        return anchos_sugeridos  # caben todos

    factor = disponible / total
    return [max(30, int(a * factor)) for a in anchos_sugeridos]  # min 30pt
```

**Por que 532 y 712:**
- Portrait letter: 612pt - 40 - 40 = 532pt
- Landscape letter: 792pt - 40 - 40 = 712pt

## Deteccion automatica portrait/landscape

```python
def _determinar_pagina(columnas, orientacion_solicitada):
    from reportlab.lib.pagesizes import letter, landscape

    if orientacion_solicitada == 'horizontal':
        return landscape(letter)

    total_width = sum(c[2] for c in columnas)
    if len(columnas) >= 8 or total_width > 500:
        return landscape(letter)

    return letter
```

## Formateo de celdas por tipo

```python
FORMATTERS = {
    'texto':      lambda v: str(v) if v else '—',
    'texto_largo': lambda v: str(v)[:50] + '..' if v and len(str(v)) > 50 else (str(v) if v else '—'),
    'entero':     lambda v: f"{int(v):,}" if v else '0',
    'moneda':     lambda v: f"${float(v):,.2f}" if v else '$0.00',
    'decimal':    lambda v: f"{float(v):,.1f}" if v else '0.0',
    'fecha':      lambda v: str(v) if v else '—',
    'fecha_hora': lambda v: str(v)[:16] if v else '—',
    'duracion':   lambda v: _formatear_tiempo(v) if v else '—',
    'porcentaje': lambda v: f"{float(v):.1f}%" if v else '0%',
    'boolean':    lambda v: 'Si' if v else 'No',
}
```

## Truncado inteligente

```python
def _formatear_celda(self, item, columna, tipo_campo):
    key = columna[1]
    value = item.get(key)
    formatter = FORMATTERS.get(tipo_campo, FORMATTERS['texto'])
    texto = formatter(value)

    max_chars = max(10, columna[2] // 5)  # ~5pt por caracter
    if len(texto) > max_chars:
        texto = texto[:max_chars - 2] + '..'

    return Paragraph(texto, self.style_normal)
```

## Reduccion de fuente por cantidad de columnas

```python
def _ajustar_estilo_segun_columnas(self, num_columnas):
    if num_columnas <= 7:
        return  # default 8pt
    elif num_columnas <= 10:
        self.style_normal.fontSize = 7
        self.style_bold.fontSize = 7
    else:
        self.style_normal.fontSize = 6
        self.style_bold.fontSize = 6
```

## Tabla agrupada con subtotales

```python
def _construir_tabla_agrupada(self, datos, columnas, campo_agrupacion):
    from collections import OrderedDict

    grupos = OrderedDict()
    for item in datos:
        valor = item.get(campo_agrupacion, 'Sin valor')
        grupos.setdefault(valor, []).append(item)

    rows = []
    numeric_keys = [c[1] for c in columnas if self._es_numerico(c[1])]
    total_general = {k: 0 for k in numeric_keys}

    for grupo_valor, items in grupos.items():
        # Encabezado de grupo
        rows.append([Paragraph(f"<b>{grupo_valor}</b>", self.style_bold)]
                     + [''] * (len(columnas) - 1))

        # Filas del grupo
        for item in items:
            rows.append([self._formatear_celda(item, c, self._tipo_campo(c[1]))
                         for c in columnas])

        # Subtotal
        subtotales = {}
        for k in numeric_keys:
            subtotales[k] = sum(float(i.get(k, 0) or 0) for i in items)
            total_general[k] += subtotales[k]

        subtotal_row = [Paragraph("<b>Subtotal</b>", self.style_bold)]
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

## Encabezados repetidos en cada pagina

```python
# En generate():
doc = SimpleDocTemplate(buffer, pagesize=pagina, ...)
doc.build(story,
          onFirstPage=lambda d: self._draw_header(d, columnas),
          onLaterPages=lambda d: self._draw_header(d, columnas))

def _draw_header(self, doc, columnas):
    header = [Paragraph(f"<b>{c[0]}</b>", self.style_bold) for c in columnas]
    t = Table([header], colWidths=doc._colWidths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
    ]))
    t.wrapOn(doc, doc.width, doc.topMargin)
    t.drawOn(doc, doc.leftMargin, doc.height + doc.topMargin - 20)
```

## Limites praticos

| Columnas | Estrategia | Fuente |
|----------|-----------|--------|
| 1-5 | Portrait, anchos originales | 8pt |
| 6-7 | Portrait, anchos escalados | 8pt |
| 8-10 | Landscape automatico | 7pt |
| 11-15 | Landscape, truncado | 6pt |
| 16-20 | Landscape, truncado agresivo | 6pt |
| 20+ | Aviso al usuario | 6pt |

## Paginacion

reportlab `SimpleDocTemplate` pagina automaticamente. Para tablas muy largas:
- El `Table` de reportlab maneja filas que exceden la pagina
- Los `RepeatableParagraph` repiten contenido en cada pagina
- Usar `KeepTogether` para grupos (evita cortar un grupo a mitad)

```python
from reportlab.platypus import KeepTogether

# Mantener grupo junto (si cabe en una pagina)
story.append(KeepTogether(grupo_rows))
```

## Matriz de tipos vs operaciones

| Tipo | Selectable | Sortable | Groupable | Aggregate |
|------|-----------|----------|-----------|-----------|
| texto | Si | Si | Si | No |
| texto_largo | Si | No | No | No |
| entero | Si | Si | Si | suma |
| moneda | Si | Si | No | suma |
| decimal | Si | Si | No | promedio |
| fecha | Si | Si | No | No |
| fecha_hora | Si | Si | No | No |
| duracion | Si | Si | No | promedio |
| porcentaje | Si | Si | No | promedio |
| boolean | Si | Si | Si | No |

## Errores comunes y como evitarlos

1. **Columnas no caben:** Siempre calcular anchos proporcionales, nunca fijos
2. **Texto cortado:** Truncar con `..` antes de crear Paragraph
3. **Subtotales incorrectos:** Solo sumar columnas con `aggregate`
4. **Landscape innecesario:** Usar deteccion automatica, no forzar
5. **PDF ilegible:** Reducir fuente para muchas columnas
6. **Grupo cortado:** Usar `KeepTogether` para grupos pequeños
