# Contexto: Sistema de Reportes (Itinerario)

## Arquitectura general

El sistema de reportes es un dashboard progresivo tipo "Profit Plus":
- Seleccionas un módulo → aparecen filtros contextuales (algunos vía AJAX)
- Seleccionas filtros → preview en tabla + KPIs + distribución
- Botón "Generar PDF" produce un PDF con KPIs + distribuciones + tabla de datos

### Archivos clave

| Archivo | Rol |
|---------|-----|
| `app/controller/reportes_controller.py` | Rutas Flask (`/reportes/*`), funciones de filtros (`_filtros_*`), obtención de datos (`_obtener_datos`), configuración de módulos |
| `app/static/js/GestionReportes.js` | Frontend: `MODULE_CONFIG` por módulo, `cargarOpcionesAjax`, render de filtros/tabla/KPIs |
| `app/view/reportes/dashboard.html` | Template: card grid + panel de filtros dinámico + tabla preview |
| `app/helpers/generators/base_report.py` | Clase base: `_seccion_kpis()`, `_seccion_distribucion()`, `_header()`, `_tabla()`, `_build_rows()` |
| `app/helpers/generators/*_report.py` | 12 generadores PDF (uno por módulo + resumen) |

## Estados de implementación

### ✅ Completos (nivel Contratos)
- **contratos**: filtros (tipo, estatus, patrocinador AJAX, monto min/max, fecha) con progresividad tipo→patrocinador
- **bitacora**: filtros (usuario AJAX, acción AJAX, módulo AJAX, fecha) con 3 selects progresivos
- **inventario**: filtros (tipo AJAX→estado AJAX progresivo, costo min/max, fecha), KPIs (total, costo_total, costo_promedio), PDF con distribución por tipo/estado

### 🔄 Pendientes de mejorar (aplicar mismo patrón)
Cada uno necesita: más filtros (categórico + rango numérico + fecha), progresividad entre filtros, KPIs enriquecidos, distribución en PDF.

#### guiones
- Filtros actuales: estado (select estático), fecha
- Faltan: `elementos_min`/`elementos_max` (rango #elementos), progresividad
- KPIs: ya tiene (total, borradores, publicados, en_vivo, finalizados, tiempo_total)
- PDF: ya tiene distribución por estado
- Archivo: `_filtros_guiones` → agregar `elementos_min`/`max`, progresividad

#### premios
- Filtros actuales: estado (estático), patrocinador_id (AJAX), fecha
- Faltan: `cantidad_min`/`cantidad_max` (rango), `cantidad_entregada_min`/`max`
- Progresividad: estado → patrocinador_id
- KPIs: ya tiene (total, pendientes, entregados, tasa_entrega, por_patrocinador)
- PDF: ya tiene distribución por estado
- Archivo: `_filtros_premios` + JS `dependsOn`

#### balance
- Filtros actuales: tipo_pago (AJAX), patrocinador_id (AJAX), monto min/max, fecha
- Progresividad: tipo_pago → patrocinador_id
- Bug conocido: columna `referencia` puede ser NULL en preview
- KPIs: ya tiene (total_pagos, monto_total, promedio, monto_min, monto_max, tipos_pago distrib)
- PDF: ya tiene distribución por tipo_pago

#### tareas
- Filtros actuales: Estado (estático), usuario (AJAX), fecha
- Progresividad: Estado → usuario_asignado
- Bug: key `Estado` con mayúscula es inconsistente
- KPIs: ya tiene (total, pendientes, en_progreso, completadas, completadas_pct)
- PDF: ya tiene distribución por estado

#### patrocinadores
- Filtros actuales: tipo_contrato (estático), fecha
- Faltan: `estado_filter` (activo/inactivo)
- KPIs: ya tiene (total, activos, inactivos, por_tipo_contrato)
- PDF: ya tiene por tipo_contrato (si existe en kpis)
- Bug: nombre `estado_filter` es feo, refactor a `estado_pat`

#### usuarios
- Filtros actuales: rol (AJAX), departamento (AJAX), fecha
- Faltan: `activo` (sí/no)
- Progresividad: departamento → rol
- KPIs: ya tiene (total, activos, inactivos, por_rol, por_departamento)
- PDF: ya tiene distribución por rol

#### mantenimiento
- Filtros actuales: estado (AJAX), recurso_id (AJAX), fecha
- Faltan: rango numérico (costo? días?)
- Progresividad: estado → recurso_id
- KPIs: ya tiene (total, en_espera, en_reparacion, reparados, dados_baja)
- PDF: ya tiene distribución por estado

#### reels
- Filtros actuales: patrocinador_id (AJAX), fecha
- Faltan: `duracion_min`/`duracion_max` (en segundos), progresividad con patrocinador
- KPIs: ya tiene (total, total_videos, duracion_total, duracion_promedio)

## Patrón para implementar un módulo (receta)

### 1. Backend: `_filtros_<modulo>(params)`
- Devolver en JSON: arrays para selects + `{campo}_min`/`{campo}_max` para rangos
- Si hay progresividad: filtrar datos según `params.get('campo_dependencia')`
- Usar `try/except` con log del error real (no silencioso)

### 2. Backend: `_obtener_datos` sección del módulo
- Agregar filtros faltantes (rango numérico)
- Agregar KPIs: total + contadores + promedios/totales
- Mantener distribuciones (`tipos`, `estados`, `por_*`)

### 3. Frontend: `MODULE_CONFIG.<modulo>`
```javascript
filters: [
    { id: 'select_con_progresividad', label: '...', type: 'select', loadVia: 'ajax',
      colClass: 'col-md-3', progressive: ['select_dependiente'] },
    { id: 'select_dependiente', label: '...', type: 'select', loadVia: 'ajax',
      dependsOn: ['select_con_progresividad'], colClass: 'col-md-3' },
    { id: 'campo_min', label: '... Mín', type: 'number', placeholder: '0', colClass: 'col-md-2' },
    { id: 'campo_max', label: '... Máx', type: 'number', placeholder: '999999', colClass: 'col-md-2' },
    { id: 'fecha_inicio', ..., 'fecha_fin', ... },
],
columns: [...],
kpiCards: [
    { key: 'total', label: 'Total', color: '#2563eb' },
    { key: '...', label: '...', color: '...' },
],
```

### 4. Frontend: `cargarOpcionesAjax`
Si devuelves un nuevo campo tipo `{campo}_min`/`{campo}_max`, agregar bloque similar al de `monto_min`/`monto_max`.

### 5. PDF: `<modulo>_report.py`
Agregar `_seccion_distribucion` con los datos de distribución (tipos, estados, etc.) disponibles en `kpis`.

## Convenciones
- `progressive` en el FILTRO ORIGEN (el que al cambiar recarga al destino)
- `dependsOn` en el FILTRO DESTINO (el que se recarga cuando cambia el origen)
- <select> options: primer option siempre `value=""` con label "Todos..." (o el equivalente)
- Rangos numéricos: enviar `{campo}_min`/`{campo}_max` desde backend como hint (placeholders en frontend)
- Fechas: `fecha_inicio`/`fecha_fin` siempre presentes
- columnas preview: deben coincidir con lo que devuelve `_obtener_datos`
- kpiCards keys: deben coincidir con las claves del dict `kpis`
