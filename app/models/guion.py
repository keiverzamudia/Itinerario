class Guion:
    def __init__(self, id=None, nombre=None, estado='borrador',
                 creado_en=None, modificado_en=None, tiempo_inning=None,
                 **kwargs):
        self.id = id
        self.nombre = nombre
        self.estado = estado
        self.creado_en = creado_en
        self.modificado_en = modificado_en
        self.tiempo_inning = tiempo_inning
        self.fechas = []
        self.elementos = []
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'estado': self.estado,
            'fechas': [str(f.fecha) for f in self.fechas],
            'elementos': [e.to_dict() for e in self.elementos],
        }


class GuionFecha:
    def __init__(self, id=None, guion_id=None, fecha=None, **kwargs):
        self.id = id
        self.guion_id = guion_id
        self.fecha = fecha
        for k, v in kwargs.items():
            setattr(self, k, v)


from datetime import time, timedelta, datetime


class ElementoGuion:
    def __init__(self, id=None, guion_id=None, fecha_id=None,
                 tipo='pregame', hora=None, inning=None,
                 medio_inning=None, contenido=None,
                 duracion_estimada=0, encargado=None, orden=0,
                 creado_en=None, estado='pendiente', **kwargs):
        self.id = id
        self.guion_id = guion_id
        self.fecha_id = fecha_id
        self.tipo = tipo
        if isinstance(hora, timedelta):
            hora = (datetime.min + hora).time()
        self.hora = hora
        self.inning = inning
        self.medio_inning = medio_inning
        self.contenido = contenido
        self.duracion_estimada = duracion_estimada
        self.encargado = encargado
        self.orden = orden
        self.creado_en = creado_en
        self.estado = estado
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'hora': str(self.hora) if self.hora else None,
            'inning': self.inning,
            'medio_inning': self.medio_inning,
            'contenido': self.contenido,
            'duracion_estimada': self.duracion_estimada,
            'encargado': self.encargado,
            'orden': self.orden,
        }
