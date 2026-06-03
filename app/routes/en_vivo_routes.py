from flask import Blueprint
from app.controllers.en_vivo_controller import EnVivoController
from flask_login import login_required
from app.helpers.decorators import permiso_requerido

bp = Blueprint('en_vivo', __name__, url_prefix='/en-vivo')
controller = EnVivoController()

bp.route('/')(login_required(permiso_requerido('envivo.view')(controller.index)))
bp.route('/<int:guion_id>')(login_required(permiso_requerido('envivo.view')(controller.ver)))
bp.route('/iniciar/<int:guion_id>')(login_required(permiso_requerido('envivo.control')(controller.iniciar)))
bp.route('/finalizar/<int:guion_id>')(login_required(permiso_requerido('envivo.control')(controller.finalizar)))
bp.route('/api/sincronizar/<int:guion_id>', methods=['POST'])(login_required(permiso_requerido('envivo.control')(controller.sincronizar)))
bp.route('/api/guiones-por-fecha', methods=['POST'])(login_required(permiso_requerido('envivo.view')(controller.guiones_por_fecha)))
