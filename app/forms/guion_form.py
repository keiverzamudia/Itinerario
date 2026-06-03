# app/forms/guion_form.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, TimeField, IntegerField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length, Optional

class GuionForm(FlaskForm):
    """Formulario para crear/editar guion (nombre y fechas)"""
    
    nombre = StringField('Nombre del Guión', 
                        validators=[DataRequired(message='El nombre es obligatorio'),
                                   Length(min=3, max=200)])
    
    fechas = HiddenField('Fechas seleccionadas')
    
    tiempo_inning = StringField('Tiempo estándar por inning',
                                validators=[Optional()],
                                render_kw={'placeholder': 'ej: 2,30'})
    
    submit = SubmitField('Continuar')


class ElementoGuionForm(FlaskForm):
    """Formulario para agregar elementos al guion"""
    
    tipo = SelectField('Tipo de Elemento', choices=[
        ('pregame', 'Pre-Game (por hora)'),
        ('game', 'Game (por inning)')
    ], validators=[DataRequired()])
    
    hora = TimeField('Hora del Evento', 
                    validators=[Optional()],
                    format='%H:%M')
    
    inning = SelectField('Inning', choices=[
        ('', '--'),
        ('1', '1ro'), ('2', '2do'), ('3', '3ro'), ('4', '4to'),
        ('5', '5to'), ('6', '6to'), ('7', '7mo'), ('8', '8vo'), ('9', '9no')
    ], validators=[Optional()])
    
    medio_inning = SelectField('Medio Inning', choices=[
        ('', '--'),
        ('alta', 'Alta'),
        ('baja', 'Baja')
    ], validators=[Optional()])
    
    contenido = TextAreaField('¿Qué va a suceder?', 
                             validators=[DataRequired(message='El contenido es obligatorio'),
                                        Length(min=3, max=500)])
    
    duracion_estimada = StringField('Tiempo estimado',
                                    validators=[DataRequired(message='La duración es obligatoria')],
                                    render_kw={'placeholder': 'ej: 2,30'})
    
    encargado = SelectField('¿Quién es el encargado?', 
                           validators=[DataRequired(message='El encargado es obligatorio')],
                           choices=[])
    
    fecha_id = HiddenField('ID de la fecha seleccionada')
    
    submit = SubmitField('Agregar Elemento')
    submit_final = SubmitField('Finalizar Guión')


class PublicarGuionForm(FlaskForm):
    """Formulario para publicar guión"""
    submit = SubmitField('Publicar Guión')
