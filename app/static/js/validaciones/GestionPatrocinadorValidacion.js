import { validarRazonSocial, validarSelect, validarTelefono, validarEmail, validarNombre } from '../validacion.js';

export function validarFormularioPatrocinador() {
    const nombre = document.getElementById('nombre_empresa');
    const rifTipo = document.getElementById('rif_tipo');
    const rifNum = document.getElementById('rif');
    const nombreContacto = document.getElementById('nombre_contacto');
    const tipoContrato = document.getElementById('tipo_contrato');
    const telefono = document.getElementById('telefono');
    const email = document.getElementById('email');
    const encargado = document.getElementById('encargado_id');

    const rifCompleto = rifTipo.value + rifNum.value.trim();
    const rifValido = rifNum.value.trim().length >= 7 && /^[VVEJGvvejg]-?\d{7,10}$/.test(rifCompleto);
    if (!rifValido) {
        rifNum.classList.add('is-invalid');
        rifNum.classList.remove('is-valid');
        const fb = rifNum.closest('.input-group')?.parentElement?.querySelector('.invalid-feedback');
        if (fb) fb.textContent = 'El RIF debe tener entre 7 y 10 dígitos';
    } else {
        rifNum.classList.remove('is-invalid');
        rifNum.classList.add('is-valid');
        const fb = rifNum.closest('.input-group')?.parentElement?.querySelector('.invalid-feedback');
        if (fb) fb.textContent = '';
    }

    return (
        validarRazonSocial(nombre) &&
        rifValido &&
        validarSelect(tipoContrato) &&
        (telefono.value ? validarTelefono(telefono) : true) &&
        (email.value ? validarEmail(email) : true) &&
        validarNombre(nombreContacto) &&
        validarSelect(encargado)
    );
}
