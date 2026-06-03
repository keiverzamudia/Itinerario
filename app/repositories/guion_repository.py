from datetime import datetime, date
from app.repositories.base_repository import BaseRepository
from app.models.guion import Guion, GuionFecha, ElementoGuion


class GuionRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def _row_to_guion(self, row):
        if not row:
            return None
        g = Guion(**row)
        fechas_rows = self.fetch_all(
            "SELECT * FROM guion_fechas WHERE guion_id = %s ORDER BY fecha",
            (g.id,)
        )
        g.fechas = [GuionFecha(**r) for r in fechas_rows]
        elementos_rows = self.fetch_all(
            "SELECT * FROM elementos_guion WHERE guion_id = %s ORDER BY orden",
            (g.id,)
        )
        g.elementos = [ElementoGuion(**r) for r in elementos_rows]
        return g

    def consultar(self, **filtros):
        sql = "SELECT * FROM guiones WHERE 1=1"
        params = []
        if filtros.get('estado'):
            sql += " AND estado = %s"
            params.append(filtros['estado'])
        sql += " ORDER BY creado_en DESC"
        rows = self.fetch_all(sql, params)
        guiones = [self._row_to_guion(r) for r in rows]
        return guiones

    def contar(self, **filtros):
        sql = "SELECT COUNT(*) as total FROM guiones WHERE 1=1"
        params = []
        if filtros.get('estado'):
            sql += " AND estado = %s"
            params.append(filtros['estado'])
        row = self.fetch_one(sql, params)
        return row['total'] if row else 0

    def obtener_por_id(self, id_registro):
        row = self.fetch_one("SELECT * FROM guiones WHERE id = %s", (id_registro,))
        return self._row_to_guion(row)

    def registrar(self, datos):
        id = self.execute(
            "INSERT INTO guiones (nombre, tiempo_inning, estado, creado_en) VALUES (%s, %s, 'borrador', NOW())",
            (datos['nombre'], datos.get('tiempo_inning'))
        )
        for fecha in datos.get('fechas', []):
            self.execute(
                "INSERT INTO guion_fechas (guion_id, fecha) VALUES (%s, %s)",
                (id, fecha)
            )
        return self.obtener_por_id(id)

    def modificar(self, id_registro, datos):
        sets = []
        params = []
        if 'nombre' in datos:
            sets.append("nombre = %s")
            params.append(datos['nombre'])
        if 'estado' in datos:
            sets.append("estado = %s")
            params.append(datos['estado'])
        if 'tiempo_inning' in datos:
            sets.append("tiempo_inning = %s")
            params.append(datos['tiempo_inning'])
        if sets:
            sets.append("modificado_en = NOW()")
            params.append(id_registro)
            self.execute(f"UPDATE guiones SET {', '.join(sets)} WHERE id = %s", params)
        if 'fechas' in datos:
            self.execute("DELETE FROM guion_fechas WHERE guion_id = %s", (id_registro,))
            for fecha in datos['fechas']:
                self.execute(
                    "INSERT INTO guion_fechas (guion_id, fecha) VALUES (%s, %s)",
                    (id_registro, fecha)
                )
        return self.obtener_por_id(id_registro)

    def eliminar(self, id_registro):
        guion = self.obtener_por_id(id_registro)
        if not guion:
            return None
        nombre = guion.nombre
        self.execute("DELETE FROM elementos_guion WHERE guion_id = %s", (id_registro,))
        self.execute("DELETE FROM guion_fechas WHERE guion_id = %s", (id_registro,))
        self.execute("DELETE FROM guiones WHERE id = %s", (id_registro,))
        return nombre

    def obtener_fechas(self, guion_id):
        rows = self.fetch_all(
            "SELECT * FROM guion_fechas WHERE guion_id = %s ORDER BY fecha",
            (guion_id,)
        )
        return [GuionFecha(**r) for r in rows]


class ElementoGuionRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def consultar(self, **filtros):
        sql = "SELECT * FROM elementos_guion WHERE 1=1"
        params = []
        if filtros.get('guion_id'):
            sql += " AND guion_id = %s"
            params.append(filtros['guion_id'])
        if filtros.get('tipo'):
            sql += " AND tipo = %s"
            params.append(filtros['tipo'])
        sql += " ORDER BY orden"
        rows = self.fetch_all(sql, params)
        return [ElementoGuion(**r) for r in rows]

    def obtener_por_id(self, id_registro):
        row = self.fetch_one("SELECT * FROM elementos_guion WHERE id = %s", (id_registro,))
        return ElementoGuion(**row) if row else None

    def registrar(self, datos):
        id = self.execute(
            """INSERT INTO elementos_guion
               (guion_id, fecha_id, tipo, hora, inning, medio_inning,
                contenido, duracion_estimada, encargado, orden, creado_en)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())""",
            (
                datos['guion_id'], datos.get('fecha_id'),
                datos['tipo'], datos.get('hora'),
                datos.get('inning'), datos.get('medio_inning'),
                datos['contenido'], datos['duracion_estimada'],
                datos['encargado'], datos.get('orden', 0),
            )
        )
        return self.obtener_por_id(id)

    def modificar(self, id_registro, datos):
        sets = []
        params = []
        for campo in ['tipo', 'hora', 'inning', 'medio_inning', 'contenido',
                      'duracion_estimada', 'encargado', 'orden', 'fecha_id', 'estado']:
            if campo in datos:
                sets.append(f"{campo} = %s")
                params.append(datos[campo])
        if sets:
            params.append(id_registro)
            self.execute(f"UPDATE elementos_guion SET {', '.join(sets)} WHERE id = %s", params)
        return self.obtener_por_id(id_registro)

    def eliminar(self, id_registro):
        self.execute("DELETE FROM elementos_guion WHERE id = %s", (id_registro,))

    def obtener_ocupados(self, guion_id):
        elementos = self.consultar(guion_id=guion_id)
        horas_usadas = set()
        innings_usados = {}
        for e in elementos:
            if e.tipo == 'pregame' and e.hora:
                horas_usadas.add(str(e.hora)[:5])
            elif e.tipo == 'game' and e.inning:
                key = f"{e.inning}-{e.medio_inning}"
                innings_usados[key] = e.id
        return horas_usadas, innings_usados

    def obtener_ultimo_orden(self, guion_id, tipo):
        row = self.fetch_one(
            "SELECT MAX(orden) as max_orden FROM elementos_guion WHERE guion_id = %s AND tipo = %s",
            (guion_id, tipo)
        )
        return row['max_orden'] if row and row['max_orden'] else 0

    def consultar_excepto(self, guion_id, elemento_id):
        rows = self.fetch_all(
            "SELECT * FROM elementos_guion WHERE guion_id = %s AND id != %s ORDER BY tipo, orden",
            (guion_id, elemento_id)
        )
        return [ElementoGuion(**r) for r in rows]

    def obtener_por_guion_ordenados(self, guion_id):
        pregame = self.consultar(guion_id=guion_id, tipo='pregame')
        game = self.consultar(guion_id=guion_id, tipo='game')
        pregame.sort(key=lambda e: str(e.hora) if e.hora else '23:59')
        game.sort(key=lambda e: (e.inning or 99, e.medio_inning or 'zzz'))
        return pregame, game
