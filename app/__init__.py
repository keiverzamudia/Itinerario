from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO
from flask_login import LoginManager

csrf = CSRFProtect()
socketio = SocketIO(cors_allowed_origins="*")
usuarios_conectados = {}
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicia sesión para acceder'
login_manager.login_message_category = 'warning'


def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')

    app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui-cambiala'
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    csrf.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)

    from app.database.connection import DatabaseManager
    DatabaseManager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.repositories.usuario_repository import UsuarioRepository
        return UsuarioRepository().obtener_por_id(int(user_id))

    with app.app_context():
        from app.services.rol_service import RolService
        RolService().seed_permisos_iniciales()

    from app.routes import auth_routes, dashboard_routes, guion_routes
    from app.routes import mantenimiento_routes, premio_routes, usuario_routes
    from app.routes import rol_routes, bitacora_routes, gestion_tarea_routes
    from app.routes import patrocinador_routes, contrato_routes, balance_routes
    from app.routes import inventario_routes, reels_routes

    for bp in [auth_routes.bp, dashboard_routes.bp, guion_routes.bp,
               mantenimiento_routes.bp, premio_routes.bp, usuario_routes.bp,
               rol_routes.bp, bitacora_routes.bp, gestion_tarea_routes.bp,
               patrocinador_routes.bp, contrato_routes.bp, balance_routes.bp,
               inventario_routes.bp, reels_routes.bp]:
        app.register_blueprint(bp)

    from app.routes import en_vivo_routes
    csrf.exempt(en_vivo_routes.bp)
    app.register_blueprint(en_vivo_routes.bp)

    @socketio.on('connect')
    def handle_connect():
        pass

    @socketio.on('registrar_usuario')
    def handle_registrar_usuario(data):
        from flask import request
        sid = request.sid
        usuarios_conectados[sid] = {
            'user_id': data.get('user_id'),
            'nombre': data.get('nombre'),
            'pagina': data.get('pagina', '/'),
            'en_vivo_id': data.get('en_vivo_id')
        }
        _emit_usuarios_actualizados()

    @socketio.on('cambio_pagina')
    def handle_cambio_pagina(data):
        from flask import request
        sid = request.sid
        if sid in usuarios_conectados:
            usuarios_conectados[sid]['pagina'] = data.get('pagina', '/')
            usuarios_conectados[sid]['en_vivo_id'] = data.get('en_vivo_id')
            _emit_usuarios_actualizados()

    @socketio.on('disconnect')
    def handle_disconnect():
        from flask import request
        sid = request.sid
        usuarios_conectados.pop(sid, None)
        _emit_usuarios_actualizados()

    def _emit_usuarios_actualizados():
        total = len(usuarios_conectados)
        usuarios_lista = [
            {'nombre': u['nombre'], 'pagina': u['pagina'], 'en_vivo_id': u['en_vivo_id']}
            for u in usuarios_conectados.values()
        ]
        socketio.emit('usuarios_actualizados', {
            'count': total,
            'usuarios': usuarios_lista
        })

    return app
