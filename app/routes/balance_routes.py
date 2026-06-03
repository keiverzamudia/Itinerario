from flask import Blueprint
from app.controllers.balance_controller import BalanceController
from flask_login import login_required
from app.helpers.decorators import permiso_requerido

bp = Blueprint('balance', __name__, url_prefix='/balance')
controller = BalanceController()

bp.route('/')(
    login_required(permiso_requerido('balance.view')(controller.dashboard))
)
bp.route('/registrar-pago', methods=['POST'])(
    login_required(permiso_requerido('balance.create')(controller.registrar_pago))
)
bp.route('/editar-pago', methods=['POST'])(
    login_required(permiso_requerido('balance.edit')(controller.editar_pago))
)
bp.route('/eliminar-pago/<int:pago_id>', methods=['POST'])(
    login_required(permiso_requerido('balance.delete')(controller.eliminar_pago))
)
bp.route('/api/contrato/<int:id_contrato>')(
    login_required(permiso_requerido('balance.view')(controller.api_contrato))
)
bp.route('/api/pago/<int:id_pago>')(
    login_required(permiso_requerido('balance.view')(controller.api_pago))
)
bp.route('/contrato/<int:contrato_id>/pdf')(
    login_required(permiso_requerido('balance.view')(controller.generar_pdf_contrato))
)
