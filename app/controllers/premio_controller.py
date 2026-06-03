from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from app.services.premio_service import PremioService
from app.helpers.decorators import permiso_requerido
from app.helpers.bitacora_helper import registrar_actividad
from app.config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS


class PremioController:
    def __init__(self):
        self.service = PremioService()

    def _allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def dashboard(self):
        if request.method == 'POST':
            action = request.form.get('action')
            permiso_map = {
                'crear': 'premio.create',
                'editar': 'premio.edit',
                'entregar': 'premio.entregar',
                'crear_y_entregar': 'premio.entregar',
            }
            permiso_necesario = permiso_map.get(action)
            if permiso_necesario and not current_user.tiene_permiso(permiso_necesario):
                flash('No tienes permiso para esta acción', 'danger')
                return redirect(url_for('premio.dashboard'))

            if action == 'crear':
                nombre = request.form.get('nombre')
                id_patrocinador = request.form.get('id_patrocinador')
                descripcion = request.form.get('descripcion')
                fecha_creacion_str = request.form.get('fecha_creacion')
                hora_creacion_str = request.form.get('hora_creacion')
                foto_filename = None
                if 'foto' in request.files:
                    foto = request.files['foto']
                    if foto and foto.filename and self._allowed_file(foto.filename):
                        filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{foto.filename}")
                        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                        foto.save(os.path.join(UPLOAD_FOLDER, filename))
                        foto_filename = filename
                if self.service.crear(nombre, fecha_creacion_str, hora_creacion_str,
                                      id_patrocinador=id_patrocinador, descripcion=descripcion,
                                      foto_filename=foto_filename):
                    registrar_actividad('create', 'premios', 'Crear premio',
                                        f'Premio "{nombre}" creado')
                    flash('Premio creado exitosamente', 'success')
                else:
                    for error in self.service.get_errores():
                        flash(error, 'danger')

            elif action == 'editar':
                premio_id = request.form.get('premio_id')
                nombre = request.form.get('nombre')
                id_patrocinador = request.form.get('id_patrocinador')
                descripcion = request.form.get('descripcion')
                if not premio_id or not nombre:
                    flash('Faltan datos para editar', 'danger')
                else:
                    foto_filename = self.service.obtener_foto_actual(premio_id)
                    if 'foto' in request.files:
                        foto = request.files['foto']
                        if foto and foto.filename and self._allowed_file(foto.filename):
                            filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{foto.filename}")
                            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                            foto.save(os.path.join(UPLOAD_FOLDER, filename))
                            foto_filename = filename
                    if self.service.editar(premio_id, nombre,
                                           id_patrocinador=id_patrocinador,
                                           descripcion=descripcion,
                                           foto_filename=foto_filename):
                        registrar_actividad('update', 'premios', 'Editar premio',
                                            f'Premio #{premio_id} editado')
                        flash('Premio actualizado correctamente', 'success')
                    else:
                        for error in self.service.get_errores():
                            flash(error, 'danger')

            elif action == 'entregar':
                premio_id = request.form.get('premio_id')
                if not premio_id:
                    flash('No se identificó el premio', 'danger')
                elif self.service.entregar(premio_id, user_id=current_user.id):
                    registrar_actividad('update', 'premios', 'Entregar premio',
                                        f'Premio #{premio_id} entregado')
                    flash('Premio entregado exitosamente', 'success')
                else:
                    for error in self.service.get_errores():
                        flash(error, 'danger' if 'encontrado' in error else 'warning')

            elif action == 'crear_y_entregar':
                premio_id = request.form.get('id_premio')
                id_patrocinador = request.form.get('id_patrocinador')
                descripcion = request.form.get('descripcion')
                if not premio_id:
                    flash('No se seleccionó un premio válido', 'danger')
                elif self.service.crear_y_entregar(premio_id, id_patrocinador=id_patrocinador, descripcion=descripcion, user_id=current_user.id):
                    registrar_actividad('update', 'premios', 'Entregar premio existente',
                                        f'Premio #{premio_id} entregado')
                    flash('Premio entregado exitosamente', 'success')
                else:
                    for error in self.service.get_errores():
                        flash(error, 'danger' if 'encontrado' in error else 'warning')

            return redirect(url_for('premio.dashboard'))

        data = self.service.obtener_dashboard()
        return render_template('premio/dashboard.html', **data)

    def eliminar(self, id):
        nombre = self.service.eliminar(id)
        if nombre:
            registrar_actividad('delete', 'premios', 'Eliminar premio',
                                f'Premio "{nombre}" eliminado')
            flash(f'Premio "{nombre}" eliminado', 'warning')
        else:
            for error in self.service.get_errores():
                flash(error, 'danger' if 'encontrado' in error else 'warning')
        return redirect(url_for('premio.dashboard'))

    def api_obtener(self, id):
        data = self.service.obtener_api(id)
        if data:
            return jsonify(data)
        return jsonify({'error': 'No encontrado'}), 404
