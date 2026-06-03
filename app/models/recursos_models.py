en# app/models/recurso_model.py
from app import db
from datetime import datetime

class TipoRecurso(db.Model):
    __tablename__ = 'tipo_recurso'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))

    def __repr__(self):
        return f'<TipoRecurso {self.nombre}>'


class EstadoRecurso(db.Model):
    __tablename__ = 'estado_recurso'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))

    def __repr__(self):
        return f'<EstadoRecurso {self.nombre}>'


class EstadoAsignacion(db.Model):
    __tablename__ = 'estado_asignacion'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))

    def __repr__(self):
        return f'<EstadoAsignacion {self.nombre}>'


class Recurso(db.Model):
    __tablename__ = 'recursos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo_recurso.id'), nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estado_recurso.id'), nullable=False, default=1)
    fecha_compra = db.Column(db.Date)
    costo = db.Column(db.Numeric(10,2))
    eliminado = db.Column(db.Boolean, default=False, nullable=False)

    # Relaciones
    tipo = db.relationship('TipoRecurso', backref='recursos')
    estado = db.relationship('EstadoRecurso', backref='recursos')

    def __repr__(self):
        return f'<Recurso {self.nombre}>'


class AsignacionRecurso(db.Model):
    __tablename__ = 'asignaciones_recursos'
    id = db.Column(db.Integer, primary_key=True)
    recurso_id = db.Column(db.Integer, db.ForeignKey('recursos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_asignacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_devolucion_esperada = db.Column(db.Date)
    fecha_devolucion_real = db.Column(db.DateTime)
    estado_asignacion_id = db.Column(db.Integer, db.ForeignKey('estado_asignacion.id'), default=1)
    notas = db.Column(db.Text)

    # Relaciones
    recurso = db.relationship('Recurso', backref='asignaciones')
    # Asumiendo que existe modelo Usuario
    usuario = db.relationship('Usuario', backref='asignaciones_recursos')
    estado_asignacion = db.relationship('EstadoAsignacion', backref='asignaciones')

    def __repr__(self):
        return f'<AsignacionRecurso {self.id} - Recurso {self.recurso_id}>'