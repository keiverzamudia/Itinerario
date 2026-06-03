from app.repositories.base_repository import BaseRepository
from app.models.reel import Reel, Video


class ReelRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def consultar(self):
        rows = self.fetch_all("SELECT * FROM reels ORDER BY creado_en DESC")
        reels = [Reel(**r) for r in rows]
        for reel in reels:
            reel.videos = self._obtener_videos(reel.id)
        return reels

    def obtener_por_id(self, id):
        row = self.fetch_one("SELECT * FROM reels WHERE id = %s", (id,))
        if not row:
            return None
        reel = Reel(**row)
        reel.videos = self._obtener_videos(id)
        return reel

    def _obtener_videos(self, reel_id):
        rows = self.fetch_all(
            "SELECT * FROM videos WHERE reel_id = %s ORDER BY orden ASC",
            (reel_id,)
        )
        return [Video(**r) for r in rows]

    def registrar(self, datos):
        id = self.execute(
            "INSERT INTO reels (nombre, patrocinado, duracion_total, creado_en) VALUES (%s, %s, %s, NOW())",
            (datos.get('nombre'), datos.get('patrocinado'), datos.get('duracion_total', 0))
        )
        return self.obtener_por_id(id)

    def modificar(self, id, datos):
        sets = []
        params = []
        for campo in ['nombre', 'patrocinado', 'duracion_total']:
            if campo in datos:
                sets.append(f"{campo} = %s")
                params.append(datos[campo])
        sets.append("modificado_en = NOW()")
        params.append(id)
        self.execute(f"UPDATE reels SET {', '.join(sets)} WHERE id = %s", params)
        return self.obtener_por_id(id)

    def eliminar(self, id):
        self.execute("DELETE FROM videos WHERE reel_id = %s", (id,))
        self.execute("DELETE FROM reels WHERE id = %s", (id,))


class VideoRepository(BaseRepository):
    def __init__(self):
        super().__init__('estadio_db')

    def consultar_por_reel(self, reel_id):
        rows = self.fetch_all(
            "SELECT * FROM videos WHERE reel_id = %s ORDER BY orden ASC",
            (reel_id,)
        )
        return [Video(**r) for r in rows]

    def registrar(self, datos):
        id = self.execute(
            "INSERT INTO videos (nombre, duracion_segundos, orden, reel_id) VALUES (%s, %s, %s, %s)",
            (datos.get('nombre'), datos.get('duracion_segundos', 0),
             datos.get('orden'), datos.get('reel_id'))
        )
        return Video(id=id, **datos)

    def eliminar(self, id):
        self.execute("DELETE FROM videos WHERE id = %s", (id,))
