from flask import Blueprint
from app.controllers.bitacora_controller import BitacoraController
from flask_login import login_required
from app.helpers.decorators import permiso_requerido

bp = Blueprint('bitacora', __name__, url_prefix='/bitacora')
controller = BitacoraController()

bp.route('/')(login_required(permiso_requerido('rol.view')(controller.dashboard)))
bp.route('/usuario/<int:usuario_id>')(login_required(permiso_requerido('rol.view')(controller.reporte_usuario)))
