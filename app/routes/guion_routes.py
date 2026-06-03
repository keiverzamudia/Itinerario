from flask import Blueprint
from app.controllers.guion_controller import GuionController
from flask_login import login_required
from app.helpers.decorators import permiso_requerido

bp = Blueprint('guion', __name__, url_prefix='/guiones')
controller = GuionController()

bp.route('/')(login_required(permiso_requerido('guion.view')(controller.dashboard)))
bp.route('/crear', methods=['GET', 'POST'])(login_required(permiso_requerido('guion.create')(controller.crear)))
bp.route('/agregar-elemento/<int:id>', methods=['GET', 'POST'])(login_required(permiso_requerido('guion.edit')(controller.agregar_elementos)))
bp.route('/editar-elemento/<int:guion_id>/<int:elemento_id>', methods=['GET', 'POST'])(login_required(permiso_requerido('guion.edit')(controller.editar_elemento)))
bp.route('/eliminar-elemento/<int:guion_id>/<int:elemento_id>')(login_required(permiso_requerido('guion.edit')(controller.eliminar_elemento)))
bp.route('/editar/<int:id>', methods=['GET', 'POST'])(login_required(permiso_requerido('guion.edit')(controller.editar)))
bp.route('/previsualizar/<int:id>')(login_required(permiso_requerido('guion.preview')(controller.previsualizar)))
bp.route('/publicar/<int:id>', methods=['GET', 'POST'])(login_required(permiso_requerido('guion.publish')(controller.publicar)))
bp.route('/eliminar/<int:id>')(login_required(permiso_requerido('guion.delete')(controller.eliminar)))
bp.route('/api/horas-usadas/<int:guion_id>')(login_required(permiso_requerido('guion.view')(controller.api_horas_usadas)))
