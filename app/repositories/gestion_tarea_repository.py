from datetime import datetime
from app.repositories.base_repository import BaseRepository
from app.models.gestion_tarea import Tarea, TareasAsignadas


class TareaRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def consultar(self, activas=True):
        sql = "SELECT * FROM tareas"
        params = []
        if activas:
            sql += " WHERE Estatus = 1"
        sql += " ORDER BY id_tarea DESC"
        rows = self.fetch_all(sql, params)
        return [Tarea(**r) for r in rows]

    def obtener_por_id(self, id_tarea):
        row = self.fetch_one(
            "SELECT * FROM tareas WHERE id_tarea = %s",
            (id_tarea,)
        )
        return Tarea(**row) if row else None

    def registrar(self, datos):
        id = self.execute(
            "INSERT INTO tareas (Nombre_Tarea, Instruccion, id_usuario_creador, Estatus) VALUES (%s, %s, %s, 1)",
            (datos['Nombre_Tarea'], datos['Instruccion'], datos.get('id_usuario_creador'))
        )
        return self.obtener_por_id(id)

    def modificar(self, id_tarea, datos):
        sets = []
        params = []
        for campo in ['Nombre_Tarea', 'Instruccion']:
            if campo in datos:
                sets.append(f"{campo} = %s")
                params.append(datos[campo])
        if sets:
            params.append(id_tarea)
            self.execute(
                f"UPDATE tareas SET {', '.join(sets)} WHERE id_tarea = %s",
                params
            )
        return self.obtener_por_id(id_tarea)

    def eliminar(self, id_tarea):
        tarea = self.obtener_por_id(id_tarea)
        if not tarea:
            return None
        self.execute("UPDATE tareas SET Estatus = 0 WHERE id_tarea = %s", (id_tarea,))
        return tarea


class TareasAsignadasRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def consultar(self, **filtros):
        sql = """SELECT ta.*, t.Nombre_Tarea
                 FROM tareas_asignadas ta
                 JOIN tareas t ON ta.id_tarea = t.id_tarea
                 WHERE ta.Estatus = 1"""
        params = []
        if filtros.get('id_usuario'):
            sql += " AND ta.id_usuario = %s"
            params.append(filtros['id_usuario'])
        if filtros.get('id_tarea'):
            sql += " AND ta.id_tarea = %s"
            params.append(filtros['id_tarea'])
        sql += " ORDER BY ta.fecha_asignacion_tarea DESC"
        rows = self.fetch_all(sql, params)
        return [TareasAsignadas(**r) for r in rows]

    def obtener_por_id(self, id_asignacion):
        row = self.fetch_one(
            """SELECT ta.*, t.Nombre_Tarea
               FROM tareas_asignadas ta
               JOIN tareas t ON ta.id_tarea = t.id_tarea
               WHERE ta.id_asignacion = %s""",
            (id_asignacion,)
        )
        return TareasAsignadas(**row) if row else None

    def obtener_por_usuario(self, usuario_id):
        rows = self.fetch_all(
            """SELECT ta.*, t.Nombre_Tarea, t.Instruccion
               FROM tareas_asignadas ta
               JOIN tareas t ON ta.id_tarea = t.id_tarea
               WHERE ta.id_usuario = %s AND ta.Estatus = 1 AND t.Estatus = 1
               ORDER BY ta.fecha_asignacion_tarea DESC""",
            (usuario_id,)
        )
        return [TareasAsignadas(**r) for r in rows]

    def registrar(self, datos):
        id = self.execute(
            """INSERT INTO tareas_asignadas
               (id_tarea, id_usuario, Estado, fecha_asignacion_tarea, Estatus)
               VALUES (%s, %s, %s, %s, 1)""",
            (
                datos['id_tarea'],
                datos['id_usuario'],
                datos.get('Estado', 'Pendiente'),
                datos.get('fecha_asignacion_tarea', datetime.now()),
            )
        )
        return self.obtener_por_id(id)

    def modificar_estado(self, id_asignacion, estado):
        self.execute(
            "UPDATE tareas_asignadas SET Estado = %s WHERE id_asignacion = %s",
            (estado, id_asignacion)
        )

    def contar_pendientes(self, usuario_id):
        row = self.fetch_one(
            """SELECT COUNT(*) as total FROM tareas_asignadas ta
               JOIN tareas t ON ta.id_tarea = t.id_tarea
               WHERE ta.id_usuario = %s AND ta.Estatus = 1 AND t.Estatus = 1
               AND ta.Estado != 'Completada'""",
            (usuario_id,)
        )
        return row['total'] if row else 0
