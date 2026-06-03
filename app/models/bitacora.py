class SesionUsuario:
    def __init__(self, id=None, usuario_id=None, inicio_sesion=None,
                 fin_sesion=None, ip_address=None, user_agent=None,
                 duracion_segundos=None, **kwargs):
        self.id = id
        self.usuario_id = usuario_id
        self.inicio_sesion = inicio_sesion
        self.fin_sesion = fin_sesion
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.duracion_segundos = duracion_segundos
        self.usuario_nombre = None
        for k, v in kwargs.items():
            setattr(self, k, v)


class ActividadUsuario:
    def __init__(self, id=None, sesion_id=None, usuario_id=None,
                 tipo_accion=None, modulo=None, accion='',
                 detalle=None, pagina=None, ip_address=None,
                 created_at=None, **kwargs):
        self.id = id
        self.sesion_id = sesion_id
        self.usuario_id = usuario_id
        self.tipo_accion = tipo_accion
        self.modulo = modulo
        self.accion = accion
        self.detalle = detalle
        self.pagina = pagina
        self.ip_address = ip_address
        self.created_at = created_at
        self.usuario_nombre = None
        for k, v in kwargs.items():
            setattr(self, k, v)


class CambioPorModulo:
    def __init__(self, id=None, actividad_id=None, tabla_afectada=None,
                 registro_id=None, campo=None, valor_anterior=None,
                 valor_nuevo=None, created_at=None, **kwargs):
        self.id = id
        self.actividad_id = actividad_id
        self.tabla_afectada = tabla_afectada
        self.registro_id = registro_id
        self.campo = campo
        self.valor_anterior = valor_anterior
        self.valor_nuevo = valor_nuevo
        self.created_at = created_at
        for k, v in kwargs.items():
            setattr(self, k, v)


class ErrorAplicacion:
    def __init__(self, id=None, usuario_id=None, tipo_error=None,
                 mensaje=None, traceback=None, pagina=None,
                 ip_address=None, created_at=None, **kwargs):
        self.id = id
        self.usuario_id = usuario_id
        self.tipo_error = tipo_error
        self.mensaje = mensaje
        self.traceback = traceback
        self.pagina = pagina
        self.ip_address = ip_address
        self.created_at = created_at
        self.usuario_nombre = None
        for k, v in kwargs.items():
            setattr(self, k, v)
