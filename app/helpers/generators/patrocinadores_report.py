from app.helpers.generators.base_report import BaseReportGenerator
from reportlab.platypus import Paragraph
from reportlab.lib import colors


class PatrocinadoresReport(BaseReportGenerator):
    MODULO = 'patrocinadores'
    TITULO = 'REPORTE DE PATROCINADORES'
    COLUMNAS = [
        ('Empresa', 'nombre_empresa', 150),
        ('RIF', 'rif', 75), ('Teléfono', 'telefono', 75),
        ('Contrato', 'tipo_contrato', 70),
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
            Paragraph(str(d.get('nombre_empresa', ''))[:32], self.style_normal),
            str(d.get('rif', '—')), str(d.get('telefono', '—')),
            str(d.get('tipo_contrato', '—')),
        ] for d in datos]
