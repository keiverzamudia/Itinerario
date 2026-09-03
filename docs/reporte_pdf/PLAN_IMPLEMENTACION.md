# Plan de Implementacion

**Fecha:** 2026-09-01
**Estado:** Pendiente de aprobacion.

---

## FASE 0: Fundaciones (1-2 dias)

### Tareas:
1. Crear `app/helpers/reportes_campos.py` con:
   - `CAMPOS_DISPONIBLES` (11 modulos, ~80 campos total)
   - `COLUMNAS_DEFAULT` (las mismas de hoy por modulo)
   - `FORMATTERS` (9 tipos)
2. Crear tests unitarios para:
   - Cada campo tiene label, key, type, width, order
   - Cada formatter produce output correcto
   - COLUMNAS_DEFAULT coincide con COLUMNAS de cada generador
3. Endpoint GET `/reportes/campos/<modulo>` con whitelist

### Criterio de aceptacion:
- Tests pasan
- Endpoint devuelve JSON valido
- Sin cambios en funcionalidad existente

---

## FASE 1: Columnas dinamicas en BaseReportGenerator (2-3 dias)

### Tareas:
1. Agregar metodo `_obtener_columnas(opciones)` a `BaseReportGenerator`
2. Agregar metodo `_calcular_anchos(columnas, orientacion)`
3. Agregar metodo `_formatear_celda(item, columna, tipo_campo)`
4. Modificar `generate()` para usar columnas dinamicas cuando `opciones['columnas_seleccionadas']` existe
5. Sin esa opcion, comportamiento identico al actual

### Criterio de aceptacion:
- PDF sin opciones = byte-a-byte identico al actual
- PDF con columnas_seleccionadas = respeta la seleccion
- Tests de regresion pasan

---

## FASE 2: Endpoint y validacion (1-2 dias)

### Tareas:
1. Ampliar `generar()` en `reportes_controller.py` para:
   - Extraer `columnas_seleccionadas` de `request.form`
   - Extraer `orientacion` de `request.form`
   - Validar contra `CAMPOS_DISPONIBLES`
   - Whitelist server-side de orientacion
2. Ampliar `preview()` para que devuelva columnas seleccionadas
3. Tests de validacion

### Criterio de aceptacion:
- Campos invalidos se descartan
- Orientacion invalida usa default
- Preview refleja columnas seleccionadas

---

## FASE 3: Panel de campos en frontend (2-3 dias)

### Tareas:
1. Agregar contenedor `#campoPanel` en `dashboard.html`
2. Agregar funcion `renderCampos(modulo)` en `GestionReportes.js`
3. Cargar campos desde `/reportes/campos/<modulo>` via AJAX
4. Renderizar checkboxes con defaults marcados
5. Incluir campos seleccionados en POST a `/reportes/preview` y `/reportes/generar`
6. Checkbox "Seleccionar todo" / "Limpiar seleccion"

### Criterio de aceptacion:
- Panel muestra campos correctos por modulo
- Defaults estan marcados
- Cambios se reflejan en preview y PDF
- Sin seleccion = mismo comportamiento de siempre

---

## FASE 4: Orientacion dinamica (1 dia)

### Tareas:
1. Implementar `_determinar_pagina(columnas, orientacion)` en `BaseReportGenerator`
2. Si 8+ columnas o ancho > 500pt → landscape automatico
3. Agregar dropdown de orientacion en panel de filtros
4. Enviar orientacion en POST

### Criterio de aceptacion:
- Landscape automatico cuando hay muchas columnas
- El usuario puede forzar portrait/horizontal
- PDF generado con orientacion correcta

---

## FASE 5: Agrupacion y subtotales (2-3 dias)

### Tareas:
1. Implementar `_construir_tabla_agrupada(datos, columnas, campo_agrupacion)` en `BaseReportGenerator`
2. Agregar dropdown "Agrupar por" (solo campos con `groupable: True`)
3. Subtotales para columnas con `aggregate`
4. Fila de total general
5. Tests de agrupacion

### Criterio de aceptacion:
- Agrupacion produce filas de grupo + subtotales + total general
- Sin agrupar_por = comportamiento identico al actual
- Subtotales suman solo columnas numericas

---

## FASE 6: Manejo de muchos campos (1-2 dias)

### Tareas:
1. Implementar `_ajustar_estilo_segun_columnas(num_columnas)` en `BaseReportGenerator`
2. Reduccion de fuente para 8+ columnas
3. Truncado inteligente de texto largo
4. Aviso "Demasiadas columnas" para 25+
5. Tests con 1, 5, 10, 15, 20 columnas

### Criterio de aceptacion:
- PDF legible con hasta 15 columnas
- PDF funcional con 20 columnas (landscape, fuente reducida)
- Aviso para 25+ columnas

---

## FASE 7: Ordenamiento dinamico (1 dia)

### Tareas:
1. Ampliar `generar()` para aceptar `orden_campo` y `orden_direccion`
2. Aplicar `_ordenar_datos()` con el campo elegido
3. Agregar dropdown "Ordenar por" en panel de filtros
4. Enviar en POST

### Criterio de aceptacion:
- PDF refleja el orden seleccionado
- Sin orden = comportamiento actual (el que devuelve el modelo)

---

## FASE 8: Testing completo (2-3 dias)

### Tareas:
1. Tests de regresion: cada modulo, sin opciones, PDF identico
2. Tests de columnas dinamicas: 1, 5, 10, 20 columnas
3. Tests de agrupacion: con y sin subtotales
4. Tests de orientacion: portrait/landscape/auto
5. Tests de validacion: campos invalidos, orientacion invalida
6. Tests de limites: max columnas, max registros
7. Tests de compatibilidad: preview + PDF coherentes

### Criterio de aceptacion:
- Suite completa pasa
- 0 regressions en funcionalidad existente

---

## FASE 9: Optimizacion y pulido (1-2 dias)

### Tareas:
1. Log de tiempos de generacion
2. Optimizacion de queries si se detecta lentitud
3. Indices en BD si se justifica
4. Documentacion de uso en `reportes-context.md`
5. Actualizacion de `CHECKLIST.md`

### Criterio de aceptacion:
- PDF genera en < 5 segundos para 1000 registros
- Documentacion actualizada

---

## Resumen de fases

| Fase | Dias estimados | Dependencias |
|------|---------------|--------------|
| F0: Fundaciones | 1-2 | Ninguna |
| F1: Columnas dinamicas | 2-3 | F0 |
| F2: Endpoint validacion | 1-2 | F1 |
| F3: Panel frontend | 2-3 | F2 |
| F4: Orientacion | 1 | F1 |
| F5: Agrupacion | 2-3 | F1, F4 |
| F6: Muchos campos | 1-2 | F1 |
| F7: Ordenamiento | 1 | F2 |
| F8: Testing | 2-3 | F3-F7 |
| F9: Optimizacion | 1-2 | F8 |
| **TOTAL** | **14-21 dias** | |

---

## Orden de construccion recomendado

```
F0 -> F1 -> F2 -> F3 -> F7 (orden) -> F4 (orientacion) -> F5 (agrupacion)
                                                              -> F6 (muchos campos)
                                                              -> F8 (testing)
                                                              -> F9 (optimizacion)
```

**Razon:** F0-F3 son la base. F7 es barato. F4-F6 se pueden hacer en paralelo despues de F1-F2. F8 es el cierre. F9 es polish.

---

*Documento de plan de implementacion.*
