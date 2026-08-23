import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user
from app.helpers.decorators import verificar_acceso
from app.helpers.permission_map import TAREA
from app.model.tarea_model import TareaModel, TareasAsignadasModel
from app.model.auth_model import UsuarioModel
from app.model.bitacora_model import ActividadModel

bp = Blueprint('gestion_tarea', __name__, url_prefix='/gestion-tarea')

bp.before_request(verificar_acceso(TAREA))


def _registrar_bitacora(tipo, accion, detalle):
    try:
        ActividadModel().registrar({
            'usuario_id': current_user.id,
            'tipo_accion': tipo,
            'modulo': 'tareas',
            'accion': accion,
            'detalle': json.dumps({'detalle': detalle}),
            'pagina': request.path,
            'ip_address': request.remote_addr,
        })
    except Exception:
        pass


@bp.route('/', methods=['GET', 'POST'])
def dashboard():
    tarea_model = TareaModel()
    asignacion_model = TareasAsignadasModel()
    usuario_model = UsuarioModel()

    if request.method == 'POST':
        if request.form.get('registrar'):
            if not current_user.tiene_permiso('gestion_tarea.create'):
                return jsonify({'error': 'No tienes permiso para esta accion'}), 403
            nombre = request.form.get('Nombre_Tarea', '').strip()
            instruccion = request.form.get('Instruccion', '').strip()
            if not nombre or not instruccion:
                return jsonify({'success': False, 'error': 'Nombre e instrucción son obligatorios'})
            tarea_model.set_nombre_tarea(nombre)
            tarea_model.set_instruccion(instruccion)
            tarea_model.set_id_usuario_creador(current_user.id)
            ok = tarea_model.confirmar_registro()
            if ok:
                _registrar_bitacora('create', 'Crear tarea', f'Tarea "{nombre}" creada')
            return jsonify({'success': bool(ok), 'error': None if ok else 'Error al crear tarea'})

        if request.form.get('editar'):
            if not current_user.tiene_permiso('gestion_tarea.edit'):
                return jsonify({'error': 'No tienes permiso para esta accion'}), 403
            id_tarea = request.form.get('id_tarea')
            nombre = request.form.get('Nombre_Tarea', '').strip()
            instruccion = request.form.get('Instruccion', '').strip()
            if not id_tarea or not nombre or not instruccion:
                return jsonify({'success': False, 'error': 'Datos incompletos'})
            tarea_model.set_nombre_tarea(nombre)
            tarea_model.set_instruccion(instruccion)
            ok = tarea_model.confirmar_modificacion(id_tarea)
            if ok:
                _registrar_bitacora('update', 'Editar tarea', f'Tarea "{nombre}" editada')
            return jsonify({'success': bool(ok), 'error': None if ok else 'Error al editar tarea'})

        if request.form.get('eliminar'):
            if not current_user.tiene_permiso('gestion_tarea.delete'):
                return jsonify({'error': 'No tienes permiso para esta accion'}), 403
            id_tarea = request.form.get('id_tarea')
            tarea = tarea_model.confirmar_eliminacion(id_tarea)
            if tarea:
                _registrar_bitacora('delete', 'Eliminar tarea', f'Tarea "{tarea["Nombre_Tarea"]}" eliminada')
            return jsonify({'success': bool(tarea), 'error': None if tarea else 'Error al eliminar tarea'})

        if request.form.get('asignar'):
            if not current_user.tiene_permiso('gestion_tarea.create'):
                return jsonify({'error': 'No tienes permiso para esta accion'}), 403
            id_tarea = request.form.get('id_tarea')
            id_usuario = request.form.get('id_usuario')
            if not id_tarea or not id_usuario:
                return jsonify({'success': False, 'error': 'Selecciona tarea y empleado'})
            ok = asignacion_model.registrar({
                'id_tarea': id_tarea, 'id_usuario': id_usuario,
            })
            if ok:
                tarea = tarea_model.obtener_por_id(id_tarea)
                _registrar_bitacora('update', 'Asignar tarea', f'Tarea "{tarea["Nombre_Tarea"]}" asignada a usuario #{id_usuario}')
            return jsonify({'success': bool(ok), 'error': None if ok else 'Error al asignar tarea'})

        if request.form.get('consultar'):
            data = []
            for t in tarea_model.consultar():
                data.append({
                    'id_tarea': t['id_tarea'], 'Nombre_Tarea': t['Nombre_Tarea'],
                    'Instruccion': t['Instruccion'], 'Estatus': t['Estatus'],
                })
            return jsonify(data)

        return jsonify({'error': 'Acción no reconocida'})

    tareas = tarea_model.consultar()
    usuarios = usuario_model.consultar(activo=1)
    total = len(tareas)
    tareas_activas = [(t['id_tarea'], f"{t['id_tarea']} - {t['Nombre_Tarea']}") for t in tareas if t['Estatus']]
    empleados_activos = [(u.id, f"{u.cedula} - {u.nombre}") for u in usuarios]
    return render_template('gestion_tarea/dashboard.html', tareas=tareas, total=total,
                           tareas_activas=tareas_activas, empleados_activos=empleados_activos)


@bp.route('/mis-tareas')
def tareas_usuario():
    asignacion_model = TareasAsignadasModel()
    tareas = asignacion_model.obtener_por_usuario(current_user.id)
    pendientes = asignacion_model.contar_pendientes(current_user.id)
    return render_template('gestion_tarea/tareas_usuario_vista.html', tareas=tareas, pendientes=pendientes)


@bp.route('/seguimiento', methods=['GET'])
def seguimiento():
    return render_template('gestion_tarea/seguimiento.html')


@bp.route('/consultar-asignaciones', methods=['POST'])
def consultar_asignaciones():
    if not current_user.tiene_permiso('gestion_tarea.supervisar'):
        return jsonify({'error': 'Sin permiso'}), 403
    asignacion_model = TareasAsignadasModel()
    data = []
    for a in asignacion_model.consultar_todas():
        data.append({
            'id_asignacion': a['id_asignacion'],
            'id_tarea': a['id_tarea'],
            'id_usuario': a['id_usuario'],
            'Estado': a['Estado'],
            'Nombre_Tarea': a['Nombre_Tarea'],
            'Instruccion': a['Instruccion'],
            'usuario_nombre': a['usuario_nombre'],
            'usuario_cedula': a['usuario_cedula'],
            'fecha_asignacion_tarea': a['fecha_asignacion_tarea'].strftime('%d/%m/%Y %H:%M') if a.get('fecha_asignacion_tarea') else '',
        })
    return jsonify(data)


@bp.route('/completar', methods=['POST'])
def completar():
    asignacion_model = TareasAsignadasModel()
    id_asignacion = request.form.get('id_asignacion')
    es_ajax = request.accept_mimetypes.accept_json

    if not id_asignacion:
        if es_ajax:
            return jsonify({'error': 'Asignación faltante'}), 400
        flash('Información de asignación faltante.', 'danger')
        return redirect(url_for('gestion_tarea.tareas_usuario'))
    asignacion = asignacion_model.obtener_por_id(id_asignacion)
    if not asignacion:
        if es_ajax:
            return jsonify({'error': 'Asignación no encontrada'}), 404
        flash('Asignación no encontrada', 'danger')
        return redirect(url_for('gestion_tarea.tareas_usuario'))
    if asignacion['id_usuario'] != int(current_user.id) and not current_user.tiene_permiso('gestion_tarea.supervisar'):
        if es_ajax:
            return jsonify({'error': 'Sin permiso para completar esta tarea'}), 403
        flash('No tienes permiso para completar esta tarea', 'danger')
        return redirect(url_for('gestion_tarea.tareas_usuario'))
    asignacion_model.modificar_estado(id_asignacion, 'Completada')
    _registrar_bitacora('update', 'Completar tarea', f'Tarea "{asignacion["Nombre_Tarea"]}" completada')
    if es_ajax:
        return jsonify({'success': True, 'mensaje': 'Tarea completada'})
    flash('Actividad marcada como completada', 'success')
    return redirect(url_for('gestion_tarea.tareas_usuario'))
