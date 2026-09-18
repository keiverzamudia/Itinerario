from flask import Blueprint, render_template
from flask_login import current_user
from app.model.ayuda_model import obtener_preguntas_frecuentes

bp = Blueprint('ayuda', __name__, url_prefix='/ayuda')


@bp.route('/', methods=['GET'])
def dashboard():
    if not current_user.is_authenticated:
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))

    categorias = obtener_preguntas_frecuentes()
    total_preguntas = sum(len(c['preguntas']) for c in categorias)

    return render_template('ayuda/dashboard.html',
                           categorias=categorias,
                           total_preguntas=total_preguntas)