# Campos Dinamicos: Definicion por Modulo

**Fecha:** 2026-09-01

---

## 1. Estructura de un campo

```python
{
    'label': str,           # Nombre visible (UI + PDF)
    'key': str,             # Clave en el dict de datos
    'type': str,            # Tipo para formateo
    'width': int,           # Ancho sugerido en puntos (portrait letter ~532pt util)
    'order': int,           # Orden de aparicion
    'groupable': bool,      # Se puede agrupar por este campo
    'sortable': bool,       # Se puede ordenar por este campo
    'aggregate': str|None,  # 'suma' | 'conteo' | 'promedio' | None
}
```

### Tipos disponibles

| Tipo | Formato | Ejemplo |
|------|---------|---------|
| `texto` | str(v) or '—' | "Panamericana" |
| `texto_largo` | truncado a 50 chars | "Descripcion larga..." |
| `entero` | f"{int(v):,}" | "1,234" |
| `moneda` | f"${float(v):,.2f}" | "$12,345.67" |
| `decimal` | f"{float(v):,.1f}" | "12.3" |
| `fecha` | str(v) | "2026-01-15" |
| `fecha_hora` | str(v)[:16] | "2026-01-15 14:30" |
| `duracion` | _formatear_tiempo(v) | "2h 30m" |
| `porcentaje` | f"{float(v):.1f}%" | "85.5%" |
| `boolean` | 'Si' / 'No' | "Si" |

---

## 2. Campos por modulo

### 2.1 Guiones

| Campo | Label | Tipo | Width | Group | Sort | Aggregate |
|-------|-------|------|-------|-------|------|-----------|
| `nombre` | Nombre | texto | 150 | Si | Si | None |
| `game` | Game | entero | 40 | Si | Si | None |
| `pregame` | Pre-Game | entero | 50 | Si | Si | None |
| `fecha_ejecucion` | Ejecucion | fecha | 70 | Si | Si | None |
| `estado` | Estado | texto | 60 | Si | Si | None |
| `tiempo_total` | Tiempo | duracion | 60 | No | Si | None |
| `creado_en` | Creado | fecha_hora | 75 | No | Si | None |
| `encargado` | Encargado | texto | 100 | Si | Si | None |

**Default:** nombre, game, pregame, fecha_ejecucion, estado, tiempo_total

### 2.2 Inventario

| Campo | Label | Tipo | Width | Group | Sort | Aggregate |
|-------|-------|------|-------|-------|------|-----------|
| `id` | ID | entero | 30 | No | Si | None |
| `nombre` | Nombre | texto | 130 | Si | Si | None |
| `tipo_nombre` | Tipo | texto | 80 | Si | Si | None |
| `estado_nombre` | Estado | texto | 70 | Si | Si | None |
| `fecha_compra` | Compra | fecha | 70 | No | Si | None |
| `costo` | Costo | moneda | 70 | No | Si | suma |
| `descripcion` | Descripcion | texto_largo | 150 | No | No | None |

**Default:** id, nombre, tipo_nombre, estado_nombre, fecha_compra

### 2.3 Premios

| Campo | Label | Tipo | Width | Group | Sort | Aggregate |
|-------|-------|------|-------|-------|------|-----------|
| `nombre` | Nombre | texto | 120 | Si | Si | None |
| `patrocinador` | Patrocinador | texto | 90 | Si | Si | None |
| `estado` | Estado | texto | 55 | Si | Si | None |
| `total` | Total | entero | 35 | No | Si | suma |
| `entregados` | Entregados | entero | 40 | No | Si | suma |
| `fecha_creacion` | Creacion | fecha | 65 | No | Si | None |
| `fecha_entrega` | Entrega | fecha_hora | 75 | No | Si | None |

**Default:** nombre, patrocinador, estado, total, entregados, fecha_creacion

### 2.4 Contratos

| Campo | Label | Tipo | Width | Group | Sort | Aggregate |
|-------|-------|------|-------|-------|------|-----------|
| `nombre_empresa` | Empresa | texto | 115 | Si | Si | None |
| `tipo` | Tipo | texto | 50 | Si | Si | None |
| `estatus` | Estatus | texto | 50 | Si | Si | None |
| `fecha_inicio` | Inicio | fecha | 60 | No | Si | None |
| `fecha_fin` | Fin | fecha | 60 | No | Si | None |
| `dias_restantes` | Dias | entero | 35 | No | Si | None |
| `monto_total` | Monto | moneda | 60 | No | Si | suma |

**Default:** nombre_empresa, tipo, estatus, fecha_inicio, fecha_fin, dias_restantes, monto_total

### 2.5 Balance

| Campo | Label | Tipo | Width | Group | Sort | Aggregate |
|-------|-------|------|-------|-------|------|-----------|
| `nombre_patrocinador` | Patrocinador | texto | 120 | Si | Si | None |
| `tipo_pago` | Tipo Pago | texto | 70 | Si | Si | None |
| `monto` | Monto | moneda | 75 | No | Si | suma |
| `referencia` | Referencia | texto | 85 | No | Si | None |
| `fecha_pago` | Fecha Pago | fecha | 70 | No | Si | None |

**Default:** nombre_patrocinador, tipo_pago, monto, referencia, fecha_pago

### 2.6 Tareas

| Campo | Label | Tipo | Width | Group | Sort | Aggregate |
|-------|-------|------|-------|-------|------|-----------|
| `tarea` | Tarea | texto | 150 | Si | Si | None |
| `estado` | Estado | texto | 65 | Si | Si | None |
| `asignado` | Asignado a | texto | 80 | Si | Si | None |
| `fecha` | Fecha | fecha_hora | 75 | No | Si | None |

**Default:** tarea, estado, asignado, fecha

### 2.7 Patrocinadores

| Campo | Label | Tipo | Width | Group | Sort | Aggregate |
|-------|-------|------|-------|-------|------|-----------|
| `nombre_empresa` | Empresa | texto | 150 | Si | Si | None |
| `rif` | RIF | texto | 75 | No | Si | None |
| `telefono` | Telefono | texto | 75 | No | Si | None |
| `tipo_contrato` | Contrato | texto | 70 | Si | Si | None |
| `estado` | Estado | texto | 55 | Si | Si | None |

**Default:** nombre_empresa, rif, telefono, tipo_contrato

### 2.8 Usuarios

| Campo | Label | Tipo | Width | Group | Sort | Aggregate |
|-------|-------|------|-------|-------|------|-----------|
| `nombre` | Nombre | texto | 110 | Si | Si | None |
| `email` | Email | texto | 120 | No | Si | None |
| `rol` | Rol | texto | 70 | Si | Si | None |
| `depto` | Depto | texto | 70 | Si | Si | None |
| `estado` | Estado | texto | 55 | Si | Si | None |

**Default:** nombre, email, rol, depto, estado

### 2.9 Mantenimiento

| Campo | Label | Tipo | Width | Group | Sort | Aggregate |
|-------|-------|------|-------|-------|------|-----------|
| `recurso` | Recurso | texto | 110 | Si | Si | None |
| `estado` | Estado | texto | 65 | Si | Si | None |
| `ingreso` | Ingreso | fecha | 65 | No | Si | None |
| `diagnostico` | Diagnostico | texto_largo | 130 | No | No | None |
| `dias_en_taller` | Dias | entero | 45 | No | Si | promedio |

**Default:** recurso, estado, ingreso, diagnostico

### 2.10 Reels

| Campo | Label | Tipo | Width | Group | Sort | Aggregate |
|-------|-------|------|-------|-------|------|-----------|
| `nombre` | Nombre | texto | 120 | Si | Si | None |
| `patrocinador` | Patrocinador | texto | 100 | Si | Si | None |
| `videos` | Videos | entero | 50 | No | Si | suma |
| `duracion_total` | Duracion | duracion | 80 | No | Si | None |
| `creado_en` | Creado | fecha_hora | 75 | No | Si | None |

**Default:** nombre, patrocinador, videos, duracion_total

### 2.11 Bitacora

| Campo | Label | Tipo | Width | Group | Sort | Aggregate |
|-------|-------|------|-------|-------|------|-----------|
| `id` | ID | entero | 30 | No | Si | None |
| `usuario` | Usuario | texto | 85 | Si | Si | None |
| `accion` | Accion | texto | 65 | Si | Si | None |
| `modulo` | Modulo | texto | 65 | Si | Si | None |
| `detalle` | Detalle | texto_largo | 145 | No | No | None |
| `fecha` | Fecha | fecha_hora | 75 | No | Si | None |

**Default:** id, usuario, accion, modulo, detalle, fecha

---

## 3. Campos calculados (futuro)

Campos que no existen en una sola tabla pero se pueden derivar:

| Modulo | Campo calculado | Formula |
|--------|----------------|---------|
| contratos | `dias_restantes` | DATEDIFF(fecha_fin, CURDATE()) |
| mantenimiento | `dias_en_taller` | DATEDIFF(COALESCE(fecha_salida, CURDATE()), fecha_ingreso) |
| balance | `monto_total_contrato` | SUM(monto) GROUP BY id_contrato |
| reels | `duracion_total` | SUM(duracion_segundos) / 60 |

Estos campos ya se calculan en `reportes_data.py`. La capa de campos los consume como cualquier otro.

---

*Documento de definicion de campos por modulo.*
