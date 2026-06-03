from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.services.patrocinador_service import PatrocinadorService
from app.helpers.decorators import permiso_requerido
from app.helpers.bitacora_helper import registrar_actividad
from app.forms.patrocinador_form import PatrocinadorForm


class PatrocinadorController:
    def __init__(self):
        self.service = PatrocinadorService()

    def dashboard(self):
        form = PatrocinadorForm()

        if request.method == 'POST':
            action = request.form.get('action')

            if action == 'crear':
                if not current_user.tiene_permiso('patrocinador.create'):
                    flash('No tienes permiso para crear patrocinadores', 'danger')
                    return redirect(url_for('patrocinador.dashboard'))
                if form.validate_on_submit():
                    p = self.service.crear(
                        form.nombre_empresa.data,
                        form.rif.data,
                        form.nombre_contacto.data,
                        form.telefono.data,
                        form.email.data,
                    )
                    if p:
                        registrar_actividad('create', 'patrocinadores', 'Crear patrocinador',
                                            f'Patrocinador "{form.nombre_empresa.data}" creado')
                        flash('Patrocinador registrado exitosamente', 'success')
                    else:
                        for error in self.service.get_errores():
                            flash(error, 'danger')
                else:
                    flash('Error al registrar. Revise los campos del formulario.', 'danger')

            elif action == 'editar':
                if not current_user.tiene_permiso('patrocinador.edit'):
                    flash('No tienes permiso para editar patrocinadores', 'danger')
                    return redirect(url_for('patrocinador.dashboard'))
                id_p = request.form.get('id_patrocinador')
                if self.service.editar(
                    id_p, form.nombre_empresa.data, form.rif.data,
                    form.nombre_contacto.data, form.telefono.data, form.email.data
                ):
                    registrar_actividad('update', 'patrocinadores', 'Editar patrocinador',
                                        f'Patrocinador #{id_p} editado')
                    flash('Patrocinador actualizado exitosamente', 'success')
                else:
                    for error in self.service.get_errores():
                        flash(error, 'danger')
                return redirect(url_for('patrocinador.dashboard'))

            elif action == 'eliminar':
                if not current_user.tiene_permiso('patrocinador.delete'):
                    flash('No tienes permiso para eliminar patrocinadores', 'danger')
                    return redirect(url_for('patrocinador.dashboard'))
                id_p = request.form.get('id_patrocinador')
                p = self.service.eliminar(id_p)
                if p:
                    registrar_actividad('delete', 'patrocinadores', 'Eliminar patrocinador',
                                        f'Patrocinador "{p.nombre_empresa}" eliminado')
                    flash(f'Patrocinador "{p.nombre_empresa}" eliminado', 'warning')
                else:
                    for error in self.service.get_errores():
                        flash(error, 'danger')

            return redirect(url_for('patrocinador.dashboard'))

        data = self.service.obtener_dashboard()
        return render_template('patrocinador/patrocinador.html', form=form, **data)

    def api_obtener(self, id):
        data = self.service.obtener_api(id)
        if data:
            return jsonify(data)
        return jsonify({'error': 'No encontrado'}), 404
