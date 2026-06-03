import { validarRazonSocial, validarRif, validarTelefono, validarEmail, limpiarInvalido } from './validacion.js';

window.prepararCrear = function() {
    document.getElementById('form_action').value = 'crear';
    document.getElementById('form_id_patrocinador').value = '';
    document.getElementById('input_nombre_empresa').value = '';
    document.getElementById('input_rif').value = '';
    document.getElementById('input_telefono').value = '';
    document.getElementById('input_email').value = '';
    document.getElementById('input_nombre_contacto').value = '';
    document.getElementById('btnSubmitModal').textContent = 'Guardar Patrocinador';
};

window.editarPatrocinador = function(id) {
    fetch('/patrocinadores/api/obtener/' + id)
        .then(r => r.json())
        .then(data => {
            document.getElementById('form_action').value = 'editar';
            document.getElementById('form_id_patrocinador').value = data.id_patrocinador;
            document.getElementById('input_nombre_empresa').value = data.nombre_empresa || '';
            document.getElementById('input_rif').value = data.rif || '';
            document.getElementById('input_telefono').value = data.telefono || '';
            document.getElementById('input_email').value = data.email || '';
            document.getElementById('input_nombre_contacto').value = data.nombre_contacto || '';
            document.getElementById('btnSubmitModal').textContent = 'Actualizar Patrocinador';
            new bootstrap.Modal(document.getElementById('modalPatrocinador')).show();
        });
};

window.prepararEliminar = function(id) {
    Swal.fire({
        title: '¿Eliminar patrocinador?',
        text: 'Esta acción no se puede deshacer.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('delete_id_patrocinador').value = id;
            const form = document.querySelector('#modalConfirmarEliminar form');
            form.submit();
        }
    });
};

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formPatrocinador');
    if (!form) return;

    const nombreEmpresa = document.getElementById('input_nombre_empresa');
    const rif = document.getElementById('input_rif');
    const telefono = document.getElementById('input_telefono');
    const email = document.getElementById('input_email');

    if (nombreEmpresa) {
        nombreEmpresa.addEventListener('input', function() { validarRazonSocial(this); });
        nombreEmpresa.addEventListener('blur', function() { validarRazonSocial(this); });
    }
    if (rif) {
        rif.addEventListener('input', function() { validarRif(this); });
        rif.addEventListener('blur', function() { validarRif(this); });
    }
    if (telefono) {
        telefono.addEventListener('input', function() { if (this.value.trim()) validarTelefono(this); else limpiarInvalido(this); });
        telefono.addEventListener('blur', function() { if (this.value.trim()) validarTelefono(this); else limpiarInvalido(this); });
    }
    if (email) {
        email.addEventListener('input', function() { if (this.value.trim()) validarEmail(this); else limpiarInvalido(this); });
        email.addEventListener('blur', function() { if (this.value.trim()) validarEmail(this); else limpiarInvalido(this); });
    }

    form.addEventListener('submit', function(e) {
        const valEmpresa = validarRazonSocial(nombreEmpresa);
        const valRif = rif.value ? validarRif(rif) : (limpiarInvalido(rif), true);
        const valTel = telefono.value ? validarTelefono(telefono) : (limpiarInvalido(telefono), true);
        const valEmail = email.value ? validarEmail(email) : (limpiarInvalido(email), true);

        if (!valEmpresa || !valRif || !valTel || !valEmail) {
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
            title: esCrear ? '¿Crear patrocinador?' : '¿Guardar cambios?',
            text: esCrear ? 'Se creará un nuevo patrocinador en el sistema.' : 'Se actualizarán los datos de este patrocinador.',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#198754',
            cancelButtonColor: '#6c757d',
            confirmButtonText: esCrear ? 'Sí, crear' : 'Sí, guardar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                HTMLFormElement.prototype.submit.call(form);
            }
        });
    });
});
