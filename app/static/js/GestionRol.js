import { validarNombre } from './validacion.js';

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.select-all-module').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var modulo = this.getAttribute('data-modulo');
            var checkboxes = document.querySelectorAll('.permiso-item[data-modulo="' + modulo + '"] .permiso-checkbox');
            var allChecked = true;
            checkboxes.forEach(function(cb) {
                if (!cb.checked) allChecked = false;
            });
            checkboxes.forEach(function(cb) {
                if (!cb.disabled) cb.checked = allChecked ? false : true;
            });
        });
    });

    const nombreInput = document.getElementById('nombre');
    if (nombreInput) {
        nombreInput.addEventListener('input', function() { validarNombre(this); });
        nombreInput.addEventListener('blur', function() { validarNombre(this); });
    }
});
