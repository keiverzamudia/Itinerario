from flask import Blueprint, render_template, request, jsonify, current_app, flash, redirect, url_for
from flask_login import login_required
from app import socketio
from app.services.en_vivo_service import EnVivoService
from app.helpers.decorators import permiso_requerido


class EnVivoController:
    def __init__(self):
        self.service = EnVivoService()

    def index(self):
        data = self.service.obtener_index()
        return render_template('en_vivo/index.html', **data)

    def ver(self, guion_id):
        data, guion = self.service.obtener_datos_vivo(guion_id)
        if data is None:
            flash('Este guion no está en vivo. Inícialo primero.', 'warning')
            return redirect(url_for('en_vivo.index'))
        return render_template('en_vivo/vivo.html', **data)

    def iniciar(self, guion_id):
        guion = self.service.iniciar(guion_id)
        if guion:
            flash(f'Guion "{guion.nombre}" iniciado en vivo!', 'success')
            return redirect(url_for('en_vivo.ver', guion_id=guion_id))
        for error in self.service.get_errores():
            flash(f'{error}', 'warning')
        return redirect(url_for('en_vivo.index'))

    def finalizar(self, guion_id):
        self.service.finalizar(guion_id)
        flash('Guion finalizado', 'info')
        return redirect(url_for('en_vivo.index'))

    def sincronizar(self, guion_id):
        data = request.get_json()
        estados = data.get('estados', [])
        self.service.sincronizar_estados(guion_id, estados)
        socketio.emit('actualizar_estados', {
            'guion_id': guion_id,
            'estados': estados
        })
        return jsonify({'success': True})

    def guiones_por_fecha(self):
        data = request.get_json()
        fecha_str = data.get('fecha')
        if not fecha_str:
            return jsonify({'guiones': []})
        result = self.service.buscar_guiones_por_fecha(fecha_str)
        return jsonify(result)
