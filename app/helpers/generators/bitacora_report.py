from app.helpers.generators.base_report import BaseReportGenerator
from reportlab.platypus import Paragraph
from reportlab.lib import colors


class BitacoraReport(BaseReportGenerator):
    MODULO = 'bitacora'
    TITULO = 'REPORTE DE ACTIVIDAD / BITÁCORA'
    COLUMNAS = [
        ('ID', 'id', 30), ('Usuario', 'usuario', 85), ('Acción', 'accion', 65),
        ('Módulo', 'modulo', 65), ('Detalle', 'detalle', 145), ('Fecha', 'fecha', 75),
    ]

    def _post_table_sections(self, kpis, opciones):
        sections = []
        if kpis:
            items = [(k, kpis.get(k, 0)) for k in ('creaciones', 'ediciones', 'eliminaciones') if kpis.get(k, 0) > 0]
            if items:
                sections.extend(self._seccion_distribucion('Distribución por Acción', items, colors.HexColor('#15803d')))
        return sections

    def _build_rows(self, datos):
        return [[
            str(d.get('id', '')),
            str(d.get('usuario_nombre', '—'))[:18],
            str(d.get('tipo_accion', '—')),
            str(d.get('modulo', '—')),
            str(d.get('accion', '—'))[:30],
            str(d.get('created_at', ''))[:16] if d.get('created_at') else '—',
        ] for d in datos]
