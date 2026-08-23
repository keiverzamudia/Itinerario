import { validarNombre } from '../validacion.js';

function mostrarError(campo, mensaje) {
    campo.classList.add('is-invalid');
    campo.classList.remove('is-valid');
    var fb = campo.parentElement.querySelector('.invalid-feedback');
    if (fb) fb.textContent = mensaje;
}

function mostrarValido(campo) {
    campo.classList.remove('is-invalid');
    campo.classList.add('is-valid');
    var fb = campo.parentElement.querySelector('.invalid-feedback');
    if (fb) fb.textContent = '';
}

export function validarNombreReel(campo) {
    var val = campo.value.trim();
    if (!val) { mostrarError(campo, 'El nombre es obligatorio'); return false; }
    if (val.length < 2) { mostrarError(campo, 'Mínimo 2 caracteres'); return false; }
    mostrarValido(campo);
    return true;
}

export function validarDuracionReel(campo) {
    var val = campo.value.trim();
    if (!val) { mostrarError(campo, 'La duración es obligatoria'); return false; }
    if (!/^\d{1,2}(,\d{1,2})?$/.test(val)) { mostrarError(campo, 'Solo números y coma (ej: 3,30 o 5)'); return false; }
    mostrarValido(campo);
    return true;
}

export function validarFormularioReel() {
    return validarNombreReel(document.getElementById('nombreReel')) &&
           validarDuracionReel(document.getElementById('duracionTotal'));
}
