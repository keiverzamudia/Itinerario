from app.helpers.generators.base_report import BaseReportGenerator
from reportlab.platypus import Paragraph
from reportlab.lib import colors


class TareasReport(BaseReportGenerator):
    MODULO = 'tareas'
    TITULO = 'REPORTE DE TAREAS'
    COLUMNAS = [
        ('Tarea', 'tarea', 150), ('Estado', 'estado', 65),
        ('Asignado a', 'asignado', 80), ('Fecha', 'fecha', 75),
    ]

    def _post_table_sections(self, kpis, opciones):
        sections = []
        if kpis:
            items = [(k, kpis.get(k, 0)) for k in ('pendientes', 'en_progreso', 'completadas') if kpis.get(k, 0) > 0]
            if items:
                sections.extend(self._seccion_distribucion('Distribución por Estado', items, colors.HexColor('#15803d')))
        return sections

    def _build_rows(self, datos):
        return [[
            Paragraph(str(d.get('nombre_tarea', ''))[:30], self.style_normal),
            str(d.get('estado', 'Pendiente')),
            str(d.get('asignado_a', '—')), str(d.get('fecha_asignacion_tarea', ''))[:10] or '—',
        ] for d in datos]
