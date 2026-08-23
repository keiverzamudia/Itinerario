import { validarNombre } from '../validacion.js';

export function validarFormularioGuion() {
    var nombre = document.getElementById('nombre') || document.getElementById('nombre_base');
    return nombre ? validarNombre(nombre) : true;
}
