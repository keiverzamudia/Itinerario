from flask import Blueprint
from app.controllers.contrato_controller import ContratoController
from flask_login import login_required
from app.helpers.decorators import permiso_requerido

bp = Blueprint('contrato', __name__, url_prefix='/contratos')
controller = ContratoController()

bp.route('/', methods=['GET', 'POST'])(
    login_required(permiso_requerido('contrato.view')(controller.dashboard))
)
bp.route('/api/obtener/<int:id>')(
    login_required(permiso_requerido('contrato.view')(controller.api_obtener))
)
