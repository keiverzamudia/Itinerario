from flask import Blueprint
from app.controllers.auth_controller import AuthController

bp = Blueprint('auth', __name__, url_prefix='/auth')
controller = AuthController()

bp.route('/login', methods=['GET', 'POST'])(controller.login)
bp.route('/logout')(controller.logout)
