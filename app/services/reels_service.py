from app.repositories.reels_repository import ReelRepository, VideoRepository
from app.traits.validaciones import ValidacionesMixin


class ReelsService(ValidacionesMixin):
    def __init__(self):
        self.reel_repo = ReelRepository()
        self.video_repo = VideoRepository()

    def obtener_reels(self):
        return self.reel_repo.consultar()

    def obtener_reel(self, id):
        return self.reel_repo.obtener_por_id(id)

    def crear_reel(self, datos):
        self.limpiar_errores()
        if not datos.get('nombre'):
            self.errores.append('El nombre del reel es obligatorio')
            return None
        if self.errores:
            return None
        return self.reel_repo.registrar(datos)

    def editar_reel(self, id, datos):
        self.limpiar_errores()
        reel = self.reel_repo.obtener_por_id(id)
        if not reel:
            self.errores.append('Reel no encontrado')
            return None
        if self.errores:
            return None
        return self.reel_repo.modificar(id, datos)

    def eliminar_reel(self, id):
        self.limpiar_errores()
        reel = self.reel_repo.obtener_por_id(id)
        if not reel:
            self.errores.append('Reel no encontrado')
            return False
        self.reel_repo.eliminar(id)
        return True

    def agregar_video(self, reel_id, datos):
        self.limpiar_errores()
        reel = self.reel_repo.obtener_por_id(reel_id)
        if not reel:
            self.errores.append('Reel no encontrado')
            return None
        if not datos.get('nombre'):
            self.errores.append('El nombre del video es obligatorio')
            return None
        if self.errores:
            return None
        datos['reel_id'] = reel_id
        video = self.video_repo.registrar(datos)
        self._actualizar_duracion_total(reel_id)
        return video

    def eliminar_video(self, video_id, reel_id):
        self.video_repo.eliminar(video_id)
        self._actualizar_duracion_total(reel_id)

    def _actualizar_duracion_total(self, reel_id):
        videos = self.video_repo.consultar_por_reel(reel_id)
        total_segundos = sum(v.duracion_segundos or 0 for v in videos)
        total_minutos = total_segundos / 60.0
        self.reel_repo.modificar(reel_id, {'duracion_total': total_minutos})
