from app.helpers.generators.base_report import BaseReportGenerator
from reportlab.platypus import Paragraph
from reportlab.lib import colors


class GuionesReport(BaseReportGenerator):
    MODULO = 'guiones'
    TITULO = 'REPORTE DE GUIONES'
    COLUMNAS = [
        ('Nombre', 'nombre', 150), ('Game', 'game', 40),
        ('Pre-Game', 'pregame', 50), ('Ejecución', 'fecha_ejecucion', 70),
        ('Estado', 'estado', 60), ('Tiempo', 'tiempo_total', 60),
    ]

    def _post_table_sections(self, kpis, opciones):
        sections = []
        if kpis:
            items = [(k, kpis.get(k, 0)) for k in ('borradores', 'publicados', 'en_vivo', 'finalizados') if kpis.get(k, 0) > 0]
            if items:
                sections.extend(self._seccion_distribucion('Distribución por Estado', items))
        return sections

    def _build_rows(self, datos):
        return [[
            Paragraph(str(d.get('nombre', ''))[:35], self.style_normal),
            str(d.get('game', 0)), str(d.get('pregame', 0)),
            str(d.get('fecha_ejecucion', '—')), str(d.get('estado', '')),
            str(d.get('tiempo_total', '0m')),
        ] for d in datos]
