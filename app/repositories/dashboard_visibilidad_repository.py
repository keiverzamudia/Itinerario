from app.repositories.base_repository import BaseRepository
from app.models.dashboard_visibilidad import DashboardVisibilidad, UsuarioDashboardVis, MODULOS_DASHBOARD


class DashboardVisibilidadRepository(BaseRepository):
    def __init__(self):
        super().__init__('no_funcional')

    def obtener_por_rol(self, rol_id):
        rows = self.fetch_all(
            "SELECT * FROM dashboard_visibilidad WHERE rol_id = %s", (rol_id,)
        )
        return {r['modulo_key']: DashboardVisibilidad(**r) for r in rows}

    def obtener_modulos_visibles_rol(self, rol_id):
        rows = self.fetch_all(
            "SELECT modulo_key FROM dashboard_visibilidad WHERE rol_id = %s AND visible = 1",
            (rol_id,)
        )
        return {r['modulo_key'] for r in rows}

    def guardar_para_rol(self, rol_id, modulos_visibles):
        self.execute("DELETE FROM dashboard_visibilidad WHERE rol_id = %s", (rol_id,))
        for key in MODULOS_DASHBOARD:
            visible = 1 if key in modulos_visibles else 0
            self.execute(
                "INSERT INTO dashboard_visibilidad (rol_id, modulo_key, visible) VALUES (%s, %s, %s)",
                (rol_id, key, visible)
            )

    def obtener_por_usuario(self, usuario_id):
        rows = self.fetch_all(
            "SELECT * FROM usuario_dashboard_vis WHERE usuario_id = %s", (usuario_id,)
        )
        return {r['modulo_key']: UsuarioDashboardVis(**r) for r in rows}

    def obtener_modulos_visibles_usuario(self, usuario_id):
        rows = self.fetch_all(
            "SELECT modulo_key FROM usuario_dashboard_vis WHERE usuario_id = %s AND visible = 1",
            (usuario_id,)
        )
        return {r['modulo_key'] for r in rows}

    def guardar_para_usuario(self, usuario_id, modulos_visibles):
        self.execute("DELETE FROM usuario_dashboard_vis WHERE usuario_id = %s", (usuario_id,))
        for key in MODULOS_DASHBOARD:
            visible = 1 if key in modulos_visibles else 0
            self.execute(
                "INSERT INTO usuario_dashboard_vis (usuario_id, modulo_key, visible) VALUES (%s, %s, %s)",
                (usuario_id, key, visible)
            )

    def obtener_modulos_visibles_final(self, usuario_id, rol_nombre):
        from app.repositories.rol_repository import RolRepository
        rol_repo = RolRepository()
        rol = rol_repo.obtener_por_nombre(rol_nombre)
        if not rol:
            return set(MODULOS_DASHBOARD)

        role_config = self.obtener_por_rol(rol.id)
        user_overrides = self.obtener_por_usuario(usuario_id)

        resultado = set()
        for key in MODULOS_DASHBOARD:
            if key in user_overrides:
                if user_overrides[key].visible:
                    resultado.add(key)
            elif key in role_config:
                if role_config[key].visible:
                    resultado.add(key)
            else:
                resultado.add(key)
        return resultado
