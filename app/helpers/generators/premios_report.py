from app.helpers.generators.base_report import BaseReportGenerator
from reportlab.platypus import Paragraph
from reportlab.lib import colors


class PremiosReport(BaseReportGenerator):
    MODULO = 'premios'
    TITULO = 'REPORTE DE PREMIOS'
    COLUMNAS = [
        ('Nombre', 'nombre', 120), ('Patrocinador', 'patrocinador', 90),
        ('Estado', 'estado', 55), ('Total', 'total', 35), ('Entreg.', 'entregados', 40),
        ('Creación', 'creacion', 65),
    ]

    def _post_table_sections(self, kpis, opciones):
        sections = []
        if kpis:
            items = [(k, kpis.get(k, 0)) for k in ('pendientes', 'entregados') if kpis.get(k, 0) > 0]
            if items:
                sections.extend(self._seccion_distribucion('Distribución por Estado', items, colors.HexColor('#f59e0b')))
        return sections

    def _build_rows(self, datos):
        return [[
            str(d.get('nombre', ''))[:28],
            str(d.get('patrocinador_nombre', '—')),
            str(d.get('estado', '')), str(d.get('cantidad', 1)),
            str(d.get('cantidad_entregada', 0)),
            str(d.get('fecha_creacion', ''))[:10] if d.get('fecha_creacion') else '—',
        ] for d in datos]
