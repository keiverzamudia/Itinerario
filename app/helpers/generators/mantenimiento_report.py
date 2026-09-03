from app.helpers.generators.base_report import BaseReportGenerator
from reportlab.platypus import Paragraph
from reportlab.lib import colors


class MantenimientoReport(BaseReportGenerator):
    MODULO = 'mantenimiento'
    TITULO = 'REPORTE DE MANTENIMIENTO'
    COLUMNAS = [
        ('Recurso', 'recurso', 110), ('Estado', 'estado', 65),
        ('Ingreso', 'ingreso', 65), ('Diagnóstico', 'diagnostico', 130),
    ]

    def _post_table_sections(self, kpis, opciones):
        sections = []
        if kpis:
            items = [(k, kpis.get(k, 0)) for k in ('en_espera', 'en_reparacion', 'reparados', 'dados_baja') if kpis.get(k, 0) > 0]
            if items:
                sections.extend(self._seccion_distribucion('Distribución por Estado', items, colors.HexColor('#f59e0b')))
        return sections

    def _build_rows(self, datos):
        return [[
            Paragraph(str(d.get('recurso_nombre', '—'))[:24], self.style_normal),
            str(d.get('estado', '—')),
            str(d.get('fecha_ingreso', ''))[:10] if d.get('fecha_ingreso') else '—',
            str(d.get('diagnostico', '—'))[:28],
        ] for d in datos]
