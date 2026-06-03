class Recurso:
    def __init__(self, id=None, nombre=None, descripcion=None, tipo_id=None,
                 estado_id=1, fecha_compra=None, costo=None,
                 eliminado=0, creado_en=None, modificado_en=None, **kwargs):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.tipo_id = tipo_id
        self.estado_id = estado_id
        self.fecha_compra = fecha_compra
        self.costo = costo
        self.eliminado = eliminado
        self.creado_en = creado_en
        self.modificado_en = modificado_en
        self.mantenimientos = []
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'tipo_id': self.tipo_id,
            'estado_id': self.estado_id,
        }


class Mantenimiento:
    def __init__(self, id=None, recurso_id=None, usuario_id=None,
                 estado='en_espera', fecha_ingreso=None, fecha_salida=None,
                 diagnostico=None, observaciones=None, creado_en=None, **kwargs):
        self.id = id
        self.recurso_id = recurso_id
        self.usuario_id = usuario_id
        self.estado = estado
        self.fecha_ingreso = fecha_ingreso
        self.fecha_salida = fecha_salida
        self.diagnostico = diagnostico
        self.observaciones = observaciones
        self.creado_en = creado_en
        self.historial = []
        self.recurso = None
        self.usuario_nombre = None
        for k, v in kwargs.items():
            setattr(self, k, v)


class HistorialMantenimiento:
    def __init__(self, id=None, mantenimiento_id=None, usuario_id=None,
                 accion=None, descripcion=None, creado_en=None, **kwargs):
        self.id = id
        self.mantenimiento_id = mantenimiento_id
        self.usuario_id = usuario_id
        self.accion = accion
        self.descripcion = descripcion
        self.creado_en = creado_en
        self.usuario_nombre = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self):
        return {
            'id': self.id,
            'mantenimiento_id': self.mantenimiento_id,
            'usuario_id': self.usuario_id,
            'usuario_nombre': self.usuario_nombre,
            'accion': self.accion,
            'descripcion': self.descripcion,
            'creado_en': str(self.creado_en) if self.creado_en else None,
        }
