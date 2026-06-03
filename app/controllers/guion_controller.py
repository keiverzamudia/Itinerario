from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.forms.guion_form import GuionForm, ElementoGuionForm, PublicarGuionForm
from app.services.guion_service import GuionService
from app.helpers.decorators import permiso_requerido
from app.helpers.bitacora_helper import registrar_actividad


class GuionController:
    def __init__(self):
        self.service = GuionService()

    def dashboard(self):
        data = self.service.obtener_dashboard()
        return render_template('guion/dashboard.html', **data)

    def crear(self):
        form = GuionForm()
        if form.validate_on_submit():
            guion = self.service.crear_guion(form.nombre.data, form.fechas.data, form.tiempo_inning.data)
            if guion:
                registrar_actividad('create', 'guion', 'Crear guión',
                                    f'Guión "{form.nombre.data}" creado')
                return redirect(url_for('guion.agregar_elementos', id=guion.id))
            for error in self.service.get_errores():
                flash(f'{error}', 'warning')
        return render_template('guion/crear.html', form=form)

    def agregar_elementos(self, id):
        form = ElementoGuionForm()
        form.encargado.choices = self.service.obtener_usuarios_choices()
        data = self.service.obtener_datos_agregar(id)
        if form.validate_on_submit():
            form_data = {
                'tipo': form.tipo.data,
                'hora': form.hora.data,
                'inning': form.inning.data,
                'medio_inning': form.medio_inning.data,
                'contenido': form.contenido.data,
                'duracion_estimada': form.duracion_estimada.data if form.duracion_estimada.data else str(request.form.get('duracion_estimada', '')),
                'encargado': form.encargado.data,
            }
            if self.service.agregar_elemento(id, form_data):
                registrar_actividad('create', 'guion', 'Agregar elemento',
                                    f'Elemento {form.tipo.data} agregado a guión #{id}')
                if form.submit_final.data:
                    flash('¡Guión creado exitosamente!', 'success')
                    return redirect(url_for('guion.dashboard'))
                return redirect(url_for('guion.agregar_elementos', id=id))
            for error in self.service.get_errores():
                flash(f'{error}', 'warning')
        return render_template('guion/agregar_elementos.html', form=form, **data)

    def editar_elemento(self, guion_id, elemento_id):
        data = self.service.obtener_datos_editar_elemento(guion_id, elemento_id)
        if data is None:
            flash('Elemento no pertenece a este guion', 'danger')
            return redirect(url_for('guion.dashboard'))
        form = ElementoGuionForm()
        form.encargado.choices = self.service.obtener_usuarios_choices()
        if request.method == 'GET':
            form.tipo.data = data['elemento'].tipo
            form.hora.data = data['elemento'].hora
            form.inning.data = str(data['elemento'].inning) if data['elemento'].inning else ''
            form.medio_inning.data = data['elemento'].medio_inning or ''
            form.contenido.data = data['elemento'].contenido
            seg = data['elemento'].duracion_estimada
            mins = seg // 60
            secs = seg % 60
            form.duracion_estimada.data = f"{mins},{secs}" if secs else str(mins)
            form.encargado.data = data['elemento'].encargado
        if form.validate_on_submit():
            form_data = {
                'tipo': form.tipo.data,
                'hora': form.hora.data,
                'inning': form.inning.data,
                'medio_inning': form.medio_inning.data,
                'contenido': form.contenido.data,
                'duracion_estimada': form.duracion_estimada.data if form.duracion_estimada.data else str(request.form.get('duracion_estimada', '')),
                'encargado': form.encargado.data,
            }
            if self.service.editar_elemento(guion_id, elemento_id, form_data):
                registrar_actividad('update', 'guion', 'Editar elemento',
                                    f'Elemento #{elemento_id} de guión #{guion_id} editado')
                flash('Elemento actualizado', 'success')
                return redirect(url_for('guion.agregar_elementos', id=guion_id))
            for error in self.service.get_errores():
                flash(f'{error}', 'warning')
        return render_template('guion/editar_elemento.html', form=form, **data)

    def eliminar_elemento(self, guion_id, elemento_id):
        if self.service.eliminar_elemento(guion_id, elemento_id):
            registrar_actividad('delete', 'guion', 'Eliminar elemento',
                                f'Elemento #{elemento_id} de guión #{guion_id} eliminado')
            flash('Elemento eliminado', 'warning')
        else:
            flash('Elemento no pertenece a este guion', 'danger')
        return redirect(url_for('guion.agregar_elementos', id=guion_id))

    def editar(self, id):
        guion = self.service.guion_repo.obtener_por_id(id)
        if not guion:
            flash('Guión no encontrado', 'danger')
            return redirect(url_for('guion.dashboard'))
        form = GuionForm()
        fechas_json = [str(f.fecha) if hasattr(f, 'fecha') else '' for f in guion.fechas]
        form.fechas.data = ','.join(fechas_json)
        form.nombre.data = guion.nombre
        if guion.tiempo_inning:
            mins = guion.tiempo_inning // 60
            secs = guion.tiempo_inning % 60
            form.tiempo_inning.data = f"{mins},{secs}" if secs else str(mins)
        if form.validate_on_submit():
            guion = self.service.editar_guion(id, form.nombre.data, form.fechas.data, form.tiempo_inning.data)
            if guion:
                registrar_actividad('update', 'guion', 'Editar guión',
                                    f'Guión "{form.nombre.data}" actualizado')
                flash('¡Guión actualizado!', 'success')
                return redirect(url_for('guion.dashboard'))
            for error in self.service.get_errores():
                flash(f'{error}', 'warning')
        return render_template('guion/editar.html', form=form, guion=guion, fechas_json=fechas_json)

    def previsualizar(self, id):
        data = self.service.obtener_datos_previsualizar(id)
        return render_template('guion/previsualizar.html', **data)

    def publicar(self, id):
        guion = self.service.guion_repo.obtener_por_id(id)
        if not guion:
            flash('Guión no encontrado', 'danger')
            return redirect(url_for('guion.dashboard'))
        form = PublicarGuionForm()
        if form.validate_on_submit():
            self.service.publicar_guion(id)
            registrar_actividad('update', 'guion', 'Publicar guión',
                                f'Guión "{guion.nombre}" publicado')
            flash(f'Guión "{guion.nombre}" publicado!', 'success')
            return redirect(url_for('guion.dashboard'))
        return render_template('guion/publicar.html', form=form, guion=guion)

    def eliminar(self, id):
        nombre = self.service.eliminar_guion(id)
        registrar_actividad('delete', 'guion', 'Eliminar guión',
                            f'Guión "{nombre}" eliminado')
        flash(f'Guión "{nombre}" eliminado', 'warning')
        return redirect(url_for('guion.dashboard'))

    def api_horas_usadas(self, guion_id):
        horas, innings = self.service.obtener_horas_usadas(guion_id)
        return jsonify({'horas': horas, 'innings': innings})
