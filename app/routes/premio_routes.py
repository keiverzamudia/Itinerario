from flask import Blueprint
from app.controllers.premio_controller import PremioController
from flask_login import login_required
from app.helpers.decorators import permiso_requerido

bp = Blueprint('premio', __name__, url_prefix='/premios')
controller = PremioController()

bp.route('/', methods=['GET', 'POST'])(login_required(permiso_requerido('premio.view')(controller.dashboard)))
bp.route('/eliminar/<int:id>')(login_required(permiso_requerido('premio.delete')(controller.eliminar)))
bp.route('/api/obtener/<int:id>')(login_required(permiso_requerido('premio.view')(controller.api_obtener)))
