from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.rol_service import RolService
from app.forms.rol_form import PermisosForm, CrearRolForm
from app.helpers.decorators import permiso_requerido
from app.helpers.bitacora_helper import registrar_actividad
from app.models.dashboard_visibilidad import MODULOS_DASHBOARD, MODULOS_DASHBOARD_INFO


class RolController:
    def __init__(self):
        self.service = RolService()

    def dashboard(self):
        data = self.service.obtener_dashboard()
        return render_template('rol/dashboard.html', **data)

    def editar(self, id):
        form = PermisosForm()
        if form.validate_on_submit():
            permiso_ids = request.form.getlist('permisos')
            if self.service.actualizar_permisos(id, permiso_ids):
                registrar_actividad('update', 'roles', 'Actualizar permisos de usuario',
                                    f'Permisos de usuario #{id} actualizados')
            dash_mods = request.form.getlist('dashboard_modulos')
            self.service.guardar_visibilidad_dashboard_usuario(id, dash_mods)
            flash('Permisos y visibilidad del dashboard actualizados', 'success')
            return redirect(url_for('rol.dashboard'))
        data = self.service.obtener_datos_editar(id)
        vis_data = self.service.obtener_datos_visibilidad_usuario(id, data['usuario'].rol)
        data.update(vis_data)
        return render_template('rol/editar_permisos.html', form=form, **data)

    def editar_rol(self, id):
        form = PermisosForm()
        if form.validate_on_submit():
            permiso_ids = request.form.getlist('permisos')
            if self.service.actualizar_permisos_rol(id, permiso_ids):
                registrar_actividad('update', 'roles', 'Actualizar permisos del rol',
                                    f'Permisos del rol #{id} actualizados')
            dash_mods = request.form.getlist('dashboard_modulos')
            self.service.guardar_visibilidad_dashboard_rol(id, dash_mods)
            flash('Permisos y visibilidad del dashboard actualizados', 'success')
            return redirect(url_for('rol.dashboard'))
        data = self.service.obtener_datos_editar_rol(id)
        vis_data = self.service.obtener_datos_visibilidad_rol(id)
        data.update(vis_data)
        return render_template('rol/editar_rol.html', form=form, **data)

    def crear(self):
        form = CrearRolForm()
        if form.validate_on_submit():
            nombre = form.nombre.data.strip()
            descripcion = form.descripcion.data.strip() if form.descripcion.data else ''
            permiso_ids = request.form.getlist('permisos')
            rol = self.service.crear_rol(nombre, descripcion, permiso_ids)
            if rol:
                dash_mods = request.form.getlist('dashboard_modulos')
                self.service.guardar_visibilidad_dashboard_rol(rol.id, dash_mods)
                registrar_actividad('create', 'roles', 'Crear rol',
                                    f'Rol "{nombre}" creado')
                flash(f'Rol "{nombre}" creado exitosamente', 'success')
                return redirect(url_for('rol.dashboard'))
            else:
                for error in self.service.get_errores():
                    flash(f'{error}', 'danger')
        permisos_agrupados = self.service.permiso_repo.obtener_por_modulos()
        return render_template('rol/crear_rol.html', form=form,
                               permisos_agrupados=permisos_agrupados,
                               modulos_dashboard_info=MODULOS_DASHBOARD_INFO)
