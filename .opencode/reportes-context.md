# Contexto: Sistema de Reportes (Itinerario)

## Arquitectura general

El sistema de reportes tiene DOS flujos paralelos:

1. **Flujo clásico** (reportes dinámicos): seleccionas módulo → filtros → preview → PDF con columnas personalizables
2. **Constructor visual**: asistente por pasos para análisis ad-hoc (wizard con métricas, dimensiones, filtros)

### Archivos clave

| Archivo | Rol |
|---------|-----|
| `app/controller/reportes_controller.py` | Rutas Flask (`/reportes/*`), filtros, obtención de datos, endpoint `/campos/<modulo>` |
| `app/static/js/GestionReportes.js` | Frontend clásico: `MODULE_CONFIG`, filtros, panel de columnas, preview, descarga |
| `app/view/reportes/dashboard.html` | Template: card grid + panel de filtros + panel de columnas + preview |
| `app/helpers/reportes_campos.py` | Definición de ~80 campos dinámicos, formateadores, defaults |
| `app/helpers/reportes_data.py` | Funciones de datos por módulo (`_datos_*`) con KPIs |
| `app/helpers/reportes_utils.py` | Utilidades (ordenamiento, sanitización) |
| `app/helpers/generators/base_report.py` | Clase base con motor dinámico: columnas, anchos, agrupación, subtotales |
| `app/helpers/generators/*_report.py` | 11 generadores (uno por módulo) + constructor_report |

## Motor de reportes PDF dinámico (FASE 0-8, completado)

### Flujo

1. Usuario selecciona módulo → `cargarCampos(modulo)` fetch desde `/reportes/campos/<modulo>`
2. Panel de columnas muestra checkboxes con campos disponibles (defaults marcados)
3. Dropdowns: orientación (vertical/horizontal/auto), agrupar por, ordenar por
4. POST a `/reportes/generar` incluye `columnas_seleccionadas[]`, `orientacion`, `agrupar_por`, `ordenar_por`
5. Controller valida contra `CAMPOS_DISPONIBLES` (whitelist server-side)
6. `BaseReportGenerator.generate()` resuelve columnas → anchos → página → estilo → tabla

### Métodos en BaseReportGenerator

- `_obtener_columnas(opciones)` — resuelve dinámicas vs default
- `_calcular_anchos(columnas, orientacion)` — proporcionales que caben en la página
- `_determinar_pagina(columnas, orientacion)` — letter/landscape auto
- `_ajustar_estilo_segun_columnas(n)` — reduce fuente 7pt (8-10 cols) o 6pt (11+)
- `_formatear_celda(item, columna, tipo)` — formatea + trunca por ancho
- `_construir_tabla_simple(datos, columnas)` — header + filas
- `_construir_tabla_agrupada(datos, columnas, campo)` — grupos + subtotales + total general
- `_post_table_sections(kpis, opciones)` — hook para distribuciones (override en subclases)
- `_secciones_analisis(kpis, opciones)` — resumen ejecutivo + Top-N + comparativa

### Generadores simplificados

Cada generador ahora solo define:
- `MODULO`, `TITULO`, `COLUMNAS` (default)
- `_post_table_sections(kpis, opciones)` — distribuciones específicas del módulo
- `_build_rows(datos)` — formateo de filas para tabla default

Excepción: `ReelsReport` mantiene `generate()` custom (layout con cards + tabla anidada).

### Tests

- `tests/test_reportes_campos.py` — 89 tests de campos y formateadores
- `tests/test_reportes_pdf_dinamico.py` — 36 tests: regresión, columnas dinámicas, agrupación, orientación, validación, ordenamiento, análisis completo
- Suite total: **226 tests pasan**

## Convenciones

- `CAMPOS_DISPONIBLES` en `reportes_campos.py` es la fuente de verdad de campos
- Whitelist server-side: controller valida contra `CAMPOS_DISPONIBLES` antes de pasar a generador
- `_post_table_sections` es el hook para distribuciones — cada módulo lo overridea
- `COLUMNAS` en cada generador es el fallback cuando no hay selección dinámica
- Tests usan fixture `app` para crear el contexto Flask (evita error de `rol_model._asegurar_schema`)
