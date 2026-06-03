

# from flask_wtf import FlaskForm
# from wtforms import StringField, TextAreaField, SelectField, SubmitField
# from wtforms.validators import DataRequired, Length

# class PremioForm(FlaskForm):
#     nombre = StringField('Nombre del Premio', validators=[DataRequired(), Length(min=3, max=100)])
#     patrocinador_id = SelectField('Patrocinador', coerce=int, validators=[DataRequired()])
#     descripcion = TextAreaField('Descripción', validators=[Length(max=500)])
#     submit = SubmitField('Guardar Premio')


# app/forms/premio_form.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SelectField, SubmitField, DateTimeField, TimeField
from wtforms.validators import DataRequired, Length, Optional

class PremioForm(FlaskForm):
    nombre = StringField('Nombre del Premio', validators=[DataRequired(), Length(min=3, max=100)])
    patrocinador_id = SelectField('Patrocinador', coerce=int, validators=[Optional()])
    descripcion = TextAreaField('Descripción', validators=[Length(max=500)])
    fecha_creacion = DateTimeField('Fecha y Hora', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    foto = FileField('Foto del Premio', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Solo imágenes')])
    submit = SubmitField('Guardar Premio')


