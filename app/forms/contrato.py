# app/forms/contrato.py

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ContratoForm(FlaskForm):
    id_patrocinador = SelectField('Patrocinador', coerce=int, validators=[DataRequired(message="Debe seleccionar un patrocinador")])
    fecha_inicio = DateField('Fecha de Inicio', format='%Y-%m-%d', validators=[DataRequired(message="Fecha de inicio obligatoria")])
    fecha_fin = DateField('Fecha de Fin', format='%Y-%m-%d', validators=[DataRequired(message="Fecha de fin obligatoria")])
    
    estatus = SelectField('Estatus del Contrato', choices=[
        ('Vigente', 'Vigente'),
        ('Vencido', 'Vencido'),
        ('Borrador', 'Borrador')
    ], validators=[DataRequired()])

    # 🌟 CAMBIO AQUÍ: Cambiamos de StringField a SelectField
    # Usamos strings ("1", "2", etc.) debido a que tu columna física en la DB es varchar(50)
    tipo = SelectField('Tipo de Contrato', choices=[
        ('1', 'Bronce'),
        ('2', 'Plata'),
        ('3', 'Oro')
    ], validators=[DataRequired(message="Debe seleccionar un tipo de contrato")])
    
    monto_total = DecimalField('Monto Total', validators=[
        DataRequired(message="El monto total del contrato es obligatorio"),
        NumberRange(min=0, message="El monto no puede ser un valor negativo")
    ])

    submit = SubmitField('Guardar Contrato')