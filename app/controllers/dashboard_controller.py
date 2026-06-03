from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app import usuarios_conectados
from app.services.dashboard_service import DashboardService
from app.helpers.decorators import permiso_requerido
from app.models.dashboard_visibilidad import MODULOS_DASHBOARD_INFO


class DashboardController:
    def __init__(self):
        self.service = DashboardService()

    def index(self):
        return redirect(url_for('auth.login'))

    def panel(self):
        total_sockets = len(usuarios_conectados)

        live = self.service.obtener_metrica_live()

        modulos_visibles = self.service.obtener_modulos_visibles(current_user)

        metricas = self.service.obtener_metricas_modulos(modulos_visibles)

        actividad = self.service.obtener_actividad_reciente()

        alertas = self.service.obtener_alertas()

        usuarios_info = []
        for u in usuarios_conectados.values():
            path = u.get('pagina', '/')
            if path.startswith('/dashboard'):
                modulo = 'Inicio'
            elif path.startswith('/usuario'):
                modulo = 'Usuarios'
            elif path.startswith('/guion'):
                modulo = 'Gestión de Guión'
            elif path.startswith('/en-vivo'):
                modulo = 'Guion en Vivo'
            elif path.startswith('/contrato'):
                modulo = 'Contratos'
            elif path.startswith('/patrocinador'):
                modulo = 'Patrocinantes'
            elif path.startswith('/premio'):
                modulo = 'Premios'
            elif path.startswith('/mantenimiento'):
                modulo = 'Mantenimiento'
            elif path.startswith('/gestion-tarea'):
                modulo = 'Tareas'
            elif path.startswith('/balance'):
                modulo = 'Balance'
            elif path.startswith('/bitacora'):
                modulo = 'Bitácora'
            elif path.startswith('/rol'):
                modulo = 'Roles'
            else:
                modulo = path
            usuarios_info.append({
                'nombre': u.get('nombre', 'Desconocido'),
                'modulo': modulo,
                'en_vivo': u.get('en_vivo_id') is not None
            })

        return render_template('dashboard/index.html',
                               usuarios_en_linea=total_sockets,
                               usuarios_info=usuarios_info,
                               live=live,
                               metricas=metricas,
                               actividad=actividad,
                               alertas=alertas,
                               modulos_visibles=modulos_visibles,
                               modulos_dashboard_info=MODULOS_DASHBOARD_INFO)
