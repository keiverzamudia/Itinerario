from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.rol_repository import RolRepository
from app.forms.usuario_form import UsuarioForm, EditarUsuarioForm, CambiarPasswordForm
from app.helpers.decorators import permiso_requerido
from app.helpers.bitacora_helper import registrar_actividad


class UsuarioController:
    def __init__(self):
        self.repo = UsuarioRepository()

    def dashboard(self):
        usuarios = self.repo.consultar()
        form = UsuarioForm()
        roles = RolRepository().consultar()
        form.rol.choices = [(r.nombre, r.nombre) for r in roles]
        return render_template('usuario/dashboard.html',
                               usuarios=usuarios, form=form, roles=roles)

    def crear(self):
        form = UsuarioForm()
        roles = RolRepository().consultar()
        form.rol.choices = [(r.nombre, r.nombre) for r in roles]
        if form.validate_on_submit():
            usuario_data = {
                'nombre': form.nombre.data,
                'email': form.email.data,
                'cedula': form.cedula.data,
                'rol': form.rol.data,
                'departamento': form.departamento.data,
                'telefono': form.telefono.data,
                'password_hash': generate_password_hash(form.password.data),
            }
            usuario = self.repo.registrar(usuario_data)
            if not usuario:
                flash('Error al crear el usuario. Intenta de nuevo.', 'danger')
                return redirect(url_for('usuario.dashboard'))
            registrar_actividad('create', 'usuarios', 'Crear usuario',
                                f'Usuario "{usuario.nombre}" ({usuario.email}) creado')
            flash('Usuario creado exitosamente', 'success')
            return redirect(url_for('usuario.dashboard'))
        for field, errors in form.errors.items():
            for error in errors:
                try:
                    label = form[field].label.text
                    flash(f'{label}: {error}', 'danger')
                except (AttributeError, KeyError):
                    flash(error, 'danger')
        return redirect(url_for('usuario.dashboard'))

    def cambiar_contrasena(self):
        from werkzeug.security import generate_password_hash
        from app.forms.usuario_form import CambiarPasswordForm
        form = CambiarPasswordForm()
        if form.validate_on_submit():
            if not current_user.check_password(form.password_actual.data):
                flash('Contraseña actual incorrecta', 'danger')
                return redirect(url_for('usuario.cambiar_contrasena'))
            self.repo.modificar(current_user.id, {
                'password_hash': generate_password_hash(form.password_nueva.data)
            })
            registrar_actividad('update', 'usuarios', 'Cambiar contraseña',
                                f'Usuario #{current_user.id} cambió su contraseña')
            flash('Contraseña actualizada. Por favor inicia sesión nuevamente.', 'success')
            return redirect(url_for('auth.login'))
        return render_template('usuario/cambiar_password.html', form=form)

    def perfil(self):
        return render_template('usuario/perfil.html', usuario=current_user)

    def ver(self, id):
        usuario = self.repo.obtener_por_id(id)
        if not usuario:
            flash('Usuario no encontrado', 'danger')
            return redirect(url_for('usuario.dashboard'))
        return render_template('usuario/ver.html', usuario=usuario)

    def editar(self, id):
        usuario = self.repo.obtener_por_id(id)
        if not usuario:
            flash('Usuario no encontrado', 'danger')
            return redirect(url_for('usuario.dashboard'))
        if not current_user.is_admin() and current_user.id != id:
            flash('No tienes permiso para editar este usuario', 'danger')
            return redirect(url_for('usuario.dashboard'))
        form = EditarUsuarioForm()
        roles = RolRepository().consultar()
        form.rol.choices = [(r.nombre, r.nombre) for r in roles]
        if request.method == 'GET':
            form.nombre.data = usuario.nombre
            form.email.data = usuario.email
            form.cedula.data = usuario.cedula
            form.rol.data = usuario.rol
            form.departamento.data = usuario.departamento
            form.telefono.data = usuario.telefono
            form.activo.data = usuario.activo
        if form.validate_on_submit():
            datos = {
                'nombre': form.nombre.data,
                'email': form.email.data,
                'cedula': form.cedula.data,
                'rol': form.rol.data,
                'departamento': form.departamento.data,
                'telefono': form.telefono.data,
                'activo': form.activo.data,
            }
            if form.password.data:
                datos['password_hash'] = generate_password_hash(form.password.data)
            self.repo.modificar(id, datos)
            registrar_actividad('update', 'usuarios', 'Editar usuario',
                                f'Usuario #{id} editado')
            flash('Usuario actualizado', 'success')
            return redirect(url_for('usuario.dashboard'))
        return render_template('usuario/editar.html', form=form, usuario=usuario)

    def eliminar(self, id):
        if not current_user.is_admin():
            flash('No tienes permiso para eliminar usuarios', 'danger')
            return redirect(url_for('usuario.dashboard'))
        usuario = self.repo.obtener_por_id(id)
        if not usuario:
            flash('Usuario no encontrado', 'danger')
            return redirect(url_for('usuario.dashboard'))
        if usuario.id == current_user.id:
            flash('No puedes eliminar tu propio usuario', 'danger')
            return redirect(url_for('usuario.dashboard'))
        self.repo.eliminar(id)
        registrar_actividad('delete', 'usuarios', 'Eliminar usuario',
                            f'Usuario "{usuario.nombre}" ({usuario.email}) eliminado')
        flash('Usuario eliminado', 'warning')
        return redirect(url_for('usuario.dashboard'))

    def api_obtener(self, id):
        usuario = self.repo.obtener_por_id(id)
        if not usuario:
            return jsonify({'error': 'No encontrado'}), 404
        return jsonify({
            'id': usuario.id,
            'nombre': usuario.nombre,
            'cedula': usuario.cedula,
            'telefono': usuario.telefono,
            'email': usuario.email,
            'departamento': usuario.departamento,
            'rol': usuario.rol,
            'activo': usuario.activo,
        })
