from flask import Blueprint
from app.controllers.dashboard_controller import DashboardController
from flask_login import login_required
from app.helpers.decorators import permiso_requerido

bp = Blueprint('dashboard', __name__, url_prefix='/')
controller = DashboardController()

bp.route('/')(controller.index)
bp.route('/dashboard')(login_required(permiso_requerido('dashboard.view')(controller.panel)))
