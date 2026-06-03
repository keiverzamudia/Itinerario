from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, ValidationError
from app.repositories.usuario_repository import UsuarioRepository


class UsuarioForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])

    cedula = StringField('Cédula', validators=[DataRequired(), Length(min=5, max=20)])
    rol = SelectField('Rol', choices=[
        ('Usuario', 'Usuario'),
        ('Administrador', 'Administrador'),
        ('Superadmin', 'Superadmin')
    ], validators=[DataRequired()])
    departamento = SelectField('Departamento', choices=[
        ('Medios', 'Medios'),
        ('Palco de Operaciones', 'Palco de Operaciones')
    ], validators=[DataRequired()])

    telefono = StringField('Teléfono', validators=[Length(max=20)])
    activo = BooleanField('Activo', default=True)

    submit = SubmitField('Guardar Usuario')

    def validate_cedula(self, field):
        repo = UsuarioRepository()
        usuarios = repo.consultar()
        for u in usuarios:
            if u.cedula == field.data:
                raise ValidationError('Esta cédula ya está registrada')

    def validate_email(self, field):
        repo = UsuarioRepository()
        usuarios = repo.consultar()
        for u in usuarios:
            if u.email == field.data:
                raise ValidationError('Este email ya está registrado')


class EditarUsuarioForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    cedula = StringField('Cédula', validators=[DataRequired(), Length(min=5, max=20)])
    rol = SelectField('Rol', choices=[
        ('Usuario', 'Usuario'),
        ('Administrador', 'Administrador'),
        ('Superadmin', 'Superadmin')
    ], validators=[DataRequired()])
    departamento = SelectField('Departamento', choices=[
        ('Medios', 'Medios'),
        ('Palco de Operaciones', 'Palco de Operaciones')
    ], validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[Length(max=20)])
    activo = BooleanField('Activo', default=True)
    password = PasswordField('Nueva Contraseña', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[Optional(), EqualTo('password')])
    submit = SubmitField('Actualizar Usuario')


class CambiarPasswordForm(FlaskForm):
    password_actual = PasswordField('Contraseña Actual', validators=[DataRequired()])
    password_nueva = PasswordField('Nueva Contraseña', validators=[DataRequired(), Length(min=6)])
    confirmar_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password_nueva')])
    submit = SubmitField('Cambiar Contraseña')
