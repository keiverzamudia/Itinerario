# GUIA DEFINITIVA DE DEFENSA — v2.0 Actualizada

## Sistema: Itinerario — Estadio Antonio Herrera Gutierrez

---

## CHECK RAPIDO: CUMPLIMIENTO DEL BAREMO

| # | Requisito | Estado | Ubicacion |
|---|-----------|--------|-----------|
| 1 | Contrasenas cifradas | ✅ | `werkzeug pbkdf2:sha256` → `usuario_model.py` |
| 2 | Sesiones de usuario | ✅ | Flask-Login + sesion unica → `__init__.py:113-126` |
| 3 | Bitacora del sistema | ✅ | `bitacora_helper.py` + 40+ puntos en 12 controladores |
| 4 | Validacion frontend + backend | ✅ | 22 funcs JS (`validacion.js`) + mixin Python |
| 5 | Consulta con filtros | ✅ | DataTables + filtros backend + filtros progresivos |
| 6 | Confirmacion antes de eliminar | ✅ | SweetAlert2 en todos los modulos CRUD |
| 7 | Captcha | ✅ | Captcha de beisbol custom → `auth_controller.py` |
| 8 | Reportes PDF parametrizados | ✅ | 14 generadores con KPIs y Top-N |
| 9 | Vista SQL | ✅ | `v_balance_contratos` |
| 10 | Trigger | ✅ | `trg_pagos_after_insert` + `trg_pagos_after_update` |
| 11 | Procedimiento almacenado | ✅ | `sp_resumen_financiero` |
| 12 | Respaldo de BD | ✅ | Boton "Respaldar BD" en Roles |

---

## A. SISTEMA Y PROGRAMACION (20%)

### A.1 Validaciones — Doble capa

**Frontend** — 22 funciones en `static/js/validacion.js`:
- `validarNombre`, `validarEmail`, `validarPassword`, `validarCedula`
- `validarTelefono`, `validarFecha`, `validarHora`, `validarSelect`
- `validarTexto`, `validarTextoLargo`, `validarDescripcion`
- `validarRif`, `validarCosto`, `validarCantidad`, `validarCodigo`
- Cada modulo tiene su archivo: `GestionUsuarioValidacion.js`, `GestionInventarioValidacion.js`, `GestionPatrocinadorValidacion.js`, `GestionRolValidacion.js`, `GestionContratoValidacion.js`

**Backend** — `ValidacionesMixin` en `model/validaciones_model.py`:
- `validar_obligatorio`, `validar_longitud`, `validar_email`, `validar_rif`, `validar_fecha`, `sanitizar_texto`
- Los 13 modelos lo heredan y cada uno tiene `_validar_datos_*()`

### A.2 Seguridad — 5 capas

1. **Cifrado**: `pbkdf2:sha256` via Werkzeug (mas seguro que MD5)
2. **Sesiones**: Flask-Login + sesion unica forzada en `before_request`
3. **Captcha**: 4 tiles rotados/coloreados, validacion server-side con `session.pop()`
4. **CSRF**: Flask-WTF global, token en 47+ formularios
5. **Permisos**: `before_request` con `verificar_acceso(PERMISSION_MAP)` en 13 blueprints

### A.3 Bitacora — Trazabilidad completa

- **Tabla**: `seguridad.actividad_usuario` (usuario_id, tipo_accion, modulo, accion, detalle JSON, pagina, ip, timestamp)
- **Helper centralizado**: `bitacora_helper.registrar_bitacora(modulo, tipo, accion, detalle)`
- **40+ puntos de registro** en 12 controladores
- **Respaldo DB-level**: Triggers en `pagos` alimentan la misma tabla automaticamente
- **Dashboard**: Muestra rol del usuario junto al nombre + icono de ojo para ver detalle

### A.4 Reportes PDF — 14 generadores

Cada modulo tiene su generador heredando de `BaseReportGenerator`:
- Encabezado con datos del usuario y filtros aplicados
- KPIs calculados (totales, promedios, porcentajes)
- Distribuciones por categoria
- Resumen ejecutivo + Top-N + Comparativa de periodos
- **Filtros progresivos**: seleccionar tipo → filtra estados disponibles

---

## B. BASE DE DATOS (10%)

### B.1 Diseno

- **2 esquemas**: `estadio_db` (20 tablas, negocio) + `seguridad` (15 tablas, usuarios/auditoria)
- **35 tablas en 3NF** con PKs auto-increment, UNIQUE constraints
- **73 indices** entre ambos esquemas
- Tablas lookup: `estado_asignacion`, `estado_recurso`, `tipo_recurso`, `departamentos`
- FKs cross-schema aplicadas en codigo (MySQL no permite FKs entre esquemas)

### B.2 Vista SQL — `v_balance_contratos`

```sql
-- Une contratos + patrocinadores + pagos en una sola vista
-- Devuelve: monto_total, monto_pagado, saldo_pendiente, porcentaje_pagado, cantidad_pagos
SELECT * FROM v_balance_contratos WHERE estatus_contrato = 'Vigente';
```

**Como defenderla:** "Creé una vista que responde la pregunta mas frecuente del negocio: 'cuanto ha pagado cada patrocinador vs. lo contratado?' Sin repetir el JOIN de 3 tablas en cada consulta."

### B.3 Triggers — Auditoria financiera en `pagos`

- `trg_pagos_after_insert`: Captura cada pago nuevo → inserta en `actividad_usuario`
- `trg_pagos_after_update`: Captura modificaciones (monto, estado, referencia) → inserta diff antes/despues en JSON

**Como defenderlo:** "Los pagos son los datos mas sensibles (dinero). Los triggers son la segunda linea de defensa: aunque alguien ejecute SQL directo, queda la trazabilidad automatica en la bitacora."

### B.4 Procedimiento — `sp_resumen_financiero(fecha_inicio, fecha_fin)`

Devuelve 4 result sets en 1 sola llamada:
1. Resumen de contratos (total, vigentes, vencidos)
2. Pagos recibidos (total, promedio, mayor)
3. Top-10 patrocinadores por monto pagado
4. Contratos por vencer (proximos 30 dias)

**Como defenderlo:** "Un solo `CALL sp_resumen_financiero('2026-01-01', '2026-12-31')` genera todo el dashboard financiero. Evita 4 round-trips a la BD."

### B.5 Respaldo de BD

- Boton "Respaldar BD" en el modulo de Roles y Permisos
- Ejecuta `mysqldump` server-side y descarga el archivo `.sql`
- Solo respalda `estadio_db` (esquema de negocio)

**Como defenderlo:** "Desde el sistema mismo, cualquier administrador puede generar un respaldo completo de la base de datos de negocio con un click. El archivo se descarga automaticamente."

### B.6 Concurrencia

- `autocommit(True)` por defecto + `transaction()` context manager para multi-statement
- Nivel de aislamiento: REPEATABLE READ (default MySQL)
- Para ~30 usuarios simultaneos es suficiente

**Pregunta trampa:** "Que pasa si dos usuarios editan el mismo registro?"
**Respuesta:** "Uso transacciones atomicas con commit/rollback. Para este volumen, REPEATABLE READ es adecuado."

---

## C. INGENIERIA DE SOFTWARE (15%)

- **19 modulos** con arquitectura MVC clara
- **Chatbot** basado en reglas (sin LLM) en `helpers/chat_knowledge.py`
- **Notificaciones** en tiempo real: SocketIO push + badge + dropdown
- **Roles y permisos**: 52 permisos, sistema many-to-many
- **Bitacora** completa con trazabilidad

---

## D. SERVIDORES Y CONCURRENCIA (5%)

- **Flask** + **Flask-SocketIO** + **eventlet**
- Dev: `run.py` → `socketio.run(app, debug=True, port=5001)`
- Prod: `gunicorn -k eventlet -w 1 wsgi:app`
- No Apache (stack Python, no PHP)

**Error handlers**: 404, 500, y error de conexion BD → todos renderizan `error.html`

---

## E. NOTIFICACIONES EN TIEMPO REAL

- Tabla `seguridad.notificaciones` + `NotificacionModel`
- API REST: `GET /notificaciones/api` → JSON con tiempo relativo
- Push: SocketIO `notificacion_nueva` → salas privadas `user_{id}`
- Frontend: Campana en `head.html` + `notificaciones.js` (pull + push + toast)

---

## F. CAMBIOS REALIZADOS — SESION COMPLETA

### F.1 Bitacora mejorada

- **Archivo**: `app/view/bitacora/dashboard.html`
- **Cambio**: Badge de rol junto al nombre del usuario
- **Cambio**: Icono de ojo al lado de la fecha que lleva al reporte de usuario

### F.2 Respaldo de BD

- **Archivos modificados**:
  - `app/controller/rol_controller.py` → nueva ruta `POST /roles/respaldo`
  - `app/helpers/permission_map.py` → nuevo permiso `rol.respaldo`
  - `app/view/rol/dashboard.html` → boton "Respaldar BD" + funcion JS con SweetAlert
- **Funcionamiento**: SweetAlert confirma → `mysqldump` genera archivo → descarga automatica

### F.3 Objetos SQL para la defensa

- **Vista**: `v_balance_contratos` (contratos + patrocinadores + pagos)
- **Triggers**: `trg_pagos_after_insert` y `trg_pagos_after_update` (auditoria financiera)
- **Procedimiento**: `sp_resumen_financiero(fecha_inicio, fecha_fin)` (4 result sets)

### F.4 Validaciones alineadas

| Archivo | Cambio |
|---------|--------|
| `static/js/validacion.js` | `validarNombre`: minimo 2→3 |
| `static/js/GestionMantenimiento.js` | diagnostico minimo 3→10 |
| `static/js/validaciones/GestionInventarioValidacion.js` | Agregada validacion de costo |
| `model/mantenimiento_model.py` | `modificar()` valida diagnostico y observaciones |
| `model/guion_model.py` | `modificar()` elementos valida contenido, hora, inning |
| `model/premio_model.py` | `_validar_datos_premio()` valida cantidad |

### F.5 Fix: Bugs de reportes (6 fixes)

| Bug | Archivo | Fix |
|-----|---------|-----|
| Bitacora PDF mostraba `accion` en vez de `detalle` | `bitacora_report.py:48` | Cambiado a `d.get('detalle')` |
| Mantenimiento PDF faltaba columna "Dias" | `mantenimiento_report.py` | Agregada columna `dias_en_taller` |
| Fechas NULL siempre incluidas con filtro activo | `reportes_utils.py:40` | Excluidas cuando hay filtro de fecha |
| Formato inconsistente date vs datetime | `reportes_controller.py:514` | Check `isinstance(v, date)` |
| Contratos filtro fecha solo revisaba `fecha_inicio` | `reportes_data.py:350` | Verifica solapamiento inicio↔fin |
| base_report.py mutaba dict del caller | `base_report.py` | `filtros.pop` → `filtros.get` |

### F.6 Reels — Duracion en segundos

- `duracion_total` ahora en SECONDS (convertido desde minutos)
- Vista detalle muestra duracion planificada vs consumida con barra de progreso

### F.7 Patrocinador — RIF separado

- RIF separado en selector V/E/J/G + numeros separados
- `nombre_contacto` ahora requerido con validacion

### F.8 Constructor report — Error con detalle

- Error response ahora incluye campo `detalle` para debugging
- Frontend muestra el detalle en SweetAlert de error

### F.9 Seed data realista

- **10 patrocinadores** — Empresas venezolanas reales
- **10 contratos** — Montos desde $8,000 hasta $150,000
- **14 pagos** — Pagos parciales con referencias
- **6 guiones** con 30 elementos (programacion completa)
- **6 usuarios** con passwords `password123`

---

## G. CHECKLIST DE DEFENSA

### Demostrar EN VIVO:

1. Login con captcha → mostrar rechazo si captcha mal
2. Sesion unica → 2 navegadores, mostrar cierre automatico
3. CRUD completo (ej: inventario) → crear, editar, buscar, eliminar con SweetAlert
4. Validacion → enviar formulario vacio, mostrar errores inline
5. Bitacora → ir al modulo, mostrar registros de acciones recientes + rol + ojito
6. Reportes → generar PDF con filtros, mostrar archivo
7. Notificaciones → asignar tarea, mostrar campana con badge
8. Roles/permisos → mostrar acceso restringido
9. Respaldo BD → boton en Roles, descargar archivo .sql
10. Objetos SQL → mostrar vista, triggers y procedimiento en MySQL

### Explicar TEORICAMENTE:

- Normalizacion 3NF (ej: `departamentos` es tabla lookup)
- Indices (73 total, aceleran busquedas)
- Vista (simplifica JOINs frecuentes)
- Trigger (auditoria automatica sin codigo de aplicacion)
- Procedimiento (encapsula logica reutilizable)
- Transacciones (`transaction()` con commit/rollback)
- Concurrencia (REPEATABLE READ, suficiente para ~30 usuarios)
- Backup (desde el sistema con `mysqldump`)

### Preguntas trampa:

1. **"Por que no MD5?"** → "Esta obsoleto. Use pbkdf2:sha256, estandar actual."
2. **"Por que no Apache?"** → "Stack Python/Flask, no PHP. Gunicorn para produccion."
3. **"Que pasa si falla la BD?"** → "Error handler + rollback automatico en transacciones."
4. **"Como escalas?"** → "Mover SocketIO a Redis + multiples workers."

---

## H. ESTRUCTURA DEL SISTEMA

```
app/
├── __init__.py          # create_app(), 19 blueprints, SocketIO, CSRF
├── config.py            # DATABASE_CONFIG (lee .env)
├── database.py          # Database.get_connection(), transaction()
├── controller/          # 19 controladores (uno por modulo)
├── model/               # 19 modelos con validadores + SQL
├── helpers/             # decorators, bitacora, reportes, chat
├── view/                # Templates HTML por modulo
└── static/js/           # 28 archivos JS (Gestion*.js)

estadio_db.sql           # 20 tablas + vista + triggers + procedimiento
seguridad.sql            # 15 tablas (usuarios, roles, bitacora, etc.)
```

**19 modulos:** Auth, Dashboard, Usuarios, Guiones, En Vivo, Mantenimiento, Premios, Contratos, Balance, Tareas, Patrocinadores, Bitacora, Roles, Inventario, Reels, Reportes, Chat, Notificaciones, Ayuda.

---

## I. USUARIOS DE PRUEBA

| Email | Contrasena | Rol |
|-------|-----------|-----|
| keiver@cardenales.com | password123 | Superadmin |
| carlos@mendoza.com | password123 | Superadmin |
| ana.perez@outlook.com | password123 | Administrador |
| genesis@cardenales.com | password123 | Administrador |
| maria.gonzalez@gmail.com | password123 | Usuario |
| roberto.diaz@hotmail.com | password123 | Usuario |

---

*Ultima actualizacion: 18 de septiembre 2026*
