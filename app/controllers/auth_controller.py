from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.repositories.usuario_repository import UsuarioRepository
from app.forms.auth_form import LoginForm
from app.helpers.bitacora_helper import iniciar_sesion, finalizar_sesion, registrar_actividad


class AuthController:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()

    def login(self):
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.panel'))
        form = LoginForm()
        if form.validate_on_submit():
            usuario = self.usuario_repo.obtener_por_email(form.email.data)
            if usuario and usuario.check_password(form.password.data):
                if not usuario.activo:
                    flash('Cuenta desactivada. Contacte al administrador.', 'danger')
                    return redirect(url_for('auth.login'))
                login_user(usuario, remember=form.remember.data)
                self.usuario_repo.actualizar_ultimo_acceso(usuario.id)
                sesion = iniciar_sesion()
                if sesion:
                    session['bitacora_sesion_id'] = sesion.id
                flash(f'¡Bienvenido {usuario.nombre}!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('dashboard.panel'))
            else:
                flash('Email o contraseña incorrectos', 'danger')
        return render_template('auth/login.html', form=form)

    def logout(self):
        sesion_id = session.pop('bitacora_sesion_id', None)
        if sesion_id:
            finalizar_sesion(sesion_id)
        registrar_actividad('logout', 'auth', 'Cierre de sesión',
                            f'Usuario {current_user.email} cerró sesión')
        logout_user()
        flash('Sesión cerrada correctamente', 'info')
        return redirect(url_for('auth.login'))
