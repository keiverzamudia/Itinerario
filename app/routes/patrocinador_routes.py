from flask import Blueprint
from app.controllers.patrocinador_controller import PatrocinadorController
from flask_login import login_required
from app.helpers.decorators import permiso_requerido

bp = Blueprint('patrocinador', __name__, url_prefix='/patrocinadores')
controller = PatrocinadorController()

bp.route('/', methods=['GET', 'POST'])(
    login_required(permiso_requerido('patrocinador.view')(controller.dashboard))
)
bp.route('/api/obtener/<int:id>')(
    login_required(permiso_requerido('patrocinador.view')(controller.api_obtener))
)
