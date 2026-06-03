class Premio:
    def __init__(self, id=None, nombre=None, descripcion=None,
                 id_patrocinador=None, estado='pendiente', estatus=False,
                 fecha_creacion=None, hora_creacion=None, fecha_hora_creacion=None,
                 foto='default-premio.png', fecha_entrega=None,
                 entregado_por=None, **kwargs):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.id_patrocinador = id_patrocinador
        self.estado = estado
        self.estatus = bool(estatus) if estatus is not None else False
        self.fecha_creacion = fecha_creacion
        self.hora_creacion = hora_creacion
        self.fecha_hora_creacion = fecha_hora_creacion
        self.foto = foto
        self.fecha_entrega = fecha_entrega
        self.entregado_por = entregado_por
        for k, v in kwargs.items():
            setattr(self, k, v)


class Patrocinador:
    def __init__(self, id_patrocinador=None, nombre_empresa=None,
                 rif=None, tipo_contrato=1, nombre_contacto=None, telefono=None,
                 email=None, estado=1, **kwargs):
        self.id_patrocinador = id_patrocinador
        self.nombre_empresa = nombre_empresa
        self.rif = rif
        self.tipo_contrato = tipo_contrato if tipo_contrato is not None else 1
        self.nombre_contacto = nombre_contacto
        self.telefono = telefono
        self.email = email
        self.estado = estado if estado is not None else 1
        for k, v in kwargs.items():
            setattr(self, k, v)
