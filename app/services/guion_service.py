from datetime import date
from app.repositories.guion_repository import GuionRepository, ElementoGuionRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.traits.validaciones import ValidacionesMixin


class GuionService(ValidacionesMixin):
    def __init__(self):
        self.guion_repo = GuionRepository()
        self.elemento_repo = ElementoGuionRepository()
        self.usuario_repo = UsuarioRepository()

    def _parsear_duracion(self, val):
        if not val:
            return 0
        val = str(val).strip()
        if ',' in val:
            partes = val.split(',')
            minutos = int(partes[0]) if partes[0] else 0
            seg_str = partes[1].ljust(2, '0')[:2]
            segundos = int(seg_str)
        else:
            try:
                minutos = int(val)
            except ValueError:
                minutos = 0
            segundos = 0
        return minutos * 60 + segundos

    def obtener_dashboard(self):
        guiones = self.guion_repo.consultar()
        total = self.guion_repo.contar()
        borradores = self.guion_repo.contar(estado='borrador')
        publicados = self.guion_repo.contar(estado='publicado')
        for g in guiones:
            g.pregame_count = len([e for e in g.elementos if e.tipo == 'pregame'])
            g.game_count = len([e for e in g.elementos if e.tipo == 'game'])
        return {
            'guiones': guiones,
            'total': total,
            'borradores': borradores,
            'publicados': publicados,
        }

    def crear_guion(self, nombre, fechas_json, tiempo_inning=None):
        self.limpiar_errores()
        self.validar_obligatorios(['nombre'], {'nombre': nombre})
        self.validar_longitud(nombre, 3, 200, 'nombre')
        if not fechas_json:
            self.errores.append('Debes seleccionar al menos una fecha')
        if self.tiene_errores():
            return None
        fechas = [date.fromisoformat(f) for f in fechas_json.split(',')]
        data = {'nombre': nombre, 'fechas': fechas}
        if tiempo_inning:
            data['tiempo_inning'] = self._parsear_duracion(tiempo_inning)
        return self.guion_repo.registrar(data)

    def obtener_datos_agregar(self, guion_id):
        guion = self.guion_repo.obtener_por_id(guion_id)
        if not guion:
            return {}
        fechas = self.guion_repo.obtener_fechas(guion_id)
        pregame, game = self.elemento_repo.obtener_por_guion_ordenados(guion_id)
        elementos = pregame + game
        horas_usadas, innings_usados = self.elemento_repo.obtener_ocupados(guion_id)
        tiempo_total_seg = sum(e.duracion_estimada for e in elementos)
        return {
            'guion': guion,
            'fechas': fechas,
            'elementos': elementos,
            'horas_usadas': horas_usadas,
            'innings_usados': innings_usados,
            'tiempo_total_seg': tiempo_total_seg,
            'tiempo_inning': guion.tiempo_inning,
        }

    def agregar_elemento(self, guion_id, data):
        self.limpiar_errores()
        horas_usadas, innings_usados = self.elemento_repo.obtener_ocupados(guion_id)
        if data.get('tipo') == 'pregame' and not data.get('hora'):
            self.errores.append('Para Pre-Game debes indicar una hora')
        elif data.get('tipo') == 'game' and (not data.get('inning') or not data.get('medio_inning')):
            self.errores.append('Para Game debes seleccionar inning y medio')
        else:
            clave_inning = f"{data['inning']}-{data['medio_inning']}" if data.get('inning') else None
            if data['tipo'] == 'pregame' and data['hora'].strftime('%H:%M') in horas_usadas:
                self.errores.append('Esa hora ya está ocupada')
            elif data['tipo'] == 'game' and clave_inning in innings_usados:
                self.errores.append('Ese inning ya está ocupado')
        if self.tiene_errores():
            return False
        ultimo_orden = self.elemento_repo.obtener_ultimo_orden(guion_id, data['tipo'])
        elemento_data = {
            'guion_id': guion_id,
            'fecha_id': None,
            'tipo': data['tipo'],
            'hora': data.get('hora') if data['tipo'] == 'pregame' else None,
            'inning': int(data['inning']) if data.get('inning') else None,
            'medio_inning': data.get('medio_inning') if data.get('medio_inning') else None,
            'contenido': data['contenido'],
            'duracion_estimada': self._parsear_duracion(data.get('duracion_estimada')),
            'encargado': data['encargado'],
            'orden': ultimo_orden + 1,
        }
        self.elemento_repo.registrar(elemento_data)
        return True

    def obtener_datos_editar_elemento(self, guion_id, elemento_id):
        guion = self.guion_repo.obtener_por_id(guion_id)
        elemento = self.elemento_repo.obtener_por_id(elemento_id)
        if not elemento or elemento.guion_id != guion_id:
            return None
        fechas = self.guion_repo.obtener_fechas(guion_id)
        otros = self.elemento_repo.consultar_excepto(guion_id, elemento_id)
        horas_usadas = set()
        innings_usados = {}
        for e in otros:
            if e.tipo == 'pregame' and e.hora:
                horas_usadas.add(str(e.hora)[:5])
            elif e.tipo == 'game' and e.inning:
                key = f"{e.inning}-{e.medio_inning}"
                innings_usados[key] = e.id
        return {
            'guion': guion,
            'elemento': elemento,
            'fechas': fechas,
            'horas_usadas': horas_usadas,
            'innings_usados': innings_usados,
        }

    def editar_elemento(self, guion_id, elemento_id, data):
        self.limpiar_errores()
        elemento = self.elemento_repo.obtener_por_id(elemento_id)
        if not elemento or elemento.guion_id != guion_id:
            self.errores.append('Elemento no pertenece a este guion')
            return False
        otros = self.elemento_repo.consultar_excepto(guion_id, elemento_id)
        horas_usadas = set()
        innings_usados = {}
        for e in otros:
            if e.tipo == 'pregame' and e.hora:
                horas_usadas.add(str(e.hora)[:5])
            elif e.tipo == 'game' and e.inning:
                key = f"{e.inning}-{e.medio_inning}"
                innings_usados[key] = e.id
        if data.get('tipo') == 'pregame' and not data.get('hora'):
            self.errores.append('Para Pre-Game debes indicar una hora')
        elif data.get('tipo') == 'game' and (not data.get('inning') or not data.get('medio_inning')):
            self.errores.append('Para Game debes seleccionar inning y medio')
        else:
            clave_inning = f"{data['inning']}-{data['medio_inning']}" if data.get('inning') else None
            if data['tipo'] == 'pregame' and data['hora'].strftime('%H:%M') in horas_usadas:
                self.errores.append('Esa hora ya está ocupada')
            elif data['tipo'] == 'game' and clave_inning in innings_usados:
                self.errores.append('Ese inning ya está ocupado')
        if self.tiene_errores():
            return False
        update_data = {
            'tipo': data['tipo'],
            'hora': data.get('hora') if data['tipo'] == 'pregame' else None,
            'inning': int(data['inning']) if data.get('inning') else None,
            'medio_inning': data.get('medio_inning') if data.get('medio_inning') else None,
            'contenido': data['contenido'],
            'duracion_estimada': self._parsear_duracion(data.get('duracion_estimada')),
            'encargado': data['encargado'],
            'fecha_id': None,
        }
        self.elemento_repo.modificar(elemento_id, update_data)
        return True

    def eliminar_elemento(self, guion_id, elemento_id):
        elemento = self.elemento_repo.obtener_por_id(elemento_id)
        if not elemento or elemento.guion_id != guion_id:
            self.errores.append('Elemento no pertenece a este guion')
            return False
        self.elemento_repo.eliminar(elemento_id)
        return True

    def editar_guion(self, id, nombre, fechas_json, tiempo_inning=None):
        self.limpiar_errores()
        self.validar_obligatorios(['nombre'], {'nombre': nombre})
        if not fechas_json:
            self.errores.append('Debes seleccionar al menos una fecha')
        if self.tiene_errores():
            return None
        fechas = [date.fromisoformat(f) for f in fechas_json.split(',')]
        data = {'nombre': nombre, 'fechas': fechas}
        if tiempo_inning:
            data['tiempo_inning'] = self._parsear_duracion(tiempo_inning)
        return self.guion_repo.modificar(id, data)

    def obtener_datos_previsualizar(self, guion_id):
        guion = self.guion_repo.obtener_por_id(guion_id)
        if not guion:
            return {}
        fechas = self.guion_repo.obtener_fechas(guion_id)
        pregame, game = self.elemento_repo.obtener_por_guion_ordenados(guion_id)
        elementos = pregame + game
        tiempo_total_seg = sum(e.duracion_estimada for e in elementos)
        return {
            'guion': guion,
            'fechas': fechas,
            'pregame': pregame,
            'game': game,
            'tiempo_total_seg': tiempo_total_seg,
        }

    def publicar_guion(self, id):
        return self.guion_repo.modificar(id, {'estado': 'publicado'})

    def eliminar_guion(self, id):
        return self.guion_repo.eliminar(id)

    def obtener_horas_usadas(self, guion_id):
        horas_usadas, innings_usados = self.elemento_repo.obtener_ocupados(guion_id)
        return list(horas_usadas), innings_usados

    def obtener_usuarios_choices(self):
        usuarios = self.usuario_repo.consultar()
        return [(u.nombre, u.nombre) for u in usuarios]
