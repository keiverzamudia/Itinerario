class TipoRecurso:
    def __init__(self, id=None, nombre=None, descripcion=None, **kwargs):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        for k, v in kwargs.items():
            setattr(self, k, v)


class EstadoRecurso:
    def __init__(self, id=None, nombre=None, descripcion=None, **kwargs):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        for k, v in kwargs.items():
            setattr(self, k, v)


class EstadoAsignacion:
    def __init__(self, id=None, nombre=None, descripcion=None, **kwargs):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        for k, v in kwargs.items():
            setattr(self, k, v)


class RecursoInventario:
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
        self.tipo_nombre = None
        self.estado_nombre = None
        for k, v in kwargs.items():
            setattr(self, k, v)


class AsignacionRecurso:
    def __init__(self, id=None, recurso_id=None, usuario_id=None,
                 fecha_asignacion=None, fecha_devolucion_esperada=None,
                 fecha_devolucion_real=None, estado_asignacion_id=1,
                 notas=None, **kwargs):
        self.id = id
        self.recurso_id = recurso_id
        self.usuario_id = usuario_id
        self.fecha_asignacion = fecha_asignacion
        self.fecha_devolucion_esperada = fecha_devolucion_esperada
        self.fecha_devolucion_real = fecha_devolucion_real
        self.estado_asignacion_id = estado_asignacion_id
        self.notas = notas
        self.recurso_nombre = None
        self.usuario_nombre = None
        self.estado_asignacion_nombre = None
        for k, v in kwargs.items():
            setattr(self, k, v)
