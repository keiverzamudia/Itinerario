from datetime import datetime


class Pago:
    def __init__(self, id_pago=None, id_contrato=None, monto=None,
                 tipo_pago=None, referencia=None, fecha_pago=None,
                 hora_pago=None, registrado_por=None, Descripción=None,
                 estado=0, fecha_registro=None, **kwargs):
        self.id_pago = id_pago
        self.id_contrato = id_contrato
        self.monto = monto
        self.tipo_pago = tipo_pago
        self.referencia = referencia
        self.fecha_pago = fecha_pago
        self.hora_pago = hora_pago
        self.registrado_por = registrado_por
        self.Descripción = Descripción
        self.estado = estado if estado is not None else 0
        self.fecha_registro = fecha_registro or datetime.now()
        self.nombre_patrocinador = None
        self.nombre_empresa = None
        for k, v in kwargs.items():
            setattr(self, k, v)
