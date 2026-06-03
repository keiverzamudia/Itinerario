import { validarEmail, validarPassword, validarConfirmPassword } from './validacion.js';

document.addEventListener('DOMContentLoaded', function() {
    initLoginForm();
    initCambiarPassword();
});

function initLoginForm() {
    const form = document.getElementById('loginForm');
    if (!form) return;

    const email = form.querySelector('[name="email"]');
    const password = form.querySelector('[name="password"]');
    const btnLogin = document.getElementById('btnLogin');
    const loading = document.getElementById('loginLoading');
    const logo = document.getElementById('loadingLogo');
    const title = document.getElementById('loadingTitle');
    const track = document.getElementById('loadingTrack');
    const barFill = document.getElementById('loadingBarFill');
    const balls = document.querySelectorAll('.loading-baseball');

    if (email) {
        email.addEventListener('blur', function() { validarEmail(this); });
    }
    if (password) {
        password.addEventListener('blur', function() { validarPassword(this); });
    }

    form.addEventListener('submit', function(e) {
        const valEmail = email && email.value ? validarEmail(email) : false;
        const valPass = password && password.value ? validarPassword(password) : false;

        if (!valEmail || !valPass) {
            e.preventDefault();
            Swal.fire({
                title: '❌ Error de validación',
                text: 'Corrige los campos marcados en rojo antes de continuar.',
                icon: 'error',
                confirmButtonColor: '#3085d6'
            });
            return;
        }

        if (!btnLogin || !loading) return;
        e.preventDefault();

        btnLogin.disabled = true;
        loading.classList.add('show');

        requestAnimationFrame(function() {
            logo.classList.add('show');
            setTimeout(function() { title.classList.add('show'); }, 150);
            setTimeout(function() { track.classList.add('show'); }, 300);

            var current = 0;
            var total = balls.length;
            var interval = setInterval(function() {
                if (current >= total) {
                    clearInterval(interval);
                    barFill.style.width = '100%';
                    HTMLFormElement.prototype.submit.call(form);
                    return;
                }
                balls[current].classList.add('active');
                current++;
                barFill.style.width = (current / total) * 100 + '%';
            }, 500);
        });
    });
}

function initCambiarPassword() {
    const form = document.querySelector('form:has(#password_nueva)');
    if (!form) return;

    const actual = document.getElementById('password_actual');
    const nueva = document.getElementById('password_nueva');
    const confirmar = document.getElementById('confirmar_password');
    const submitBtn = form.querySelector('[type="submit"]');

    if (nueva) {
        nueva.addEventListener('blur', function() { validarPassword(this); });
    }
    if (confirmar) {
        confirmar.addEventListener('blur', function() { validarConfirmPassword(nueva, this); });
    }

    if (submitBtn) {
        submitBtn.addEventListener('click', function(e) {
            const valActual = actual && actual.value;
            const valNueva = nueva ? validarPassword(nueva) : false;
            const valConfirm = confirmar ? validarConfirmPassword(nueva, confirmar) : false;

            if (!valActual || !valNueva || !valConfirm) {
                e.preventDefault();
                Swal.fire({
                    title: '❌ Error de validación',
                    text: 'Corrige los campos marcados en rojo.',
                    icon: 'error',
                    confirmButtonColor: '#3085d6'
                });
            }
        });
    }
}
