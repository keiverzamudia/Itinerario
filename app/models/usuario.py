from werkzeug.security import generate_password_hash, check_password_hash


class Usuario:
    def __init__(self, id=None, nombre=None, email=None, password_hash=None,
                 cedula=None, rol=None, departamento=None, telefono=None,
                 activo=True, fecha_registro=None, ultimo_acceso=None, **kwargs):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password_hash = password_hash
        self.cedula = cedula
        self.rol = rol
        self.departamento = departamento
        self.telefono = telefono
        self.activo = bool(activo) if activo is not None else True
        self.fecha_registro = fecha_registro
        self.ultimo_acceso = ultimo_acceso
        self._permisos_cache = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.activo

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_superadmin(self):
        return self.rol == 'Superadmin'

    def is_admin(self):
        return self.rol in ('Administrador', 'Superadmin')

    def tiene_permiso(self, codigo):
        if self.is_superadmin():
            return True
        if self._permisos_cache is None:
            from app.repositories.rol_repository import UsuarioPermisoRepository
            self._permisos_cache = UsuarioPermisoRepository().obtener_permisos_usuario(self.id, self.rol)
        return codigo in self._permisos_cache

    def __repr__(self):
        return f'<Usuario {self.nombre}>'
