from app.repositories.base_repository import BaseRepository
from app.models.inventario import (
    TipoRecurso, EstadoRecurso, EstadoAsignacion,
    RecursoInventario, AsignacionRecurso
)


class TipoRecursoRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def consultar(self):
        rows = self.fetch_all("SELECT * FROM tipo_recurso ORDER BY nombre")
        return [TipoRecurso(**r) for r in rows]

    def obtener_por_id(self, id):
        row = self.fetch_one("SELECT * FROM tipo_recurso WHERE id = %s", (id,))
        return TipoRecurso(**row) if row else None

    def registrar(self, datos):
        id = self.execute(
            "INSERT INTO tipo_recurso (nombre, descripcion) VALUES (%s, %s)",
            (datos.get('nombre'), datos.get('descripcion'))
        )
        return self.obtener_por_id(id)

    def modificar(self, id, datos):
        self.execute(
            "UPDATE tipo_recurso SET nombre = %s, descripcion = %s WHERE id = %s",
            (datos.get('nombre'), datos.get('descripcion'), id)
        )
        return self.obtener_por_id(id)

    def eliminar(self, id):
        self.execute("DELETE FROM tipo_recurso WHERE id = %s", (id,))

    def en_uso(self, id):
        row = self.fetch_one(
            "SELECT COUNT(*) as total FROM recursos WHERE tipo_id = %s AND eliminado = 0", (id,)
        )
        return row['total'] > 0 if row else False


class EstadoRecursoRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def consultar(self):
        rows = self.fetch_all("SELECT * FROM estado_recurso ORDER BY id")
        return [EstadoRecurso(**r) for r in rows]

    def obtener_por_id(self, id):
        row = self.fetch_one("SELECT * FROM estado_recurso WHERE id = %s", (id,))
        return EstadoRecurso(**row) if row else None


class EstadoAsignacionRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def consultar(self):
        rows = self.fetch_all("SELECT * FROM estado_asignacion ORDER BY id")
        return [EstadoAsignacion(**r) for r in rows]

    def obtener_por_id(self, id):
        row = self.fetch_one("SELECT * FROM estado_asignacion WHERE id = %s", (id,))
        return EstadoAsignacion(**row) if row else None


class RecursoInventarioRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def consultar(self, solo_activos=True, tipo_id=None, estado_id=None):
        sql = """SELECT r.*, t.nombre as tipo_nombre, e.nombre as estado_nombre
                 FROM recursos r
                 LEFT JOIN tipo_recurso t ON r.tipo_id = t.id
                 LEFT JOIN estado_recurso e ON r.estado_id = e.id
                 WHERE 1=1"""
        params = []
        if solo_activos:
            sql += " AND r.eliminado = 0"
        if tipo_id:
            sql += " AND r.tipo_id = %s"
            params.append(tipo_id)
        if estado_id:
            sql += " AND r.estado_id = %s"
            params.append(estado_id)
        sql += " ORDER BY r.creado_en DESC"
        rows = self.fetch_all(sql, params)
        return [RecursoInventario(**r) for r in rows]

    def obtener_por_id(self, id):
        row = self.fetch_one(
            """SELECT r.*, t.nombre as tipo_nombre, e.nombre as estado_nombre
               FROM recursos r
               LEFT JOIN tipo_recurso t ON r.tipo_id = t.id
               LEFT JOIN estado_recurso e ON r.estado_id = e.id
               WHERE r.id = %s""",
            (id,)
        )
        return RecursoInventario(**row) if row else None

    def contar(self, solo_activos=True, estado_id=None):
        sql = "SELECT COUNT(*) as total FROM recursos WHERE 1=1"
        params = []
        if solo_activos:
            sql += " AND eliminado = 0"
        if estado_id:
            sql += " AND estado_id = %s"
            params.append(estado_id)
        row = self.fetch_one(sql, params)
        return row['total'] if row else 0

    def registrar(self, datos):
        fields = ['nombre', 'descripcion', 'tipo_id', 'estado_id', 'fecha_compra', 'costo', 'creado_en']
        cols = [f for f in fields if f in datos]
        placeholders = ', '.join(['%s'] * len(cols))
        sql = f"INSERT INTO recursos ({', '.join(cols)}) VALUES ({placeholders})"
        params = [datos[f] for f in cols]
        id = self.execute(sql, params)
        return self.obtener_por_id(id)

    def modificar(self, id, datos):
        sets = []
        params = []
        for campo in ['nombre', 'descripcion', 'tipo_id', 'estado_id', 'fecha_compra', 'costo']:
            if campo in datos:
                sets.append(f"{campo} = %s")
                params.append(datos[campo])
        if not sets:
            return self.obtener_por_id(id)
        sets.append("modificado_en = NOW()")
        params.append(id)
        self.execute(f"UPDATE recursos SET {', '.join(sets)} WHERE id = %s", params)
        return self.obtener_por_id(id)

    def eliminar_logico(self, id):
        self.execute("UPDATE recursos SET eliminado = 1, modificado_en = NOW() WHERE id = %s", (id,))

    def tiene_asignaciones_pendientes(self, id):
        row = self.fetch_one(
            "SELECT COUNT(*) as total FROM asignaciones_recursos WHERE recurso_id = %s AND fecha_devolucion_real IS NULL",
            (id,)
        )
        return row['total'] > 0 if row else False

    def total_asignaciones(self, id):
        row = self.fetch_one(
            "SELECT COUNT(*) as total FROM asignaciones_recursos WHERE recurso_id = %s", (id,)
        )
        return row['total'] if row else 0


class AsignacionRecursoRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def consultar(self, recurso_id=None, usuario_id=None, estado_asig_id=None):
        sql = """SELECT a.*, r.nombre as recurso_nombre, e.nombre as estado_asignacion_nombre,
                        u.nombre as usuario_nombre
                 FROM asignaciones_recursos a
                 JOIN recursos r ON a.recurso_id = r.id
                 LEFT JOIN estado_asignacion e ON a.estado_asignacion_id = e.id
                 LEFT JOIN no_funcional.usuarios u ON a.usuario_id = u.id
                 WHERE 1=1"""
        params = []
        if recurso_id:
            sql += " AND a.recurso_id = %s"
            params.append(recurso_id)
        if usuario_id:
            sql += " AND a.usuario_id = %s"
            params.append(usuario_id)
        if estado_asig_id:
            sql += " AND a.estado_asignacion_id = %s"
            params.append(estado_asig_id)
        sql += " ORDER BY a.fecha_asignacion DESC"
        rows = self.fetch_all(sql, params)
        return [AsignacionRecurso(**r) for r in rows]

    def obtener_por_id(self, id):
        row = self.fetch_one(
            """SELECT a.*, r.nombre as recurso_nombre, e.nombre as estado_asignacion_nombre,
                      u.nombre as usuario_nombre
               FROM asignaciones_recursos a
               JOIN recursos r ON a.recurso_id = r.id
               LEFT JOIN estado_asignacion e ON a.estado_asignacion_id = e.id
               LEFT JOIN no_funcional.usuarios u ON a.usuario_id = u.id
               WHERE a.id = %s""",
            (id,)
        )
        return AsignacionRecurso(**row) if row else None

    def obtener_asignacion_activa(self, recurso_id):
        row = self.fetch_one(
            "SELECT * FROM asignaciones_recursos WHERE recurso_id = %s AND fecha_devolucion_real IS NULL LIMIT 1",
            (recurso_id,)
        )
        return AsignacionRecurso(**row) if row else None

    def registrar(self, datos):
        fields = ['recurso_id', 'usuario_id', 'fecha_devolucion_esperada', 'notas', 'estado_asignacion_id', 'fecha_asignacion']
        cols = [f for f in fields if f in datos]
        placeholders = ', '.join(['%s'] * len(cols))
        sql = f"INSERT INTO asignaciones_recursos ({', '.join(cols)}) VALUES ({placeholders})"
        params = [datos[f] for f in cols]
        id = self.execute(sql, params)
        return self.obtener_por_id(id)

    def devolver(self, id):
        self.execute(
            """UPDATE asignaciones_recursos
               SET fecha_devolucion_real = NOW(), estado_asignacion_id = 2
               WHERE id = %s""",
            (id,)
        )
        return self.obtener_por_id(id)

    def contar_pendientes_por_recurso(self, recurso_id):
        row = self.fetch_one(
            "SELECT COUNT(*) as total FROM asignaciones_recursos WHERE recurso_id = %s AND fecha_devolucion_real IS NULL",
            (recurso_id,)
        )
        return row['total'] if row else 0
