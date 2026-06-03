import { validarTexto, validarTextoLargo } from './validacion.js';

document.addEventListener('DOMContentLoaded', function() {
    const formCrear = document.querySelector('#modalCrearTarea form');
    if (formCrear) {
        const nombre = formCrear.querySelector('[name="Nombre_Tarea"]');
        const instruccion = formCrear.querySelector('[name="Instruccion"]');

        if (nombre) {
            nombre.addEventListener('input', function() { validarTexto(this); });
            nombre.addEventListener('blur', function() { validarTexto(this); });
        }
        if (instruccion) {
            instruccion.addEventListener('input', function() { validarTextoLargo(this); });
            instruccion.addEventListener('blur', function() { validarTextoLargo(this); });
        }

        formCrear.addEventListener('submit', function(e) {
            const valNombre = validarTexto(nombre);
            const valInst = validarTextoLargo(instruccion);

            if (!valNombre || !valInst) {
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
            Swal.fire({
                title: '¿Crear tarea?',
                text: 'Se creará una nueva tarea en el sistema.',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#198754',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Sí, crear',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    HTMLFormElement.prototype.submit.call(formCrear);
                }
            });
        });
    }

    const formEditar = document.querySelector('#modalEditarTarea form');
    if (formEditar) {
        const nombre = document.getElementById('edit_Nombre_Tarea');
        const instruccion = document.getElementById('edit_Instruccion');

        if (nombre) {
            nombre.addEventListener('input', function() { validarTexto(this); });
            nombre.addEventListener('blur', function() { validarTexto(this); });
        }
        if (instruccion) {
            instruccion.addEventListener('input', function() { validarTextoLargo(this); });
            instruccion.addEventListener('blur', function() { validarTextoLargo(this); });
        }

        formEditar.addEventListener('submit', function(e) {
            const valNombre = validarTexto(nombre);
            const valInst = validarTextoLargo(instruccion);

            if (!valNombre || !valInst) {
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
            Swal.fire({
                title: '¿Guardar cambios?',
                text: 'Se actualizarán los datos de esta tarea.',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#198754',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Sí, guardar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    HTMLFormElement.prototype.submit.call(formEditar);
                }
            });
        });
    }
});

window.editarTarea = function(id, nombre, instruccion) {
    document.getElementById('edit_Nombre_Tarea').value = nombre;
    document.getElementById('edit_Instruccion').value = instruccion;
    document.querySelector('#modalEditarTarea input[name="id_tarea"]').value = id;
    new bootstrap.Modal(document.getElementById('modalEditarTarea')).show();
};

window.confirmarEliminar = function(id, nombre) {
    Swal.fire({
        title: '¿Eliminar tarea?',
        text: `Se eliminará: "${nombre}"`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonText: 'Cancelar',
        confirmButtonText: 'Sí, eliminar'
    }).then(result => {
        if (result.isConfirmed) {
            document.querySelector('#formEliminar input[name="id_tarea"]').value = id;
            document.getElementById('formEliminar').submit();
        }
    });
};
