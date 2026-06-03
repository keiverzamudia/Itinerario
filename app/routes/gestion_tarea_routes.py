from flask import Blueprint
from app.controllers.gestion_tarea_controller import GestionTareaController
from flask_login import login_required
from app.helpers.decorators import permiso_requerido

bp = Blueprint('gestion_tarea', __name__, url_prefix='/gestion-tareas')
controller = GestionTareaController()

bp.route('/', methods=['GET', 'POST'])(
    login_required(permiso_requerido('gestion_tarea.view')(controller.dashboard))
)
bp.route('/mis-tareas')(
    login_required(permiso_requerido('gestion_tarea.view')(controller.tareas_usuario))
)
bp.route('/completar', methods=['POST'])(
    login_required(permiso_requerido('gestion_tarea.complete')(controller.completar_tarea))
)
