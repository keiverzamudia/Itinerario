/* app/static/js/GestionAyuda.js — Búsqueda y filtrado del Centro de Ayuda */
document.addEventListener('DOMContentLoaded', function () {
    var busqueda = document.getElementById('busquedaAyuda');
    var botones  = document.querySelectorAll('.btn-filtro');
    var grupos   = document.querySelectorAll('.grupo-categoria');
    var items    = document.querySelectorAll('.item-pregunta');
    var sinResultados = document.getElementById('sinResultados');
    var activo   = 'todas';

    function normalizar(t) {
        return t.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    }

    function aplicarFiltro() {
        var q = normalizar(busqueda.value.trim());
        var visibles = 0;

        grupos.forEach(function (grupo) {
            var cat = grupo.dataset.categoria;
            var coincideCat = activo === 'todas' || cat === activo;
            var preguntasGrupo = grupo.querySelectorAll('.item-pregunta');
            var visiblesGrupo = 0;

            preguntasGrupo.forEach(function (item) {
                var texto = normalizar(item.dataset.pregunta || '');
                var coincideTexto = !q || texto.indexOf(q) !== -1;
                var visible = coincideCat && coincideTexto;
                item.classList.toggle('d-none', !visible);
                if (visible) visiblesGrupo++;
            });

            grupo.classList.toggle('d-none', visiblesGrupo === 0);
            visibles += visiblesGrupo;
        });

        if (sinResultados) {
            sinResultados.classList.toggle('d-none', visibles > 0);
            sinResultados.classList.toggle('d-block', visibles === 0);
        }
    }

    if (busqueda) {
        busqueda.addEventListener('input', aplicarFiltro);
    }

    botones.forEach(function (btn) {
        btn.addEventListener('click', function () {
            botones.forEach(function (b) {
                b.classList.remove('btn-primary', 'activo');
                b.classList.add('btn-outline-secondary');
            });
            btn.classList.add('btn-primary', 'activo');
            btn.classList.remove('btn-outline-secondary');
            activo = btn.dataset.categoria;
            aplicarFiltro();
        });
    });
});