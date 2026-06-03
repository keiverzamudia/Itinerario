import { validarFecha, validarFechaFutura, validarFechaFin, validarSelect, validarCosto } from './validacion.js';

window.prepararCrear = function() {
    document.getElementById('form_action').value = 'crear';
    document.getElementById('form_id_contrato').value = '';
    document.getElementById('input_id_patrocinador').value = '';
    document.getElementById('input_tipo').value = '';
    document.getElementById('input_fecha_inicio').value = '';
    document.getElementById('input_fecha_fin').value = '';
    document.getElementById('input_monto_total').value = '';
    document.getElementById('input_estatus').value = 'Borrador';
    document.getElementById('btnSubmitModal').textContent = 'Guardar Contrato';
};

window.editarContrato = function(id) {
    fetch('/contratos/api/obtener/' + id)
        .then(r => r.json())
        .then(data => {
            document.getElementById('form_action').value = 'editar';
            document.getElementById('form_id_contrato').value = data.id_contrato;
            document.getElementById('input_id_patrocinador').value = data.id_patrocinador;
            document.getElementById('input_fecha_inicio').value = data.fecha_inicio;
            document.getElementById('input_fecha_fin').value = data.fecha_fin;
            document.getElementById('input_estatus').value = data.estatus;
            document.getElementById('input_tipo').value = data.tipo;
            document.getElementById('input_monto_total').value = data.monto_total;
            document.getElementById('btnSubmitModal').textContent = 'Actualizar Contrato';
            new bootstrap.Modal(document.getElementById('modalContrato')).show();
        });
};

window.prepararEliminar = function(id) {
    Swal.fire({
        title: '¿Eliminar contrato?',
        text: 'Esta acción no se puede deshacer.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('delete_id_contrato').value = id;
            const form = document.querySelector('#modalConfirmarEliminar form');
            HTMLFormElement.prototype.submit.call(form);
        }
    });
};

document.addEventListener('DOMContentLoaded', function() {
    const formContrato = document.getElementById('formContrato');
    if (formContrato) {
        const patrocinador = document.getElementById('input_id_patrocinador');
        const tipo = document.getElementById('input_tipo');
        const monto = document.getElementById('input_monto_total');
        const fechaInicio = document.getElementById('input_fecha_inicio');
        const fechaFin = document.getElementById('input_fecha_fin');
        const estatus = document.getElementById('input_estatus');

        if (patrocinador) patrocinador.addEventListener('change', function() { validarSelect(this); });
        if (tipo) tipo.addEventListener('change', function() { validarSelect(this); });
        if (monto) monto.addEventListener('blur', function() { validarCosto(this); });
        if (fechaInicio) fechaInicio.addEventListener('blur', function() {
            validarFechaFutura(this);
            if (fechaFin && fechaFin.value) validarFechaFin(fechaFin, this);
        });
        if (fechaFin) fechaFin.addEventListener('blur', function() { validarFechaFin(this, fechaInicio); });
        if (estatus) estatus.addEventListener('change', function() { validarSelect(this); });

        formContrato.addEventListener('submit', function(e) {
            const valPat = validarSelect(patrocinador);
            const valTipo = validarSelect(tipo);
            const valMonto = validarCosto(monto);
            const valInicio = validarFecha(fechaInicio);
            const valFin = validarFechaFin(fechaFin, fechaInicio);
            const valEstatus = validarSelect(estatus);

            if (!valPat || !valTipo || !valMonto || !valInicio || !valFin || !valEstatus) {
                e.preventDefault();
                Swal.fire({
                    title: 'Error de validación',
                    text: 'Corrige los campos marcados en rojo.',
                    icon: 'error',
                    confirmButtonColor: '#3085d6'
                });
                return;
            }

            e.preventDefault();
            const esCrear = document.getElementById('form_action').value === 'crear';
            Swal.fire({
                title: esCrear ? '¿Crear contrato?' : '¿Guardar cambios?',
                text: esCrear ? 'Se creará un nuevo contrato en el sistema.' : 'Se actualizarán los datos de este contrato.',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#198754',
                cancelButtonColor: '#6c757d',
                confirmButtonText: esCrear ? 'Sí, crear' : 'Sí, guardar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    HTMLFormElement.prototype.submit.call(formContrato);
                }
            });
        });
    }
});
