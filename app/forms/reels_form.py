from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError
import json

class ReelForm(FlaskForm):
    """Formulario de Backend para validar la creación y edición de Reels."""
    
    nombre = StringField(
        'Nombre del Reel', 
        validators=[DataRequired(message="El nombre del reel es obligatorio")]
    )
    
    patrocinante = StringField(
        'Patrocinante', 
        validators=[Optional()]
    )
    
    duracion_total = DecimalField(
        'Duración Total', 
        places=2, 
        validators=[DataRequired(message="La duración total es obligatoria")]
    )
    
    # Campo oculto indispensable para capturar el JSON dinámico generado por JS en el HTML
    videos_json = HiddenField(
        'Videos JSON', 
        validators=[DataRequired(message="Debe agregar al menos un video")]
    )
    
    submit = SubmitField('Guardar Reel')

   
    def validate_videos_json(self, field):
        try:
            videos = json.loads(field.data)
            if not isinstance(videos, list) or len(videos) == 0:
                raise ValidationError('Debe agregar al menos un video a la lista.')
        except (ValueError, TypeError, json.JSONDecodeError):
            raise ValidationError('El formato de la lista de videos es inválido.')