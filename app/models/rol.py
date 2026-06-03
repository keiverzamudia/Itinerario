class Rol:
    def __init__(self, id=None, nombre=None, descripcion='', **kwargs):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return f'<Rol {self.nombre}>'


class Permiso:
    def __init__(self, id=None, nombre=None, codigo=None, modulo=None, descripcion='', **kwargs):
        self.id = id
        self.nombre = nombre
        self.codigo = codigo
        self.modulo = modulo
        self.descripcion = descripcion
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return f'<Permiso {self.codigo}>'


class RolPermiso:
    def __init__(self, id=None, rol_id=None, permiso_id=None, **kwargs):
        self.id = id
        self.rol_id = rol_id
        self.permiso_id = permiso_id
        for k, v in kwargs.items():
            setattr(self, k, v)


class UsuarioPermiso:
    def __init__(self, id=None, usuario_id=None, permiso_id=None, fecha_asignacion=None, **kwargs):
        self.id = id
        self.usuario_id = usuario_id
        self.permiso_id = permiso_id
        self.fecha_asignacion = fecha_asignacion
        for k, v in kwargs.items():
            setattr(self, k, v)
