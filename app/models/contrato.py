class Contrato:
    def __init__(self, id_contrato=None, id_patrocinador=None,
                 fecha_inicio=None, fecha_fin=None, estado=1,
                 estatus='Borrador', tipo=None, monto_total=None,
                 **kwargs):
        self.id_contrato = id_contrato
        self.id_patrocinador = id_patrocinador
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado if estado is not None else 1
        self.estatus = estatus
        self.tipo = tipo
        self.monto_total = monto_total
        self.nombre_empresa = None
        for k, v in kwargs.items():
            setattr(self, k, v)
