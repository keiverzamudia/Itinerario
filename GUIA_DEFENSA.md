# GUÍA DEFINITIVA DE DEFENSA — Sistema Itinerario

## Resumen Ejecutivo del Sistema

| Requisito del baremo | ¿Lo tienes? | Dónde |
|---|---|---|
| Contraseñas cifradas | ✅ Sí (mejor que MD5) | `werkzeug pbkdf2:sha256` en `usuario_model.py:96,142,184` |
| Sesiones de usuario | ✅ Sí | `Flask-Login` + sesión única forzada `__init__.py:113-126` |
| Bitácora | ✅ Sí (muy completa) | `bitacora_helper.py` + 40+ llamadas en 12 controladores |
| Validación frontend + backend | ✅ Sí (22 funciones JS + mixin Python) | `static/js/validacion.js` + `model/validaciones_model.py` |
| Consulta con filtros | ✅ Sí | DataTables + filtros backend + filtros de reportes progresivos |
| Confirmación antes de eliminar | ✅ Sí | SweetAlert2 en todos los módulos |
| Captcha | ✅ Sí (temático béisbol) | `auth_controller.py:20-44` + `captcha_baseball.html` |
| Reportes PDF | ✅ Sí (14 generadores) | `helpers/generators/` con KPIs, resumen ejecutivo, Top-N |
| **Vistas SQL** | ❌ **NO** | No hay `CREATE VIEW` en ningún `.sql` |
| **Procedimientos/Funciones** | ❌ **NO** | No hay `CREATE PROCEDURE` ni `CREATE FUNCTION` |
| **Triggers** | ❌ **NO** | No hay `CREATE TRIGGER` en ningún `.sql` |

---

## A. SISTEMA Y PROGRAMACIÓN (20%)

### Pregunta: "¿Qué validaciones tiene el sistema?"

**Tu respuesta:** Mi sistema tiene validación en **dos capas**:

1. **Frontend** — 22 funciones de validación en `static/js/validacion.js` (nombre, email, cédula, teléfono, fecha, RIF, costo, etc.) que aplican clases CSS `is-invalid`/`is-valid` en tiempo real. Cada módulo tiene su propio archivo en `static/js/validaciones/`:
   - `GestionUsuarioValidacion.js` — nombre, email, cédula, rol, departamento, teléfono, contraseña
   - `GestionInventarioValidacion.js` — tipo, nombre, descripción, fecha
   - `GestionPatrocinadorValidacion.js` — empresa, RIF, tipo contrato, teléfono, email
   - `GestionRolValidacion.js` — nombre, descripción
   - `GestionContratoValidacion.js` — patrocinador, tipo, fechas, monto, estatus

2. **Backend** — Un mixin reutilizable `ValidacionesMixin` en `app/model/validaciones_model.py` con métodos: `validar_obligatorio`, `validar_longitud`, `validar_email`, `validar_rif`, `validar_fecha`, `sanitizar_texto`. Los 13 modelos lo heredan.

### Pregunta: "¿Cómo funciona la seguridad?"

**Tu respuesta:** Mi sistema tiene **5 capas de seguridad**:

1. **Cifrado de contraseñas** con `werkzeug.security.generate_password_hash` (algoritmo `pbkdf2:sha256`, más seguro que MD5). El baremo pide MD5, pero usé el estándar actual de la industria.
2. **Sesiones** con Flask-Login + sesión única: si alguien inicia sesión desde otro dispositivo, la anterior se cierra automáticamente (`__init__.py:113-126`).
3. **Captcha** personalizado con temática de béisbol: genera 4 caracteres aleatorios, los renderiza como tiles rotados/coloreados, y valida server-side con `session.pop()`.
4. **CSRF** global con Flask-WTF: token oculto en los 47+ formularios del sistema.
5. **Permisos** por ruta: 13 blueprints usan `before_request` con `verificar_acceso(PERMISSION_MAP)` que verifica el código de permiso del usuario contra la BD.

### Pregunta: "¿Cómo funciona la bitácora?"

**Tu respuesta:** La bitácora está centralizada en `app/helpers/bitacora_helper.py`. Cada controlador llama a `registrar_bitacora(modulo, tipo, accion, detalle)` que inserta en la tabla `seguridad.actividad_usuario` con: usuario_id, tipo_accion, modulo, accion, detalle (JSON), página, IP y timestamp. Hay **40+ puntos de registro** en 12 controladores. El helper tiene `try/except` para que un fallo de bitácora nunca rompa la operación principal.

### Pregunta: "¿Cómo funcionan los reportes?"

**Tu respuesta:** Tengo **14 generadores PDF** heredando de `BaseReportGenerator` en `helpers/generators/`. Cada módulo tiene el suyo. Los reportes incluyen: encabezado con datos del usuario, filtros aplicados, KPIs calculados, distribuciones por categoría, resumen ejecutivo, Top-N destacados y comparativa con período anterior. El sistema tiene filtros **progresivos** (ej: seleccionar tipo de inventario filtra los estados disponibles).

---

## B. BASE DE DATOS (10%)

### Diseño de la BD

- **Dos esquemas separados**: `estadio_db` (negocio, 20 tablas) y `seguridad` (usuarios/auditoría, 15 tablas).
- **35 tablas normalizadas a 3NF** con PKs auto-increment, UNIQUE constraints e índices.
- Las tablas de catálogo (`estado_asignacion`, `estado_recurso`, `tipo_recurso`, `departamentos`) son tablas lookup correctas.
- Las FKs cross-schema (ej: `tareas.usuario_id` → `seguridad.usuarios`) se aplican en código, no en BD (MySQL no permite FKs entre esquemas).

### Índices

- **73 índices** entre ambos esquemas.
- Los más importantes:
  - `idx_usuario_leida` (notificaciones compuesto: usuario_id + leida)
  - `idx_grupo_id` (guiones por grupo)
  - `idx_mantenimientos_estado`, `idx_mantenimientos_recurso`
  - `idx_asignaciones_recurso`, `idx_asignaciones_estado`

### Concurrencia

- Tu sistema usa `autocommit(True)` por defecto y un context manager `transaction()` para escrituras multi-statement (`app/database.py:33-44`).
- El nivel de aislamiento es el default de MySQL (REPEATABLE READ).
- **No usas** `SELECT FOR UPDATE`, `LOCK TABLES` ni columnas de versión para concurrencia optimista.

### Pregunta típica: "¿Qué pasa si dos usuarios editan el mismo registro?"

**Tu respuesta:** Mi sistema maneja la concurrencia a nivel de aplicación con transacciones atómicas (`transaction()` context manager en `app/database.py`). Para escrituras multi-statement (como asignar tareas que cruza esquemas), uso una transacción que hace `commit` atómico o `rollback`. En caso de fallo, la excepción se propaga y se revierte. Para el volumen actual (~30 usuarios simultáneos), el nivel REPEATABLE READ de MySQL es adecuado.

### Pregunta: "¿Cómo haces backup y restauración?"

**Tu respuesta:**
- **Backup:** `mysqldump -u root -p estadio_db > backup_estadio_db.sql` y lo mismo para `seguridad`.
- **Restauración:** `mysql -u root -p estadio_db < backup_estadio_db.sql`.
- Para un backup completo: `mysqldump -u root -p --all-databases > backup_completo.sql`.

---

## C. INGENIERÍA DE SOFTWARE (15%)

Tu sistema tiene:

- **19 módulos** con arquitectura MVC clara (controller → model → view).
- **Chatbot** basado en reglas (sin LLM) en `helpers/chat_knowledge.py`.
- **Sistema de notificaciones** en tiempo real con SocketIO (push + badge + dropdown).
- **Dashboard** principal con widgets de acceso rápido.
- **Roles y permisos** granulares (19 blueprints, 50+ permisos, sistema many-to-many).
- **Bitácora** completa con trazabilidad de quién hace qué.

> **Nota:** Los diagramas UML, la plantilla IBM y el SRS son documentación que debes tener aparte. El código no los contiene.

---

## D. SERVIDORES Y CONCURRENCIA (5%)

### Pregunta: "¿Cómo configuraste el servidor?"

**Tu respuesta:** Mi servidor es **Flask** con **Flask-SocketIO** y **eventlet** como servidor async.

- **Desarrollo:** `run.py` ejecuta `socketio.run(app, debug=True, port=5001)`.
- **Producción:** `gunicorn -k eventlet -w 1 wsgi:app` (un solo worker porque el estado de usuarios conectados está en memoria).

**¿Por qué no Apache?** Mi sistema es Python/Flask, no PHP. Flask es un framework WSGI que incluye su propio servidor de desarrollo. En producción se usa gunicorn, que es un servidor WSGI estándar. No necesito Apache ni VirtualHost.

### Pregunta: "¿Cómo manejas los errores?"

**Tu respuesta:** Tengo 3 manejadores de error registrados en `app/__init__.py`:
- **404** — Página no encontrada
- **500** — Error interno del servidor
- **Error de conexión BD** — `pymysql.err.OperationalError`

Todos renderizan una plantilla de error estilizada (`app/view/error/error.html`). Cada operación de BD está envuelta en `try/except` que registra el error con `logger.exception()` y nunca expone trazas al usuario.

---

## E. NOTIFICACIONES EN TIEMPO REAL

- **Backend:** Tabla `seguridad.notificaciones` con campos: usuario_id, tipo, titulo, mensaje, url, leida, fecha_creacion.
- **Modelo:** `NotificacionModel` con crear, listar, contar_no_leidas, marcar_leida, marcar_todas.
- **Controlador:** API REST en `/notificaciones/api` que devuelve JSON con tiempo relativo ("hace 5 min").
- **Frontend:** Campana global en `components/head.html` con badge dinámico.
- **Push:** SocketIO emite `notificacion_nueva` a salas privadas `user_{id}`.
- **JS:** `static/js/notificaciones.js` — pull al abrir dropdown + push por socket + SweetAlert toast.

---

## F. PUNTOS QUE FALTAN Y NECESITAS CREAR (CRÍTICOS)

El baremo **exige** al menos: una vista, un trigger, y un procedimiento o función.

### 1. Vista SQL

```sql
-- Vista para reportes estadísticos de contratos
CREATE VIEW vista_resumen_contratos AS
SELECT
    c.id_contrato,
    p.nombre_empresa,
    c.tipo,
    c.monto_total,
    c.estado,
    c.estatus,
    c.fecha_inicio,
    c.fecha_fin,
    DATEDIFF(c.fecha_fin, CURDATE()) AS dias_restantes
FROM contrato c
JOIN patrocinadores p ON c.id_patrocinador = p.id_patrocinador;
```

**Cómo defenderla:** "Creé una vista que une contratos con patrocinadores para facilitar los reportes estadísticos. Permite consultar el estado, monto y días restantes de cada contrato sin repetir el JOIN en cada consulta."

### 2. Trigger (alimenta bitácora automáticamente)

```sql
-- Trigger que registra en bitácora cuando se modifica un contrato
DELIMITER //
CREATE TRIGGER trg_bitacora_contrato_update
AFTER UPDATE ON contrato
FOR EACH ROW
BEGIN
    INSERT INTO seguridad.actividad_usuario
        (usuario_id, tipo_accion, modulo, accion, detalle, created_at)
    VALUES
        (NEW.id_contrato, 'update', 'contratos', 'Modificación de contrato',
         JSON_OBJECT(
            'registro_id', NEW.id_contrato,
            'campo', 'monto_total',
            'anterior', OLD.monto_total,
            'nuevo', NEW.monto_total
         ),
         NOW());
END //
DELIMITER ;
```

**Cómo defenderlo:** "Creé un trigger que dispara automáticamente después de cada UPDATE en la tabla `contratos`. Inserta un registro en la bitácora (`actividad_usuario`) con el valor anterior y el nuevo usando `JSON_OBJECT`. Así queda trazabilidad automática de quién modificó qué dato sensible."

### 3. Procedimiento Almacenado o Función

```sql
-- Función que calcula el total de pagos de un contrato
DELIMITER //
CREATE FUNCTION total_pagos_contrato(p_id_contrato INT)
RETURNS DECIMAL(12,2)
DETERMINISTIC
BEGIN
    DECLARE v_total DECIMAL(12,2);
    SELECT IFNULL(SUM(monto), 0)
    INTO v_total
    FROM pagos
    WHERE id_contrato = p_id_contrato;
    RETURN v_total;
END //
DELIMITER ;

-- Ejemplo de uso:
-- SELECT id_contrato, nombre_empresa, total_pagos_contrato(id_contrato) AS total_pagado
-- FROM vista_resumen_contratos;
```

**Cómo defenderlo:** "Creé una función almacenada que calcula el total pagado por un contrato sumando todos sus pagos. Se puede usar directamente en consultas SQL o结合 con la vista `vista_resumen_contratos` para reportes completos."

---

## G. CHECKLIST RÁPIDO PARA LA DEFENSA

### Lo que debes demostrar EN VIVO:

- [ ] **Login** con captcha de béisbol → mostrar que rechaza si el captcha está mal
- [ ] **Sesión única** → abrir dos navegadores, iniciar sesión en ambos, mostrar que el primero se cierra
- [ ] **Dashboard** principal con widgets
- [ ] **CRUD de un módulo** (ej: inventario) → crear, editar, buscar, eliminar con SweetAlert
- [ ] **Validación** → intentar enviar un formulario vacío, mostrar errores en frontend
- [ ] **Bitácora** → ir al módulo de bitácora, mostrar registros de las acciones que acabas de hacer
- [ ] **Reportes** → generar un PDF con filtros, mostrar el archivo generado
- [ ] **Notificaciones** → asignar una tarea a otro usuario, mostrar la campana con badge
- [ ] **Roles/permisos** → mostrar que un usuario sin permiso no puede acceder a cierta ruta
- [ ] **EN VIVO** → si tienes guiones publicados, mostrar el módulo en vivo con SocketIO

### Lo que debes explicar TEÓRICAMENTE:

- [ ] **Normalización 3NF** → explica por qué separaste tablas (ej: `departamentos` es tabla lookup, no un campo en `usuarios`)
- [ ] **Índices** → explica que aceleran las búsquedas en columnas frecuentemente filtradas
- [ ] **Vista** → explica que simplifica consultas con JOINs frecuentes
- [ ] **Trigger** → explica que alimenta la bitácora automáticamente sin código de aplicación
- [ ] **Función almacenada** → explica que encapsula lógica de cálculo reutilizable
- [ ] **Transacciones** → explica el patrón `transaction()` con commit/rollback
- [ ] **Concurrencia** → explica que MySQL usa REPEATABLE READ por defecto y que para tu volumen es suficiente
- [ ] **Backup** → muestra el comando `mysqldump`

### Preguntas trampa que pueden hacerte:

1. **"¿Por qué no usaste MD5?"** → "MD5 está obsoleto y vulnerable. Usé `pbkdf2:sha256` que es el estándar actual de Werkzeug/Flask. Si el baremo requiere MD5 explícitamente, puedo cambiarlo, pero técnicamente es peor."
2. **"¿Por qué no tienes Apache?"** → "Mi stack es Python/Flask, no PHP. Flask tiene su propio servidor de desarrollo y gunicorn para producción. Apache es para PHP/Java."
3. **"¿Qué pasa si falla la BD?"** → "Tengo un error handler registrado para `pymysql.err.OperationalError` que muestra una página de error amigable. Las transacciones hacen rollback automático."
4. **"¿Cómo escalas?"** → "Actualmente uso 1 worker con estado en memoria para ~30 usuarios. Para escalar necesitaría mover el estado de SocketIO a Redis y usar múltiples workers."

---

## H. CÓMO AGREGAR LA VISTA, TRIGGER Y FUNCIÓN A TU BD

### Paso 1: Ejecutar el SQL

```bash
mysql -u root -p estadio_db < sql_defensa.sql
```

### Paso 2: El archivo `sql_defensa.sql`

Contiene los 3 objetos SQL listos para ejecutar (vista + trigger + función).

### Paso 3: Verificar

```sql
-- Ver la vista
SELECT * FROM vista_resumen_contratos LIMIT 5;

-- Ver la función
SELECT total_pagos_contrato(1);

-- Ver los triggers
SHOW TRIGGERS FROM estadio_db;
```

---

## I. ESTRUCTURA DEL SISTEMA (para estudiar)

```
app/
├── __init__.py          # create_app(), 19 blueprints, SocketIO, CSRF, sesión única
├── config.py            # DATABASE_CONFIG (lee .env)
├── database.py          # Database.get_connection(), transaction()
├── controller/          # 19 controladores Flask (uno por módulo)
├── model/               # 19 modelos con setters validadores + SQL
├── helpers/             # decorators, bitacora, reportes, chat, email
├── view/                # Templates HTML (un subdirectorio por módulo)
└── static/
    ├── js/              # 28 archivos JS (Gestion*.js por módulo)
    └── css/             # Estilos por módulo

estadio_db.sql           # Esquema de negocio (20 tablas)
seguridad.sql            # Esquema de seguridad (15 tablas)
```

**19 módulos:** Auth, Dashboard, Usuarios, Guiones, En Vivo, Mantenimiento, Premios, Contratos, Balance, Tareas, Patrocinadores, Bitácora, Roles, Inventario, Reels, Reportes, Chat, Notificaciones, Ayuda.
