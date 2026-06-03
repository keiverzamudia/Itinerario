# app/forms/rol_form.py

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class PermisosForm(FlaskForm):
    submit = SubmitField('Guardar Permisos')


class CrearRolForm(FlaskForm):
    nombre = StringField('Nombre del Rol', validators=[DataRequired(), Length(min=3, max=50)])
    descripcion = TextAreaField('Descripción', validators=[Length(max=200)])
    submit = SubmitField('Crear Rol')
