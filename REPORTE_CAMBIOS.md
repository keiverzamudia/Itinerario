# REPORTE DE CAMBIOS PENDIENTES — Para Aprobación

---

## PARTE 1: CAMBIOS EN BITÁCORA

### 1.1 Agregar Rol junto al nombre del usuario

**Archivo:** `app/view/bitacora/dashboard.html`

**Cambio actual (línea ~76 del template):**
```html
<td>
    {% if act.usuario %}
    <a href="...">{{ act.usuario.nombre }}</a>
    {% else %}
    <span class="text-muted">Usuario #{{ act.usuario_id }}</span>
    {% endif %}
</td>
```

**Cambio propuesto:**
```html
<td>
    {% if act.usuario %}
    <a href="...">{{ act.usuario.nombre }}</a>
    <span class="badge bg-primary bg-opacity-10 text-primary ms-1 small">{{ act.usuario.rol }}</span>
    {% else %}
    <span class="text-muted">Usuario #{{ act.usuario_id }}</span>
    {% endif %}
</td>
```

**Resultado visual:** `Keiver Zamudia` + chip `Administrador` al lado.

---

### 1.2 Agregar ojito (icono de ojo) al lado de la fecha

**Archivo:** `app/view/bitacora/dashboard.html`

**Cambio actual (línea ~82 del template):**
```html
<td class="small text-muted">{{ act.created_at.strftime('%d/%m %H:%M') if act.created_at else '' }}</td>
```

**Cambio propuesto:**
```html
<td class="small text-muted">
    {{ act.created_at.strftime('%d/%m %H:%M') if act.created_at else '' }}
    <a href="{{ url_for('bitacora.reporte_usuario', usuario_id=act.usuario_id) }}"
       class="ms-2 text-primary" title="Ver actividad de {{ act.usuario.nombre if act.usuario else 'este usuario' }}">
        <i class="fas fa-eye"></i>
    </a>
</td>
```

**Resultado visual:** `17/09 21:10` + ojito azul que lleva al reporte de usuario.

---

### 1.3 Agregar búsqueda por nombre de usuario en el dashboard

**Archivo:** `app/view/bitacora/dashboard.html`

**Cambio:** Agregar un campo de búsqueda junto al select de usuario para filtrar actividades por nombre de usuario (ya existe el select, solo agregar un input de texto que filtre la tabla DataTable).

**Nota:** DataTables ya tiene búsqueda integrada, así que esto ya funciona con el `class="datatable"`.

---

## PARTE 2: RESPALDO DE BASE DE DATOS

### 2.1 Ruta nueva en el controlador

**Archivo:** `app/controller/rol_controller.py`

**Nuevo endpoint:**
```python
@bp.route('/respaldo', methods=['POST'], endpoint='respaldo')
def respaldo():
    # Genera mysqldump de estadio_db
    # Guarda en static/reportes/backups/
    # Retorna el archivo para descarga
```

**Flujo:**
1. Recibe POST con `csrf_token` (ya protegido)
2. Ejecuta `mysqldump` via `subprocess` del esquema `estadio_db`
3. Guarda el archivo como `estadio_db_backup_YYYYMMDD_HHMMSS.sql`
4. Retorna el archivo como descarga (`send_file`)
5. Registra en bitácora

### 2.2 Botón en el template de Roles

**Archivo:** `app/view/rol/dashboard.html`

**Cambio:** Agregar botón "Respaldar BD" al lado de "Crear Rol" en el header:
```html
<a href="...crear" class="btn btn-primary">Crear Rol</a>
<button class="btn btn-success" onclick="respaldarBD()">
    <i class="fas fa-database me-1"></i>Respaldar BD
</button>
```

### 2.3 JavaScript para el respaldo

**Archivo:** `app/static/js/GestionRol.js` (o inline en el template)

**Función:**
```javascript
function respaldarBD() {
    Swal.fire({
        title: '¿Crear respaldo completo?',
        text: 'Se descargará un archivo .sql con toda la base de datos estadio_db',
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#28a745',
        confirmButtonText: 'Sí, respaldar'
    }).then((result) => {
        if (result.isConfirmed) {
            // POST a /roles/respaldo con CSRF token
            // Descargar el archivo
        }
    });
}
```

### 2.4 Permiso necesario

Agregar `'rol.respaldo': 'rol.edit'` al diccionario `ROL` en `app/helpers/permission_map.py` (opcional, o reutilizar `rol.edit`).

---

## PARTE 3: OBJETOS SQL PARA LA DEFENSA (Vista + Trigger + Procedimiento)

### 3.1 VISTA: `v_balance_contratos`

**¿Por qué?** El módulo de reportes y balance necesita constantemente la pregunta: "¿cuánto ha pagado cada patrocinador vs. lo contratado?" Esta vista Elimina el JOIN de 3 tablas + SUM + GROUP BY que se repite en Python.

```sql
CREATE OR REPLACE VIEW estadio_db.v_balance_contratos AS
SELECT
    c.id_contrato,
    p.id_patrocinador,
    p.nombre_empresa,
    p.rif,
    c.fecha_inicio,
    c.fecha_fin,
    c.tipo,
    c.estado AS estado_contrato,
    c.estatus AS estatus_contrato,
    c.monto_total,
    COALESCE(SUM(pg.monto), 0) AS monto_pagado,
    c.monto_total - COALESCE(SUM(pg.monto), 0) AS saldo_pendiente,
    CASE
        WHEN c.monto_total = 0 THEN 0
        ELSE ROUND(COALESCE(SUM(pg.monto), 0) / c.monto_total * 100, 1)
    END AS porcentaje_pagado,
    COUNT(pg.id_pago) AS cantidad_pagos,
    MAX(pg.fecha_pago) AS ultimo_pago
FROM estadio_db.contrato c
JOIN estadio_db.patrocinadores p ON p.id_patrocinador = c.id_patrocinador
LEFT JOIN estadio_db.pagos pg ON pg.id_contrato = c.id_contrato
GROUP BY
    c.id_contrato, p.id_patrocinador, p.nombre_empresa, p.rif,
    c.fecha_inicio, c.fecha_fin, c.tipo, c.estado, c.estatus, c.monto_total;
```

**Uso:** `SELECT * FROM v_balance_contratos WHERE estatus_contrato = 'Vigente'`

---

### 3.2 TRIGGER: Auditoría financiera en pagos

**¿Por qué?** Los pagos son los datos más sensibles del sistema (dinero). Un trigger en MySQL captura cambios aunque alguien bypass el código de la aplicación.

```sql
DELIMITER //

-- Trigger AFTER INSERT: captura cada pago nuevo
CREATE TRIGGER trg_pagos_after_insert
AFTER INSERT ON estadio_db.pagos
FOR EACH ROW
BEGIN
    INSERT INTO seguridad.actividad_usuario
        (usuario_id, tipo_accion, modulo, accion, detalle, created_at)
    VALUES
        (NEW.registrado_por, 'insert', 'pago_audit',
         CONCAT('Pago #', NEW.id_pago, ' registrado: $', NEW.monto),
         JSON_OBJECT(
             'tabla', 'pagos',
             'registro_id', NEW.id_pago,
             'monto', NEW.monto,
             'tipo_pago', NEW.tipo_pago,
             'referencia', NEW.referencia,
             'estado', NEW.estado,
             'id_contrato', NEW.id_contrato
         ),
         NOW());
END//

-- Trigger AFTER UPDATE: captura modificaciones a pagos existentes
CREATE TRIGGER trg_pagos_after_update
AFTER UPDATE ON estadio_db.pagos
FOR EACH ROW
BEGIN
    IF OLD.monto != NEW.monto
       OR OLD.estado != NEW.estado
       OR OLD.referencia != NEW.referencia
       OR OLD.tipo_pago != NEW.tipo_pago THEN
        INSERT INTO seguridad.actividad_usuario
            (usuario_id, tipo_accion, modulo, accion, detalle, created_at)
        VALUES
            (NEW.registrado_por, 'update', 'pago_audit',
             CONCAT('Pago #', NEW.id_pago, ' modificado'),
             JSON_OBJECT(
                 'tabla', 'pagos',
                 'registro_id', NEW.id_pago,
                 'monto_antes', OLD.monto, 'monto_despues', NEW.monto,
                 'estado_antes', OLD.estado, 'estado_despues', NEW.estado,
                 'referencia_antes', OLD.referencia, 'referencia_despues', NEW.referencia,
                 'tipo_pago_antes', OLD.tipo_pago, 'tipo_pago_despues', NEW.tipo_pago
             ),
             NOW());
    END IF;
END//

DELIMITER ;
```

**Cómo defenderlo:** "Creé dos triggers en la tabla `pagos` que actúan como segunda línea de defensa de auditoría financiera. Capturan INSERTs y UPDATEs, y escriben directamente en la tabla de bitácora `actividad_usuario` con los valores antes/después en formato JSON. Esto garantiza trazabilidad aunque alguien ejecute SQL directo."

---

### 3.3 PROCEDIMIENTO ALMACENADO: Resumen financiero

**¿Por qué?** El dashboard de balance necesita 4 consultas diferentes en una sola vista. Un procedimiento las ejecuta todas en un solo llamado.

```sql
DELIMITER //

CREATE PROCEDURE estadio_db.sp_resumen_financiero(
    IN p_fecha_inicio DATE,
    IN p_fecha_fin DATE
)
BEGIN
    -- 1. Resumen de contratos en el rango
    SELECT
        COUNT(*) AS total_contratos,
        SUM(monto_total) AS monto_total_contratado,
        SUM(CASE WHEN estatus = 'Vigente' THEN 1 ELSE 0 END) AS contratos_vigentes,
        SUM(CASE WHEN estatus = 'Vencido' THEN 1 ELSE 0 END) AS contratos_vencidos
    FROM estadio_db.contrato
    WHERE fecha_inicio BETWEEN p_fecha_inicio AND p_fecha_fin;

    -- 2. Pagos recibidos en el rango
    SELECT
        COUNT(*) AS total_pagos,
        COALESCE(SUM(monto), 0) AS total_cobrado,
        COALESCE(AVG(monto), 0) AS promedio_pago,
        COALESCE(MAX(monto), 0) AS pago_mayor
    FROM estadio_db.pagos
    WHERE fecha_pago BETWEEN p_fecha_inicio AND p_fecha_fin
      AND estado = 1;

    -- 3. Top patrocinadores por monto pagado
    SELECT
        pat.nombre_empresa,
        COUNT(pg.id_pago) AS num_pagos,
        SUM(pg.monto) AS total_pagado
    FROM estadio_db.pagos pg
    JOIN estadio_db.contrato c ON c.id_contrato = pg.id_contrato
    JOIN estadio_db.patrocinadores pat ON pat.id_patrocinador = c.id_patrocinador
    WHERE pg.fecha_pago BETWEEN p_fecha_inicio AND p_fecha_fin
      AND pg.estado = 1
    GROUP BY pat.nombre_empresa
    ORDER BY total_pagado DESC
    LIMIT 10;

    -- 4. Contratos por vencer (30 días)
    SELECT
        pat.nombre_empresa,
        c.id_contrato,
        c.fecha_fin,
        c.monto_total,
        DATEDIFF(c.fecha_fin, CURDATE()) AS dias_restantes
    FROM estadio_db.contrato c
    JOIN estadio_db.patrocinadores pat ON pat.id_patrocinador = c.id_patrocinador
    WHERE c.estatus = 'Vigente'
      AND c.fecha_fin BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
    ORDER BY c.fecha_fin ASC;
END//

DELIMITER ;
```

**Uso:** `CALL sp_resumen_financiero('2026-01-01', '2026-12-31')` → devuelve 4 result sets.

**Cómo defenderlo:** "Creé un procedimiento almacenado que genera un resumen financiero completo en una sola llamada: resumen de contratos, pagos recibidos, top patrocinadores y contratos por vencer. Evita 4 round-trips a la base de datos."

---

## PARTE 4: AUDITORÍA DE VALIDACIONES — MÓDULO POR MÓDULO

### Módulos con TODO correcto (no necesitan cambios)

| Módulo | Backend | Frontend | SweetAlert | Estado |
|---|---|---|---|---|
| **Auth** | ✅ email, password, captcha | ✅ email, password, captcha | N/A (flash) | OK |
| **Usuarios** | ✅ nombre, email, cedula, rol, depto, tel, pwd | ✅ todos + AJAX uniqueness | ✅ crear, editar, eliminar | OK |
| **Contratos** | ✅ patrocinador, fechas, tipo, monto | ✅ patrocinador, tipo, fechas, monto | ✅ crear, editar, eliminar | OK |
| **Tareas** | ✅ nombre, instruccion | ✅ nombre, instruccion | ✅ crear, editar, eliminar | OK |
| **Balance** | ✅ monto > 0 | ✅ contrato, monto, fecha, hora | ✅ crear, editar, eliminar | OK |
| **Patrocinadores** | ✅ empresa, rif, tipo, encargado | ✅ empresa, rif, tipo, tel, email | ✅ crear, editar, eliminar | OK |
| **Reportes** | ✅ filtros | ✅ filtros | ✅ generar, eliminar | OK |
| **Bitácora** | Solo lectura | Solo lectura | N/A | OK |
| **Chat** | Solo pass-through | N/A | N/A | OK |
| **Notificaciones** | Solo sistema | JS pull+push | N/A (toast) | OK |
| **Dashboard** | Solo lectura | Solo lectura | N/A | OK |
| **Ayuda** | Solo estático | Solo búsqueda | N/A | OK |
| **En Vivo** | Reglas de negocio | N/A (operacional) | ✅ finalizar | OK |

---

### Módulos con INCONSISTENCIAS (necesitan cambios)

#### 1. GUIONES — Nombre mínimo inconsistente

| | Backend | Frontend | Problema |
|---|---|---|---|
| nombre | 3-50 chars | 2+ chars (`validarNombre`) | Un nombre de 2 chars pasa JS pero falla server |

**Solución:** Alinear frontend a 3+ chars (cambiar `validacion.js` línea 38: `minimo` de 2 a 3) O subir backend a 2. **Recomendado:** dejar backend como autoridad, alinear frontend a 3.

---

#### 2. MANTENIMIENTO — Diagnóstico mínimo inconsistente

| | Backend | Frontend | Problema |
|---|---|---|---|
| diagnostico | 10-500 chars | 3+ chars | Un diagnóstico de 5 chars pasa JS pero falla server |

**Solución:** Alinear frontend a 10+ chars. En `GestionMantenimiento.js` cambiar el mínimo de 3 a 10.

---

#### 3. INVENTARIO — Costo no validado en frontend

| | Backend | Frontend | Problema |
|---|---|---|---|
| costo | > 0 numérico | NO validado | Campo vacío o negativo pasa JS, falla server |

**Solución:** Agregar `validarCosto` en `GestionInventarioValidacion.js` para el campo costo.

---

#### 4. REELS — Sin validación JS en crear/editar

| | Backend | Frontend | Problema |
|---|---|---|---|
| nombre | 2-50 chars | Solo `required` HTML | Sin feedback visual inline |

**Solución:** Crear `GestionReelValidacion.js` con `validarNombre` y `validarDescripcion`. O agregar validación inline en los templates.

---

#### 5. ROLES — Sin SweetAlert en CRUD

| | Backend | Frontend | Problema |
|---|---|---|---|
| crear | flash msg | form submit directo | Sin confirmación SweetAlert |
| editar permisos | flash msg | form submit directo | Sin confirmación SweetAlert |

**Solución:** Agregar SweetAlert de confirmación en crear rol, editar permisos y guardar cambios (similar a cómo lo hacen usuarios/inventario).

---

#### 6. PREMIOS — Cantidad no validada en backend

| | Backend | Frontend | Problema |
|---|---|---|---|
| cantidad | default 1 (sin validación) | >= 1 | Frontend es más estricto que backend |

**Solución:** Agregar `validar_entero_positivo` para `cantidad` en `PremioModel._validar_datos_premio`.

---

#### 7. MANTENIMIENTO — `modificar()` no valida

| | Backend | Frontend | Problema |
|---|---|---|---|
| modificar | NO llama `_validar_datos_mantenimiento` | N/A | Edición bypass validación |

**Solución:** Agregar llamada a `_validar_datos_mantenimiento` al inicio de `MantenimientoModel.modificar()`.

---

#### 8. ELEMENTOS GUION — `modificar()` no valida

| | Backend | Frontend | Problema |
|---|---|---|---|
| modificar | NO llama `_validar_datos_elemento` | N/A | Edición bypass validación |

**Solución:** Agregar llamada a `_validar_datos_elemento` al inicio de `ElementoGuionModel.modificar()`.

---

## RESUMEN DE CAMBIOS TOTALES

| # | Archivo | Cambio | Prioridad |
|---|---|---|---|
| 1 | `app/view/bitacora/dashboard.html` | Agregar badge de rol + ojito | ALTA |
| 2 | `app/controller/rol_controller.py` | Ruta `/roles/respaldo` para backup | ALTA |
| 3 | `app/view/rol/dashboard.html` | Botón "Respaldar BD" | ALTA |
| 4 | `app/static/js/GestionRol.js` | Función `respaldarBD()` con SweetAlert | ALTA |
| 5 | `estadio_db.sql` | Vista `v_balance_contratos` | ALTA |
| 6 | `estadio_db.sql` | Triggers `trg_pagos_after_insert/update` | ALTA |
| 7 | `estadio_db.sql` | Procedimiento `sp_resumen_financiero` | ALTA |
| 8 | `app/static/js/validacion.js` | Cambiar mínimo nombre de 2 a 3 | MEDIA |
| 9 | `app/static/js/GestionMantenimiento.js` | Cambiar mínimo diagnostico de 3 a 10 | MEDIA |
| 10 | `app/static/js/validaciones/GestionInventarioValidacion.js` | Agregar validación de costo | MEDIA |
| 11 | Crear `app/static/js/validaciones/GestionReelValidacion.js` | Validación nombre + descripción | MEDIA |
| 12 | `app/view/rol/dashboard.html` | SweetAlert en crear/editar rol | MEDIA |
| 13 | `app/model/premio_model.py` | Validar cantidad en backend | BAJA |
| 14 | `app/model/mantenimiento_model.py` | Validar en `modificar()` | BAJA |
| 15 | `app/model/guion_model.py` | Validar en `modificar()` elementos | BAJA |

---

## INSTRUCCIONES PARA APROBAR

Responde con:
- **"APRUEBO TODO"** — ejecuto todos los cambios
- **"APRUEVO PARTE"** — indica qué números apruebas (ej: "apruebo 1-7, 8 no")
- **"CAMBIA X"** — indica qué quieres modificar de alguna propuesta
