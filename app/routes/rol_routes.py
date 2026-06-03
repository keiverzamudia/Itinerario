from flask import Blueprint
from app.controllers.rol_controller import RolController
from flask_login import login_required
from app.helpers.decorators import permiso_requerido

bp = Blueprint('rol', __name__, url_prefix='/roles')
controller = RolController()

bp.route('/')(login_required(permiso_requerido('rol.view')(controller.dashboard)))
bp.route('/editar/<int:id>', methods=['GET', 'POST'])(login_required(permiso_requerido('rol.edit')(controller.editar)))
bp.route('/editar-rol/<int:id>', methods=['GET', 'POST'])(login_required(permiso_requerido('rol.edit')(controller.editar_rol)))
bp.route('/crear', methods=['GET', 'POST'])(login_required(permiso_requerido('rol.edit')(controller.crear)))
