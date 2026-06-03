from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.services.bitacora_service import BitacoraService
from app.repositories.usuario_repository import UsuarioRepository
from app.helpers.decorators import permiso_requerido
from datetime import datetime


class BitacoraController:
    def __init__(self):
        self.service = BitacoraService()
        self.usuario_repo = UsuarioRepository()

    def dashboard(self):
        data = self.service.obtener_dashboard()
        usuarios = self.usuario_repo.consultar()
        data['usuarios'] = usuarios
        return render_template('bitacora/dashboard.html', **data)

    def reporte_usuario(self, usuario_id):
        usuario = self.usuario_repo.obtener_por_id(usuario_id)
        if not usuario:
            flash('Usuario no encontrado', 'danger')
            return redirect(url_for('bitacora.dashboard'))

        fecha_desde = request.args.get('fecha_desde')
        fecha_hasta = request.args.get('fecha_hasta')
        modulo = request.args.get('modulo')
        tipo_accion = request.args.get('tipo_accion')

        if fecha_desde:
            try:
                fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
            except ValueError:
                fecha_desde = None
        if fecha_hasta:
            try:
                fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            except ValueError:
                fecha_hasta = None

        data = self.service.obtener_reporte_usuario(
            usuario_id, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,
            modulo=modulo, tipo_accion=tipo_accion,
        )
        if not data:
            flash('Usuario no encontrado', 'danger')
            return redirect(url_for('bitacora.dashboard'))

        data['usuarios'] = self.usuario_repo.consultar()
        return render_template('bitacora/usuario.html', **data)
