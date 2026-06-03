from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class PatrocinadorForm(FlaskForm):
    nombre_empresa = StringField('Nombre de la Empresa', validators=[
        DataRequired(message="El nombre de la empresa es obligatorio"),
        Length(max=100, message="El nombre no puede exceder los 100 caracteres") 
    ])
    
    rif = StringField('Cédula o RIF', validators=[
        DataRequired(message="El RIF o Cédula es obligatorio"),
        Length(max=20, message="El RIF no puede exceder los 20 caracteres")
    ])
    
    
    nombre_contacto = TextAreaField('Nombre del Contacto', validators=[
        DataRequired(message="El nombre de contacto es obligatorio")
    ])
    
    telefono = StringField('Teléfono de Contacto', validators=[
        DataRequired(message="El teléfono es obligatorio"),
        Length(max=20, message="El teléfono no puede exceder los 20 caracteres")
    ])
    
    email = StringField('Correo Electrónico', validators=[
        DataRequired(message="El correo electrónico es obligatorio"),
        Email(message="Ingrese un formato de correo válido"),
        Length(max=100, message="El correo no puede exceder los 100 caracteres")
    ])
    
    submit = SubmitField('Guardar Patrocinador')