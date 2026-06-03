from flask import Blueprint
from app.controllers.usuario_controller import UsuarioController
from app.helpers.decorators import permiso_requerido
from flask_login import login_required

bp = Blueprint('usuario', __name__, url_prefix='/usuarios')
controller = UsuarioController()

bp.route('/')(login_required(permiso_requerido('usuario.view')(controller.dashboard)))
bp.route('/crear', methods=['GET', 'POST'])(login_required(permiso_requerido('usuario.create')(controller.crear)))
bp.route('/cambiar-contrasena', methods=['GET', 'POST'])(login_required(permiso_requerido('usuario.perfil')(controller.cambiar_contrasena)))
bp.route('/perfil')(login_required(permiso_requerido('usuario.perfil')(controller.perfil)))
bp.route('/ver/<int:id>')(login_required(permiso_requerido('usuario.view')(controller.ver)))
bp.route('/editar/<int:id>', methods=['GET', 'POST'])(login_required(permiso_requerido('usuario.edit')(controller.editar)))
bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])(login_required(permiso_requerido('usuario.delete')(controller.eliminar)))
bp.route('/api/obtener/<int:id>')(login_required(permiso_requerido('usuario.view')(controller.api_obtener)))
