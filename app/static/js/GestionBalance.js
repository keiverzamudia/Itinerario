import { validarCosto, validarFecha, validarHora, validarSelect } from './validacion.js';

document.addEventListener('DOMContentLoaded', function() {
    const selectContrato = document.getElementById('selectContrato');
    const infoContrato = document.getElementById('infoContrato');
    const nombrePatrocinadorSpan = document.getElementById('nombrePatrocinador');
    const montoTotalSpan = document.getElementById('montoTotalContrato');
    const saldoPendienteSpan = document.getElementById('saldoPendienteContrato');
    const montoPago = document.getElementById('montoPago');

    if (selectContrato) {
        selectContrato.addEventListener('change', async function() {
            const contratoId = this.value;
            if (contratoId) {
                try {
                    const response = await fetch(`/balance/api/contrato/${contratoId}`);
                    const data = await response.json();
                    if (!data.error) {
                        nombrePatrocinadorSpan.textContent = data.nombre_patrocinador || 'Sin patrocinador';
                        montoTotalSpan.textContent = data.monto_total.toFixed(2);
                        saldoPendienteSpan.textContent = data.saldo_pendiente.toFixed(2);
                        infoContrato.style.display = 'block';
                        if (montoPago) montoPago.max = data.saldo_pendiente;
                    }
                } catch (err) {
                    console.error("Error al obtener la información del contrato:", err);
                }
            } else {
                infoContrato.style.display = 'none';
            }
        });
    }

    if (montoPago) {
        montoPago.addEventListener('blur', function() { validarCosto(this); });
    }

    document.addEventListener('click', async function(e) {
        const btn = e.target.closest('.btn-editar-pago');
        if (btn) {
            const pagoId = btn.getAttribute('data-id');
            try {
                const response = await fetch(`/balance/api/pago/${pagoId}`);
                const data = await response.json();
                
                document.getElementById('edit_pago_id').value = data.id_pago;
                document.getElementById('edit_monto').value = data.monto;
                document.getElementById('edit_tipo_pago').value = data.tipo_pago;
                document.getElementById('edit_referencia').value = data.referencia || '';
                document.getElementById('edit_fecha_pago').value = data.fecha_pago.split('/').reverse().join('-');
                document.getElementById('edit_hora_pago').value = data.hora_pago;
                document.getElementById('edit_notas').value = data.Descripción || '';
                
                new bootstrap.Modal(document.getElementById('modalEditarPago')).show();
            } catch (err) {
                console.error("Error al obtener datos del pago:", err);
            }
        }
    });

    document.addEventListener('click', function(e) {
        const btn = e.target.closest('.btn-eliminar-pago');
        if (btn) {
            const pagoId = btn.getAttribute('data-id');
            Swal.fire({
                title: '¿Eliminar pago?',
                text: 'Esta acción no se puede deshacer.',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#dc3545',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Sí, eliminar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    const form = document.createElement('form');
                    form.method = 'POST';
                    form.action = `/balance/eliminar-pago/${pagoId}`;

                    const csrfInput = document.createElement('input');
                    csrfInput.type = 'hidden';
                    csrfInput.name = 'csrf_token';
                    csrfInput.value = document.querySelector('input[name="csrf_token"]')?.value || '';

                    form.appendChild(csrfInput);
                    document.body.appendChild(form);
                    form.submit();
                }
            });
        }
    });

    const formRegistrar = document.getElementById('formRegistrarPago');
    if (formRegistrar) {
        formRegistrar.addEventListener('submit', function(e) {
            const valContrato = validarSelect(selectContrato);
            const valMonto = validarCosto(montoPago);
            const fechaPago = document.querySelector('[name="fecha_pago"]');
            const horaPago = document.querySelector('[name="hora_pago"]');
            const valFecha = validarFecha(fechaPago);
            const valHora = validarHora(horaPago);

            if (!valContrato || !valMonto || !valFecha || !valHora) {
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
                title: '¿Registrar pago?',
                text: 'Se registrará un nuevo pago en el sistema.',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#198754',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Sí, registrar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    formRegistrar.submit();
                }
            });
        });
    }

    const formEditar = document.getElementById('formEditarPago');
    if (formEditar) {
        formEditar.addEventListener('submit', function(e) {
            e.preventDefault();
            Swal.fire({
                title: '¿Guardar cambios?',
                text: 'Se actualizarán los datos de este pago.',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#198754',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Sí, guardar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    formEditar.submit();
                }
            });
        });
    }

    document.querySelectorAll('.filter-chip').forEach(chip => {
        chip.addEventListener('click', function() {
            document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
            this.classList.add('active');
            
            const filter = this.getAttribute('data-filter');
            document.querySelectorAll('.contract-item').forEach(item => {
                if (filter === 'all') {
                    item.style.display = '';
                } else {
                    item.style.display = item.getAttribute('data-status') === filter ? '' : 'none';
                }
            });
        });
    });
});
