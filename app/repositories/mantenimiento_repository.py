from app.repositories.base_repository import BaseRepository
from app.models.mantenimiento import Recurso, Mantenimiento, HistorialMantenimiento


class RecursoRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def consultar(self, **filtros):
        sql = "SELECT * FROM recursos WHERE eliminado = 0"
        params = []
        if filtros.get('estado_id'):
            sql += " AND estado_id = %s"
            params.append(filtros['estado_id'])
        sql += " ORDER BY creado_en DESC"
        rows = self.fetch_all(sql, params)
        return [Recurso(**r) for r in rows]

    def obtener_por_id(self, id):
        row = self.fetch_one("SELECT * FROM recursos WHERE id = %s", (id,))
        return Recurso(**row) if row else None

    def contar(self, **filtros):
        sql = "SELECT COUNT(*) as total FROM recursos WHERE eliminado = 0"
        params = []
        if filtros.get('estado_id'):
            sql += " AND estado_id = %s"
            params.append(filtros['estado_id'])
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


class MantenimientoRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def consultar(self, **filtros):
        sql = "SELECT * FROM mantenimientos WHERE 1=1"
        params = []
        if filtros.get('recurso_id'):
            sql += " AND recurso_id = %s"
            params.append(filtros['recurso_id'])
        if filtros.get('estado'):
            sql += " AND estado = %s"
            params.append(filtros['estado'])
        sql += " ORDER BY creado_en DESC"
        rows = self.fetch_all(sql, params)
        mantenimientos = [Mantenimiento(**r) for r in rows]
        for m in mantenimientos:
            self._cargar_relaciones(m)
        return mantenimientos

    def obtener_por_id(self, id):
        row = self.fetch_one("SELECT * FROM mantenimientos WHERE id = %s", (id,))
        if not row:
            return None
        m = Mantenimiento(**row)
        self._cargar_relaciones(m)
        return m

    def _cargar_relaciones(self, m):
        recurso_row = self.fetch_one("SELECT * FROM recursos WHERE id = %s", (m.recurso_id,))
        if recurso_row:
            m.recurso = Recurso(**recurso_row)
        user_row = self.fetch_one("SELECT nombre FROM no_funcional.usuarios WHERE id = %s", (m.usuario_id,))
        m.usuario_nombre = user_row['nombre'] if user_row else 'Desconocido'
        hist_rows = self.fetch_all(
            "SELECT * FROM historial_mantenimiento WHERE mantenimiento_id = %s ORDER BY creado_en ASC",
            (m.id,)
        )
        m.historial = [HistorialMantenimiento(**r) for r in hist_rows]
        for h in m.historial:
            u_row = self.fetch_one("SELECT nombre FROM no_funcional.usuarios WHERE id = %s", (h.usuario_id,))
            h.usuario_nombre = u_row['nombre'] if u_row else 'Desconocido'

    def registrar(self, datos):
        sql = """INSERT INTO mantenimientos (recurso_id, usuario_id, estado,
                 fecha_ingreso, diagnostico, observaciones, creado_en)
                 VALUES (%s, %s, 'en_espera', %s, %s, %s, NOW())"""
        id = self.execute(sql, (
            datos['recurso_id'], datos['usuario_id'],
            datos['fecha_ingreso'], datos.get('diagnostico', ''),
            datos.get('observaciones', ''),
        ))
        return self.obtener_por_id(id)

    def modificar(self, id, datos):
        sets = []
        params = []
        for campo in ['estado', 'fecha_salida', 'diagnostico', 'observaciones']:
            if campo in datos:
                sets.append(f"{campo} = %s")
                params.append(datos[campo])
        if sets:
            params.append(id)
            self.execute(f"UPDATE mantenimientos SET {', '.join(sets)} WHERE id = %s", params)
        return self.obtener_por_id(id)

    def eliminar(self, id):
        self.execute("DELETE FROM mantenimientos WHERE id = %s", (id,))


class HistorialMantenimientoRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def consultar(self, **filtros):
        sql = "SELECT * FROM historial_mantenimiento WHERE 1=1"
        params = []
        if filtros.get('mantenimiento_id'):
            sql += " AND mantenimiento_id = %s"
            params.append(filtros['mantenimiento_id'])
        sql += " ORDER BY creado_en ASC"
        rows = self.fetch_all(sql, params)
        return [HistorialMantenimiento(**r) for r in rows]

    def registrar(self, datos):
        id = self.execute(
            """INSERT INTO historial_mantenimiento
               (mantenimiento_id, usuario_id, accion, descripcion, creado_en)
               VALUES (%s, %s, %s, %s, NOW())""",
            (datos['mantenimiento_id'], datos['usuario_id'],
             datos['accion'], datos.get('descripcion', ''))
        )
        return HistorialMantenimiento(id=id, **datos)
