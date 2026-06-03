# app/forms/balance_form.py

from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, StringField, DateField, TimeField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange

class PagoForm(FlaskForm):
    # Cambiar a SelectField para mostrar los contratos disponibles
    id_contrato = SelectField('Contrato', coerce=int, validators=[DataRequired()])
    monto = DecimalField('Monto a pagar', validators=[DataRequired(), NumberRange(min=0.01)], places=2)
    tipo_pago = SelectField('Tipo de Pago', choices=[
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
        ('Cheque', 'Cheque'),
        ('Depósito', 'Depósito')
    ], validators=[DataRequired()])
    referencia = StringField('Referencia', validators=[Optional()])
    fecha_pago = DateField('Fecha de Pago', validators=[DataRequired()], format='%Y-%m-%d')
    hora_pago = TimeField('Hora de Pago', validators=[DataRequired()], format='%H:%M')
    notas = TextAreaField('Notas', validators=[Optional()])
    submit = SubmitField('Registrar Pago')