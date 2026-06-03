from app.repositories.rol_repository import (
    RolRepository, PermisoRepository,
    RolPermisoRepository, UsuarioPermisoRepository
)
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.dashboard_visibilidad_repository import DashboardVisibilidadRepository
from app.models.dashboard_visibilidad import MODULOS_DASHBOARD_INFO
from app.traits.validaciones import ValidacionesMixin

PERMISOS_CATALOGO = [
    {'codigo': 'dashboard.view', 'nombre': 'Ver panel principal', 'modulo': 'Dashboard'},
    {'codigo': 'usuario.view', 'nombre': 'Ver lista de usuarios', 'modulo': 'Usuarios'},
    {'codigo': 'usuario.create', 'nombre': 'Crear usuarios', 'modulo': 'Usuarios'},
    {'codigo': 'usuario.edit', 'nombre': 'Editar usuarios', 'modulo': 'Usuarios'},
    {'codigo': 'usuario.delete', 'nombre': 'Eliminar usuarios', 'modulo': 'Usuarios'},
    {'codigo': 'usuario.perfil', 'nombre': 'Ver perfil propio', 'modulo': 'Usuarios'},
    {'codigo': 'guion.view', 'nombre': 'Ver guiones', 'modulo': 'Guión'},
    {'codigo': 'guion.create', 'nombre': 'Crear guiones', 'modulo': 'Guión'},
    {'codigo': 'guion.edit', 'nombre': 'Editar guiones', 'modulo': 'Guión'},
    {'codigo': 'guion.delete', 'nombre': 'Eliminar guiones', 'modulo': 'Guión'},
    {'codigo': 'guion.publish', 'nombre': 'Publicar guiones', 'modulo': 'Guión'},
    {'codigo': 'guion.preview', 'nombre': 'Previsualizar guiones', 'modulo': 'Guión'},
    {'codigo': 'envivo.view', 'nombre': 'Ver pantalla en vivo', 'modulo': 'En Vivo'},
    {'codigo': 'envivo.control', 'nombre': 'Controlar elementos en vivo', 'modulo': 'En Vivo'},
    {'codigo': 'premio.view', 'nombre': 'Ver premios', 'modulo': 'Premios'},
    {'codigo': 'premio.create', 'nombre': 'Crear premios', 'modulo': 'Premios'},
    {'codigo': 'premio.edit', 'nombre': 'Editar premios', 'modulo': 'Premios'},
    {'codigo': 'premio.delete', 'nombre': 'Eliminar premios', 'modulo': 'Premios'},
    {'codigo': 'premio.entregar', 'nombre': 'Entregar premios', 'modulo': 'Premios'},
    {'codigo': 'mantenimiento.view', 'nombre': 'Ver mantenimiento', 'modulo': 'Mantenimiento'},
    {'codigo': 'mantenimiento.edit', 'nombre': 'Editar recursos', 'modulo': 'Mantenimiento'},
    {'codigo': 'mantenimiento.delete', 'nombre': 'Eliminar recursos', 'modulo': 'Mantenimiento'},
    {'codigo': 'gestion_tarea.view', 'nombre': 'Ver tareas', 'modulo': 'Tareas'},
    {'codigo': 'gestion_tarea.create', 'nombre': 'Crear tareas', 'modulo': 'Tareas'},
    {'codigo': 'gestion_tarea.edit', 'nombre': 'Editar tareas', 'modulo': 'Tareas'},
    {'codigo': 'gestion_tarea.delete', 'nombre': 'Eliminar tareas', 'modulo': 'Tareas'},
    {'codigo': 'gestion_tarea.complete', 'nombre': 'Completar tareas propias', 'modulo': 'Tareas'},
    {'codigo': 'patrocinador.view', 'nombre': 'Ver patrocinadores', 'modulo': 'Patrocinadores'},
    {'codigo': 'patrocinador.create', 'nombre': 'Crear patrocinadores', 'modulo': 'Patrocinadores'},
    {'codigo': 'patrocinador.edit', 'nombre': 'Editar patrocinadores', 'modulo': 'Patrocinadores'},
    {'codigo': 'patrocinador.delete', 'nombre': 'Eliminar patrocinadores', 'modulo': 'Patrocinadores'},
    {'codigo': 'contrato.view', 'nombre': 'Ver contratos', 'modulo': 'Contratos'},
    {'codigo': 'contrato.create', 'nombre': 'Crear contratos', 'modulo': 'Contratos'},
    {'codigo': 'contrato.edit', 'nombre': 'Editar contratos', 'modulo': 'Contratos'},
    {'codigo': 'contrato.delete', 'nombre': 'Eliminar contratos', 'modulo': 'Contratos'},
    {'codigo': 'balance.view', 'nombre': 'Ver balance', 'modulo': 'Balance'},
    {'codigo': 'balance.create', 'nombre': 'Registrar pagos', 'modulo': 'Balance'},
    {'codigo': 'balance.edit', 'nombre': 'Editar pagos', 'modulo': 'Balance'},
    {'codigo': 'balance.delete', 'nombre': 'Eliminar pagos', 'modulo': 'Balance'},
    {'codigo': 'rol.view', 'nombre': 'Ver roles y permisos', 'modulo': 'Roles'},
    {'codigo': 'rol.edit', 'nombre': 'Editar permisos de usuarios', 'modulo': 'Roles'},
    {'codigo': 'inventario.view', 'nombre': 'Ver inventario de recursos', 'modulo': 'Inventario'},
    {'codigo': 'inventario.create', 'nombre': 'Crear recursos', 'modulo': 'Inventario'},
    {'codigo': 'inventario.edit', 'nombre': 'Editar recursos', 'modulo': 'Inventario'},
    {'codigo': 'inventario.delete', 'nombre': 'Eliminar recursos', 'modulo': 'Inventario'},
    {'codigo': 'inventario.assign', 'nombre': 'Asignar y devolver recursos', 'modulo': 'Inventario'},
    {'codigo': 'reels.view', 'nombre': 'Ver reels', 'modulo': 'Reels'},
    {'codigo': 'reels.create', 'nombre': 'Crear reels', 'modulo': 'Reels'},
    {'codigo': 'reels.edit', 'nombre': 'Editar reels', 'modulo': 'Reels'},
    {'codigo': 'reels.delete', 'nombre': 'Eliminar reels', 'modulo': 'Reels'},
]

PERMISOS_POR_ROL = {
    'Superadmin': [p['codigo'] for p in PERMISOS_CATALOGO],
    'Administrador': [p['codigo'] for p in PERMISOS_CATALOGO if not p['codigo'].startswith('rol.')],
    'Usuario': [
        'dashboard.view', 'guion.view', 'envivo.view',
        'usuario.perfil', 'usuario.view',
        'premio.view', 'mantenimiento.view',
        'patrocinador.view', 'contrato.view',
        'balance.view', 'gestion_tarea.view',
        'inventario.view', 'reels.view',
    ],
}


class RolService(ValidacionesMixin):
    def __init__(self):
        self.rol_repo = RolRepository()
        self.permiso_repo = PermisoRepository()
        self.rol_permiso_repo = RolPermisoRepository()
        self.usuario_permiso_repo = UsuarioPermisoRepository()
        self.usuario_repo = UsuarioRepository()
        self.dash_vis_repo = DashboardVisibilidadRepository()

    def seed_permisos_iniciales(self):
        for p in PERMISOS_CATALOGO:
            if not self.permiso_repo.obtener_por_codigo(p['codigo']):
                self.permiso_repo.registrar(p)

        roles_existentes = self.rol_repo.consultar()
        if roles_existentes:
            return

        for nombre_rol, desc in [('Superadmin', 'Acceso total al sistema'),
                                  ('Administrador', 'Acceso administrativo excepto roles'),
                                  ('Usuario', 'Acceso básico de lectura')]:
            rol = self.rol_repo.registrar({'nombre': nombre_rol, 'descripcion': desc})
            codigos = PERMISOS_POR_ROL.get(nombre_rol, [])
            for codigo in codigos:
                permiso = self.permiso_repo.obtener_por_codigo(codigo)
                if permiso:
                    self.rol_permiso_repo.registrar({'rol_id': rol.id, 'permiso_id': permiso.id})

    def obtener_dashboard(self):
        usuarios = self.usuario_repo.consultar()
        roles = {r.nombre: r for r in self.rol_repo.consultar()}
        permisos_rol_cache = {}
        for nombre_rol, rol in roles.items():
            permisos_rol_cache[nombre_rol] = {p.codigo for p in self.rol_permiso_repo.obtener_permisos_por_rol(rol.id)}

        usuarios_data = []
        for u in usuarios:
            individuales = {up.permiso_id for up in self.usuario_permiso_repo.obtener_por_usuario(u.id)}
            de_rol = permisos_rol_cache.get(u.rol, set())
            total_permisos = len(de_rol | individuales)
            usuarios_data.append({
                'usuario': u,
                'total_permisos': total_permisos,
                'de_rol': len(de_rol),
                'individuales': len(individuales),
            })

        todos_permisos = self.permiso_repo.consultar()
        roles_data = []
        for nombre_rol, rol_obj in roles.items():
            total_permisos = len(permisos_rol_cache.get(nombre_rol, set()))
            cant_usuarios = self.usuario_repo.contar(rol=nombre_rol)
            roles_data.append({
                'rol': rol_obj,
                'nombre': nombre_rol,
                'total_permisos': total_permisos,
                'cant_usuarios': cant_usuarios,
                'total_posible': len(todos_permisos),
            })

        return {
            'usuarios': usuarios_data,
            'roles': roles_data,
            'total_usuarios': len(usuarios),
            'total_permisos': len(todos_permisos),
        }

    def obtener_datos_editar(self, usuario_id):
        usuario = self.usuario_repo.obtener_por_id(usuario_id)
        if not usuario:
            return None
        rol = self.rol_repo.obtener_por_nombre(usuario.rol)
        permisos_rol = set()
        if rol:
            permisos_rol = {p.id for p in self.rol_permiso_repo.obtener_permisos_por_rol(rol.id)}

        permisos_individuales = {up.permiso_id for up in self.usuario_permiso_repo.obtener_por_usuario(usuario_id)}

        permisos_agrupados = self.permiso_repo.obtener_por_modulos()

        return {
            'usuario': usuario,
            'permisos_agrupados': permisos_agrupados,
            'permisos_rol': permisos_rol,
            'permisos_individuales': permisos_individuales,
        }

    def actualizar_permisos(self, usuario_id, permiso_ids_seleccionados):
        usuario = self.usuario_repo.obtener_por_id(usuario_id)
        if not usuario:
            return False
        rol = self.rol_repo.obtener_por_nombre(usuario.rol)
        permiso_ids_rol = set()
        if rol:
            permiso_ids_rol = {p.id for p in self.rol_permiso_repo.obtener_permisos_por_rol(rol.id)}

        seleccionados = set(int(pid) for pid in permiso_ids_seleccionados)

        self.usuario_permiso_repo.sincronizar_usuario_permisos(
            usuario_id, seleccionados, permiso_ids_rol
        )
        return True

    def crear_rol(self, nombre, descripcion, permiso_ids):
        self.limpiar_errores()
        existente = self.rol_repo.obtener_por_nombre(nombre)
        if existente:
            self.errores.append(f'Ya existe un rol con el nombre "{nombre}"')
            return None

        rol = self.rol_repo.registrar({'nombre': nombre, 'descripcion': descripcion})

        if permiso_ids:
            seleccionados = [int(pid) for pid in permiso_ids]
            self.rol_permiso_repo.sincronizar_rol_permisos(rol.id, seleccionados)

        return rol

    def obtener_datos_editar_rol(self, rol_id):
        rol = self.rol_repo.obtener_por_id(rol_id)
        if not rol:
            return None
        permisos_del_rol = {p.id for p in self.rol_permiso_repo.obtener_permisos_por_rol(rol_id)}
        permisos_agrupados = self.permiso_repo.obtener_por_modulos()
        total_usuarios = self.usuario_repo.contar(rol=rol.nombre)
        return {
            'rol': rol,
            'permisos_agrupados': permisos_agrupados,
            'permisos_del_rol': permisos_del_rol,
            'total_usuarios': total_usuarios,
        }

    def actualizar_permisos_rol(self, rol_id, permiso_ids_seleccionados):
        self.limpiar_errores()
        seleccionados = [int(pid) for pid in permiso_ids_seleccionados]
        self.rol_permiso_repo.sincronizar_rol_permisos(rol_id, seleccionados)
        return True

    def obtener_datos_visibilidad_rol(self, rol_id):
        vis = self.dash_vis_repo.obtener_por_rol(rol_id)
        return {
            'modulos_dashboard_info': MODULOS_DASHBOARD_INFO,
            'dashboard_visibles_rol': {k for k, v in vis.items() if v.visible},
            'dashboard_modulos_rol': vis,
        }

    def guardar_visibilidad_dashboard_rol(self, rol_id, modulos_visibles):
        self.dash_vis_repo.guardar_para_rol(rol_id, modulos_visibles)
        return True

    def obtener_datos_visibilidad_usuario(self, usuario_id, rol_nombre):
        rol_repo = RolRepository()
        rol = rol_repo.obtener_por_nombre(rol_nombre)
        vis_rol = self.dash_vis_repo.obtener_por_rol(rol.id) if rol else {}
        vis_user = self.dash_vis_repo.obtener_por_usuario(usuario_id)

        base_rol = {k for k, v in vis_rol.items() if v.visible}
        user_keys = set(vis_user.keys())

        return {
            'modulos_dashboard_info': MODULOS_DASHBOARD_INFO,
            'dashboard_base_rol': base_rol,
            'dashboard_user_overrides': user_keys,
            'dashboard_vis_user': vis_user,
        }

    def guardar_visibilidad_dashboard_usuario(self, usuario_id, modulos_visibles):
        self.dash_vis_repo.guardar_para_usuario(usuario_id, modulos_visibles)
        return True
