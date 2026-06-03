class Reel:
    def __init__(self, id=None, nombre=None, patrocinado=None,
                 duracion_total=0.0, creado_en=None, modificado_en=None,
                 **kwargs):
        self.id = id
        self.nombre = nombre
        self.patrocinado = patrocinado
        self.duracion_total = duracion_total
        self.creado_en = creado_en
        self.modificado_en = modificado_en
        self.videos = []
        for k, v in kwargs.items():
            setattr(self, k, v)


class Video:
    def __init__(self, id=None, nombre=None, duracion_segundos=0,
                 orden=None, reel_id=None, **kwargs):
        self.id = id
        self.nombre = nombre
        self.duracion_segundos = duracion_segundos
        self.orden = orden
        self.reel_id = reel_id
        for k, v in kwargs.items():
            setattr(self, k, v)
