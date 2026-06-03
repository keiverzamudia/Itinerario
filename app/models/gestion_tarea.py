class Tarea:
    def __init__(self, id_tarea=None, Nombre_Tarea=None, Instruccion=None,
                 id_usuario_creador=None, Estatus=True, **kwargs):
        self.id_tarea = id_tarea
        self.Nombre_Tarea = Nombre_Tarea
        self.Instruccion = Instruccion
        self.id_usuario_creador = id_usuario_creador
        self.Estatus = bool(Estatus) if Estatus is not None else True
        for k, v in kwargs.items():
            setattr(self, k, v)


class TareasAsignadas:
    def __init__(self, id_asignacion=None, id_tarea=None, id_usuario=None,
                 Estado='Pendiente', fecha_asignacion_tarea=None,
                 Estatus=True, **kwargs):
        self.id_asignacion = id_asignacion
        self.id_tarea = id_tarea
        self.id_usuario = id_usuario
        self.Estado = Estado
        self.fecha_asignacion_tarea = fecha_asignacion_tarea
        self.Estatus = bool(Estatus) if Estatus is not None else True
        self.Nombre_Tarea = None
        self.nombre_usuario = None
        for k, v in kwargs.items():
            setattr(self, k, v)
