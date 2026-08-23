import io
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable
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

    def _tabla(self, datos, style_override=None):
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

        col_widths = [w for _, _, w in self.COLUMNAS] if self.COLUMNAS else None
        table = Table(datos, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle(table_style))
        story.append(table)
        return story

    def generate(self, datos, filtros=None, kpis=None):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=letter,
            rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40,
        )

        story = []
        story.extend(self._header(filtros))

        if kpis:
            story.extend(self._seccion_kpis(kpis))

        rows = self._build_rows(datos)
        if rows:
            header = [Paragraph(f"<b>{h}</b>", self.style_bold) for h, _, _ in self.COLUMNAS]
            table_data = [header] + rows
            story.extend(self._tabla(table_data))
        else:
            story.append(Spacer(1, 20))
            story.append(Paragraph(
                "<font color='#64748b'>No hay datos para mostrar.</font>",
                self.style_normal
            ))

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
