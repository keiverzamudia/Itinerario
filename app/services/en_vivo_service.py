# app/services/en_vivo_service.py
# Capa de negocio para el módulo en vivo

from app.repositories.en_vivo_repository import EnVivoRepository
from app.traits.validaciones import ValidacionesMixin


class EnVivoService(ValidacionesMixin):
    """Orquesta lógica del módulo en vivo"""

    INNING_NAMES = {1: '1ro', 2: '2do', 3: '3ro', 4: '4to',
                    5: '5to', 6: '6to', 7: '7mo', 8: '8vo', 9: '9no'}

    def __init__(self):
        self.repo = EnVivoRepository()

    # ─── Helper: formato hora 12h ────────────────────────────────

    def _fmt12(self, hora, duracion_segundos):
        h = hora.hour
        m = hora.minute
        ampm = 'AM' if h < 12 else 'PM'
        h12 = h % 12 or 12
        total_min = h * 60 + m + (duracion_segundos // 60)
        eh = (total_min // 60) % 24
        em = total_min % 60
        eampm = 'AM' if eh < 12 else 'PM'
        eh12 = eh % 12 or 12
        return f"{h12}:{m:02d} {ampm} - {eh12}:{em:02d} {eampm}"

    # ─── Index ───────────────────────────────────────────────────

    def obtener_index(self):
        guiones = self.repo.obtener_guiones_publicados()
        hay_en_vivo = self.repo.obtener_en_vivo_actual()
        return {'guiones': guiones, 'hay_en_vivo': hay_en_vivo}

    # ─── Vista en vivo ──────────────────────────────────────────

    def obtener_datos_vivo(self, guion_id):
        guion = self.repo.obtener_por_id(guion_id)
        if guion.estado != 'en_vivo':
            return None, None

        fechas = self.repo.obtener_fechas(guion_id)
        pregame = self.repo.obtener_pregame(guion_id)
        game = self.repo.obtener_game(guion_id)
        todos = pregame + game

        # Auto-gestionar estado de elementos
        hay_activo = any(e.estado == 'en_curso' for e in todos)
        hay_completados = any(e.estado == 'completado' for e in todos)

        if not hay_activo and not hay_completados and todos:
            elementos = self.repo.obtener_elementos(guion_id)
            elementos[0].estado = 'en_curso'
            self.repo.commit()
        elif not hay_activo and todos:
            elementos = self.repo.obtener_elementos(guion_id)
            for e in elementos:
                if e.estado == 'pendiente':
                    e.estado = 'en_curso'
                    self.repo.commit()
                    break

        pregame = self.repo.obtener_pregame(guion_id)
        game = self.repo.obtener_game(guion_id)
        pregame_data = self._formatear_pregame(pregame)
        game_data = self._formatear_game(game)

        return {
            'guion': guion,
            'fechas': fechas,
            'pregame': pregame_data,
            'game': game_data,
        }, guion

    def _formatear_pregame(self, pregame):
        return [{
            'id': e.id,
            'estado': e.estado,
            'hora': self._fmt12(e.hora, e.duracion_estimada),
            'contenido': e.contenido,
            'duracion': e.duracion_estimada,
            'encargado': e.encargado,
        } for e in pregame]

    def _formatear_game(self, game):
        return [{
            'id': e.id,
            'estado': e.estado,
            'hora': f"{self.INNING_NAMES.get(e.inning, e.inning)}° {e.medio_inning.capitalize()}",
            'contenido': e.contenido,
            'duracion': e.duracion_estimada,
            'encargado': e.encargado,
        } for e in game]

    # ─── Iniciar ─────────────────────────────────────────────────

    def iniciar(self, guion_id):
        self.limpiar_errores()
        en_vivo_actual = self.repo.obtener_en_vivo_actual()
        if en_vivo_actual and en_vivo_actual.id != guion_id:
            self.errores.append(
                f'Ya hay un guion en vivo: "{en_vivo_actual.nombre}". Finalízalo primero.'
            )
            return None
        return self.repo.iniciar_en_vivo(guion_id)

    # ─── Finalizar ───────────────────────────────────────────────

    def finalizar(self, guion_id):
        return self.repo.finalizar_en_vivo(guion_id)

    # ─── Sincronizar (solo DB, SocketIO en controller) ──────────

    def sincronizar_estados(self, guion_id, estados):
        for item in estados:
            eid = item.get('id')
            estado = item.get('estado')
            if eid and estado:
                self.repo.actualizar_estado_elemento(eid, estado)
        self.repo.commit()

    # ─── Buscar por fecha (API) ──────────────────────────────────

    def buscar_guiones_por_fecha(self, fecha_str):
        guiones = self.repo.buscar_guiones_por_fecha(fecha_str)
        result = [{
            'id': g.id,
            'nombre': g.nombre,
            'elementos': len(g.elementos),
        } for g in guiones]
        return {'guiones': result}
