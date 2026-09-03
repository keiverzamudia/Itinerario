# Propuesta: Motor de Reportes PDF Dinamico

**Proyecto:** Itinerario - Sistema de Gestion del Estadio Antonio Herrera Gutierrez
**Fecha:** 2026-09-01
**Estado:** ANALISIS Y DISENO - Pendiente de aprobacion
**Autor:** Analisis automatizado + diseno basado en inspeccion de codigo real

---

## 1. Problema actual

El modulo de reportes PDF genera documentos con columnas **hardcoded** por modulo. El usuario no puede:

- Seleccionar que campos aparecen en el PDF
- Ordenar los datos por un campo elegido
- Agrupar por una columna y ver subtotales
- Cambiar orientacion cuando hay muchas columnas

Cada cambio de "quiero este campo en el reporte" requiere modificar el generador Python, el controlador, el frontend y la definicion de columnas.

---

## 2. Como funciona actualmente

```
Usuario -> Click modulo -> Filtros -> Vista Previa -> Descargar PDF
                                                              |
                                                              v
                                              Generador con COLUMNAS fijas
                                              (ej: contratos = 7 columnas hardcoded)
                                                              |
                                                              v
                                                          PDF rígido
```

**Archivos clave:**
- `app/helpers/generators/base_report.py` (394 lineas) - Clase base
- `app/helpers/generators/*_report.py` (12 archivos) - Generadores por modulo
- `app/helpers/reportes_data.py` (762 lineas) - Datos y KPIs
- `app/controller/reportes_controller.py` (777 lineas) - Rutas
- `app/static/js/GestionReportes.js` (803 lineas) - Frontend

**Ya existen DOS caminos:**
1. **Clasico:** Filtros -> datos -> generador con COLUMNAS fijas -> PDF
2. **Constructor:** Wizard -> SQL dinamico -> dataset generico -> ConstructorReport

El constructor ya resuelve analisis dinamico. El clasico sigue rigido.

---

## 3. Limitaciones

| Limitacion | Impacto |
|-----------|---------|
| Columnas hardcoded | Agregar campo = modificar 4 archivos |
| Sin seleccion de campos | El usuario ve siempre todo o nada |
| Sin agrupacion en clasico | Solo el constructor tiene GROUP BY |
| Sin subtotales en clasico | El clasico solo muestra filas |
| Sin orientacion dinamica | 10+ columnas = PDF comprimido |
| Filtros en Python (mayoria) | Lento con muchos registros |
| Config duplicada | Columnas en 3 lugares diferentes |

---

## 4. Objetivo

Evolucionar el flujo clasico para que el usuario pueda:

- **Seleccionar campos** (checkboxes de columnas disponibles)
- **Ordenar** por cualquier campo
- **Agrupar** por una columna con subtotales
- **Orientacion** automatica segun cantidad de columnas

**SIN CAMBIAR:**
- La vista actual (mismos colores, distribucion, componentes)
- El flujo del constructor (camino paralelo intacto)
- Los PDFs existentes (sin opciones = mismo resultado)

---

## 5. Arquitectura propuesta

```
FLUJO CLASICO (MEJORADO):
  Filtros + [NUEVO: seleccion de campos]
       |
       v
  Vista Previa (respeta campos seleccionados)
       |
       v
  PDF
    -> columnas dinamicas (desde CAMPOS_DISPONIBLES)
    -> anchos proporcionales
    -> orientacion automatica
    -> agrupacion + subtotales (opcional)
    -> ordenamiento dinamico

FLUJO CONSTRUCTOR (INTACTO):
  Wizard -> SQL dinamico -> dataset generico -> ConstructorReport
```

### Nuevos componentes:

| Componente | Archivo | Descripcion |
|------------|---------|-------------|
| Definicion de campos | `reportes_campos.py` | Dict por modulo con ~80 campos |
| Formateadores | `reportes_campos.py` | 9 tipos (texto, moneda, fecha, etc.) |
| Endpoint campos | `reportes_controller.py` | GET `/campos/<modulo>` |
| Columnas dinamicas | `base_report.py` | `_obtener_columnas()`, `_calcular_anchos()` |
| Agrupacion | `base_report.py` | `_construir_tabla_agrupada()` |
| Panel de campos | `dashboard.html` + `GestionReportes.js` | Checkboxes de seleccion |

---

## 6. Como funcionaran los campos

Cada modulo tiene campos disponibles definidos en Python:

```python
CAMPOS_DISPONIBLES = {
    'contratos': {
        'nombre_empresa': {'label': 'Empresa', 'type': 'texto', 'width': 115, 'groupable': True, ...},
        'monto_total': {'label': 'Monto', 'type': 'moneda', 'width': 60, 'aggregate': 'suma', ...},
        # ...
    }
}
```

El usuario ve checkboxes en el panel de filtros:

```
[_REPORTES - Contratos]
Filtros: [Select tipo] [Select patrocinador] [Rango monto] [Fechas]

Campos del reporte:
[x] Empresa     [x] Tipo      [x] Estatus
[x] Inicio      [x] Fin       [x] Dias
[x] Monto       [ ] RIF       [ ] Contacto

Agrupar por: [Ninguno v]
Ordenar por: [Monto v] [Descendente v]

[ Vista Previa ]  [ Descargar PDF ]
```

---

## 7. Como funcionaran filtros

Los filtros existentes NO cambian. Se agregan:

- **`agrupar_por`**: campo del modulo con `groupable: True`
- **`orden_campo`**: cualquier campo sortable
- **`orden_direccion`**: asc/desc
- **`orientacion`**: vertical/horizontal/auto

Todos se validan server-side contra `CAMPOS_DISPONIBLES`.

---

## 8. Como funcionaran agrupaciones

```
ESTADO: Pendiente (3)
  [data rows...]
  Subtotal Pendiente: $15,000

ESTADO: En Progreso (2)
  [data rows...]
  Subtotal En Progreso: $8,000

ESTADO: Completada (5)
  [data rows...]
  Subtotal Completada: $42,000

TOTAL GENERAL: $65,000
```

Solo columnas numericas (moneda, entero, porcentaje) se suman en subtotales.

---

## 9. Como funcionan totales

```
| Columna      | Subtotal Grupo | Total General |
|--------------|---------------|---------------|
| Monto        | $15,000       | $65,000       |
| Cantidad     | 12            | 45            |
```

Calculo: `sum(float(item.get(key, 0) or 0) for item in grupo)`

---

## 10. Como se generara el PDF

```python
# BaseReportGenerator.generate() ampliado:
def generate(self, datos, filtros, kpis, opciones):
    columnas = self._obtener_columnas(opciones)  # NUEVO
    orientacion = opciones.get('orientacion')
    pagina = self._determinar_pagina(columnas, orientacion)  # NUEVO

    # ... header, KPIs, analisis (IGUAL QUE AHORA) ...

    agrupar_por = opciones.get('agrupar_por')
    if agrupar_por:
        rows = self._construir_tabla_agrupada(datos, columnas, agrupar_por)  # NUEVO
    else:
        rows = self._construir_tabla_simple(datos, columnas)  # Refactor del actual

    anchos = self._calcular_anchos(columnas, orientacion)  # NUEVO
    story.extend(self._tabla(rows, colWidths=anchos))

    doc = SimpleDocTemplate(buffer, pagesize=pagina, ...)
    doc.build(story)
```

---

## 11. Seguridad

- **Whitelist de campos:** Solo campos en `CAMPOS_DISPONIBLES` son validos
- **Whitelist de orientacion:** Solo `vertical`/`horizontal`
- **Whitelist de agrupacion:** Solo campos con `groupable: True`
- **Sin SQL dinamico:** El flujo clasico NO construye queries nuevas
- **Permisos:** `@permiso_requerido('reportes.dashboard')` sin cambios
- **Auditoria:** `reportes_generados` registra columnas usadas

---

## 12. Rendimiento

| Estrategia | Cuando |
|-----------|--------|
| Filtros en SQL (migracion gradual) | Fase futura |
| LIMIT 10,000 registros | Siempre |
| Anchos proporcionales | 8+ columnas |
| Landscape automatico | 8+ columnas |
| Fuente reducida (7pt/6pt) | 10+/15+ columnas |
| Truncado de texto | Siempre |

---

## 13. Compatibilidad

| Que | Cambia? |
|-----|---------|
| Vista actual | NO |
| Filtros existentes | NO |
| KPIs existentes | NO |
| Constructor | NO |
| PDFs sin opciones | NO (byte-a-byte identico) |
| Permisos | NO |
| CSS/estilos | NO |
| Base de datos | NO |
| Modelos | NO |

---

## 14. Skills utilizadas

| Skill | Como se usa |
|-------|------------|
| reportes-pdf | Contrato `opciones`, orientacion, columnas, gráficos |
| reportes-detallados | Patron de filtros AJAX progresivos |
| db-transacciones | Parametros SQL %s, DictCursor |
| ponytail | Anti-sobreeningenieria, minimos cambios |

---

## 15. Skills faltantes

| Skill | Prioridad | Impacto |
|-------|-----------|---------|
| `reportes-pdf-dynamic` | CRITICA | Guia de PDF con columnas dinamicas |
| `reportes-data-optimization` | ALTA | Mover filtros a SQL |
| `reportes-testing` | MEDIA | Tests del motor dinamico |

---

## 16. Plan de implementacion

| Fase | Descripcion | Dias |
|------|------------|------|
| F0 | Fundaciones (reportes_campos.py + tests) | 1-2 |
| F1 | Columnas dinamicas en BaseReportGenerator | 2-3 |
| F2 | Endpoint y validacion | 1-2 |
| F3 | Panel de campos en frontend | 2-3 |
| F4 | Orientacion dinamica | 1 |
| F5 | Agrupacion y subtotales | 2-3 |
| F6 | Manejo de muchos campos | 1-2 |
| F7 | Ordenamiento dinamico | 1 |
| F8 | Testing completo | 2-3 |
| F9 | Optimizacion y pulido | 1-2 |
| **TOTAL** | | **14-21 dias** |

---

## 17. Riesgos

| Riesgo | Probabilidad | Mitigacion |
|--------|-------------|------------|
| Regresion en PDFs | MEDIA | Tests byte-a-byte |
| Complejidad UX | MEDIA | Defaults sensatos |
| Rendimiento | MEDIA | Limites claros |
| Duplicacion config | ALTA | Fuente unica futura |

---

## 18. Decisiones pendientes

1. **Instalar `reportes-pdf-dynamic`?** Se recomienda SI.
2. **Migrar filtros a SQL?** Solo si rendimiento lo justifica.
3. **Indices en BD?** Solo si hay evidencia de lentitud.
4. **Plantillas guardadas?** Diferido a fase futura.

---

## 19. Que ocurrira si se responde "APROBADO"

1. Se creara `app/helpers/reportes_campos.py`
2. Se modificara `base_report.py` (metodos nuevos + generate() ampliado)
3. Se ampliara `reportes_controller.py` (endpoint + validacion)
4. Se modificara `dashboard.html` (panel de campos)
5. Se modificara `GestionReportes.js` (logica de campos)
6. Se crearan tests en `tests/`
7. Se actualizara `reportes-context.md`
8. Se actualizara `CHECKLIST.md`

**NO se tocara:**
- Generadores existentes (12 archivos)
- Modelos existentes
- Base de datos
- Constructores
- CSS/estilos
- SocketIO
- Vistas de otros modulos

---

*Propuesta completa para revision. Esperando aprobacion para implementar.*
