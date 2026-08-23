# AGENTS.md — Guía del proyecto Itinerario

Guía de orientación para agentes IA. Léela antes de tocar código. Si algo de aquí contradice el código real, manda el código: verifica y actualiza esta guía.

## Qué es

Sistema web de gestión operativa del **Estadio Antonio Herrera Gutiérrez** (béisbol): guiones de shows en vivo, estado on-air, inventario, contratos/patrocinadores, premios, balance, tareas, mantenimiento, reels, usuarios/roles/permisos, bitácora, reportes PDF y un asistente chat basado en reglas (sin LLM). Migración de PHP a Flask.

## Stack y cómo correr

- Python 3 + Flask 3 (app factory), PyMySQL crudo (**sin ORM**), Flask-Login, Flask-WTF (CSRF), Flask-SocketIO + eventlet, reportlab (PDFs).
- BD MySQL: dos esquemas — `estadio_db` (negocio) y `seguridad` (usuarios/roles/sesiones). Esquema completo en `estadio_db.sql` y `seguridad.sql` de la raíz.
- Config por `.env` (ver `.env.example`): SECRET_KEY, DB_*, MAIL_*.
- Dev: `venv/bin/python run.py` → http://localhost:5001. Prod: `gunicorn -k eventlet -w 1 wsgi:app`.
- Instalar deps: `venv/bin/pip install -r requirements.txt`.

## Mapa de directorios

```
run.py / wsgi.py        # arranque dev / prod
app/__init__.py          # create_app(): registra 17 blueprints, CSRF, SocketIO,
                         # presencia global (usuarios_conectados), sesión única
app/config.py            # DATABASE_CONFIG (lee .env)
app/database.py          # Database.get_connection('estadio_db'|'seguridad'),
                         # transaction() contextmanager, DictCursor, autocommit ON
app/controller/          # Rutas Flask, UN blueprint por módulo (bp)
app/model/               # Clases con setters validadores (ValidacionesMixin) + SQL
app/helpers/             # decorators.py (permiso_requerido, verificar_acceso),
                         # permission_map.py, email_service.py,
                         # generators/ (12 generadores PDF + base_report.py),
                         # chat_knowledge.py (reglas del asistente)
app/view/                # Templates HTML (un subdirectorio por módulo)
app/static/js|css        # JS/CSS por módulo (Gestion*.js); validaciones JS en
                         # static/js/validaciones/ (solo UX, NO reemplazan server-side)
docs/                    # ARQUITECTURA_INVENTARIO.md, GUIA_DEFENSA.md,
                         # GUION_Y_ENVIVO_GUIA.md
.opencode/skills/        # Skills: seguridad, db-transacciones, refactor-controladores,
                         # tests-pytest, reportes-pdf, reportes-detallados
.opencode/reportes-context.md  # Estado detallado del sistema de reportes
```

## Arquitectura en una mirada

1. **Flujo MVC:** ruta en `controller/<modulo>_controller.py` → modelo en `model/<modulo>_model.py` (setters validan) → template en `view/<modulo>/`. Sin capa servicios.
2. **BD:** conexión por request en `flask.g`, teardown cierra sola. Autocommit activo: escrituras multi-statement DEBEN usar `with transaction():`.
3. **Auth:** Flask-Login + hash werkzeug; CAPTCHA propio en login; sesión única forzada en `before_request` (`verificar_sesion_unica`) contra `SesionModel`.
4. **Permisos:** cada ruta usa `@permiso_requerido('<codigo>')` o `verificar_acceso(PERMISSION_MAP)` como before_request del blueprint. Códigos en `permission_map.py`; seed en `RolModel.seed_permisos_iniciales()`.
5. **Bitácora:** acciones registradas vía `_registrar_bitacora(...)` en cada controlador (hoy duplicado — ver skill refactor-controladores).
6. **Tiempo real:** SocketIO para presencia y estados en_vivo. `usuarios_conectados` es un dict global en memoria (solo válido con `-w 1`). El handshake NO está autenticado aún (deuda conocida).
7. **Reportes PDF:** dashboard progresivo (`view/reportes/dashboard.html` + `static/js/GestionReportes.js`) → `reportes_controller.generar()` → generador por módulo en `helpers/generators/` heredando `BaseReportGenerator`. PDFs se guardan en `static/reportes/YYYY/MM/` y se registran en `ReporteModel`.

## Reglas anti-alucinación (obligatorias)

- **Nunca inventes tablas, columnas ni campos.** Antes de escribir SQL o modelos, confirma nombres reales en `app/model/*.py`, en los `.sql` de la raíz o leyendo la tabla real.
- No asumas que existe una librería: revisa `requirements.txt` primero. Nada nuevo sin justificarlo.
- UI, mensajes, comentarios y commits **en español** (así está todo el proyecto).
- Las validaciones JS no cuentan: toda escritura valida también en servidor.
- Los tests corren contra BDs de test (`*_test`), nunca contra las reales. Suite base en `tests/` (conftest clona los `.sql` a `estadio_db_test`/`seguridad_test`); correr con `venv/bin/pytest -q` y ver `CHECKLIST.md`.
- No toques `venv/`, `__pycache__/`, `.DS_Store`, `run.py.bak`.

## Cómo extender (recetas cortas)

- **Ruta nueva:** crear endpoint en el blueprint del módulo con su decorador de permiso; POST valida server-side y registra bitácora.
- **Módulo nuevo:** controller con `bp` + model + view + registro en `create_app()` + entrada en permisos.
- **Filtro de reporte:** seguir la receta de `.opencode/reportes-context.md` (backend `_filtros_<modulo>` + sección `_obtener_datos` + `MODULE_CONFIG.<modulo>` en JS). Convenciones: `progressive` en filtro origen, `dependsOn` en destino, primer option `value=""` = "Todos...".
- **Generador PDF nuevo:** clase en `helpers/generators/<modulo>_report.py` extendiendo `BaseReportGenerator` (MODULO, TITULO, COLUMNAS, `_build_rows`) + registro en el dict `generadores` de `generar()`.

## Deudas conocidas (no reintroducirlas, atacarlas al tocar el archivo)

SocketIO sin auth + CORS `"*"` · SECRET_KEY con fallback hardcodeado · open redirect en `next` del login · `except Exception: pass` silenciosos · `_registrar_bitacora` duplicado en ~15 controladores · `reportes_controller.py` ~1.200 líneas · presencia SocketIO no escala a múltiples workers. (Resueltas: SECRET_KEY, CORS, auth de sockets, open redirect — ver `CHECKLIST.md`.)
