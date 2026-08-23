import { validarTexto, validarTextoLargo } from '../validacion.js';

export function validarFormularioTarea() {
    var nombre = document.querySelector('#modalCrearTarea [name="Nombre_Tarea"]') ||
                 document.getElementById('edit_Nombre_Tarea');
    var instr = document.querySelector('#modalCrearTarea [name="Instruccion"]') ||
                document.getElementById('edit_Instruccion');
    var ok = true;
    if (nombre && nombre.value) ok = validarTexto(nombre) && ok;
    if (instr && instr.value) ok = validarTextoLargo(instr) && ok;
    return ok;
}
