import { validarNombre, validarFecha, validarHora, validarSelect, validarTextoLargo, limpiarInvalido } from './validacion.js';

window.cargarPremioEnTicket = function(elemento) {
    const id = elemento.getAttribute('data-id');
    const nombre = elemento.getAttribute('data-nombre');
    const idPat = elemento.getAttribute('data-patrocinador-id');
    const desc = elemento.getAttribute('data-descripcion');

    document.querySelectorAll('.premio-card').forEach(c => c.classList.remove('selected'));
    elemento.classList.add('selected');

    document.querySelector('.id-placeholder-msg').classList.add('d-none');
    document.getElementById('ticket-activo').classList.remove('d-none');
    
    const badge = document.getElementById('pos-badge-estado');
    badge.className = "badge rounded-pill bg-primary px-2 py-1 fw-bold mb-2";
    badge.innerText = "Nueva Entrega";
    
    document.getElementById('ticket-item-nombre').innerHTML = "🎁 " + nombre;
    document.getElementById('pos-input-id-premio').value = id;
    document.getElementById('pos-textarea-notas').value = desc;
    
    const selectPat = document.getElementById('pos-select-patrocinador');
    selectPat.removeAttribute('disabled'); 
    document.getElementById('pos-textarea-notas').removeAttribute('readonly');
    selectPat.value = idPat ? idPat : "";
    
    const btnDespachar = document.getElementById('btn-despachar-pos');
    btnDespachar.removeAttribute('disabled');
    btnDespachar.setAttribute('type', 'submit');

    document.getElementById('pos-entregado-por').classList.add('d-none');
}

document.addEventListener('click', function(e) {
    const itemHistorial = e.target.closest('.item-historial-click');
    if (itemHistorial) {
        document.querySelectorAll('.premio-card').forEach(c => c.classList.remove('selected'));
        
        const nombre = itemHistorial.getAttribute('data-nombre');
        const patrocinadorNombre = itemHistorial.getAttribute('data-patrocinador');
        const desc = itemHistorial.getAttribute('data-descripcion');
        const usuarioNombre = itemHistorial.getAttribute('data-usuario-nombre');

        document.querySelector('.id-placeholder-msg').classList.add('d-none');
        document.getElementById('ticket-activo').classList.remove('d-none');
        
        const badge = document.getElementById('pos-badge-estado');
        badge.className = "badge rounded-pill bg-success px-2 py-1 fw-bold mb-2";
        badge.innerText = "Premio Entregado";
        
        document.getElementById('ticket-item-nombre').innerHTML = "🏆 " + nombre;
        document.getElementById('pos-textarea-notas').value = desc;
        document.getElementById('pos-textarea-notas').setAttribute('readonly', 'true');
        
        const selectPat = document.getElementById('pos-select-patrocinador');
        selectPat.setAttribute('disabled', 'true');
        for (let i = 0; i < selectPat.options.length; i++) {
            if (selectPat.options[i].text === patrocinadorNombre) {
                selectPat.selectedIndex = i;
                break;
            }
        }

        document.getElementById('btn-despachar-pos').setAttribute('disabled', 'true');

        document.getElementById('pos-entregado-por-text').textContent = usuarioNombre || '—';
        document.getElementById('pos-entregado-por').classList.remove('d-none');
    }
});

document.getElementById('btn-limpiar-ticket').addEventListener('click', function() {
    document.querySelector('.id-placeholder-msg').classList.remove('d-none');
    document.getElementById('ticket-activo').classList.add('d-none');
    document.getElementById('form-pos-entrega').reset();
    document.getElementById('pos-input-id-premio').value = "";
    document.getElementById('pos-textarea-notas').removeAttribute('readonly');
    document.getElementById('pos-select-patrocinador').removeAttribute('disabled');
    document.getElementById('btn-despachar-pos').setAttribute('disabled', 'true');
    document.querySelectorAll('.premio-card').forEach(c => c.classList.remove('selected'));
    document.getElementById('pos-entregado-por').classList.add('d-none');
});

function abrirEditarPremio(id) {
    fetch(`/premios/api/obtener/${id}`)
        .then(response => response.json())
        .then(premio => {
            document.getElementById('edit_premio_id').value = premio.id;
            document.getElementById('edit_nombre').value = premio.nombre;
            document.getElementById('edit_descripcion').value = premio.descripcion || '';
            
            const selectPat = document.getElementById('edit_patrocinador');
            for (let i = 0; i < selectPat.options.length; i++) {
                if (selectPat.options[i].value == premio.id_patrocinador) {
                    selectPat.selectedIndex = i;
                    break;
                }
            }
            
            if (premio.foto && premio.foto !== 'default-premio.png') {
                const fotoContainer = document.getElementById('foto_actual_container');
                const fotoImg = document.getElementById('foto_actual_img');
                fotoImg.src = `/static/uploads/premios/${premio.foto}`;
                fotoContainer.style.display = 'block';
            } else {
                document.getElementById('foto_actual_container').style.display = 'none';
            }
            
            const modal = new bootstrap.Modal(document.getElementById('editarPremioModal'));
            modal.show();
        })
        .catch(error => console.error('Error:', error));
}

document.getElementById('pos-buscador').addEventListener('input', function(e) {
    const busqueda = e.target.value.toLowerCase();
    document.querySelectorAll('.tarjeta-item-pos').forEach(t => {
        const nombre = t.getAttribute('data-nombre');
        t.style.display = nombre.includes(busqueda) ? 'block' : 'none';
    });
});

window.confirmarEdicion = function(id) {
    Swal.fire({
        title: '✏️ Editar Premio',
        text: '¿Estás seguro de que deseas editar este premio?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#198754',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Sí, editar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            abrirEditarPremio(id);
        }
    });
};

window.confirmarEliminacion = function(id, nombre) {
    Swal.fire({
        title: '¿Eliminar premio?',
        html: `¿Estás seguro de eliminar <strong>${nombre}</strong>?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = `/premios/eliminar/${id}`;
        }
    });
};

document.addEventListener('DOMContentLoaded', function() {
    const nombreCrear = document.getElementById('nombre_crear');
    if (nombreCrear) {
        nombreCrear.addEventListener('input', function() { validarNombre(this); });
        nombreCrear.addEventListener('blur', function() { validarNombre(this); });
    }

    const fechaCreacion = document.getElementById('fecha_creacion');
    if (fechaCreacion) {
        fechaCreacion.addEventListener('input', function() { if (this.value) validarFecha(this); else limpiarInvalido(this); });
        fechaCreacion.addEventListener('blur', function() { if (this.value) validarFecha(this); else limpiarInvalido(this); });
    }

    const horaCreacion = document.getElementById('hora_creacion');
    if (horaCreacion) {
        horaCreacion.addEventListener('input', function() { if (this.value) validarHora(this); else limpiarInvalido(this); });
        horaCreacion.addEventListener('blur', function() { if (this.value) validarHora(this); else limpiarInvalido(this); });
    }

    const idPatrocinador = document.getElementById('id_patrocinador');
    if (idPatrocinador) {
        idPatrocinador.addEventListener('change', function() { validarSelect(this); });
    }

    const editNombre = document.getElementById('edit_nombre');
    if (editNombre) {
        editNombre.addEventListener('input', function() { validarNombre(this); });
        editNombre.addEventListener('blur', function() { validarNombre(this); });
    }

    const editDescripcion = document.getElementById('edit_descripcion');
    if (editDescripcion) {
        editDescripcion.addEventListener('input', function() { if (this.value.trim()) validarTextoLargo(this); else limpiarInvalido(this); });
        editDescripcion.addEventListener('blur', function() { if (this.value.trim()) validarTextoLargo(this); else limpiarInvalido(this); });
    }

    const formCrear = document.querySelector('#modalCrearBase form');
    if (formCrear) {
        formCrear.addEventListener('submit', function(e) {
            const valNombre = validarNombre(nombreCrear);
            const valFecha = fechaCreacion && fechaCreacion.value ? validarFecha(fechaCreacion) : (fechaCreacion ? (limpiarInvalido(fechaCreacion), true) : true);
            const valHora = horaCreacion && horaCreacion.value ? validarHora(horaCreacion) : (horaCreacion ? (limpiarInvalido(horaCreacion), true) : true);
            const valSelect = validarSelect(idPatrocinador);

            if (!valNombre || !valFecha || !valHora || !valSelect) {
                e.preventDefault();
                Swal.fire({
                    title: 'Error de validación',
                    text: 'Por favor, corrige los campos marcados en rojo antes de guardar.',
                    icon: 'error',
                    confirmButtonColor: '#3085d6'
                });
                return;
            }

            e.preventDefault();
            Swal.fire({
                title: '¿Crear premio?',
                text: 'Se creará un nuevo premio en el sistema.',
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#198754',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Sí, crear',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    formCrear.submit();
                }
            });
        });
    }

    const formEditar = document.getElementById('formEditarPremio');
    if (formEditar) {
        formEditar.addEventListener('submit', function(e) {
            const valNombre = editNombre && editNombre.value.trim().length >= 2;

            if (!valNombre) {
                if (editNombre) validarNombre(editNombre);
                e.preventDefault();
                Swal.fire({
                    title: 'Error de validación',
                    text: 'El nombre debe tener al menos 2 caracteres.',
                    icon: 'error',
                    confirmButtonColor: '#3085d6'
                });
                return;
            }

            e.preventDefault();
            Swal.fire({
                title: '¿Guardar cambios?',
                text: 'Se actualizarán los datos de este premio.',
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
});
