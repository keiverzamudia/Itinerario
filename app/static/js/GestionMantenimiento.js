document.addEventListener('DOMContentLoaded', function () {
    const accionBtns = document.querySelectorAll('.btn-confirmar-accion');
    accionBtns.forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            const mensaje = this.getAttribute('data-confirm') || '¿Estás seguro?';
            e.preventDefault();
            const form = this.closest('form');
            Swal.fire({
                title: '¿Confirmar acción?',
                text: mensaje,
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: 'rgba(232, 42, 42, 0.9)',
                confirmButtonText: 'Sí, continuar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed && form) {
                    HTMLFormElement.prototype.submit.call(form);
                }
            });
        });
    });

    const formNota = document.getElementById('formNota');
    if (formNota) {
        formNota.addEventListener('submit', function (e) {
            const descripcion = document.getElementById('descripcion');
            if (descripcion && descripcion.value.trim().length < 3) {
                e.preventDefault();
                descripcion.classList.add('is-invalid');
                Swal.fire({
                    title: '❌ Error de validación',
                    text: 'La nota debe tener al menos 3 caracteres.',
                    icon: 'error',
                    confirmButtonColor: '#3085d6'
                });
                return;
            }
        });
    }

    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (el) {
        return new bootstrap.Tooltip(el);
    });
});
