from datetime import datetime
from app.repositories.base_repository import BaseRepository
from app.models.bitacora import SesionUsuario, ActividadUsuario, CambioPorModulo, ErrorAplicacion
from app.repositories.usuario_repository import UsuarioRepository


class SesionRepository(BaseRepository):
    def __init__(self):
        super().__init__('no_funcional')

    def consultar(self, **filtros):
        sql = "SELECT * FROM sesiones_usuario WHERE 1=1"
        params = []
        if filtros.get('usuario_id'):
            sql += " AND usuario_id = %s"
            params.append(filtros['usuario_id'])
        sql += " ORDER BY inicio_sesion DESC"
        rows = self.fetch_all(sql, params)
        sesiones = [SesionUsuario(**r) for r in rows]
        self._cargar_nombres_usuario(sesiones)
        return sesiones

    def _cargar_nombres_usuario(self, items):
        user_ids = set()
        for item in items:
            if hasattr(item, 'usuario_id') and item.usuario_id:
                user_ids.add(item.usuario_id)
        if not user_ids:
            return
        user_repo = UsuarioRepository()
        for uid in user_ids:
            user = user_repo.obtener_por_id(uid)
            for item in items:
                if getattr(item, 'usuario_id', None) == uid:
                    item.usuario = user

    def obtener_por_id(self, id_registro):
        row = self.fetch_one("SELECT * FROM sesiones_usuario WHERE id = %s", (id_registro,))
        return SesionUsuario(**row) if row else None

    def registrar(self, datos):
        id = self.execute(
            "INSERT INTO sesiones_usuario (usuario_id, inicio_sesion, ip_address, user_agent) VALUES (%s, NOW(), %s, %s)",
            (datos['usuario_id'], datos.get('ip_address'), datos.get('user_agent'))
        )
        return self.obtener_por_id(id)

    def modificar(self, id_registro, datos):
        sets = []
        params = []
        for campo in ['fin_sesion', 'duracion_segundos', 'ip_address', 'user_agent']:
            if campo in datos:
                sets.append(f"{campo} = %s")
                params.append(datos[campo])
        if sets:
            params.append(id_registro)
            self.execute(f"UPDATE sesiones_usuario SET {', '.join(sets)} WHERE id = %s", params)
        return self.obtener_por_id(id_registro)

    def eliminar(self, id_registro):
        self.execute("DELETE FROM sesiones_usuario WHERE id = %s", (id_registro,))
        return True

    def cerrar_sesion(self, sesion_id):
        s = self.obtener_por_id(sesion_id)
        if not s:
            return None
        fin = datetime.utcnow()
        duracion = None
        if s.inicio_sesion:
            duracion = int((fin - s.inicio_sesion).total_seconds())
        self.modificar(sesion_id, {'fin_sesion': fin, 'duracion_segundos': duracion})
        return self.obtener_por_id(sesion_id)


class ActividadRepository(BaseRepository):
    def __init__(self):
        super().__init__('no_funcional')

    def consultar(self, **filtros):
        sql = "SELECT * FROM actividad_usuario WHERE 1=1"
        params = []
        if filtros.get('usuario_id'):
            sql += " AND usuario_id = %s"
            params.append(filtros['usuario_id'])
        if filtros.get('modulo'):
            sql += " AND modulo = %s"
            params.append(filtros['modulo'])
        if filtros.get('tipo_accion'):
            sql += " AND tipo_accion = %s"
            params.append(filtros['tipo_accion'])
        if filtros.get('fecha_desde'):
            sql += " AND created_at >= %s"
            params.append(filtros['fecha_desde'])
        if filtros.get('fecha_hasta'):
            sql += " AND created_at <= %s"
            params.append(filtros['fecha_hasta'])
        sql += " ORDER BY created_at DESC"
        if filtros.get('limite'):
            sql += " LIMIT %s"
            params.append(filtros['limite'])
        rows = self.fetch_all(sql, params)
        items = [ActividadUsuario(**r) for r in rows]
        SesionRepository()._cargar_nombres_usuario(items)
        return items

    def obtener_por_id(self, id_registro):
        row = self.fetch_one("SELECT * FROM actividad_usuario WHERE id = %s", (id_registro,))
        return ActividadUsuario(**row) if row else None

    def registrar(self, datos):
        id = self.execute(
            """INSERT INTO actividad_usuario
               (sesion_id, usuario_id, tipo_accion, modulo, accion, detalle, pagina, ip_address, created_at)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())""",
            (
                datos.get('sesion_id'), datos['usuario_id'],
                datos['tipo_accion'], datos['modulo'],
                datos.get('accion', ''), str(datos.get('detalle', '')),
                datos.get('pagina'), datos.get('ip_address'),
            )
        )
        return self.obtener_por_id(id)

    def modificar(self, id_registro, datos):
        sets = []
        params = []
        for campo in ['tipo_accion', 'modulo', 'accion', 'detalle', 'pagina']:
            if campo in datos:
                sets.append(f"{campo} = %s")
                params.append(datos[campo])
        if sets:
            params.append(id_registro)
            self.execute(f"UPDATE actividad_usuario SET {', '.join(sets)} WHERE id = %s", params)
        return self.obtener_por_id(id_registro)

    def eliminar(self, id_registro):
        self.execute("DELETE FROM actividad_usuario WHERE id = %s", (id_registro,))
        return True

    def obtener_modulos_distintos(self):
        rows = self.fetch_all("SELECT DISTINCT modulo FROM actividad_usuario WHERE modulo IS NOT NULL")
        return [r['modulo'] for r in rows]


class CambioRepository(BaseRepository):
    def __init__(self):
        super().__init__('no_funcional')

    def consultar(self, **filtros):
        sql = "SELECT * FROM cambios_por_modulo WHERE 1=1"
        params = []
        if filtros.get('actividad_id'):
            sql += " AND actividad_id = %s"
            params.append(filtros['actividad_id'])
        if filtros.get('tabla_afectada'):
            sql += " AND tabla_afectada = %s"
            params.append(filtros['tabla_afectada'])
        if filtros.get('actividad_ids'):
            ids = filtros['actividad_ids']
            placeholders = ', '.join(['%s'] * len(ids))
            sql += f" AND actividad_id IN ({placeholders})"
            params.extend(ids)
        sql += " ORDER BY created_at DESC"
        rows = self.fetch_all(sql, params)
        return [CambioPorModulo(**r) for r in rows]

    def obtener_por_id(self, id_registro):
        row = self.fetch_one("SELECT * FROM cambios_por_modulo WHERE id = %s", (id_registro,))
        return CambioPorModulo(**row) if row else None

    def registrar(self, datos):
        id = self.execute(
            """INSERT INTO cambios_por_modulo
               (actividad_id, tabla_afectada, registro_id, campo, valor_anterior, valor_nuevo, created_at)
               VALUES (%s, %s, %s, %s, %s, %s, NOW())""",
            (
                datos['actividad_id'], datos['tabla_afectada'],
                datos.get('registro_id'), datos['campo'],
                datos.get('valor_anterior'), datos.get('valor_nuevo'),
            )
        )
        return CambioPorModulo(id=id, **datos)

    def modificar(self, id_registro, datos):
        pass

    def eliminar(self, id_registro):
        self.execute("DELETE FROM cambios_por_modulo WHERE id = %s", (id_registro,))
        return True


class ErrorRepository(BaseRepository):
    def __init__(self):
        super().__init__('no_funcional')

    def consultar(self, **filtros):
        sql = "SELECT * FROM errores_aplicacion WHERE 1=1"
        params = []
        if filtros.get('usuario_id'):
            sql += " AND usuario_id = %s"
            params.append(filtros['usuario_id'])
        if filtros.get('tipo_error'):
            sql += " AND tipo_error = %s"
            params.append(filtros['tipo_error'])
        sql += " ORDER BY created_at DESC"
        if filtros.get('limite'):
            sql += " LIMIT %s"
            params.append(filtros['limite'])
        rows = self.fetch_all(sql, params)
        items = [ErrorAplicacion(**r) for r in rows]
        SesionRepository()._cargar_nombres_usuario(items)
        return items

    def obtener_por_id(self, id_registro):
        row = self.fetch_one("SELECT * FROM errores_aplicacion WHERE id = %s", (id_registro,))
        return ErrorAplicacion(**row) if row else None

    def registrar(self, datos):
        id = self.execute(
            """INSERT INTO errores_aplicacion
               (usuario_id, tipo_error, mensaje, traceback, pagina, ip_address, created_at)
               VALUES (%s, %s, %s, %s, %s, %s, NOW())""",
            (
                datos.get('usuario_id'), datos['tipo_error'],
                datos['mensaje'], datos.get('traceback'),
                datos.get('pagina'), datos.get('ip_address'),
            )
        )
        return self.obtener_por_id(id)

    def modificar(self, id_registro, datos):
        pass

    def eliminar(self, id_registro):
        self.execute("DELETE FROM errores_aplicacion WHERE id = %s", (id_registro,))
        return True
