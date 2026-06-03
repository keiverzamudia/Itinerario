from flask import Blueprint
from app.controllers.mantenimiento_controller import MantenimientoController
from flask_login import login_required
from app.helpers.decorators import permiso_requerido

bp = Blueprint('mantenimiento', __name__, url_prefix='/mantenimiento')
controller = MantenimientoController()

bp.route('/')(login_required(permiso_requerido('mantenimiento.view')(controller.dashboard)))
bp.route('/ingresar/<int:recurso_id>', methods=['GET', 'POST'])(login_required(permiso_requerido('mantenimiento.edit')(controller.ingresar)))
bp.route('/ver/<int:id>')(login_required(permiso_requerido('mantenimiento.view')(controller.ver)))
bp.route('/agregar-nota/<int:id>', methods=['POST'])(login_required(permiso_requerido('mantenimiento.edit')(controller.agregar_nota)))
bp.route('/reparar/<int:id>', methods=['POST'])(login_required(permiso_requerido('mantenimiento.edit')(controller.reparar)))
bp.route('/dar-baja/<int:id>', methods=['POST'])(login_required(permiso_requerido('mantenimiento.delete')(controller.dar_baja)))
bp.route('/finalizar/<int:id>', methods=['POST'])(login_required(permiso_requerido('mantenimiento.edit')(controller.finalizar)))
