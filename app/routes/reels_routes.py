from flask import Blueprint
from app.controllers.reels_controller import ReelsController
from flask_login import login_required
from app.helpers.decorators import permiso_requerido

bp = Blueprint('reels', __name__, url_prefix='/reels')
controller = ReelsController()

bp.route('/')(login_required(permiso_requerido('reels.view')(controller.dashboard)))
bp.route('/crear', methods=['GET', 'POST'])(login_required(permiso_requerido('reels.create')(controller.crear)))
bp.route('/ver/<int:id>')(login_required(permiso_requerido('reels.view')(controller.ver)))
bp.route('/editar/<int:id>', methods=['GET', 'POST'])(login_required(permiso_requerido('reels.edit')(controller.editar)))
bp.route('/eliminar/<int:id>', methods=['POST'])(login_required(permiso_requerido('reels.delete')(controller.eliminar)))
bp.route('/<int:reel_id>/agregar-video', methods=['POST'])(login_required(permiso_requerido('reels.edit')(controller.agregar_video)))
bp.route('/<int:reel_id>/eliminar-video/<int:video_id>', methods=['POST'])(login_required(permiso_requerido('reels.edit')(controller.eliminar_video)))
