from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, InputRequired


class TareaForm(FlaskForm):
    Nombre_Tarea = StringField('Nombre de la Tarea', validators=[DataRequired(), Length(min=2, max=100)])
    Instruccion = TextAreaField('Instrucción', validators=[DataRequired(), Length(min=5)])
    id_usuario = SelectField('Asignar a', coerce=int, validators=[InputRequired()])
    submit = SubmitField('Guardar Tarea')


class EditarTareaForm(FlaskForm):
    id_tarea = HiddenField('ID de la Tarea', validators=[DataRequired()])
    Nombre_Tarea = StringField('Nombre de la Tarea', validators=[DataRequired(), Length(min=2, max=100)])
    Instruccion = TextAreaField('Instrucción', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Actualizar Tarea')


class EliminarTareaForm(FlaskForm):
    id_tarea = HiddenField('ID de la Tarea', validators=[DataRequired()])
    submit = SubmitField('Eliminar Tarea')
