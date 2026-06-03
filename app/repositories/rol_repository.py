from app.repositories.base_repository import BaseRepository
from app.models.rol import Rol, Permiso, RolPermiso, UsuarioPermiso


class RolRepository(BaseRepository):
    def __init__(self):
        super().__init__('no_funcional')

    def _row_to_rol(self, row):
        return Rol(**row) if row else None

    def consultar(self, **filtros):
        sql = "SELECT * FROM roles WHERE 1=1"
        params = []
        if filtros.get('nombre'):
            sql += " AND nombre = %s"
            params.append(filtros['nombre'])
        sql += " ORDER BY nombre"
        rows = self.fetch_all(sql, params)
        return [Rol(**r) for r in rows]

    def obtener_por_id(self, id_registro):
        row = self.fetch_one("SELECT * FROM roles WHERE id = %s", (id_registro,))
        return self._row_to_rol(row)

    def obtener_por_nombre(self, nombre):
        row = self.fetch_one("SELECT * FROM roles WHERE nombre = %s", (nombre,))
        return self._row_to_rol(row)

    def registrar(self, datos):
        id = self.execute(
            "INSERT INTO roles (nombre, descripcion) VALUES (%s, %s)",
            (datos['nombre'], datos.get('descripcion', ''))
        )
        return self.obtener_por_id(id)

    def modificar(self, id_registro, datos):
        sets = []
        params = []
        for campo in ['nombre', 'descripcion']:
            if campo in datos:
                sets.append(f"{campo} = %s")
                params.append(datos[campo])
        if sets:
            params.append(id_registro)
            self.execute(f"UPDATE roles SET {', '.join(sets)} WHERE id = %s", params)
        return self.obtener_por_id(id_registro)

    def eliminar(self, id_registro):
        self.execute("DELETE FROM roles WHERE id = %s", (id_registro,))
        return True


class PermisoRepository(BaseRepository):
    def __init__(self):
        super().__init__('no_funcional')

    def consultar(self, **filtros):
        sql = "SELECT * FROM permisos WHERE 1=1"
        params = []
        if filtros.get('modulo'):
            sql += " AND modulo = %s"
            params.append(filtros['modulo'])
        sql += " ORDER BY modulo, nombre"
        rows = self.fetch_all(sql, params)
        return [Permiso(**r) for r in rows]

    def obtener_por_id(self, id_registro):
        row = self.fetch_one("SELECT * FROM permisos WHERE id = %s", (id_registro,))
        return Permiso(**row) if row else None

    def obtener_por_codigo(self, codigo):
        row = self.fetch_one("SELECT * FROM permisos WHERE codigo = %s", (codigo,))
        return Permiso(**row) if row else None

    def obtener_por_modulos(self):
        permisos = self.consultar()
        agrupados = {}
        for p in permisos:
            agrupados.setdefault(p.modulo, []).append(p)
        return agrupados

    def registrar(self, datos):
        id = self.execute(
            "INSERT INTO permisos (nombre, codigo, modulo, descripcion) VALUES (%s, %s, %s, %s)",
            (datos['nombre'], datos['codigo'], datos['modulo'], datos.get('descripcion', ''))
        )
        return self.obtener_por_id(id)

    def modificar(self, id_registro, datos):
        sets = []
        params = []
        for campo in ['nombre', 'codigo', 'modulo', 'descripcion']:
            if campo in datos:
                sets.append(f"{campo} = %s")
                params.append(datos[campo])
        if sets:
            params.append(id_registro)
            self.execute(f"UPDATE permisos SET {', '.join(sets)} WHERE id = %s", params)
        return self.obtener_por_id(id_registro)

    def eliminar(self, id_registro):
        self.execute("DELETE FROM permisos WHERE id = %s", (id_registro,))
        return True


class RolPermisoRepository(BaseRepository):
    def __init__(self):
        super().__init__('no_funcional')

    def consultar(self, **filtros):
        sql = "SELECT * FROM rol_permiso WHERE 1=1"
        params = []
        if filtros.get('rol_id'):
            sql += " AND rol_id = %s"
            params.append(filtros['rol_id'])
        rows = self.fetch_all(sql, params)
        return [RolPermiso(**r) for r in rows]

    def obtener_por_rol(self, rol_id):
        return self.consultar(rol_id=rol_id)

    def obtener_permisos_por_rol(self, rol_id):
        rows = self.fetch_all(
            """SELECT p.* FROM permisos p
               JOIN rol_permiso rp ON p.id = rp.permiso_id
               WHERE rp.rol_id = %s""",
            (rol_id,)
        )
        return [Permiso(**r) for r in rows]

    def registrar(self, datos):
        try:
            id = self.execute(
                "INSERT INTO rol_permiso (rol_id, permiso_id) VALUES (%s, %s)",
                (datos['rol_id'], datos['permiso_id'])
            )
            return RolPermiso(id=id, **datos)
        except Exception:
            self.rollback()
            return None

    def modificar(self, id_registro, datos):
        pass

    def eliminar(self, id_registro):
        self.execute("DELETE FROM rol_permiso WHERE id = %s", (id_registro,))
        return True

    def sincronizar_rol_permisos(self, rol_id, permiso_ids):
        self.execute("DELETE FROM rol_permiso WHERE rol_id = %s", (rol_id,))
        for pid in permiso_ids:
            self.execute(
                "INSERT INTO rol_permiso (rol_id, permiso_id) VALUES (%s, %s)",
                (rol_id, pid)
            )


class UsuarioPermisoRepository(BaseRepository):
    def __init__(self):
        super().__init__('no_funcional')

    def consultar(self, **filtros):
        sql = "SELECT * FROM usuario_permiso WHERE 1=1"
        params = []
        if filtros.get('usuario_id'):
            sql += " AND usuario_id = %s"
            params.append(filtros['usuario_id'])
        rows = self.fetch_all(sql, params)
        return [UsuarioPermiso(**r) for r in rows]

    def obtener_por_usuario(self, usuario_id):
        return self.consultar(usuario_id=usuario_id)

    def obtener_permisos_por_usuario(self, usuario_id):
        rows = self.fetch_all(
            """SELECT p.* FROM permisos p
               JOIN usuario_permiso up ON p.id = up.permiso_id
               WHERE up.usuario_id = %s""",
            (usuario_id,)
        )
        return [Permiso(**r) for r in rows]

    def registrar(self, datos):
        try:
            id = self.execute(
                "INSERT INTO usuario_permiso (usuario_id, permiso_id) VALUES (%s, %s)",
                (datos['usuario_id'], datos['permiso_id'])
            )
            return UsuarioPermiso(id=id, **datos)
        except Exception:
            self.rollback()
            return None

    def modificar(self, id_registro, datos):
        pass

    def eliminar(self, id_registro):
        self.execute("DELETE FROM usuario_permiso WHERE id = %s", (id_registro,))
        return True

    def sincronizar_usuario_permisos(self, usuario_id, permiso_ids, permiso_ids_rol):
        permisos_individuales = set(permiso_ids) - set(permiso_ids_rol)
        actuales_rows = self.fetch_all(
            "SELECT permiso_id FROM usuario_permiso WHERE usuario_id = %s",
            (usuario_id,)
        )
        actuales = {r['permiso_id'] for r in actuales_rows}
        nuevas = permisos_individuales - actuales
        remover = actuales - permisos_individuales
        for pid in nuevas:
            self.execute(
                "INSERT INTO usuario_permiso (usuario_id, permiso_id, fecha_asignacion) VALUES (%s, %s, NOW())",
                (usuario_id, pid)
            )
        if remover:
            ids_str = ','.join(str(pid) for pid in remover)
            self.execute(
                f"DELETE FROM usuario_permiso WHERE usuario_id = %s AND permiso_id IN ({ids_str})",
                (usuario_id,)
            )

    def obtener_permisos_usuario(self, usuario_id, rol_nombre):
        sql = """
            SELECT p.codigo FROM permisos p
            JOIN rol_permiso rp ON p.id = rp.permiso_id
            JOIN roles r ON r.id = rp.rol_id
            WHERE r.nombre = %s
            UNION
            SELECT p.codigo FROM permisos p
            JOIN usuario_permiso up ON p.id = up.permiso_id
            WHERE up.usuario_id = %s
        """
        rows = self.fetch_all(sql, (rol_nombre, usuario_id))
        return {r['codigo'] for r in rows}
