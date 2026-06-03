from app.repositories.patrocinador_repository import PatrocinadorRepository
from app.traits.validaciones import ValidacionesMixin


class PatrocinadorService(ValidacionesMixin):
    def __init__(self):
        self.repo = PatrocinadorRepository()

    def obtener_dashboard(self):
        return {'patrocinadores': self.repo.consultar()}

    def crear(self, nombre_empresa, rif, nombre_contacto, telefono, email):
        self.limpiar_errores()
        if not nombre_empresa or not rif:
            self.errores.append('Nombre de empresa y RIF son obligatorios')
            return None
        return self.repo.registrar({
            'nombre_empresa': nombre_empresa,
            'rif': rif,
            'nombre_contacto': nombre_contacto,
            'telefono': telefono,
            'email': email,
        })

    def editar(self, id_patrocinador, nombre_empresa, rif, nombre_contacto,
               telefono, email):
        self.limpiar_errores()
        existente = self.repo.obtener_por_id(id_patrocinador)
        if not existente:
            self.errores.append('Patrocinador no encontrado')
            return False
        self.repo.modificar(id_patrocinador, {
            'nombre_empresa': nombre_empresa,
            'rif': rif,
            'nombre_contacto': nombre_contacto,
            'telefono': telefono,
            'email': email,
        })
        return True

    def eliminar(self, id_patrocinador):
        self.limpiar_errores()
        resultado = self.repo.eliminar(id_patrocinador)
        if not resultado:
            self.errores.append('Patrocinador no encontrado')
            return None
        return resultado

    def obtener_api(self, id_patrocinador):
        p = self.repo.obtener_por_id(id_patrocinador)
        if p:
            return {
                'id_patrocinador': p.id_patrocinador,
                'nombre_empresa': p.nombre_empresa,
                'rif': p.rif,
                'nombre_contacto': p.nombre_contacto,
                'telefono': p.telefono,
                'email': p.email,
            }
        return None
