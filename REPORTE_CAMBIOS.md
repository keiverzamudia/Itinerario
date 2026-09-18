# REPORTE DE CAMBIOS — Sistema Itinerario v2.0

---

## RESUMEN EJECUTIVO

| Categoría | Estado |
|-----------|--------|
| Validaciones alineadas (frontend + backend) | ✅ HECHO |
| Fix bugs de reportes (6 fixes) | ✅ HECHO |
| Reels duración en segundos | ✅ HECHO |
| Reels detalle vista (planificado vs consumido) | ✅ HECHO |
| Pagos balance (estado = 1 = activo) | ✅ HECHO |
| Constructor report (error con detalle) | ✅ HECHO |
| Bitácora mejorada (badge + ojo) | ✅ HECHO |
| Respaldo de BD (XAMPP compatible) | ✅ HECHO |
| Objetos SQL (vista + triggers + procedimiento) | ✅ HECHO |
| Patrocinador RIF separado + nombre_contacto | ✅ HECHO |
| Guiones botón ← volver | ✅ HECHO |
| Seed data realista (estadio de béisbol) | ✅ HECHO |

---

## 1. SEED DATA — Archivos SQL para la defensa

### 1.1 `seed_estadio_db.sql` — Base de datos de negocio

**Contenido:**
- **10 patrocinadores** — Empresas venezolanas reales (Maltin Polar, Pepsi, Banesco, etc.)
- **10 contratos** — Montos desde $8,000 hasta $150,000, todos vigentes en 2026
- **14 pagos** — Pagos parciales (25-50%) con referencias únicas
- **12 recursos** — Equipos del estadio (cámaras, mezcladora, pantallas, etc.)
- **6 reels** — Contenido de patrocinadores con 15 videos
- **10 premios** — De patrocinadores, mix de entregados/pendientes
- **6 tareas** — Preparativos de juego
- **6 guiones** — Programación de juegos (1 finalizado, 5 borrador)
- **30 elementos de guión** — Programación detallada (pregame/game/postgame)
- **2 mantenimientos** — Historial de reparaciones

**Objetos SQL incluidos:**
- `v_balance_contratos` — Vista que une contratos + patrocinadores + pagos
- `trg_pagos_after_insert` — Trigger de auditoría financiera (INSERT)
- `trg_pagos_after_update` — Trigger de auditoría financiera (UPDATE)
- `sp_resumen_financiero(fecha_inicio, fecha_fin)` — Procedimiento con 4 result sets

### 1.2 `seed_seguridad.sql` — Usuarios y auditoría

**Contenido:**
- **3 roles** — Superadmin, Administrador, Usuario
- **52 permisos** — Todos los módulos del sistema
- **6 usuarios** — Nombres realistas venezolanos (contraseña: `password123`)
- **Actividad de bitácora** — 15 registros de ejemplo (logins, CRUD, tareas)
- **Notificaciones** — 4 de ejemplo
- **Sesiones** — 5 registros de sesiones
- **Sincronizaciones** — 8 registros de en_vivo

---

## 2. CAMBIOS APLICADOS ANTERIORMENTE

### 2.1 Bitácora mejorada
- **Badge de rol** junto al nombre del usuario en `app/view/bitacora/dashboard.html`
- **Icono de ojo** que lleva al reporte de usuario
- **Dashboard:** rol visible + icono de acción

### 2.2 Respaldo de BD
- **Ruta:** `POST /roles/respaldo` en `app/controller/rol_controller.py`
- **XAMPP path:** Búsqueda automática en `/Applications/XAMPP/xamppfiles/bin/mysqldump`
- **Sin `--routines`:** Removido por compatibilidad con MariaDB
- **Salida:** Validada por tamaño, no por exit code

### 2.3 Validaciones alineadas

| Archivo | Cambio |
|---------|--------|
| `static/js/validacion.js` | `validarNombre`: mínimo 2→3 |
| `static/js/GestionMantenimiento.js` | diagnostico mínimo 3→10 |
| `static/js/validaciones/GestionInventarioValidacion.js` | Agregada validación de costo |
| `model/mantenimiento_model.py` | `modificar()` valida diagnostico y observaciones |
| `model/guion_model.py` | `modificar()` elementos valida contenido, hora, inning |
| `model/premio_model.py` | `_validar_datos_premio()` valida cantidad |

### 2.4 Bugs de reportes (6 fixes)

| Bug | Archivo | Fix |
|-----|---------|-----|
| Bitácora PDF mostraba `accion` en vez de `detalle` | `bitacora_report.py:48` | Cambiado a `d.get('detalle')` |
| Mantenimiento PDF faltaba columna "Días" | `mantenimiento_report.py` | Agregada columna `dias_en_taller` |
| Fechas NULL siempre incluidas con filtro activo | `reportes_utils.py:40` | Excluidas cuando hay filtro de fecha |
| Formato inconsistente date vs datetime | `reportes_controller.py:514` | Check `isinstance(v, date)` |
| Contratos filtro fecha solo revisaba `fecha_inicio` | `reportes_data.py:350` | Verifica solapamiento inicio↔fin |
| base_report.py mutaba dict del caller | `base_report.py` | `filtros.pop` → `filtros.get` |

### 2.5 Reels
- **`duracion_total`** ahora en SECONDS (convertido desde minutos)
- **Vista detalle** muestra duración planificada vs consumida con barra de progreso
- **Reels detail view** en `app/view/reels/ver_reel.html`

### 2.6 Patrocinador
- **RIF:** Separado en selector V/E/J/G + números separados
- **`nombre_contacto`:** Ahora requerido con validación
- **JS:** `GestionPatrocinador.js` combina RIF antes de submit

### 2.7 Guiones
- **Botón ←** en página "Agregar Elemento" para volver al guión

### 2.8 Constructor report
- **Error response** ahora incluye campo `detalle` para debugging
- **Frontend** muestra el detalle en SweetAlert de error
- **Fix:** `TableStyle` import agregado a `constructor_report.py`

---

## 3. INSTRUCCIONES DE USO

### Para restaurar la BD:
```bash
# 1. Crear las BDs
mysql -u root -e "CREATE DATABASE IF NOT EXISTS estadio_db;"
mysql -u root -e "CREATE DATABASE IF NOT EXISTS seguridad;"

# 2. Importar estructura + seed
mysql -u root estadio_db < seed_estadio_db.sql
mysql -u root seguridad < seed_seguridad.sql

# 3. Verificar
mysql -u root -e "SELECT COUNT(*) AS contratos FROM estadio_db.contrato;"
mysql -u root -e "SELECT COUNT(*) AS usuarios FROM seguridad.usuarios;"
```

### Usuarios de prueba:
| Email | Contraseña | Rol |
|-------|-----------|-----|
| keiver@cardenales.com | password123 | Superadmin |
| ana.perez@outlook.com | password123 | Administrador |
| genesis@cardenales.com | password123 | Administrador |
| carlos@mendoza.com | password123 | Superadmin |

---

## 4. CHECKLIST DE DEFENSA — CUMPLIMIENTO

| # | Requisito | Estado | Ubicación |
|---|-----------|--------|-----------|
| 1 | Contraseñas cifradas | ✅ | `werkzeug pbkdf2:sha256` |
| 2 | Sesiones de usuario | ✅ | Flask-Login + sesión única |
| 3 | Bitácora del sistema | ✅ | 40+ puntos en 12 controladores |
| 4 | Validación frontend + backend | ✅ | 22 funcs JS + mixin Python |
| 5 | Consulta con filtros | ✅ | DataTables + filtros backend |
| 6 | Confirmación antes de eliminar | ✅ | SweetAlert2 en todos los módulos |
| 7 | Captcha | ✅ | Captcha de béisbol custom |
| 8 | Reportes PDF parametrizados | ✅ | 14 generadores con KPIs y Top-N |
| 9 | Vista SQL | ✅ | `v_balance_contratos` |
| 10 | Trigger | ✅ | `trg_pagos_after_insert/update` |
| 11 | Procedimiento almacenado | ✅ | `sp_resumen_financiero` |
| 12 | Respaldo de BD | ✅ | Botón "Respaldar BD" en Roles |

---

*Última actualización: 18 de septiembre 2026*
