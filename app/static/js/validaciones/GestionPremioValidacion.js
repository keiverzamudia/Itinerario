import { validarNombre, validarSelect } from '../validacion.js';

export function validarFormularioPremio() {
    return validarNombre(document.getElementById('nombre_crear')) &&
           validarSelect(document.getElementById('id_patrocinador'));
}

export function validarFormularioPremioEditar() {
    return validarNombre(document.getElementById('edit_nombre'));
}
