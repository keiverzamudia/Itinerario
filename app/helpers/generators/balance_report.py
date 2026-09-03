from app.helpers.generators.base_report import BaseReportGenerator
from reportlab.platypus import Paragraph
from reportlab.lib import colors


class BalanceReport(BaseReportGenerator):
    MODULO = 'balance'
    TITULO = 'REPORTE DE PAGOS / BALANCE'
    COLUMNAS = [
        ('Patrocinador', 'nombre_patrocinador', 120),
        ('Tipo Pago', 'tipo_pago', 70),
        ('Monto', 'monto', 75),
        ('Referencia', 'referencia', 85),
        ('Fecha Pago', 'fecha_pago', 70),
    ]

    def _post_table_sections(self, kpis, opciones):
        sections = []
        if kpis:
            tipos = [(k, v) for k, v in kpis.get('tipos_pago', {}).items() if v > 0]
            if tipos:
                sections.extend(self._seccion_distribucion('Distribución por Tipo de Pago', tipos))
        return sections

    def _build_rows(self, datos):
        return [[
            Paragraph(str(d.get('nombre_patrocinador', '—'))[:28], self.style_normal),
            str(d.get('tipo_pago', '—')),
            f"${float(d.get('monto', 0) or 0):,.0f}",
            str(d.get('referencia', '—'))[:20],
            str(d.get('fecha_pago', '—'))[:10] if d.get('fecha_pago') else '—',
        ] for d in datos]
