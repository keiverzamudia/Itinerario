from app.helpers.generators.base_report import BaseReportGenerator
from reportlab.platypus import Paragraph
from reportlab.lib import colors


class InventarioReport(BaseReportGenerator):
    MODULO = 'inventario'
    TITULO = 'REPORTE DE INVENTARIO'
    COLUMNAS = [
        ('ID', 'id', 30), ('Nombre', 'nombre', 130),
        ('Tipo', 'tipo_nombre', 80), ('Estado', 'estado_nombre', 70),
        ('Compra', 'fecha_compra', 70),
    ]

    def _post_table_sections(self, kpis, opciones):
        sections = []
        if kpis:
            tipos_l = [(k, v) for k, v in kpis.get('tipos', {}).items() if v > 0]
            if tipos_l:
                sections.extend(self._seccion_distribucion('Distribución por Tipo', tipos_l))
            estados_l = [(k, v) for k, v in kpis.get('estados', {}).items() if v > 0]
            if estados_l:
                sections.extend(self._seccion_distribucion('Distribución por Estado', estados_l, colors.HexColor('#15803d')))
        return sections

    def _build_rows(self, datos):
        return [[
            str(d.get('id', '')),
            str(d.get('nombre', ''))[:28],
            str(d.get('tipo_nombre', '')), str(d.get('estado_nombre', '')),
            str(d.get('fecha_compra', ''))[:10] if d.get('fecha_compra') else '—',
        ] for d in datos]
