from app.repositories.guion_repository import GuionRepository, ElementoGuionRepository
from app.repositories.mantenimiento_repository import RecursoRepository, MantenimientoRepository
from app.repositories.premio_repository import PremioRepository
from app.repositories.contrato_repository import ContratoRepository
from app.repositories.patrocinador_repository import PatrocinadorRepository
from app.repositories.balance_repository import BalanceRepository
from app.repositories.gestion_tarea_repository import TareasAsignadasRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.en_vivo_repository import EnVivoRepository
from app.repositories.bitacora_repository import ActividadRepository, ErrorRepository
from app.repositories.dashboard_visibilidad_repository import DashboardVisibilidadRepository
from app.models.dashboard_visibilidad import MODULOS_DASHBOARD_INFO


class DashboardService:
    def __init__(self):
        self.guion_repo = GuionRepository()
        self.elemento_repo = ElementoGuionRepository()
        self.recurso_repo = RecursoRepository()
        self.mantenimiento_repo = MantenimientoRepository()
        self.premio_repo = PremioRepository()
        self.contrato_repo = ContratoRepository()
        self.patrocinador_repo = PatrocinadorRepository()
        self.balance_repo = BalanceRepository()
        self.tarea_asig_repo = TareasAsignadasRepository()
        self.usuario_repo = UsuarioRepository()
        self.en_vivo_repo = EnVivoRepository()
        self.actividad_repo = ActividadRepository()
        self.error_repo = ErrorRepository()
        self.dash_vis_repo = DashboardVisibilidadRepository()

    def obtener_metrica_live(self):
        guion = self.en_vivo_repo.obtener_en_vivo_actual()
        if not guion:
            return {'activo': False}
        elementos = self.elemento_repo.consultar(guion_id=guion.id)
        completados = len([e for e in elementos if e.estado == 'completado'])
        en_curso = [e for e in elementos if e.estado == 'en_curso']
        return {
            'activo': True,
            'id': guion.id,
            'nombre': guion.nombre,
            'completados': completados,
            'total': len(elementos),
            'elemento_actual': en_curso[0] if en_curso else None,
            'siguientes': self._siguientes(elementos, en_curso[0] if en_curso else None),
        }

    def _siguientes(self, elementos, actual):
        if not actual:
            return []
        idx = next((i for i, e in enumerate(elementos) if e.id == actual.id), -1)
        return elementos[idx + 1:idx + 4] if idx >= 0 else []

    def obtener_metricas_modulos(self, modulos_visibles=None):
        result = {}
        if modulos_visibles is None:
            modulos_visibles = set(MODULOS_DASHBOARD_INFO.keys())

        if 'guion' in modulos_visibles:
            result['guion'] = {
                'borrador': self.guion_repo.contar(estado='borrador'),
                'publicado': self.guion_repo.contar(estado='publicado'),
                'en_vivo': self.guion_repo.contar(estado='en_vivo'),
            }

        if 'mantenimiento' in modulos_visibles:
            result['mantenimiento'] = {
                'en_mantenimiento': self.recurso_repo.contar(estado='en_mantenimiento'),
                'disponible': self.recurso_repo.contar(estado='disponible'),
                'baja': self.recurso_repo.contar(estado='baja'),
            }

        if 'premio' in modulos_visibles:
            result['premio'] = {
                'pendiente': self.premio_repo.contar(estado='pendiente'),
                'entregado': self.premio_repo.contar(estado='entregado'),
            }

        if 'contrato' in modulos_visibles:
            contratos = self.contrato_repo.consultar(activos=True)
            result['contrato'] = {
                'vigentes': len([c for c in contratos if getattr(c, 'estatus', None) == 'Vigente']),
                'borrador': len([c for c in contratos if getattr(c, 'estatus', None) == 'Borrador']),
                'total': len(contratos),
            }

        if 'balance' in modulos_visibles:
            result['balance'] = {
                'total_pagado': self.balance_repo.get_total_pagado_general(),
            }

        if 'tarea' in modulos_visibles:
            tareas = self.tarea_asig_repo.consultar()
            result['tarea'] = {
                'pendientes': len([t for t in tareas if getattr(t, 'Estado', 'Pendiente') != 'Completada']),
                'completadas': len([t for t in tareas if getattr(t, 'Estado', None) == 'Completada']),
            }

        if 'patrocinador' in modulos_visibles:
            patro = self.patrocinador_repo.consultar(activos=True)
            result['patrocinador'] = {'activos': len(patro)}

        if 'usuario' in modulos_visibles:
            result['usuario'] = {'total': self.usuario_repo.contar()}

        return result

    def obtener_modulos_visibles(self, usuario):
        return self.dash_vis_repo.obtener_modulos_visibles_final(usuario.id, usuario.rol)

    def obtener_actividad_reciente(self, limite=10):
        return self.actividad_repo.consultar(limite=limite)

    def obtener_alertas(self):
        errores = self.error_repo.consultar(limite=5)
        return {
            'total_errores': len(errores),
            'ultimos_errores': errores,
        }
