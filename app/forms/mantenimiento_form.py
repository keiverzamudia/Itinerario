# app/forms/mantenimiento_form.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional

class IngresarMantenimientoForm(FlaskForm):
    """Formulario para ingresar un recurso a mantenimiento"""
    fecha_ingreso = DateField('Fecha de Ingreso',
                             validators=[DataRequired(message='La fecha es obligatoria')],
                             format='%Y-%m-%d')
    diagnostico = TextAreaField('Diagnóstico Inicial',
                               validators=[DataRequired(message='El diagnóstico es obligatorio'),
                                          Length(min=5, max=1000)])
    observaciones = TextAreaField('Observaciones',
                                 validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Ingresar a Mantenimiento')


class NotaMantenimientoForm(FlaskForm):
    """Formulario para agregar nota al historial"""
    descripcion = TextAreaField('Nota / Descripción',
                               validators=[DataRequired(message='La nota es obligatoria'),
                                          Length(min=3, max=1000)])
    submit = SubmitField('Agregar Nota')
