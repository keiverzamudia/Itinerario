class DashboardVisibilidad:
    def __init__(self, id=None, rol_id=None, modulo_key=None, visible=True, **kwargs):
        self.id = id
        self.rol_id = rol_id
        self.modulo_key = modulo_key
        self.visible = bool(visible)
        for k, v in kwargs.items():
            setattr(self, k, v)


class UsuarioDashboardVis:
    def __init__(self, id=None, usuario_id=None, modulo_key=None, visible=True, **kwargs):
        self.id = id
        self.usuario_id = usuario_id
        self.modulo_key = modulo_key
        self.visible = bool(visible)
        for k, v in kwargs.items():
            setattr(self, k, v)


MODULOS_DASHBOARD = [
    'guion', 'mantenimiento', 'premio', 'contrato',
    'balance', 'tarea', 'patrocinador', 'usuario',
    'actividad', 'enlinea',
]

MODULOS_DASHBOARD_INFO = {
    'guion': {'nombre': 'Guión', 'icono': 'fa-scroll', 'color': 'blue'},
    'mantenimiento': {'nombre': 'Mantenimiento', 'icono': 'fa-tools', 'color': 'amber'},
    'premio': {'nombre': 'Premios', 'icono': 'fa-gift', 'color': 'purple'},
    'contrato': {'nombre': 'Contratos', 'icono': 'fa-file-contract', 'color': 'cyan'},
    'balance': {'nombre': 'Balance', 'icono': 'fa-balance-scale', 'color': 'green'},
    'tarea': {'nombre': 'Tareas', 'icono': 'fa-tasks', 'color': 'orange'},
    'patrocinador': {'nombre': 'Patrocinantes', 'icono': 'fa-handshake', 'color': 'pink'},
    'usuario': {'nombre': 'Usuarios', 'icono': 'fa-users', 'color': 'indigo'},
    'actividad': {'nombre': 'Actividad Reciente', 'icono': 'fa-history', 'color': 'blue'},
    'enlinea': {'nombre': 'Usuarios en Línea', 'icono': 'fa-user-friends', 'color': 'green'},
}
