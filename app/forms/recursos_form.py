from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Optional

class RecursoForm(FlaskForm):
    """Formulario para la creación y edición de recursos."""
    nombre = StringField(
        'Nombre del recurso', 
        validators=[DataRequired(message="El nombre del recurso es obligatorio")]
    )
    
    descripcion = TextAreaField(
        'Descripción', 
        validators=[Optional()]
    )
    
    tipo_id = SelectField(
        'Tipo de Recurso', 
        coerce=int, 
        validators=[DataRequired(message="Debe seleccionar un tipo de recurso")]
    )
    
    fecha_compra = DateField(
        'Fecha de compra', 
        format='%Y-%m-%d', 
        validators=[Optional()]
    )
    
    costo = DecimalField(
        'Costo (€)', 
        places=2, 
        validators=[Optional()]
    )
    
    submit = SubmitField('Guardar Recurso')


class AsignacionForm(FlaskForm):
    """Formulario para gestionar las asignaciones de recursos a usuarios."""
    
   
    recurso_id = SelectField(
        'Recurso a asignar',
        coerce=int,
        validators=[Optional()]
    )
    
    usuario_id = SelectField(
        'Usuario', 
        coerce=int, 
        validators=[DataRequired(message="Debe seleccionar un usuario")]
    )
    
    fecha_devolucion_esperada = DateField(
        'Fecha de devolución esperada', 
        format='%Y-%m-%d', 
        validators=[Optional()]
    )
    
    notas = TextAreaField(
        'Notas / Observaciones', 
        validators=[Optional()]
    )
    
    submit = SubmitField('Asignar Recurso')