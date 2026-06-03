from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user
from app.services.inventario_service import InventarioService
from app.helpers.decorators import permiso_requerido
from app.helpers.bitacora_helper import registrar_actividad


class InventarioController:
    def __init__(self):
        self.service = InventarioService()

    def dashboard(self):
        data = self.service.obtener_dashboard()
        tipos = self.service.obtener_tipos()
        estados = self.service.obtener_estados()
        return render_template('recursos/dashboard_recursos.html',
                               recursos=data['recursos'],
                               total_recursos=data['total'],
                               disponibles=data['disponibles'],
                               asignados=data['asignados'],
                               en_mantenimiento=data['en_mantenimiento'],
                               tipos=tipos,
                               estados=estados)

    def crear(self):
        if request.method == 'POST':
            recurso = self.service.crear_recurso({
                'nombre': request.form.get('nombre'),
                'descripcion': request.form.get('descripcion'),
                'tipo_id': request.form.get('tipo_id'),
                'fecha_compra': request.form.get('fecha_compra'),
                'costo': request.form.get('costo'),
            })
            if recurso:
                registrar_actividad('create', 'inventario', 'Crear recurso',
                                    f'Recurso "{request.form.get("nombre")}" creado')
                flash(f'Recurso "{recurso.nombre}" creado exitosamente', 'success')
                return redirect(url_for('inventario.dashboard'))
            for err in self.service.errores:
                flash(err, 'danger')
        tipos = self.service.obtener_tipos()
        return render_template('recursos/crear_recurso.html', tipos=tipos)

    def ver(self, id):
        recurso = self.service.obtener_recurso(id)
        if not recurso:
            flash('Recurso no encontrado', 'danger')
            return redirect(url_for('inventario.dashboard'))
        asignaciones = self.service.obtener_asignaciones(recurso_id=id)
        return render_template('recursos/ver_recurso.html',
                               recurso=recurso,
                               asignaciones=asignaciones)

    def editar(self, id):
        recurso = self.service.obtener_recurso(id)
        if not recurso:
            flash('Recurso no encontrado', 'danger')
            return redirect(url_for('inventario.dashboard'))
        if request.method == 'POST':
            recurso = self.service.editar_recurso(id, {
                'nombre': request.form.get('nombre'),
                'descripcion': request.form.get('descripcion'),
                'tipo_id': request.form.get('tipo_id'),
                'fecha_compra': request.form.get('fecha_compra'),
                'costo': request.form.get('costo'),
            })
            if recurso:
                registrar_actividad('update', 'inventario', 'Editar recurso',
                                    f'Recurso "{request.form.get("nombre")}" editado')
                flash('Recurso actualizado exitosamente', 'success')
                return redirect(url_for('inventario.ver', id=id))
            for err in self.service.errores:
                flash(err, 'danger')
        tipos = self.service.obtener_tipos()
        return render_template('recursos/editar_recurso.html',
                               recurso=recurso, tipos=tipos)

    def eliminar(self, id):
        recurso = self.service.obtener_recurso(id)
        if not recurso:
            flash('Recurso no encontrado', 'danger')
            return redirect(url_for('inventario.dashboard'))
        if request.method == 'POST':
            if self.service.eliminar_recurso(id):
                registrar_actividad('delete', 'inventario', 'Eliminar recurso',
                                    f'Recurso "{recurso.nombre}" eliminado')
                flash(f'Recurso "{recurso.nombre}" dado de baja', 'success')
                return redirect(url_for('inventario.dashboard'))
            for err in self.service.errores:
                flash(err, 'danger')
        pendientes = self.service.recurso_repo.tiene_asignaciones_pendientes(id)
        total_asignaciones = self.service.total_asignaciones(id)
        return render_template('recursos/confirmar_eliminar_recurso.html',
                               recurso=recurso,
                               pendientes=pendientes,
                               total_asignaciones=total_asignaciones)

    def asignar(self, recurso_id):
        recurso = self.service.obtener_recurso(recurso_id)
        if not recurso:
            flash('Recurso no encontrado', 'danger')
            return redirect(url_for('inventario.dashboard'))
        if request.method == 'POST':
            asignacion = self.service.asignar_recurso(
                recurso_id=int(recurso_id),
                usuario_id=int(request.form.get('usuario_id')),
                fecha_devolucion=request.form.get('fecha_devolucion_esperada'),
                notas=request.form.get('notas'),
            )
            if asignacion:
                registrar_actividad('create', 'inventario', 'Asignar recurso',
                                    f'Recurso "{recurso.nombre}" asignado')
                flash(f'Recurso "{recurso.nombre}" asignado correctamente', 'success')
                return redirect(url_for('inventario.ver', id=recurso_id))
            for err in self.service.errores:
                flash(err, 'danger')
        recurso, usuarios = self.service.obtener_datos_asignar(recurso_id)
        return render_template('recursos/asignar_recurso.html',
                               recurso=recurso, usuarios=usuarios)

    def gestion_asignaciones(self):
        asignaciones = self.service.obtener_asignaciones_gestion()
        recursos = self.service.recurso_repo.consultar()
        usuarios = self.service.obtener_usuarios()
        estados_asignacion = self.service.obtener_estados_asignacion()
        return render_template('recursos/gestion_asignaciones.html',
                               asignaciones=asignaciones,
                               recursos=recursos,
                               usuarios=usuarios,
                               estados_asignacion=estados_asignacion)

    def asignar_desde_gestion(self):
        if request.method == 'POST':
            asignacion = self.service.asignar_recurso(
                recurso_id=int(request.form.get('recurso_id')),
                usuario_id=int(request.form.get('usuario_id')),
                fecha_devolucion=request.form.get('fecha_devolucion_esperada'),
                notas=request.form.get('notas'),
            )
            if asignacion:
                registrar_actividad('create', 'inventario', 'Asignar recurso',
                                    f'Recurso #{request.form.get("recurso_id")} asignado')
                flash('Recurso asignado correctamente', 'success')
            else:
                for err in self.service.errores:
                    flash(err, 'danger')
        return redirect(url_for('inventario.gestion_asignaciones'))

    def devolver_recurso(self, asignacion_id):
        if self.service.devolver_recurso(asignacion_id):
            registrar_actividad('update', 'inventario', 'Devolver recurso',
                                f'Asignación #{asignacion_id} devuelta')
            flash('Devolución procesada correctamente', 'success')
        else:
            for err in self.service.errores:
                flash(err, 'danger')
        return redirect(url_for('inventario.gestion_asignaciones'))

    def api_tipos(self):
        tipos = self.service.obtener_tipos()
        return jsonify([{'id': t.id, 'nombre': t.nombre, 'descripcion': t.descripcion} for t in tipos])

    def api_crear_tipo(self):
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        tipo = self.service.crear_tipo(nombre, descripcion)
        if tipo:
            registrar_actividad('create', 'inventario', 'Crear tipo de recurso',
                                f'Tipo "{nombre}" creado')
            return jsonify({'success': True, 'tipo': {'id': tipo.id, 'nombre': tipo.nombre, 'descripcion': tipo.descripcion}})
        return jsonify({'success': False, 'errores': self.service.errores}), 400

    def api_editar_tipo(self, id):
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        tipo = self.service.editar_tipo(id, nombre, descripcion)
        if tipo:
            registrar_actividad('update', 'inventario', 'Editar tipo de recurso',
                                f'Tipo "{nombre}" editado')
            return jsonify({'success': True, 'tipo': {'id': tipo.id, 'nombre': tipo.nombre, 'descripcion': tipo.descripcion}})
        return jsonify({'success': False, 'errores': self.service.errores}), 400

    def api_eliminar_tipo(self, id):
        if self.service.eliminar_tipo(id):
            registrar_actividad('delete', 'inventario', 'Eliminar tipo de recurso',
                                f'Tipo #{id} eliminado')
            return jsonify({'success': True})
        return jsonify({'success': False, 'errores': self.service.errores}), 400
