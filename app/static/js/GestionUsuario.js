import { validarNombre, validarEmail, validarCedula, validarTelefono, validarPassword, validarConfirmPassword, validarSelect, limpiarInvalido } from './validacion.js';

window.limpiarFormulario = function() {
    window.modoEdicion = false;
    window.usuarioIdEditando = null;
    document.getElementById('modalTitle').textContent = 'Crear Nuevo Usuario';
    document.getElementById('usuarioForm').reset();
    const activo = document.getElementById('activo');
    if (activo) activo.checked = true;
    const password = document.getElementById('password');
    const confirm = document.getElementById('confirm_password');
    if (password) password.required = true;
    if (confirm) confirm.required = true;
    const form = document.getElementById('usuarioForm');
    form.action = form.getAttribute('data-create-url');
};

async function editarUsuario(id) {
    try {
        const response = await fetch(`/usuarios/api/obtener/${id}`);
        const data = await response.json();
        if (data.error) {
            Swal.fire('Error', data.error, 'error');
            return;
        }
        window.modoEdicion = true;
        window.usuarioIdEditando = id;
        document.getElementById('modalTitle').textContent = 'Editar Usuario';
        document.getElementById('nombre').value = data.nombre || '';
        document.getElementById('cedula').value = data.cedula || '';
        document.getElementById('email').value = data.email || '';
        document.getElementById('rol').value = data.rol || '';
        document.getElementById('departamento').value = data.departamento || '';
        document.getElementById('telefono').value = data.telefono || '';
        const activo = document.getElementById('activo');
        if (activo) activo.checked = data.activo;
        const password = document.getElementById('password');
        const confirm = document.getElementById('confirm_password');
        if (password) password.required = false;
        if (confirm) confirm.required = false;
        const form = document.getElementById('usuarioForm');
        form.action = form.getAttribute('data-edit-url').replace('0', id);
        const modal = new bootstrap.Modal(document.getElementById('usuarioModal'));
        modal.show();
    } catch (err) {
        console.error('Error al obtener datos del usuario:', err);
        Swal.fire('Error', 'No se pudieron cargar los datos del usuario.', 'error');
    }
}

function confirmarEliminar(id, nombre) {
    Swal.fire({
        title: 'Eliminar usuario?',
        text: `Se eliminará a ${nombre}. Esta acción no se puede deshacer.`,
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
            form.action = `/usuarios/eliminar/${id}`;
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

document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', async function(e) {
        const btn = e.target.closest('.btn-editar-usuario');
        if (btn) {
            const id = btn.getAttribute('data-id');
            await editarUsuario(id);
        }
    });

    document.addEventListener('click', function(e) {
        const btn = e.target.closest('.btn-eliminar-usuario');
        if (btn) {
            const id = btn.getAttribute('data-id');
            const nombre = btn.getAttribute('data-nombre');
            confirmarEliminar(id, nombre);
        }
    });

    const nombre = document.getElementById('nombre');
    const cedula = document.getElementById('cedula');
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const confirm = document.getElementById('confirm_password');
    const telefono = document.getElementById('telefono');
    const rol = document.getElementById('rol');
    const departamento = document.getElementById('departamento');

    if (nombre) {
        nombre.addEventListener('input', function() { validarNombre(this); });
        nombre.addEventListener('blur', function() { validarNombre(this); });
    }
    if (cedula) {
        cedula.addEventListener('input', function() { validarCedula(this); });
        cedula.addEventListener('blur', function() { validarCedula(this); });
    }
    if (email) {
        email.addEventListener('input', function() { validarEmail(this); });
        email.addEventListener('blur', function() { validarEmail(this); });
    }
    if (password) {
        password.addEventListener('input', function() { validarPassword(this); });
        password.addEventListener('blur', function() { validarPassword(this); });
    }
    if (confirm) {
        confirm.addEventListener('input', function() { validarConfirmPassword(password, this); });
        confirm.addEventListener('blur', function() { validarConfirmPassword(password, this); });
    }
    if (telefono) {
        telefono.addEventListener('input', function() { if (this.value.trim()) validarTelefono(this); else limpiarInvalido(this); });
        telefono.addEventListener('blur', function() { if (this.value.trim()) validarTelefono(this); else limpiarInvalido(this); });
    }
    if (rol) {
        rol.addEventListener('change', function() { validarSelect(this); });
    }
    if (departamento) {
        departamento.addEventListener('change', function() { validarSelect(this); });
    }

    const btnGuardar = document.getElementById('btnGuardar');
    if (btnGuardar) {
        btnGuardar.addEventListener('click', function(e) {
            const form = document.getElementById('usuarioForm');
            const valNombre = validarNombre(nombre);
            const valCedula = validarCedula(cedula);
            const valEmail = validarEmail(email);
            const valPassword = password && password.value ? validarPassword(password) : true;
            const valConfirm = confirm && confirm.value ? validarConfirmPassword(password, confirm) : true;
            const valRol = validarSelect(rol);
            const valDepto = validarSelect(departamento);
            const valTel = telefono && telefono.value ? validarTelefono(telefono) : (telefono ? (limpiarInvalido(telefono), true) : true);

            if (!valNombre || !valCedula || !valEmail || !valPassword || !valConfirm || !valRol || !valDepto || !valTel) {
                e.preventDefault();
                const primerError = document.querySelector('.is-invalid');
                if (primerError) primerError.focus();
                return;
            }

            if (!window.modoEdicion && (!password || !password.value)) {
                e.preventDefault();
                Swal.fire({
                    title: 'Contraseña requerida',
                    text: 'Debes ingresar una contraseña para crear un usuario.',
                    icon: 'error',
                    confirmButtonColor: '#3085d6'
                });
                return;
            }

            if (!window.modoEdicion && password && confirm && password.value !== confirm.value) {
                e.preventDefault();
                validarConfirmPassword(password, confirm);
                Swal.fire({
                    title: 'Las contraseñas no coinciden',
                    text: 'Ambos campos de contraseña deben ser iguales.',
                    icon: 'error',
                    confirmButtonColor: '#3085d6'
                });
                return;
            }

            e.preventDefault();
            const titulo = window.modoEdicion ? 'Guardar cambios?' : 'Crear usuario?';
            const texto = window.modoEdicion
                ? 'Se actualizarán los datos de este usuario.'
                : 'Se creará un nuevo usuario en el sistema.';
            Swal.fire({
                title: titulo,
                text: texto,
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#198754',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Sí, ' + (window.modoEdicion ? 'guardar' : 'crear'),
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    HTMLFormElement.prototype.submit.call(form);
                }
            });
        });
    }
});
