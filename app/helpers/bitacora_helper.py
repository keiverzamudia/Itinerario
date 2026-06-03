# app/helpers/bitacora_helper.py
# Helper para registrar actividad en bitácora desde los controllers

from flask import request
from flask_login import current_user
from app.services.bitacora_service import BitacoraService

_bitacora = BitacoraService()


def registrar_actividad(tipo_accion, modulo, accion='', detalle=None):
    if not current_user or not current_user.is_authenticated:
        return None
    return _bitacora.registrar_actividad(
        usuario_id=current_user.id,
        tipo_accion=tipo_accion,
        modulo=modulo,
        accion=accion,
        detalle=detalle,
        pagina=request.path if request else None,
        ip_address=request.remote_addr if request else None,
    )


def iniciar_sesion(ip_address=None, user_agent=None):
    if not current_user or not current_user.is_authenticated:
        return None
    sesion = _bitacora.iniciar_sesion(
        usuario_id=current_user.id,
        ip_address=ip_address or (request.remote_addr if request else None),
        user_agent=user_agent or (request.user_agent.string if request else None),
    )
    if sesion:
        registrar_actividad('login', 'auth', f'Inicio de sesión',
                            f'Usuario {current_user.email} inició sesión')
    return sesion


def finalizar_sesion(sesion_id):
    _bitacora.finalizar_sesion(sesion_id)


def registrar_cambio(tabla_afectada, campo, valor_anterior=None, valor_nuevo=None, registro_id=None):
    actividad = registrar_actividad('update', tabla_afectada,
                                    f'Cambio en {campo}',
                                    f'{campo}: {valor_anterior} → {valor_nuevo}')
    if actividad:
        _bitacora.registrar_cambio(
            actividad_id=actividad.id,
            tabla_afectada=tabla_afectada,
            campo=campo,
            valor_anterior=valor_anterior,
            valor_nuevo=valor_nuevo,
            registro_id=registro_id,
        )


def registrar_error(tipo_error, mensaje, traceback=None):
    usuario_id = current_user.id if current_user and current_user.is_authenticated else None
    _bitacora.registrar_error(
        tipo_error=tipo_error,
        mensaje=mensaje,
        traceback=traceback,
        usuario_id=usuario_id,
        pagina=request.path if request else None,
        ip_address=request.remote_addr if request else None,
    )
