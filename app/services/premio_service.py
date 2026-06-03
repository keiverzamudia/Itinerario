# app/services/premio_service.py
# Capa de negocio para premios — validaciones + orquestación

from datetime import datetime
from app.repositories.premio_repository import PremioRepository
from app.traits.validaciones import ValidacionesMixin


class PremioService(ValidacionesMixin):
    """Orquesta lógica de premios con validaciones tipo PHP trait"""

    def __init__(self):
        self.repo = PremioRepository()

    # ─── Dashboard ───────────────────────────────────────────────

    def obtener_dashboard(self):
        total = self.repo.contar()
        pendientes = self.repo.contar(estado='pendiente')
        entregados = self.repo.contar(estado='entregado')
        premios_pendientes = self.repo.obtener_premios_pendientes()
        premios_entregados = self.repo.obtener_premios_entregados()
        patrocinadores = self.repo.obtener_patrocinadores()
        return {
            'total': total,
            'pendientes': pendientes,
            'entregados': entregados,
            'premios_pendientes': premios_pendientes,
            'premios_entregados': premios_entregados,
            'patrocinadores': patrocinadores,
            'now': datetime.now(),
        }

    # ─── Crear premio ────────────────────────────────────────────

    def crear(self, nombre, fecha_creacion_str, hora_creacion_str,
              id_patrocinador=None, descripcion=None, foto_filename=None):
        self.limpiar_errores()
        self.validar_obligatorios(
            ['nombre', 'fecha_creacion', 'hora_creacion'],
            {'nombre': nombre, 'fecha_creacion': fecha_creacion_str, 'hora_creacion': hora_creacion_str}
        )
        if self.tiene_errores():
            return False
        fecha_creacion = datetime.strptime(fecha_creacion_str, '%Y-%m-%d').date()
        hora_creacion = datetime.strptime(hora_creacion_str, '%H:%M').time()
        self.repo.registrar({
            'nombre': nombre,
            'id_patrocinador': id_patrocinador,
            'descripcion': descripcion,
            'fecha_creacion': fecha_creacion,
            'hora_creacion': hora_creacion,
            'foto': foto_filename or 'default-premio.png',
        })
        return True

    # ─── Editar premio ───────────────────────────────────────────

    def editar(self, premio_id, nombre, id_patrocinador=None,
               descripcion=None, foto_filename=None):
        self.limpiar_errores()
        if not premio_id or not nombre:
            self.errores.append('Faltan datos para editar')
            return False
        if self.tiene_errores():
            return False
        update_data = {
            'nombre': nombre,
            'id_patrocinador': id_patrocinador,
            'descripcion': descripcion,
        }
        if foto_filename:
            update_data['foto'] = foto_filename
        self.repo.modificar(premio_id, update_data)
        return True

    def obtener_foto_actual(self, premio_id):
        return self.repo.obtener_foto_actual(premio_id)

    # ─── Entregar premio ─────────────────────────────────────────

    def entregar(self, premio_id, user_id=None):
        self.limpiar_errores()
        resultado = self.repo.verificar_disponible(premio_id)
        if not resultado:
            self.errores.append('Premio no encontrado')
            return False
        if resultado.estado == 'entregado':
            self.errores.append(f'⚠️ El premio "{resultado.nombre}" ya fue entregado')
            return False
        self.repo.entregar(premio_id, entregado_por=user_id)
        return True

    def crear_y_entregar(self, premio_id, id_patrocinador=None, descripcion=None, user_id=None):
        self.limpiar_errores()
        resultado = self.repo.verificar_disponible(premio_id)
        if not resultado:
            self.errores.append('Premio no encontrado')
            return False
        if resultado.estado == 'entregado':
            self.errores.append(f'⚠️ El premio "{resultado.nombre}" ya fue entregado')
            return False
        self.repo.entregar(premio_id, id_patrocinador=id_patrocinador, descripcion=descripcion, entregado_por=user_id)
        return True

    # ─── Eliminar (borrado lógico) ───────────────────────────────

    def eliminar(self, id_registro):
        self.limpiar_errores()
        premio = self.repo.obtener_por_id(id_registro)
        if not premio:
            self.errores.append('Premio no encontrado')
            return None
        if premio.estatus == 1:
            self.errores.append('⚠️ Este premio ya está eliminado')
            return None
        return self.repo.eliminar(id_registro)

    # ─── API ─────────────────────────────────────────────────────

    def obtener_api(self, premio_id):
        premio = self.repo.obtener_para_api(premio_id)
        if premio:
            return {
                'id': premio.id,
                'nombre': premio.nombre,
                'id_patrocinador': premio.id_patrocinador,
                'descripcion': premio.descripcion or '',
                'foto': premio.foto or '',
            }
        return None
