import io
import os
from datetime import datetime
from collections import OrderedDict
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


class BaseReportGenerator:
    MODULO = ''
    TITULO = ''
    COLUMNAS = []

    def __init__(self, usuario_actual):
        self.usuario = usuario_actual
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        self.style_titulo = ParagraphStyle(
            'TituloReporte', parent=self.styles['Heading1'],
            fontSize=18, leading=22,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=6,
        )
        self.style_normal = self.styles['Normal']
        self.style_bold = ParagraphStyle(
            'TextoNegrita', parent=self.style_normal, fontName='Helvetica-Bold'
        )
        self.style_small = ParagraphStyle(
            'TextoSmall', parent=self.style_normal, fontSize=8,
            textColor=colors.HexColor('#64748b')
        )

    # ── Métodos para columnas dinámicas ──────────────────────────────

    def _obtener_columnas(self, opciones):
        """Resuelve qué columnas usar: dinámicas o default."""
        col_ids = (opciones or {}).get('columnas_seleccionadas')
        if not col_ids:
            return self.COLUMNAS

        from app.helpers.reportes_campos import CAMPOS_DISPONIBLES
        campos = CAMPOS_DISPONIBLES.get(self.MODULO, {})
        columnas = []
        for key in col_ids:
            if key in campos:
                c = campos[key]
                columnas.append((c['label'], key, c['width']))
        return columnas if columnas else self.COLUMNAS

    def _calcular_anchos(self, columnas, orientacion='vertical'):
        """Anchos proporcionales que caben en la página."""
        disponible = 712 if orientacion == 'horizontal' else 532
        anchos = [c[2] for c in columnas]
        total = sum(anchos)
        if total <= disponible:
            return anchos
        factor = disponible / total
        return [max(30, int(a * factor)) for a in anchos]

    def _determinar_pagina(self, columnas, orientacion_solicitada):
        """Determina tamaño y orientación de página."""
        if orientacion_solicitada == 'horizontal':
            return landscape(letter)
        total_width = sum(c[2] for c in columnas)
        if len(columnas) >= 8 or total_width > 500:
            return landscape(letter)
        return letter

    def _ajustar_estilo_segun_columnas(self, num_columnas):
        """Ajusta tamaños de fuente según cantidad de columnas."""
        if num_columnas <= 7:
            return
        elif num_columnas <= 10:
            self.style_normal.fontSize = 7
            self.style_bold = ParagraphStyle(
                'TextoNegrita7', parent=self.style_normal, fontName='Helvetica-Bold'
            )
        else:
            self.style_normal.fontSize = 6
            self.style_bold = ParagraphStyle(
                'TextoNegrita6', parent=self.style_normal, fontName='Helvetica-Bold'
            )

    def _tipo_campo(self, key):
        """Obtiene el tipo de campo desde CAMPOS_DISPONIBLES."""
        from app.helpers.reportes_campos import CAMPOS_DISPONIBLES
        campo = CAMPOS_DISPONIBLES.get(self.MODULO, {}).get(key, {})
        return campo.get('type', 'texto')

    def _es_numerico(self, key):
        """True si el campo se puede sumar en subtotales."""
        from app.helpers.reportes_campos import CAMPOS_DISPONIBLES, CAMPOS_NUMERICOS
        campo = CAMPOS_DISPONIBLES.get(self.MODULO, {}).get(key, {})
        return campo.get('type', '') in CAMPOS_NUMERICOS

    def _formatear_celda(self, item, columna, tipo_campo):
        """Formatea un valor según tipo de campo."""
        from app.helpers.reportes_campos import FORMATTERS
        key = columna[1]
        value = item.get(key)
        formatter = FORMATTERS.get(tipo_campo, FORMATTERS['texto'])
        texto = formatter(value)
        max_chars = max(10, columna[2] // 5)
        if len(texto) > max_chars:
            texto = texto[:max_chars - 2] + '..'
        return Paragraph(texto, self.style_normal)

    def _construir_tabla_simple(self, datos, columnas):
        """Tabla sin agrupar: header + filas."""
        header = [Paragraph(f"<b>{c[0]}</b>", self.style_bold) for c in columnas]
        rows = [header]
        for item in datos:
            rows.append([
                self._formatear_celda(item, c, self._tipo_campo(c[1]))
                for c in columnas
            ])
        return rows

    def _construir_tabla_agrupada(self, datos, columnas, campo_agrupacion):
        """Tabla con grupos, subtotales y total general."""
        grupos = OrderedDict()
        for item in datos:
            valor = item.get(campo_agrupacion, 'Sin valor')
            grupos.setdefault(valor, []).append(item)

        numeric_keys = [c[1] for c in columnas if self._es_numerico(c[1])]
        total_general = {k: 0.0 for k in numeric_keys}
        rows = []

        for grupo_valor, items in grupos.items():
            rows.append([
                Paragraph(f"<b>{grupo_valor}</b>", self.style_bold)
            ] + [''] * (len(columnas) - 1))

            for item in items:
                rows.append([
                    self._formatear_celda(item, c, self._tipo_campo(c[1]))
                    for c in columnas
                ])

            subtotales = {}
            for k in numeric_keys:
                subtotales[k] = sum(float(i.get(k, 0) or 0) for i in items)
                total_general[k] += subtotales[k]

            subtotal_row = [Paragraph("<b>Subtotal</b>", self.style_bold)]
            for c in columnas[1:]:
                val = subtotales.get(c[1])
                if val is not None and val != 0:
                    subtotal_row.append(
                        Paragraph(f"<b>${val:,.2f}</b>" if self._tipo_campo(c[1]) == 'moneda'
                                  else f"<b>{val:,.1f}</b>" if self._tipo_campo(c[1]) == 'decimal'
                                  else f"<b>{int(val):,}</b>",
                                  self.style_bold))
                else:
                    subtotal_row.append('')
            rows.append(subtotal_row)

        total_row = [Paragraph("<b>TOTAL GENERAL</b>", self.style_bold)]
        for c in columnas[1:]:
            val = total_general.get(c[1])
            if val and val != 0:
                total_row.append(
                    Paragraph(f"<b>${val:,.2f}</b>" if self._tipo_campo(c[1]) == 'moneda'
                              else f"<b>{val:,.1f}</b>" if self._tipo_campo(c[1]) == 'decimal'
                              else f"<b>{int(val):,}</b>",
                              self.style_bold))
            else:
                total_row.append('')
        rows.append(total_row)

        return rows

    def _post_table_sections(self, kpis, opciones):
        """Hook para distribuciones. Override en subclases."""
        return []

    # ── Header ───────────────────────────────────────────────────────
    def _header(self, filtros=None):
        story = []
        usuario_nombre = getattr(self.usuario, 'nombre', 'Sistema')
        rol = getattr(self.usuario, 'rol', 'Administrador')
        depto = getattr(self.usuario, 'departamento', 'Operaciones')

        header_data = [[
            Paragraph(
                "<font size='15'><b>ESTADIO ANTONIO HERRERA GUTIÉRREZ</b></font>",
                self.style_bold
            ),
            Paragraph(
                f"<font size='8' color='#64748b'>Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}</font>",
                self.style_normal
            ),
        ], [
            Paragraph(
                f"<font size='9' color='#475569'>Departamento: <b>{depto}</b> | Rol: <b>{rol}</b></font>",
                self.style_normal
            ),
            Paragraph(
                f"<font size='9' color='#475569'>Generado por: <b>{usuario_nombre.upper()}</b></font>",
                self.style_normal
            ),
        ]]
        header_table = Table(header_data, colWidths=[360, 180])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 6))

        story.append(HRFlowable(
            width="100%", thickness=2,
            color=colors.HexColor('#1e40af'),
            spaceAfter=8
        ))
        story.append(Paragraph(self.TITULO, self.style_titulo))

        if filtros:
            orden = filtros.pop('orden', None)
            filtros_texto = ', '.join(
                f"{k}: {v}" for k, v in filtros.items() if v
            )
            if filtros_texto:
                story.append(Paragraph(
                    f"<font size='8' color='#64748b'><i>Filtros aplicados: {filtros_texto}</i></font>",
                    self.style_small
                ))
            if orden:
                story.append(Paragraph(
                    f"<font size='8' color='#64748b'><i>Ordenado por: {orden}</i></font>",
                    self.style_small
                ))
        story.append(Spacer(1, 8))
        return story

    def _tabla(self, datos, style_override=None, col_widths=None):
        story = []
        if not datos or len(datos) < 2:
            story.append(Paragraph(
                "<font color='#64748b'>No hay datos para mostrar.</font>",
                self.style_normal
            ))
            return story

        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e40af")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
        if style_override:
            table_style.extend(style_override)

        widths = col_widths or ([w for _, _, w in self.COLUMNAS] if self.COLUMNAS else None)
        table = Table(datos, colWidths=widths, repeatRows=1)
        table.setStyle(TableStyle(table_style))
        story.append(table)
        return story

    def generate(self, datos, filtros=None, kpis=None, opciones=None):
        buffer = io.BytesIO()
        opciones = opciones or {}

        columnas = self._obtener_columnas(opciones)
        orientacion = opciones.get('orientacion', 'vertical')
        pagina = self._determinar_pagina(columnas, orientacion)
        self._ajustar_estilo_segun_columnas(len(columnas))

        doc = SimpleDocTemplate(
            buffer, pagesize=pagina,
            rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40,
        )

        story = []
        story.extend(self._header(filtros))

        if kpis:
            story.extend(self._seccion_kpis(kpis))

        story.extend(self._secciones_analisis(kpis, opciones))

        # Ordenamiento dinámico
        ordenar_por = opciones.get('ordenar_por')
        if ordenar_por:
            datos = sorted(datos, key=lambda x: x.get(ordenar_por) or '')

        # Tabla con columnas dinámicas o default
        col_ids = opciones.get('columnas_seleccionadas')
        if col_ids:
            agrupar_por = opciones.get('agrupar_por')
            if agrupar_por and any(c[1] == agrupar_por for c in columnas):
                table_data = self._construir_tabla_agrupada(datos, columnas, agrupar_por)
            else:
                table_data = self._construir_tabla_simple(datos, columnas)
        else:
            rows = self._build_rows(datos)
            if rows:
                header = [Paragraph(f"<b>{h}</b>", self.style_bold) for h, _, _ in self.COLUMNAS]
                table_data = [header] + rows
            else:
                table_data = None

        if table_data:
            anchos = self._calcular_anchos(columnas, orientacion) if col_ids else None
            story.extend(self._tabla(table_data, col_widths=anchos))
        else:
            story.append(Spacer(1, 20))
            story.append(Paragraph(
                "<font color='#64748b'>No hay datos para mostrar.</font>",
                self.style_normal
            ))

        # Hook para distribuciones (override en subclases)
        story.extend(self._post_table_sections(kpis, opciones))

        story.append(Spacer(1, 20))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cbd5e1')))
        story.append(Paragraph(
            f"<font size='7' color='#94a3b8'>Reporte generado automáticamente — "
            f"{self.TITULO} — {datetime.now().strftime('%d/%m/%Y %H:%M')}</font>",
            self.style_small
        ))

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    def _build_rows(self, datos):
        return []

    def _secciones_analisis(self, kpis, opciones):
        """Resumen ejecutivo + Top-N + comparativa, según opciones del usuario."""
        story = []
        if not kpis:
            return story
        if opciones and opciones.get('resumen'):
            story.extend(self._resumen_ejecutivo(kpis))
        if opciones and opciones.get('top_n'):
            story.extend(self._top_destacados(kpis, opciones['top_n']))
        if opciones and opciones.get('comparar'):
            story.extend(self._comparativa_periodos(kpis, opciones.get('kpis_previos')))
        return story

    def _resumen_ejecutivo(self, kpis):
        """Párrafo factual: SOLO números ya calculados, cero texto inventado."""
        story = []
        if not kpis:
            return story
        partes = []
        total = None
        for clave in ('total', 'total_pagos', 'total_registros', 'modulos'):
            if isinstance(kpis.get(clave), (int, float)):
                total = kpis[clave]
                break
        if total is not None:
            partes.append(f"Se analizaron {total} registros tras aplicar los filtros seleccionados")
        detalles = []
        for k, v in kpis.items():
            if isinstance(v, (dict, list)) or v is None:
                continue
            if k in ('total', 'total_pagos', 'total_registros', 'modulos') or len(detalles) >= 3:
                continue
            detalles.append(f"{str(k).replace('_', ' ')}: {v}")
        if detalles:
            partes.append(' · '.join(detalles))
        if not partes:
            return story
        story.append(Spacer(1, 6))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=4))
        story.append(Paragraph("<b>Resumen ejecutivo</b>", self.style_normal))
        story.append(Spacer(1, 2))
        story.append(Paragraph(
            f"<font size='9' color='#334155'>{'.'.join(partes)}.</font>",
            self.style_normal
        ))
        story.append(Spacer(1, 6))
        return story

    def _top_destacados(self, kpis, n):
        """Top N entidades por la distribución principal del módulo (reutiliza KPIs existentes)."""
        distribucion = next(
            (v for v in kpis.values() if isinstance(v, dict) and v), None
        )
        if not distribucion:
            return []
        ordenados = sorted(distribucion.items(), key=lambda x: x[1], reverse=True)[:max(int(n), 1)]
        return self._seccion_distribucion(f'Top {n} destacados', ordenados)

    def _comparativa_periodos(self, kpis, kpis_previos):
        """KPIs lado a lado vs el período anterior desplazado. Solo escalares compartidos."""
        story = []
        story.append(Spacer(1, 6))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=4))
        story.append(Paragraph("<b>Comparativa vs período anterior</b>", self.style_normal))
        story.append(Spacer(1, 4))
        if not kpis_previos:
            story.append(Paragraph(
                "<font size='9' color='#64748b'><i>Sin datos comparables en el período anterior.</i></font>",
                self.style_normal
            ))
            story.append(Spacer(1, 6))
            return story
        rows = [[Paragraph('<b>Indicador</b>', self.style_bold),
                 Paragraph('<b>Actual</b>', self.style_bold),
                 Paragraph('<b>Anterior</b>', self.style_bold),
                 Paragraph('<b>Variación</b>', self.style_bold)]]
        comparados = 0
        for k, actual in kpis.items():
            if isinstance(actual, (dict, list)) or k not in kpis_previos:
                continue
            previo = kpis_previos[k]
            if isinstance(previo, (dict, list)):
                continue
            try:
                a, p = float(str(actual).replace('$', '').replace(',', '') or 0), \
                       float(str(previo).replace('$', '').replace(',', '') or 0)
            except (ValueError, TypeError):
                continue
            if p:
                variacion = f"{(a - p) / p * 100:+.0f}%"
            elif a:
                variacion = 'Nuevo'
            else:
                variacion = '—'
            rows.append([
                Paragraph(str(k).replace('_', ' ').title(), self.style_normal),
                Paragraph(str(actual), self.style_normal),
                Paragraph(str(previo), self.style_normal),
                Paragraph(variacion, self.style_normal),
            ])
            comparados += 1
        if not comparados:
            story.append(Paragraph(
                "<font size='9' color='#64748b'><i>Sin datos comparables en el período anterior.</i></font>",
                self.style_normal
            ))
            story.append(Spacer(1, 6))
            return story
        t = Table(rows, colWidths=[220, 110, 110, 90])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('PADDING', (0, 0), (-1, -1), 4),
            ('LINEBELOW', (0, 0), (-1, -2), 0.3, colors.HexColor('#e2e8f0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ]))
        story.append(t)
        story.append(Spacer(1, 6))
        return story

    def _seccion_kpis(self, kpis):
        story = []
        if not kpis:
            return story
        story.append(Spacer(1, 8))
        items = list(kpis.items())
        chunks = [items[i:i+3] for i in range(0, len(items), 3)]
        for chunk in chunks:
            row_cells = []
            for k, v in chunk:
                if isinstance(v, (dict, list)):
                    continue
                label = k.replace('_', ' ').title()
                texto = f"<font size='7' color='#64748b'>{label}</font><br/><font size='11'><b>{v}</b></font>"
                row_cells.append(Paragraph(texto, self.style_normal))
            if len(row_cells) < 3 and len(chunks) > 1:
                for _ in range(3 - len(row_cells)):
                    row_cells.append(Paragraph("", self.style_normal))
            if row_cells:
                w = 540 // len(row_cells) if row_cells else 180
                t = Table([row_cells], colWidths=[w]*len(row_cells))
                t.setStyle(TableStyle([
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('TOPPADDING', (0,0), (-1,-1), 8),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
                    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
                ]))
                story.append(t)
                story.append(Spacer(1, 4))
        story.append(Spacer(1, 8))
        return story

    def _seccion_distribucion(self, titulo, items, color=colors.HexColor('#1e40af')):
        story = []
        if not items:
            return story
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=4))
        story.append(Paragraph(
            f"<font size='9' color='#475569'><b>{titulo}</b></font>",
            self.style_normal
        ))
        story.append(Spacer(1, 4))
        total = sum(v for _, v in items)
        rows = []
        rows.append([Paragraph("<b>Item</b>", self.style_bold),
                     Paragraph("<b>Cantidad</b>", self.style_bold),
                     Paragraph("<b>%</b>", self.style_bold)])
        for name, val in items:
            pct = f"{val * 100 // total}%" if total else "0%"
            rows.append([
                Paragraph(str(name)[:30], self.style_normal),
                Paragraph(str(val), self.style_normal),
                Paragraph(pct, self.style_normal),
            ])
        rows.append([
            Paragraph("<b>Total</b>", self.style_bold),
            Paragraph(f"<b>{total}</b>", self.style_bold),
            Paragraph("<b>100%</b>", self.style_bold),
        ])
        t = Table(rows, colWidths=[250, 100, 100])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), color),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('PADDING', (0,0), (-1,-1), 4),
            ('LINEBELOW', (0,0), (-1,-2), 0.3, colors.HexColor('#e2e8f0')),
            ('LINEBELOW', (0,-1), (-1,-1), 1, color),
            ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor('#f8fafc')]),
            ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ]))
        story.append(t)
        story.append(Spacer(1, 8))
        return story

    def save(self, pdf_bytes, usuario_id, filtros=None):
        from app.model.reportes_model import ReporteModel

        now = datetime.now()
        fecha_path = now.strftime('%Y/%m')
        nombre_archivo = f"{self.MODULO}_{now.strftime('%Y%m%d_%H%M%S')}.pdf"
        ruta_relativa = f"{fecha_path}/{nombre_archivo}"
        ruta_completa = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'static', 'reportes', ruta_relativa
        )

        os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
        with open(ruta_completa, 'wb') as f:
            f.write(pdf_bytes)

        ReporteModel().registrar({
            'usuario_id': usuario_id,
            'modulo': self.MODULO,
            'tipo_reporte': self.TITULO,
            'filtros': filtros or {},
            'archivo_ruta': ruta_relativa,
            'archivo_nombre': f"{self.MODULO}_{now.strftime('%d-%m-%Y')}.pdf",
            'archivo_tamano': len(pdf_bytes),
        })

        return ruta_relativa, nombre_archivo
