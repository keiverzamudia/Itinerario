from typing import Dict
from app.traits.validaciones import ValidacionesMixin
from app.repositories.balance_repository import BalanceRepository


class BalanceService(ValidacionesMixin):

    def __init__(self):
        super().__init__()
        self.repo = BalanceRepository()

    def obtener_contratos_activos(self):
        contratos = self.repo.obtener_contratos_activos()
        if not contratos:
            return []
        return [
            (c['id_contrato'],
             f"{c['nombre_patrocinador'] or 'Sin patrocinador'} - "
             f"Contrato #{c['id_contrato']} - ${float(c['monto_total']):.2f}")
            for c in contratos
        ]

    def obtener_contratos_activos_datos(self):
        return self.repo.obtener_contratos_activos()

    def obtener_datos_contrato(self, id_contrato):
        return self.repo.obtener_contrato_por_id(id_contrato)

    def obtener_historial_pagos(self, limit=100):
        return self.repo.get_historial_pagos(limit)

    def obtener_todos_pagos(self):
        return self.repo.get_historial_pagos(1000)

    def obtener_top_contratos(self, limit=5):
        return self.repo.obtener_top_contratos(limit)

    def validar_monto_positivo(self, monto):
        try:
            if float(monto) <= 0:
                self.errores.append('El monto debe ser mayor a cero')
        except (ValueError, TypeError):
            self.errores.append('Monto inválido')

    def registrar_pago(self, datos_pago: Dict, usuario_id: int) -> Dict:
        self.limpiar_errores()

        self.validar_obligatorios(
            ['id_contrato', 'monto', 'tipo_pago', 'fecha_pago', 'hora_pago'],
            datos_pago
        )
        self.validar_monto_positivo(datos_pago.get('monto', 0))

        if self.tiene_errores():
            return {'success': False, 'errores': self.get_errores()}

        contrato = self.repo.obtener_contrato_por_id(datos_pago['id_contrato'])
        if not contrato:
            return {'success': False, 'errores': ['Contrato no encontrado']}

        total_pagado = self.repo.get_total_pagado_by_contrato(datos_pago['id_contrato'])
        saldo_actual = float(contrato['monto_total']) - total_pagado

        if float(datos_pago['monto']) > saldo_actual:
            return {
                'success': False,
                'errores': [f'El monto excede el saldo pendiente (${saldo_actual:.2f})']
            }

        datos_pago['registrado_por'] = usuario_id
        nuevo_pago = self.repo.registrar_pago(datos_pago)

        return {
            'success': True,
            'pago_id': nuevo_pago.id_pago,
            'mensaje': (
                f'Pago registrado exitosamente. '
                f'Saldo restante: ${saldo_actual - float(datos_pago["monto"]):.2f}'
            )
        }

    def obtener_detalle_pago(self, id_pago):
        return self.repo.obtener_pago_por_id(id_pago)

    def editar_pago(self, pago_id, datos):
        try:
            resultado = self.repo.modificar_pago(pago_id, datos)
            if resultado:
                return {'success': True}
            return {'success': False, 'error': 'Pago no encontrado'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def eliminar_pago(self, pago_id):
        try:
            resultado = self.repo.eliminar_pago(pago_id)
            if resultado:
                return {'success': True}
            return {'success': False, 'error': 'Pago no encontrado'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
