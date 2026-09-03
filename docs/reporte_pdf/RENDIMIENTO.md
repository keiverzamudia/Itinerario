# Rendimiento: Analisis y Estrategia

**Fecha:** 2026-09-01

---

## 1. Cuellos de botella actuales

### 1.1 Carga de datos en Python (mayoria de modulos)

```python
# reportes_data.py - patron actual
def _datos_inventario(filtros, fi, ff):
    inv = InventarioModel().consultar()  # SELECT * FROM recursos WHERE eliminado=0
    datos = [r for r in inv if _cumple_filtros(r, filtros)]  # Filtrado en Python
    # ... calculo KPIs ...
    return datos[:2000], kpis
```

**Problema:** Carga TODOS los registros y filtra en Python. Con 100K registros, esto es lento.

### 1.2 Filtros que SI van en SQL

| Modulo | Filtros en SQL | Filtros en Python |
|--------|---------------|-------------------|
| tareas | WHERE ta.Estatus=1, JOIN usuarios | Ninguno (todos van en SQL) |
| bitacora | WHERE created_at BETWEEN, tipo_accion, modulo_filter | Ninguno |
| balance | LIMIT 2000, fecha_inicio/fin, tipo_pago | Ninguno |
| demas | Solo soft-delete | Todos los filtros |

### 1.3 Generacion PDF

- 1,000 filas: ~2-3 segundos (aceptable)
- 5,000 filas: ~10-15 segundos (limite tolerable)
- 10,000+ filas: 30+ segundos (timeout risk con eventlet)

### 1.4 Memoria

- `datos` se carga como `list[dict]` completo en memoria
- `kpis` es un dict pequeño
- El PDF se genera en `io.BytesIO()` - todo en memoria

---

## 2. Estrategia propuesta

### 2.1 Nivel 1: Filtros en SQL (prioritario)

Mover los filtros mas selectivos a SQL para reducir datos cargados:

```python
# Ejemplo: inventario
def _datos_inventario(filtros, fi, ff):
    # ANTES: inv = InventarioModel().consultar() + filtro Python
    # DESPUES: query directa con filtros en SQL

    where = ["r.eliminado = 0"]
    params = []

    if filtros.get('tipo_nombre'):
        where.append("t.nombre = %s")
        params.append(filtros['tipo_nombre'])
    if filtros.get('estado_nombre'):
        where.append("e.nombre = %s")
        params.append(filtros['estado_nombre'])
    if filtros.get('costo_min'):
        where.append("r.costo >= %s")
        params.append(float(filtros['costo_min']))
    if filtros.get('costo_max'):
        where.append("r.costo <= %s")
        params.append(float(filtros['costo_max']))
    if fi:
        where.append("r.fecha_compra >= %s")
        params.append(fi)
    if ff:
        where.append("r.fecha_compra <= %s")
        params.append(ff)

    sql = f"""
        SELECT r.*, t.nombre AS tipo_nombre, e.nombre AS estado_nombre
        FROM recursos r
        LEFT JOIN tipo_recurso t ON r.tipo_id = t.id
        LEFT JOIN estado_recurso e ON r.estado_id = e.id
        WHERE {' AND '.join(where)}
    """

    # Ejecutar y retornar
```

**Impacto:** Reduccion de 90%+ en datos cargados cuando hay filtros activos.

### 2.2 Nivel 2: LIMIT de seguridad

```python
# En todas las funciones de datos:
MAX_REGISTROS = 10000
datos = datos[:MAX_REGISTROS]
if len(datos_original) > MAX_REGISTROS:
    kpis['_ truncado'] = f"Mostrando {MAX_REGISTROS} de {len(datos_original)}"
```

### 2.3 Nivel 3: Streaming para PDFs grandes (futuro)

```python
# Solo si hay 5000+ registros:
from reportlab.lib.units import inch

def _generar_pdf_streaming(datos, columnas, ...):
    """Genera PDF paginado sin cargar todo en memoria."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []

    # Header una vez
    story.extend(self._header(filtros))

    # Paginar datos
    PAGE_SIZE = 50  # filas por pagina
    for i in range(0, len(datos), PAGE_SIZE):
        page_data = datos[i:i + PAGE_SIZE]
        for item in page_data:
            story.append([self._formatear_celda(item, c) for c in columnas])

        if i + PAGE_SIZE < len(datos):
            story.append(PageBreak())

    doc.build(story)
```

Diferido: el limite de 10,000 registros con filtros en SQL es suficiente para ~30 usuarios.

---

## 3. Optimizaciones puntuales

### 3.1 Cache de filtros AJAX

Los filtros AJAX (`_filtros_*`) se ejecutan en cada carga de modulo. Con misma consulta siempre:

```python
# Opcion 1: cache en memoria por request (ya existe via flask.g)
# Opcion 2: cache con TTL corto (60s) si hay mucha carga

from functools import lru_cache

@lru_cache(maxsize=32)
def _cache_filtros_inventario():
    # consulta una vez por request
    pass
```

No implementar a menos que haya evidencia de lentitud.

### 3.2 KPIs calculados en SQL

Los KPIs actualmente se calculan en Python sobre los datos filtrados. Para datos grandes, es mas eficiente:

```sql
-- KPIs de inventario en una sola query
SELECT
    COUNT(*) AS total,
    SUM(costo) AS costo_total,
    AVG(costo) AS costo_promedio
FROM recursos r
LEFT JOIN tipo_recurso t ON r.tipo_id = t.id
LEFT JOIN estado_recurso e ON r.estado_id = e.id
WHERE r.eliminado = 0
  AND (t.nombre = %s OR %s IS NULL)
  AND r.fecha_compra BETWEEN %s AND %s
```

Diferido: los KPIs en Python son correctos y el volumen actual (max ~2000 registros) no justifica la complejidad.

### 3.3 Indices recomendados

| Tabla | Columna | Razon |
|-------|---------|-------|
| `pagos` | `fecha_pago` | Filtro rango frecuente |
| `actividad_usuario` | `created_at` | Filtro rango en bitacora |
| `mantenimientos` | `fecha_ingreso` | Filtro rango |
| `contrato` | `fecha_inicio` | Filtro rango |
| `recursos` | `fecha_compra` | Filtro rango |

**Nota:** Requiere migracion de BD autorizada por el usuario.

---

## 4. Limites propuestos

| Escenario | Limite | Accion |
|-----------|--------|--------|
| Preview (tabla) | 100 filas | Ya implementado |
| PDF clasico | 10,000 filas | Truncar con aviso |
| PDF constructor | 500 filas (LIMITE_FILAS) | Ya implementado |
| Filtros AJAX | 1,000 opciones por select | Ya implementado |
| Memoria PDF | ~50MB | Timeout antes de llegar |

---

## 5. Monitoreo

```python
# En generate(), log de tiempos:
import time

start = time.time()
datos, kpis = _obtener_datos(modulo, filtros)
t_data = time.time() - start

start = time.time()
pdf_bytes = generador.generate(datos, filtros, kpis, opciones)
t_pdf = time.time() - start

logger.info('PDF %s: %d registros, datos=%.2fs, pdf=%.2fs',
            modulo, len(datos), t_data, t_pdf)
```

---

*Documento de analisis de rendimiento.*
