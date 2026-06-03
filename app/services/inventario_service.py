from app.repositories.inventario_repository import (
    TipoRecursoRepository, EstadoRecursoRepository, EstadoAsignacionRepository,
    RecursoInventarioRepository, AsignacionRecursoRepository
)
from app.repositories.usuario_repository import UsuarioRepository
from app.traits.validaciones import ValidacionesMixin


class InventarioService(ValidacionesMixin):
    def __init__(self):
        self.tipo_repo = TipoRecursoRepository()
        self.estado_repo = EstadoRecursoRepository()
        self.estado_asig_repo = EstadoAsignacionRepository()
        self.recurso_repo = RecursoInventarioRepository()
        self.asignacion_repo = AsignacionRecursoRepository()
        self.usuario_repo = UsuarioRepository()

    def obtener_dashboard(self):
        recursos = self.recurso_repo.consultar()
        total = self.recurso_repo.contar()
        disponibles = self.recurso_repo.contar(estado_id=1)
        asignados = self.recurso_repo.contar(estado_id=2)
        en_mantenimiento = self.recurso_repo.contar(estado_id=3)
        return {
            'recursos': recursos,
            'total': total,
            'disponibles': disponibles,
            'asignados': asignados,
            'en_mantenimiento': en_mantenimiento,
        }

    def obtener_tipos(self):
        return self.tipo_repo.consultar()

    def obtener_tipo(self, id):
        return self.tipo_repo.obtener_por_id(id)

    def crear_tipo(self, nombre, descripcion):
        self.limpiar_errores()
        if not nombre or not nombre.strip():
            self.errores.append('El nombre del tipo es obligatorio')
            return None
        if self.errores:
            return None
        return self.tipo_repo.registrar({'nombre': nombre.strip(), 'descripcion': descripcion.strip() if descripcion else None})

    def editar_tipo(self, id, nombre, descripcion):
        self.limpiar_errores()
        tipo = self.tipo_repo.obtener_por_id(id)
        if not tipo:
            self.errores.append('Tipo de recurso no encontrado')
            return None
        if not nombre or not nombre.strip():
            self.errores.append('El nombre del tipo es obligatorio')
            return None
        if self.errores:
            return None
        return self.tipo_repo.modificar(id, {'nombre': nombre.strip(), 'descripcion': descripcion.strip() if descripcion else None})

    def eliminar_tipo(self, id):
        self.limpiar_errores()
        tipo = self.tipo_repo.obtener_por_id(id)
        if not tipo:
            self.errores.append('Tipo de recurso no encontrado')
            return False
        if self.tipo_repo.en_uso(id):
            self.errores.append('No se puede eliminar un tipo que tiene recursos asociados')
            return False
        self.tipo_repo.eliminar(id)
        return True

    def obtener_estados(self):
        return self.estado_repo.consultar()

    def obtener_estados_asignacion(self):
        return self.estado_asig_repo.consultar()

    def obtener_recurso(self, id):
        return self.recurso_repo.obtener_por_id(id)

    def crear_recurso(self, datos):
        self.limpiar_errores()
        if not datos.get('nombre'):
            self.errores.append('El nombre del recurso es obligatorio')
            return None
        if not datos.get('tipo_id'):
            self.errores.append('Debe seleccionar un tipo de recurso')
            return None
        if self.errores:
            return None
        datos['estado_id'] = 1
        return self.recurso_repo.registrar(datos)

    def editar_recurso(self, id, datos):
        self.limpiar_errores()
        recurso = self.recurso_repo.obtener_por_id(id)
        if not recurso:
            self.errores.append('Recurso no encontrado')
            return None
        if self.errores:
            return None
        return self.recurso_repo.modificar(id, datos)

    def eliminar_recurso(self, id):
        self.limpiar_errores()
        recurso = self.recurso_repo.obtener_por_id(id)
        if not recurso:
            self.errores.append('Recurso no encontrado')
            return False
        if self.recurso_repo.tiene_asignaciones_pendientes(id):
            self.errores.append('El recurso tiene asignaciones activas pendientes')
            return False
        self.recurso_repo.eliminar_logico(id)
        return True

    def obtener_asignaciones(self, recurso_id=None):
        return self.asignacion_repo.consultar(recurso_id=recurso_id)

    def obtener_asignaciones_gestion(self):
        return self.asignacion_repo.consultar()

    def existe_asignacion_activa(self, recurso_id):
        return self.asignacion_repo.obtener_asignacion_activa(recurso_id) is not None

    def asignar_recurso(self, recurso_id, usuario_id, fecha_devolucion=None, notas=None):
        self.limpiar_errores()
        recurso = self.recurso_repo.obtener_por_id(recurso_id)
        if not recurso:
            self.errores.append('Recurso no encontrado')
            return None
        if recurso.eliminado:
            self.errores.append('No se puede asignar un recurso eliminado')
            return None
        if self.existe_asignacion_activa(recurso_id):
            self.errores.append('El recurso ya está asignado actualmente')
            return None
        if recurso.estado_id != 1:
            self.errores.append('El recurso no está disponible para asignación')
            return None
        if self.errores:
            return None
        asignacion = self.asignacion_repo.registrar({
            'recurso_id': recurso_id,
            'usuario_id': usuario_id,
            'fecha_devolucion_esperada': fecha_devolucion,
            'notas': notas,
            'estado_asignacion_id': 1,
        })
        self.recurso_repo.modificar(recurso_id, {'estado_id': 2})
        return asignacion

    def devolver_recurso(self, asignacion_id):
        self.limpiar_errores()
        asignacion = self.asignacion_repo.obtener_por_id(asignacion_id)
        if not asignacion:
            self.errores.append('Asignación no encontrada')
            return False
        if asignacion.fecha_devolucion_real:
            self.errores.append('Esta asignación ya fue devuelta')
            return False
        self.asignacion_repo.devolver(asignacion_id)
        self.recurso_repo.modificar(asignacion.recurso_id, {'estado_id': 1})
        return True

    def obtener_usuarios(self):
        return self.usuario_repo.consultar()

    def obtener_datos_asignar(self, recurso_id):
        recurso = self.recurso_repo.obtener_por_id(recurso_id)
        usuarios = self.obtener_usuarios()
        return recurso, usuarios

    def total_asignaciones(self, recurso_id):
        return self.recurso_repo.total_asignaciones(recurso_id)
