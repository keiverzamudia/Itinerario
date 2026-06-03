from app.repositories.contrato_repository import ContratoRepository
from app.repositories.patrocinador_repository import PatrocinadorRepository
from app.traits.validaciones import ValidacionesMixin


class ContratoService(ValidacionesMixin):
    def __init__(self):
        self.repo = ContratoRepository()
        self.patrocinador_repo = PatrocinadorRepository()

    def obtener_dashboard(self):
        contratos = self.repo.consultar()
        patrocinadores = self.patrocinador_repo.consultar()
        return {
            'contratos': contratos,
            'patrocinadores': patrocinadores,
        }

    def obtener_patrocinadores(self):
        return self.patrocinador_repo.consultar()

    def crear(self, id_patrocinador, fecha_inicio, fecha_fin, estatus,
              tipo, monto_total):
        self.limpiar_errores()
        if not id_patrocinador or not fecha_inicio or not fecha_fin:
            self.errores.append('Todos los campos obligatorios deben estar llenos')
            return False
        if fecha_fin < fecha_inicio:
            self.errores.append('La fecha de fin no puede ser anterior a la fecha de inicio')
            return False
        self.repo.registrar({
            'id_patrocinador': id_patrocinador,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'estatus': estatus,
            'tipo': tipo,
            'monto_total': monto_total,
        })
        return True

    def editar(self, id_contrato, id_patrocinador, fecha_inicio, fecha_fin,
               estatus, tipo, monto_total):
        self.limpiar_errores()
        existente = self.repo.obtener_por_id(id_contrato)
        if not existente:
            self.errores.append('Contrato no encontrado')
            return False
        if fecha_fin < fecha_inicio:
            self.errores.append('La fecha de fin no puede ser anterior a la fecha de inicio')
            return False
        self.repo.modificar(id_contrato, {
            'id_patrocinador': id_patrocinador,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'estatus': estatus,
            'tipo': tipo,
            'monto_total': monto_total,
        })
        return True

    def eliminar(self, id_contrato):
        self.limpiar_errores()
        resultado = self.repo.eliminar(id_contrato)
        if not resultado:
            self.errores.append('Contrato no encontrado')
            return None
        return resultado

    def obtener_api(self, id_contrato):
        c = self.repo.obtener_por_id(id_contrato)
        if c:
            return {
                'id_contrato': c.id_contrato,
                'id_patrocinador': c.id_patrocinador,
                'fecha_inicio': c.fecha_inicio.isoformat() if hasattr(c.fecha_inicio, 'isoformat') else str(c.fecha_inicio),
                'fecha_fin': c.fecha_fin.isoformat() if hasattr(c.fecha_fin, 'isoformat') else str(c.fecha_fin),
                'estatus': c.estatus,
                'tipo': c.tipo,
                'monto_total': float(c.monto_total) if c.monto_total is not None else "",
            }
        return None
