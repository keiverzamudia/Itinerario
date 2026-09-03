# Auditoria del Modulo Actual de Reportes PDF

**Fecha:** 2026-09-01
**Metodo:** Inspeccion completa de codigo fuente, sin modificaciones.

---

## 1. Archivos involucrados

| Archivo | Lineas | Rol |
|---------|--------|-----|
| `app/controller/reportes_controller.py` | 777 | Rutas Flask, filtros AJAX, dispatch de datos y generadores |
| `app/helpers/reportes_data.py` | 762 | Funciones de obtencion de datos por modulo + KPIs |
| `app/helpers/reportes_utils.py` | 122 | Funciones puras (parseo, ordenamiento, formato) |
| `app/helpers/reportes_catalogo.py` | 770 | Catalogo declarativo (dimensiones, metricas, filtros, fuentes SQL) |
| `app/helpers/reportes_constructor.py` | 238 | Motor SQL del constructor de reportes |
| `app/helpers/generators/base_report.py` | 394 | Clase base para generadores PDF |
| `app/helpers/generators/*_report.py` | 13 archivos | 12 generadores por modulo + 1 constructor |
| `app/model/reportes_model.py` | 82 | CRUD de reportes generados en BD |
| `app/static/js/GestionReportes.js` | 803 | Frontend clasico: MODULE_CONFIG, filtros, preview |
| `app/static/js/ReportesConstructor.js` | 586 | Frontend del wizard constructor |
| `app/view/reportes/dashboard.html` | 380 | Template principal |
| `.opencode/reportes-context.md` | 137 | Contexto tecnico del modulo |

**Total aproximado:** ~5,200 lineas de codigo funcional.

---

## 2. Flujo actual completo

```
USUARIO
  |
  v
[1] Click en tarjeta de modulo (MODULE_CONFIG en GestionReportes.js)
  |
  v
[2] Panel de filtros se abre (filtros dinamicos por modulo, algunos AJAX)
  |
  v
[3] Click "Vista Previa" -> POST /reportes/preview
  |   -> _obtener_datos(modulo, filtros) -> reportes_data.py
  |   -> Retorna: max 100 filas + KPIs + distribuciones
  |   -> Renderiza: KPI cards + tabla preview
  |
  v
[4] Click "Descargar PDF" -> POST /reportes/generar
  |   -> Extrae filtros (whitelist FILTROS_PERMITIDOS)
  |   -> Extrae opciones PDF (resumen, comparar, top_n)
  |   -> _obtener_datos(modulo, filtros) -> (datos, kpis)
  |   -> Si comparar: calcula KPIs periodo anterior
  |   -> _ordenar_datos(datos, campo, direccion)
  |   -> Generador = generadores[modulo]()  # lazy import
  |   -> generador.generate(datos, filtros, kpis, opciones)
  |   -> generador.save(bytes, usuario_id, filtros)
  |   -> Retorna: URL de descarga
  |
  v
[5] PDF servido via GET /reportes/descargar/<nombre>
```

### Flujo del Constructor (paralelo)

```
USUARIO
  |
  v
[1] Click "Constructor avanzado"
  |
  v
[2] Wizard por pasos: Modulo -> Categoria -> Dimension -> Filtros -> Metricas -> Viz -> Resultado
  |
  v
[3] POST /reportes/construir -> reportes_constructor.ejecutar()
  |   -> Valida contra reportes_catalogo.py
  |   -> Arma SQL parametrizado (GROUP BY dinamico)
  |   -> Retorna dataset generico JSON
  |
  v
[4] Preview in-page (tabla, barras CSS, torta conic-gradient, linea SVG)
  |
  v
[5] Exportar PDF/CSV -> POST /reportes/construir/exportar
      -> ConstructorReport.generar(dataset) -> PDF
```

---

## 3. Clases y funciones principales

### BaseReportGenerator (`base_report.py`)

```python
class BaseReportGenerator:
    MODULO = ''      # Identificador del modulo
    TITULO = ''      # Titulo del PDF
    COLUMNAS = []    # Lista fija de (header, key, width_pt)

    def __init__(self, usuario_actual): ...
    def _setup_styles(self): ...           # 4 estilos Paragraph
    def _header(self, filtros): ...        # Cabecera: estadio, fecha, usuario, filtros
    def _tabla(self, datos, style_override): ...  # Tabla estilizada
    def generate(self, datos, filtros, kpis, opciones): ...  # Flujo principal
    def _build_rows(self, datos): ...      # ABSTRACTO: Override en subclases
    def _secciones_analisis(self, kpis, opciones): ...  # resumen + top_n + comparativa
    def _resumen_ejecutivo(self, kpis): ...
    def _top_destacados(self, kpis, n): ...
    def _comparativa_periodos(self, kpis, kpis_previos): ...
    def _seccion_kpis(self, kpis): ...
    def _seccion_distribucion(self, titulo, items, color): ...
    def save(self, pdf_bytes, usuario_id, filtros): ...
```

### Generadores por modulo

Cada generador hereda de `BaseReportGenerator` y define:
- `MODULO`: identificador
- `TITULO`: titulo del PDF
- `COLUMNAS`: lista fija de `(header_label, key, width_pt)`
- `_build_rows(datos)`: convierte datos a filas de tabla
- `generate()` (algunos sobreescriben para layouts especiales)

**Generador mas complejo:** `ReelsReport` (108 lineas) - layout personalizado con secciones KeepTogether por reel y tablas anidadas de videos.

**Generador unico:** `ConstructorReport` - consume dataset generico, no usa COLUMNAS fijas.

### Dispatch de generadores (controller linea ~647)

```python
generadores = {
    'guiones': lambda: __import__('app.helpers.generators.guiones_report', ...),
    'inventario': ...,
    # ... 12 modulos + resumen
}
```

### Funciones de datos (`reportes_data.py`)

```python
OBTENEDORES = {
    'guiones': _datos_guiones,
    'inventario': _datos_inventario,
    # ... 12 modulos + resumen
}

def _obtener_datos(modulo, filtros):
    ob = OBTENEDORES.get(modulo)
    fi, ff = rango_fechas_defecto(modulo, filtros)
    return ob(filtros, fi, ff)  # Retorna (datos, kpis)
```

Cada funcion de datos:
1. Consulta el modelo correspondiente (o ejecuta SQL directo)
2. Aplica filtros en Python (excepto fechas que van en SQL via modelos)
3. Calcula KPIs (total, contadores, distribuciones, promedios)
4. Retorna `(list[dict], dict)` - datos y kpis

### Catalogo declarativo (`reportes_catalogo.py`)

```python
MODULO_BUILDER = {
    'contratos': {
        'nombre': 'Contratos',
        'categorias': {
            'resumen': {'tipo': 'legado'},  # -> usa OBTENEDORES
            'ingresos': {  # -> usa constructor SQL
                'fuente': 'pagos',
                'dimensiones': ['patrocinador', 'tipo_pago', 'mes'],
                'metricas': ['monto_suma', 'pago_promedio', 'pagos_conteo'],
                'filtros': ['fecha', 'patrocinador', 'tipo_pago', 'monto'],
            }
        }
    }
}

FUENTES_SQL = { ... }    # FROM/JOIN por fuente
DIMENSIONES = { ... }     # 30+ dimensiones con SQL
METRICAS = { ... }        # 25+ metricas con agg + formato
FILTROS_BUILDER = { ... } # 40+ filtros con coercion
SOFT_DELETE = { ... }     # WHERE por tabla
```

---

## 4. COLUMNAS por generador (estado actual)

| Modulo | Columnas definidas | Ancho total (pt) |
|--------|-------------------|-----------------|
| guiones | nombre(150), game(40), pregame(50), ejecucion(70), estado(60), tiempo(60) | 430 |
| inventario | id(30), nombre(130), tipo(80), estado(70), compra(70) | 380 |
| premios | nombre(120), patrocinador(90), estado(55), total(35), entreg(40), creacion(65) | 405 |
| contratos | empresa(115), tipo(50), estatus(50), inicio(60), fin(60), dias(35), monto(60) | 430 |
| balance | patrocinador(120), tipo_pago(70), monto(75), referencia(85), fecha(70) | 420 |
| tareas | tarea(150), estado(65), asignado(80), fecha(75) | 370 |
| patrocinadores | empresa(150), rif(75), telefono(75), contrato(70) | 370 |
| usuarios | nombre(110), email(120), rol(70), depto(70), estado(55) | 425 |
| mantenimiento | recurso(110), estado(65), ingreso(65), diagnostico(130) | 370 |
| reels | COLUMNAS = [] (layout custom con KeepTogether) | N/A |
| bitacora | id(30), usuario(85), accion(65), modulo(65), detalle(145), fecha(75) | 465 |
| resumen | modulo(130), total(65), activos(65), inactivos(65), pct(65) | 390 |
| constructor | COLUMNAS = [] (dynamic desde dataset) | N/A |

**Pagina letter:** 612pt ancho. Con margenes 40+40 = 532pt disponibles. Las columnas suman entre 370-465pt, dejando margen razonable.

---

## 5. KPIs por modulo

| Modulo | KPIs |
|--------|------|
| guiones | total, borradores, publicados, en_vivo, finalizados, tiempo_total, promedio_seg |
| inventario | total, costo_total, costo_promedio, tipos(dict), estados(dict) |
| premios | total, pendientes, entregados, tasa_entrega(str), por_patrocinador(dict) |
| contratos | total, vigentes, vencidos, borradores, bronce, plata, oro, monto_total, monto_promedio, monto_vigentes, monto_min, monto_max, vigentes_porcentaje, top_patrocinadores(dict) |
| balance | total_pagos, monto_total, promedio, monto_min, monto_max, tipos_pago(dict) |
| tareas | total, pendientes, en_progreso, completadas, completadas_pct(str) |
| patrocinadores | total, activos, inactivos, por_tipo(dict) |
| usuarios | total, activos, inactivos, roles(dict), departamentos(dict) |
| mantenimiento | total, en_espera, en_reparacion, reparados, dados_baja, promedio_dias(float), top_recursos(dict) |
| reels | total, total_videos, duracion_total(str), duracion_promedio(str) |
| bitacora | total, creaciones, ediciones, eliminaciones, modulos(dict), top_usuarios(dict) |
| resumen | modulos(int), total_registros, total_activos, total_inactivos |

---

## 6. Filtros por modulo

| Modulo | Filtros | Cadenas progresivas |
|--------|---------|-------------------|
| guiones | estado(static), encargado(AJAX), elementos_min/max, fecha_inicio/fin | Ninguna |
| inventario | tipo_nombre(AJAX,progressive), estado_nombre(AJAX,depends), costo_min/max, fecha | tipo_nombre -> estado_nombre |
| premios | estado(static,progressive), patrocinador_id(AJAX,depends), cantidad_min/max, entregada_min/max, fecha | estado -> patrocinador |
| contratos | tipo(static,progressive), estatus(static), patrocinador_id(AJAX,depends), monto_min/max, fecha | tipo -> patrocinador |
| balance | tipo_pago(AJAX), patrocinador_id(AJAX), monto_min/max, fecha | Ninguna |
| tareas | estado(static,progressive), asignado_a(AJAX,depends), fecha | estado -> asignado_a |
| patrocinadores | tipo_contrato(static), estado_pat(static), fecha | Ninguna |
| usuarios | departamento(AJAX,progressive), rol(AJAX,depends), activo(static), fecha | departamento -> rol |
| mantenimiento | estado(static,progressive), recurso_id(AJAX,depends), dias_min/max, fecha | estado -> recurso |
| reels | patrocinador_id(AJAX), duracion_min/max, fecha | Ninguna |
| bitacora | usuario_id(AJAX), tipo_accion(AJAX), modulo_filter(AJAX), fecha | Ninguna |

**Todos aceptan:** `fecha_inicio`, `fecha_fin`

---

## 7. Limitaciones identificadas

### 7.1 Rigidness de columnas
- Cada modulo tiene COLUMNAS hardcoded en el generador
- El usuario NO puede seleccionar que columnas aparecen en el PDF
- Agregar una columna nueva requiere modificar el generador + reportes_data.py + COLUMNAS_PREVIEW en controller + MODULE_CONFIG en JS

### 7.2 Sin agrupacion en PDF clasico
- Solo el constructor soporta GROUP BY
- El flujo clasico muestra todas las filas sin agrupar
- No hay subtotales en el PDF clasico

### 7.3 Sin ordenamiento dinamico
- El usuario puede ordenar en preview pero el PDF ignora esa opcion
- El orden del PDF es el que devuelve el modelo

### 7.4 Filtros en Python vs SQL
- Solo tareas y bitacora filtran directamente en SQL
- Los demas modulos cargan TODO y filtran en Python
- Riesgo de rendimiento con grandes volumenes

### 7.5 Sin seleccion de campos por modulo
- Todos los campos disponibles se muestran siempre
- No hay concepto de "reporte con 5 campos" vs "reporte con 20 campos"

### 7.6 Manejo limitado de muchos campos
- El ancho de pagina letter (532pt util) soporta ~7-8 columnas comodamente
- Con 10+ columnas el PDF se comprime o recorta
- No hay deteccion automatica de landscape

### 7.7 Sin paginacion de datos grandes
- `limit=2000` hardcodeado en balance, `limite=5000` en bitacora
- Sin streaming: todo se carga en memoria

### 7.8 Duplicacion de configuracion
- Columnas definidas en 3 lugares: generador Python, COLUMNAS_PREVIEW en controller, columns en MODULE_CONFIG JS

---

## 8. Dependencias

| Dependencia | Uso | Ya instalada |
|------------|-----|-------------|
| reportlab | Generacion PDF | Si |
| PyMySQL | Consultas SQL | Si |
| Flask | Web framework | Si |
| Jinja2 | Templates HTML | Si |

**Cero dependencias nuevas necesarias** para la fase de diseno.

---

## 9. Capacidades existentes reutilizables

1. **Whitelist de filtros** (`FILTROS_PERMITIDOS`): validacion server-side de parametros
2. **Progressive filters**: cascada de selects via AJAX
3. **KPIs calculados server-side**: totales, distribuciones, promedios
4. **Analysis options**: resumen ejecutivo, Top-N, comparativa de periodos
5. **Catalogo declarativo**: dimensiones, metricas, filtros por modulo
6. **Motor SQL parametrizado**: construccion segura de queries
7. **Dataset generico**: formato estandar para el constructor
8. **BaseReportGenerator**: estilos, header, tabla, KPIs, distribuciones
9. **Save + bitacora**: registro de PDFs generados
10. **Two systems**: clasico + constructor, ambos funcionales

---

*Documento generado por auditoria completa del codigo fuente. Sin modificaciones.*
