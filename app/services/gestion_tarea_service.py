from app.repositories.gestion_tarea_repository import (
    TareaRepository, TareasAsignadasRepository
)
from app.repositories.usuario_repository import UsuarioRepository
from app.traits.validaciones import ValidacionesMixin


class GestionTareaService(ValidacionesMixin):
    def __init__(self):
        self.tarea_repo = TareaRepository()
        self.asignacion_repo = TareasAsignadasRepository()
        self.usuario_repo = UsuarioRepository()

    def obtener_dashboard(self):
        tareas = self.tarea_repo.consultar()
        usuarios = self.usuario_repo.consultar(activo=1)
        total = len(tareas)
        return {'tareas': tareas, 'total': total, 'usuarios': usuarios}

    def obtener_usuarios_activos(self):
        usuarios = self.usuario_repo.consultar(activo=1)
        return [(u.id, u.nombre) for u in usuarios]

    def crear_tarea(self, nombre, instruccion, id_usuario_creador, id_usuario):
        self.limpiar_errores()
        if not nombre or not instruccion:
            self.errores.append('Nombre e instrucción son obligatorios')
            return None
        if not id_usuario:
            self.errores.append('Debe seleccionar un usuario para asignar la tarea')
            return None
        tarea = self.tarea_repo.registrar({
            'Nombre_Tarea': nombre,
            'Instruccion': instruccion,
            'id_usuario_creador': id_usuario_creador,
        })
        if tarea:
            self.asignacion_repo.registrar({
                'id_tarea': tarea.id_tarea,
                'id_usuario': id_usuario,
            })
        return tarea

    def editar_tarea(self, id_tarea, nombre, instruccion):
        self.limpiar_errores()
        tarea = self.tarea_repo.obtener_por_id(id_tarea)
        if not tarea:
            self.errores.append('Tarea no encontrada')
            return False
        if not nombre or not instruccion:
            self.errores.append('Nombre e instrucción son obligatorios')
            return False
        self.tarea_repo.modificar(id_tarea, {
            'Nombre_Tarea': nombre,
            'Instruccion': instruccion,
        })
        return True

    def eliminar_tarea(self, id_tarea):
        self.limpiar_errores()
        tarea = self.tarea_repo.obtener_por_id(id_tarea)
        if not tarea:
            self.errores.append('Tarea no encontrada')
            return None
        if not tarea.Estatus:
            self.errores.append('Esta tarea ya está eliminada')
            return None
        return self.tarea_repo.eliminar(id_tarea)

    def obtener_tareas_usuario(self, usuario_id):
        tareas = self.asignacion_repo.obtener_por_usuario(usuario_id)
        pendientes = self.asignacion_repo.contar_pendientes(usuario_id)
        return {'tareas': tareas, 'pendientes': pendientes}

    def completar_tarea(self, id_asignacion, usuario_id):
        self.limpiar_errores()
        asignacion = self.asignacion_repo.obtener_por_id(id_asignacion)
        if not asignacion:
            self.errores.append('Asignación no encontrada')
            return False
        if asignacion.id_usuario != usuario_id:
            self.errores.append('No tienes permiso para completar esta tarea')
            return False
        self.asignacion_repo.modificar_estado(id_asignacion, 'Completada')
        return True
