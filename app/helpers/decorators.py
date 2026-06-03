# app/helpers/decorators.py
# Decoradores reutilizables para permisos

from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def permiso_requerido(codigo):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('auth.login'))
            if not current_user.tiene_permiso(codigo):
                flash('No tienes permiso para acceder a esta página', 'danger')
                return redirect(url_for('dashboard.panel'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
