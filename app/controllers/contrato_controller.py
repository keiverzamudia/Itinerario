from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.services.contrato_service import ContratoService
from app.helpers.decorators import permiso_requerido
from app.helpers.bitacora_helper import registrar_actividad
from app.forms.contrato import ContratoForm


class ContratoController:
    def __init__(self):
        self.service = ContratoService()

    def _cargar_patrocinadores(self, form):
        patrocinadores = self.service.obtener_patrocinadores()
        form.id_patrocinador.choices = [
            (p.id_patrocinador, p.nombre_empresa) for p in patrocinadores
        ]

    def dashboard(self):
        form = ContratoForm()
        self._cargar_patrocinadores(form)

        if request.method == 'POST':
            action = request.form.get('action')

            if action == 'crear':
                if not current_user.tiene_permiso('contrato.create'):
                    flash('No tienes permiso para crear contratos', 'danger')
                    return redirect(url_for('contrato.dashboard'))
                if form.validate_on_submit():
                    if self.service.crear(
                        form.id_patrocinador.data,
                        form.fecha_inicio.data,
                        form.fecha_fin.data,
                        form.estatus.data,
                        form.tipo.data,
                        form.monto_total.data,
                    ):
                        registrar_actividad('create', 'contrato', 'Crear contrato',
                                            f'Contrato con patrocinador #{form.id_patrocinador.data} creado')
                        flash('Contrato registrado exitosamente', 'success')
                    else:
                        for error in self.service.get_errores():
                            flash(error, 'danger')
                else:
                    flash('Error al registrar. Revise los campos del formulario.', 'danger')

            elif action == 'editar':
                if not current_user.tiene_permiso('contrato.edit'):
                    flash('No tienes permiso para editar contratos', 'danger')
                    return redirect(url_for('contrato.dashboard'))
                id_c = request.form.get('id_contrato')
                if self.service.editar(
                    id_c, form.id_patrocinador.data,
                    form.fecha_inicio.data, form.fecha_fin.data,
                    form.estatus.data, form.tipo.data, form.monto_total.data
                ):
                    registrar_actividad('update', 'contrato', 'Editar contrato',
                                        f'Contrato #{id_c} editado')
                    flash('Contrato actualizado exitosamente', 'success')
                else:
                    for error in self.service.get_errores():
                        flash(error, 'danger')
                return redirect(url_for('contrato.dashboard'))

            elif action == 'eliminar':
                if not current_user.tiene_permiso('contrato.delete'):
                    flash('No tienes permiso para eliminar contratos', 'danger')
                    return redirect(url_for('contrato.dashboard'))
                id_c = request.form.get('id_contrato')
                c = self.service.eliminar(id_c)
                if c:
                    registrar_actividad('delete', 'contrato', 'Eliminar contrato',
                                        f'Contrato #{id_c} eliminado')
                    flash('Contrato eliminado de la lista operativa', 'warning')
                else:
                    for error in self.service.get_errores():
                        flash(error, 'danger')

            return redirect(url_for('contrato.dashboard'))

        data = self.service.obtener_dashboard()
        return render_template('contrato/contrato.html', form=form, **data)

    def api_obtener(self, id):
        data = self.service.obtener_api(id)
        if data:
            return jsonify(data)
        return jsonify({'error': 'No encontrado'}), 404
