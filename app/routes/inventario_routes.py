from flask import Blueprint
from app.controllers.inventario_controller import InventarioController
from flask_login import login_required
from app.helpers.decorators import permiso_requerido

bp = Blueprint('inventario', __name__, url_prefix='/inventario')
controller = InventarioController()

bp.route('/')(login_required(permiso_requerido('inventario.view')(controller.dashboard)))
bp.route('/crear', methods=['GET', 'POST'])(login_required(permiso_requerido('inventario.create')(controller.crear)))
bp.route('/ver/<int:id>')(login_required(permiso_requerido('inventario.view')(controller.ver)))
bp.route('/editar/<int:id>', methods=['GET', 'POST'])(login_required(permiso_requerido('inventario.edit')(controller.editar)))
bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])(login_required(permiso_requerido('inventario.delete')(controller.eliminar)))
bp.route('/asignar/<int:recurso_id>', methods=['GET', 'POST'])(login_required(permiso_requerido('inventario.assign')(controller.asignar)))
bp.route('/gestion-asignaciones')(login_required(permiso_requerido('inventario.assign')(controller.gestion_asignaciones)))
bp.route('/asignar_desde_gestion', methods=['POST'])(login_required(permiso_requerido('inventario.assign')(controller.asignar_desde_gestion)))
bp.route('/devolver/<int:asignacion_id>', methods=['POST'])(login_required(permiso_requerido('inventario.assign')(controller.devolver_recurso)))
bp.route('/api/tipos')(login_required(permiso_requerido('inventario.view')(controller.api_tipos)))
bp.route('/api/tipos/crear', methods=['POST'])(login_required(permiso_requerido('inventario.create')(controller.api_crear_tipo)))
bp.route('/api/tipos/editar/<int:id>', methods=['POST'])(login_required(permiso_requerido('inventario.edit')(controller.api_editar_tipo)))
bp.route('/api/tipos/eliminar/<int:id>', methods=['POST'])(login_required(permiso_requerido('inventario.delete')(controller.api_eliminar_tipo)))
