from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from datetime import date
from app.repositories.mantenimiento_repository import (
    RecursoRepository, MantenimientoRepository, HistorialMantenimientoRepository
)
from app.forms.mantenimiento_form import IngresarMantenimientoForm, NotaMantenimientoForm
from app.helpers.decorators import permiso_requerido
from app.helpers.bitacora_helper import registrar_actividad


ESTADOS_RECURSO = {1: 'Disponible', 2: 'Asignado', 3: 'En Mantenimiento', 4: 'Dañado', 5: 'Baja'}


class MantenimientoController:
    def __init__(self):
        self.recurso_repo = RecursoRepository()
        self.manto_repo = MantenimientoRepository()
        self.historial_repo = HistorialMantenimientoRepository()

    def dashboard(self):
        recursos = self.recurso_repo.consultar()
        total = self.recurso_repo.contar()
        en_mantenimiento = self.recurso_repo.contar(estado_id=3)
        de_baja = self.recurso_repo.contar(estado_id=5)
        return render_template('mantenimiento/dashboard.html',
                               recursos=recursos, total=total,
                               en_mantenimiento=en_mantenimiento,
                               de_baja=de_baja,
                               estados=ESTADOS_RECURSO)

    def ingresar(self, recurso_id):
        recurso = self.recurso_repo.obtener_por_id(recurso_id)
        if not recurso:
            flash('Recurso no encontrado', 'danger')
            return redirect(url_for('mantenimiento.dashboard'))
        if recurso.estado_id != 1:
            flash(f'El recurso "{recurso.nombre}" no está disponible para mantenimiento', 'warning')
            return redirect(url_for('mantenimiento.dashboard'))
        form = IngresarMantenimientoForm()
        if form.validate_on_submit():
            manto_id = self.manto_repo.registrar({
                'recurso_id': recurso.id,
                'usuario_id': current_user.id,
                'fecha_ingreso': form.fecha_ingreso.data,
                'diagnostico': form.diagnostico.data,
                'observaciones': form.observaciones.data,
            })
            self.recurso_repo.modificar(recurso.id, {'estado_id': 3})
            self.historial_repo.registrar({
                'mantenimiento_id': manto_id.id,
                'usuario_id': current_user.id,
                'accion': 'ingreso',
                'descripcion': f'Ingreso a mantenimiento. Diagnóstico: {form.diagnostico.data}',
            })
            registrar_actividad('create', 'mantenimiento', 'Ingresar a mantenimiento',
                                f'Recurso "{recurso.nombre}" ingresado a mantenimiento')
            flash(f'Recurso "{recurso.nombre}" ingresado a mantenimiento', 'success')
            return redirect(url_for('mantenimiento.ver', id=manto_id.id))
        return render_template('mantenimiento/ingresar.html', form=form, recurso=recurso)

    def ver(self, id):
        mantenimiento = self.manto_repo.obtener_por_id(id)
        if not mantenimiento:
            flash('Mantenimiento no encontrado', 'danger')
            return redirect(url_for('mantenimiento.dashboard'))
        nota_form = NotaMantenimientoForm()
        return render_template('mantenimiento/detalle.html',
                               mantenimiento=mantenimiento,
                               recurso=mantenimiento.recurso,
                               historial=mantenimiento.historial,
                               nota_form=nota_form,
                               estados=ESTADOS_RECURSO)

    def agregar_nota(self, id):
        mantenimiento = self.manto_repo.obtener_por_id(id)
        if not mantenimiento:
            flash('Mantenimiento no encontrado', 'danger')
            return redirect(url_for('mantenimiento.dashboard'))
        form = NotaMantenimientoForm()
        if form.validate_on_submit():
            self.historial_repo.registrar({
                'mantenimiento_id': mantenimiento.id,
                'usuario_id': current_user.id,
                'accion': 'nota',
                'descripcion': form.descripcion.data,
            })
            registrar_actividad('update', 'mantenimiento', 'Agregar nota',
                                f'Nota a mantenimiento #{mantenimiento.id}: {form.descripcion.data[:80]}')
            flash('Nota agregada al seguimiento', 'success')
        return redirect(url_for('mantenimiento.ver', id=mantenimiento.id))

    def reparar(self, id):
        manto = self.manto_repo.obtener_por_id(id)
        if not manto:
            flash('Mantenimiento no encontrado', 'danger')
            return redirect(url_for('mantenimiento.dashboard'))
        if manto.estado == 'en_espera':
            self.manto_repo.modificar(id, {'estado': 'en_reparacion'})
            accion = 'reparar'
            descripcion = 'Se inició el proceso de reparación.'
        elif manto.estado == 'en_reparacion':
            self.manto_repo.modificar(id, {'estado': 'reparado'})
            self.recurso_repo.modificar(manto.recurso_id, {'estado_id': 1})
            accion = 'reparar'
            descripcion = 'Recurso reparado exitosamente.'
        else:
            flash('No se puede cambiar el estado actual', 'warning')
            return redirect(url_for('mantenimiento.ver', id=id))
        self.historial_repo.registrar({
            'mantenimiento_id': id,
            'usuario_id': current_user.id,
            'accion': accion,
            'descripcion': descripcion,
        })
        registrar_actividad('update', 'mantenimiento', 'Reparar recurso',
                            f'Mantenimiento #{id}: {descripcion}')
        return redirect(url_for('mantenimiento.ver', id=id))

    def dar_baja(self, id):
        manto = self.manto_repo.obtener_por_id(id)
        if not manto:
            flash('Mantenimiento no encontrado', 'danger')
            return redirect(url_for('mantenimiento.dashboard'))
        self.manto_repo.modificar(id, {'estado': 'baja'})
        self.recurso_repo.modificar(manto.recurso_id, {'estado_id': 5})
        self.historial_repo.registrar({
            'mantenimiento_id': id,
            'usuario_id': current_user.id,
            'accion': 'baja',
            'descripcion': 'Recurso dado de baja del inventario.',
        })
        registrar_actividad('delete', 'mantenimiento', 'Dar de baja',
                            f'Recurso "{manto.recurso.nombre if manto.recurso else ""}" dado de baja')
        return redirect(url_for('mantenimiento.ver', id=id))

    def finalizar(self, id):
        manto = self.manto_repo.obtener_por_id(id)
        if not manto:
            flash('Mantenimiento no encontrado', 'danger')
            return redirect(url_for('mantenimiento.dashboard'))
        self.manto_repo.modificar(id, {'estado': 'finalizado', 'fecha_salida': date.today()})
        self.historial_repo.registrar({
            'mantenimiento_id': id,
            'usuario_id': current_user.id,
            'accion': 'finalizar',
            'descripcion': 'Mantenimiento finalizado.',
        })
        registrar_actividad('update', 'mantenimiento', 'Finalizar mantenimiento',
                            f'Mantenimiento #{id} finalizado')
        return redirect(url_for('mantenimiento.ver', id=id))
