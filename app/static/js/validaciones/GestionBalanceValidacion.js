import { validarCosto, validarFecha, validarHora, validarSelect } from '../validacion.js';

export function validarFormularioBalance() {
    var selectContrato = document.getElementById('selectContrato');
    var monto = document.getElementById('montoPago');
    var fecha = document.querySelector('[name="fecha_pago"]');
    var hora = document.querySelector('[name="hora_pago"]');
    return validarSelect(selectContrato) && validarCosto(monto) &&
           validarFecha(fecha) && validarHora(hora);
}
