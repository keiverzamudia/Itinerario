from app.helpers.generators.base_report import BaseReportGenerator
from reportlab.platypus import Paragraph
from reportlab.lib import colors


class UsuariosReport(BaseReportGenerator):
    MODULO = 'usuarios'
    TITULO = 'REPORTE DE USUARIOS'
    COLUMNAS = [
        ('Nombre', 'nombre', 110), ('Email', 'email', 120),
        ('Rol', 'rol', 70), ('Depto', 'depto', 70), ('Estado', 'estado', 55),
    ]

    def _post_table_sections(self, kpis, opciones):
        sections = []
        if kpis:
            activos = kpis.get('activos', 0)
            inactivos = kpis.get('inactivos', 0)
            items = [(k, v) for k, v in {'Activos': activos, 'Inactivos': inactivos}.items() if v > 0]
            if items:
                sections.extend(self._seccion_distribucion('Distribución por Estado', items, colors.HexColor('#15803d')))
        return sections

    def _build_rows(self, datos):
        return [[
            str(d.get('nombre', ''))[:24], str(d.get('email', ''))[:26],
            str(d.get('rol', '—')), str(d.get('departamento', '—')),
            'Activo' if d.get('activo') else 'Inactivo',
        ] for d in datos]
