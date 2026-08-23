# Checklist de mejoras — Itinerario

Plan priorizado para atacar las deudas del proyecto. Marcar `[x]` al completar.
Referencias verificadas en código; si algo cambió, actualizar esta lista.

## ✅ Fase 1 · Seguridad (COMPLETA)
- [x] SECRET_KEY sin fallback — falla al arrancar si falta (`app/__init__.py`)
- [x] CORS de sockets same-origin + `SOCKET_ALLOWED_ORIGINS` opcional
- [x] Handshake SocketIO autenticado contra sesión Flask-Login
- [x] Validación anti open-redirect de `next` en login (`auth_controller.py`)

## 🧪 Fase 2 · Tests (red de seguridad)
- [x] Setup: `pytest` instalado + `tests/conftest.py` (BDs `*_test` clonadas desde los `.sql`, CSRF off, email parcheado)
- [x] Tests validaciones puras (`ValidacionesMixin`) — `tests/test_validaciones.py`
- [x] Helpers reportes (`_parsear_fecha`, `_ordenar_datos`, `_filtrar_por_fecha`, `_formatear_tiempo`) — `tests/test_reportes_helpers.py`
- [x] Tests auth: login ok/fallido, CAPTCHA, sesión única, reset password, validación de `next` — `tests/test_auth.py`
- [x] Tests permisos: anon → login, sin permiso → rechazo, Superadmin → 200 — `tests/test_permisos.py`
- [ ] Tests transacciones compuestas (contrato+pagos): fallo a mitad → nada escrito
- [ ] Tests PDFs: bytes empiezan con `%PDF-` por módulo
- Correr con: `venv/bin/pytest -q` (24 tests verdes al cerrar esta fase). NUNCA contra BDs reales.

## 🔧 Fase 3 · Refactor (mismo comportamiento, menos código)
- [ ] Extraer `_registrar_bitacora` → `app/helpers/bitacora_helper.py` (12 copias hoy)
- [ ] Dividir `reportes_controller.py` (1.213 líneas): `_obtener_datos()` por módulo + helpers a `reportes_utils.py`
- [ ] Errores silenciosos: log real en los ~100 `except Exception` (archivo por archivo, modelos primero)

## 📊 Fase 4 · Módulo Reportes (patrón "efecto bitácora")
Referencia completa: bitácora, contratos, inventario. Receta y convenciones en
`.opencode/reportes-context.md`. De a UN módulo end-to-end antes del siguiente.

- [ ] **guiones**: encargado específico AJAX + rango `elementos_min/max` + progresividad
- [ ] **premios**: progresividad estado→patrocinador + rangos `cantidad_min/max`, `cantidad_entregada_min/max`
- [ ] **balance**: fix preview columna `referencia` NULL
- [ ] **tareas**: fix key inconsistente `Estado`→`estado` + progresividad estado→usuario
- [ ] **patrocinadores**: filtro activo/inactivo + renombrar `estado_filter`
- [ ] **usuarios**: progresividad departamento→rol + filtro activo sí/no
- [ ] **mantenimiento**: rango costo o días
- [ ] **reels**: rangos `duracion_min/max` (segundos)
- [ ] PDF análisis nuevo en `BaseReportGenerator`: resumen ejecutivo (`resumen=True`), Top-N (`top_n_analisis=N`), comparativa períodos (`comparar=True`)
- [ ] Actualizar `.opencode/reportes-context.md` al cerrar cada módulo

## ☁️ Fase 5 · Escalabilidad (opcional, solo si cambia el despliegue)
- [ ] Presencia SocketIO del dict global a Redis/BD si hay >1 worker
