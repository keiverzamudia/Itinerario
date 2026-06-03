from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.gestion_tarea_service import GestionTareaService
from app.helpers.decorators import permiso_requerido
from app.helpers.bitacora_helper import registrar_actividad
from app.forms.gestion_tarea_form import (
    TareaForm, EditarTareaForm, EliminarTareaForm
)


class GestionTareaController:
    def __init__(self):
        self.service = GestionTareaService()

    def dashboard(self):
        form = TareaForm()
        form_editar = EditarTareaForm()
        form_eliminar = EliminarTareaForm()

        if request.method == 'POST':
            action = request.form.get('action')

            if action == 'crear':
                if not current_user.tiene_permiso('gestion_tarea.create'):
                    flash('No tienes permiso para crear tareas', 'danger')
                    return redirect(url_for('gestion_tarea.dashboard'))
                form.id_usuario.choices = self.service.obtener_usuarios_activos()
                if form.validate_on_submit():
                    tarea = self.service.crear_tarea(
                        form.Nombre_Tarea.data,
                        form.Instruccion.data,
                        current_user.id,
                        form.id_usuario.data,
                    )
                    if tarea:
                        registrar_actividad('create', 'tareas', 'Crear tarea',
                                            f'Tarea "{form.Nombre_Tarea.data}" creada')
                        flash('Tarea creada exitosamente', 'success')
                    else:
                        for error in self.service.get_errores():
                            flash(error, 'danger')

            elif action == 'editar':
                if not current_user.tiene_permiso('gestion_tarea.edit'):
                    flash('No tienes permiso para editar tareas', 'danger')
                    return redirect(url_for('gestion_tarea.dashboard'))
                id_tarea = request.form.get('id_tarea')
                nombre = request.form.get('Nombre_Tarea')
                instruccion = request.form.get('Instruccion')
                if self.service.editar_tarea(id_tarea, nombre, instruccion):
                    registrar_actividad('update', 'tareas', 'Editar tarea',
                                        f'Tarea #{id_tarea} editada')
                    flash('Tarea actualizada exitosamente', 'success')
                else:
                    for error in self.service.get_errores():
                        flash(error, 'danger')

            elif action == 'eliminar':
                if not current_user.tiene_permiso('gestion_tarea.delete'):
                    flash('No tienes permiso para eliminar tareas', 'danger')
                    return redirect(url_for('gestion_tarea.dashboard'))
                id_tarea = request.form.get('id_tarea')
                tarea = self.service.eliminar_tarea(id_tarea)
                if tarea:
                    registrar_actividad('delete', 'tareas', 'Eliminar tarea',
                                        f'Tarea "{tarea.Nombre_Tarea}" eliminada')
                    flash(f'Tarea "{tarea.Nombre_Tarea}" eliminada', 'warning')
                else:
                    for error in self.service.get_errores():
                        flash(error, 'danger' if 'encontrada' in error else 'warning')

            return redirect(url_for('gestion_tarea.dashboard'))

        data = self.service.obtener_dashboard()
        form.id_usuario.choices = self.service.obtener_usuarios_activos()
        return render_template('gestion_tarea/dashboard.html',
                               form=form, form_editar=form_editar,
                               form_eliminar=form_eliminar, **data)

    def tareas_usuario(self):
        data = self.service.obtener_tareas_usuario(current_user.id)
        return render_template('gestion_tarea/tareas_usuario_vista.html', **data)

    def completar_tarea(self):
        id_asignacion = request.form.get('id_asignacion')
        if not id_asignacion:
            flash('Información de asignación faltante.', 'danger')
            return redirect(url_for('gestion_tarea.tareas_usuario'))

        if self.service.completar_tarea(id_asignacion, current_user.id):
            registrar_actividad('update', 'tareas', 'Completar tarea',
                                f'Asignación #{id_asignacion} completada por usuario #{current_user.id}')
            flash('Actividad marcada como completada', 'success')
        else:
            for error in self.service.get_errores():
                flash(error, 'danger')

        return redirect(url_for('gestion_tarea.tareas_usuario'))
