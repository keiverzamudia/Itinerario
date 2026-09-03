from app.helpers.generators.base_report import BaseReportGenerator
from reportlab.platypus import Paragraph
from reportlab.lib import colors


class ContratosReport(BaseReportGenerator):
    MODULO = 'contratos'
    TITULO = 'REPORTE DE CONTRATOS'
    COLUMNAS = [
        ('Empresa', 'nombre_empresa', 115),
        ('Tipo', 'tipo', 50),
        ('Estatus', 'estatus', 50),
        ('Inicio', 'fecha_inicio', 60),
        ('Fin', 'fecha_fin', 60),
        ('Días', 'dias_restantes', 35),
        ('Monto', 'monto_total', 60),
    ]

    def _post_table_sections(self, kpis, opciones):
        sections = []
        if kpis:
            tipos = [(k, kpis.get(k, 0)) for k in ('bronce', 'plata', 'oro') if kpis.get(k, 0) > 0]
            if tipos:
                sections.extend(self._seccion_distribucion('Distribución por Tipo', tipos))
            estatus_items = [(k, kpis.get(k, 0)) for k in ('vigentes', 'vencidos', 'borradores') if kpis.get(k, 0) > 0]
            if estatus_items:
                sections.extend(self._seccion_distribucion('Distribución por Estatus', estatus_items, colors.HexColor('#15803d')))
        return sections

    def _build_rows(self, datos):
        return [[
            Paragraph(str(d.get('nombre_empresa', '—'))[:30], self.style_normal),
            str(d.get('tipo', '—')),
            str(d.get('estatus', '—')),
            str(d.get('fecha_inicio', '—'))[:10],
            str(d.get('fecha_fin', '—'))[:10],
            str(d.get('dias_restantes', '—')),
            f"${float(d.get('monto_total', 0) or 0):,.0f}",
        ] for d in datos]
