from datetime import datetime, date
from app.repositories.base_repository import BaseRepository
from app.models.guion import Guion, GuionFecha, ElementoGuion


class EnVivoRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def _row_to_guion(self, row):
        if not row:
            return None
        return Guion(**row)

    def consultar(self, **filtros):
        sql = "SELECT * FROM guiones WHERE 1=1"
        params = []
        if filtros.get('estados'):
            estados_list = filtros['estados']
            placeholders = ', '.join(['%s'] * len(estados_list))
            sql += f" AND estado IN ({placeholders})"
            params.extend(estados_list)
        sql += " ORDER BY modificado_en DESC"
        rows = self.fetch_all(sql, params)
        return [Guion(**r) for r in rows]

    def obtener_guiones_publicados(self):
        return self.consultar(estados=['publicado', 'en_vivo', 'finalizado'])

    def obtener_en_vivo_actual(self):
        row = self.fetch_one("SELECT * FROM guiones WHERE estado = 'en_vivo' LIMIT 1")
        return self._row_to_guion(row)

    def obtener_por_id(self, id_registro):
        row = self.fetch_one("SELECT * FROM guiones WHERE id = %s", (id_registro,))
        return self._row_to_guion(row)

    def obtener_fechas(self, guion_id):
        rows = self.fetch_all(
            "SELECT * FROM guion_fechas WHERE guion_id = %s ORDER BY fecha",
            (guion_id,)
        )
        return [GuionFecha(**r) for r in rows]

    def obtener_pregame(self, guion_id):
        rows = self.fetch_all(
            "SELECT * FROM elementos_guion WHERE guion_id = %s AND tipo = 'pregame' ORDER BY hora",
            (guion_id,)
        )
        return [ElementoGuion(**r) for r in rows]

    def obtener_game(self, guion_id):
        rows = self.fetch_all(
            "SELECT * FROM elementos_guion WHERE guion_id = %s AND tipo = 'game' ORDER BY inning, medio_inning",
            (guion_id,)
        )
        return [ElementoGuion(**r) for r in rows]

    def obtener_elementos(self, guion_id):
        rows = self.fetch_all(
            "SELECT * FROM elementos_guion WHERE guion_id = %s ORDER BY orden",
            (guion_id,)
        )
        return [ElementoGuion(**r) for r in rows]

    def iniciar_en_vivo(self, guion_id):
        self.execute(
            "UPDATE guiones SET estado = 'en_vivo', modificado_en = NOW() WHERE id = %s",
            (guion_id,)
        )
        self.execute(
            "UPDATE elementos_guion SET estado = 'pendiente' WHERE guion_id = %s",
            (guion_id,)
        )
        elemento = self.fetch_one(
            "SELECT * FROM elementos_guion WHERE guion_id = %s ORDER BY orden LIMIT 1",
            (guion_id,)
        )
        if elemento:
            self.execute(
                "UPDATE elementos_guion SET estado = 'en_curso' WHERE id = %s",
                (elemento['id'],)
            )
        return self.obtener_por_id(guion_id)

    def finalizar_en_vivo(self, guion_id):
        self.execute(
            "UPDATE guiones SET estado = 'finalizado', modificado_en = NOW() WHERE id = %s",
            (guion_id,)
        )
        self.execute(
            "UPDATE elementos_guion SET estado = 'pendiente' WHERE guion_id = %s",
            (guion_id,)
        )
        return self.obtener_por_id(guion_id)

    def actualizar_estado_elemento(self, elemento_id, estado):
        self.execute(
            "UPDATE elementos_guion SET estado = %s WHERE id = %s",
            (estado, int(elemento_id))
        )

    def buscar_guiones_por_fecha(self, fecha_str):
        try:
            fecha = date.fromisoformat(fecha_str)
        except ValueError:
            return []
        rows = self.fetch_all(
            """SELECT g.* FROM guiones g
               JOIN guion_fechas gf ON g.id = gf.guion_id
               WHERE gf.fecha = %s AND g.estado = 'publicado'""",
            (fecha,)
        )
        guiones = [Guion(**r) for r in rows]
        for g in guiones:
            g.elementos = self.obtener_elementos(g.id)
        return guiones

    def commit(self):
        self._conn.commit()
