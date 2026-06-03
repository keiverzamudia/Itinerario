import json
from app.repositories.bitacora_repository import (
    SesionRepository, ActividadRepository, CambioRepository, ErrorRepository
)
from app.repositories.usuario_repository import UsuarioRepository
from app.traits.validaciones import ValidacionesMixin
from datetime import datetime


class BitacoraService(ValidacionesMixin):
    def __init__(self):
        self.sesion_repo = SesionRepository()
        self.actividad_repo = ActividadRepository()
        self.cambio_repo = CambioRepository()
        self.error_repo = ErrorRepository()
        self.usuario_repo = UsuarioRepository()

    def iniciar_sesion(self, usuario_id, ip_address=None, user_agent=None):
        return self.sesion_repo.registrar({
            'usuario_id': usuario_id,
            'ip_address': ip_address,
            'user_agent': user_agent,
        })

    def finalizar_sesion(self, sesion_id):
        return self.sesion_repo.cerrar_sesion(sesion_id)

    def obtener_sesiones(self, **filtros):
        return self.sesion_repo.consultar(**filtros)

    def registrar_actividad(self, usuario_id, tipo_accion, modulo, accion='',
                            detalle=None, pagina=None, ip_address=None, sesion_id=None):
        self.limpiar_errores()
        if not self.validar_obligatorios(
            ['usuario_id', 'tipo_accion', 'modulo'],
            {'usuario_id': usuario_id, 'tipo_accion': tipo_accion, 'modulo': modulo}
        ):
            return None
        return self.actividad_repo.registrar({
            'sesion_id': sesion_id,
            'usuario_id': usuario_id,
            'tipo_accion': tipo_accion,
            'modulo': modulo,
            'accion': accion,
            'detalle': json.dumps(detalle) if detalle is not None else None,
            'pagina': pagina,
            'ip_address': ip_address,
        })

    def obtener_actividad(self, **filtros):
        return self.actividad_repo.consultar(**filtros)

    def registrar_cambio(self, actividad_id, tabla_afectada, campo,
                         valor_anterior=None, valor_nuevo=None, registro_id=None):
        return self.cambio_repo.registrar({
            'actividad_id': actividad_id,
            'tabla_afectada': tabla_afectada,
            'registro_id': registro_id,
            'campo': campo,
            'valor_anterior': str(valor_anterior) if valor_anterior is not None else None,
            'valor_nuevo': str(valor_nuevo) if valor_nuevo is not None else None,
        })

    def registrar_error(self, tipo_error, mensaje, traceback=None,
                        usuario_id=None, pagina=None, ip_address=None):
        return self.error_repo.registrar({
            'usuario_id': usuario_id,
            'tipo_error': tipo_error,
            'mensaje': mensaje,
            'traceback': traceback,
            'pagina': pagina,
            'ip_address': ip_address,
        })

    def obtener_errores(self, **filtros):
        return self.error_repo.consultar(**filtros)

    def obtener_dashboard(self):
        sesiones_hoy = self.sesion_repo.consultar()
        actividades = self.actividad_repo.consultar()
        errores = self.error_repo.consultar()
        sesiones_activas = [s for s in sesiones_hoy if s.fin_sesion is None]
        return {
            'total_sesiones': len(sesiones_hoy),
            'sesiones_activas': len(sesiones_activas),
            'total_actividades': len(actividades),
            'total_errores': len(errores),
            'actividades_recientes': actividades[:20],
            'errores_recientes': errores[:10],
        }

    def obtener_reporte_usuario(self, usuario_id, fecha_desde=None, fecha_hasta=None,
                                  modulo=None, tipo_accion=None):
        from datetime import timedelta
        usuario = self.usuario_repo.obtener_por_id(usuario_id)
        if not usuario:
            return None

        sesiones = self.sesion_repo.consultar(usuario_id=usuario_id)
        total_sesiones = len(sesiones)
        sesion_activa = next((s for s in sesiones if s.fin_sesion is None), None)

        filtros = {'usuario_id': usuario_id}
        if fecha_desde:
            filtros['fecha_desde'] = fecha_desde
        if fecha_hasta:
            filtros['fecha_hasta'] = fecha_hasta
        if modulo:
            filtros['modulo'] = modulo
        if tipo_accion:
            filtros['tipo_accion'] = tipo_accion
        actividades = self.actividad_repo.consultar(**filtros)

        tiempo_por_modulo = {}
        actividades_por_modulo = sorted(actividades, key=lambda a: a.created_at or datetime.min)
        for a in actividades_por_modulo:
            mod = a.modulo or 'otros'
            if mod not in tiempo_por_modulo:
                tiempo_por_modulo[mod] = {
                    'modulo': mod, 'cantidad': 0,
                    'inicio': a.created_at, 'fin': a.created_at, 'tipos': set(),
                }
            t = tiempo_por_modulo[mod]
            t['cantidad'] += 1
            t['tipos'].add(a.tipo_accion)
            if a.created_at:
                if not t['inicio'] or a.created_at < t['inicio']:
                    t['inicio'] = a.created_at
                if not t['fin'] or a.created_at > t['fin']:
                    t['fin'] = a.created_at

        for mod, t in tiempo_por_modulo.items():
            if t['inicio'] and t['fin'] and t['inicio'] != t['fin']:
                t['tiempo_estimado'] = (t['fin'] - t['inicio']).total_seconds()
            else:
                t['tiempo_estimado'] = 0
            t['tipos'] = sorted(t['tipos'])

        actividad_ids = [a.id for a in actividades]
        cambios = self.cambio_repo.consultar(actividad_ids=actividad_ids) if actividad_ids else []

        errores = self.error_repo.consultar(usuario_id=usuario_id)

        modulos_disponibles = self.actividad_repo.obtener_modulos_distintos()

        return {
            'usuario': usuario,
            'total_sesiones': total_sesiones,
            'sesion_activa': sesion_activa,
            'sesiones': sesiones[:20],
            'actividades': actividades[:50],
            'total_actividades': len(actividades),
            'tiempo_por_modulo': sorted(tiempo_por_modulo.values(),
                                        key=lambda x: x['tiempo_estimado'], reverse=True),
            'cambios': cambios[:30],
            'total_cambios': len(cambios),
            'errores': errores[:20],
            'total_errores': len(errores),
            'modulos_disponibles': modulos_disponibles,
            'filtros': {
                'fecha_desde': fecha_desde,
                'fecha_hasta': fecha_hasta,
                'modulo': modulo,
                'tipo_accion': tipo_accion,
            },
        }
