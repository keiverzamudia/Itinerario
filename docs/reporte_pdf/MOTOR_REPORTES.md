# Motor de Reportes: Diseno Detallado

**Fecha:** 2026-09-01

---

## 1. Concepto

El motor es la capa que toma:
- Una fuente de datos (el modulo)
- Campos seleccionados por el usuario
- Filtros aplicados
- Ordenamiento elegido
- Agrupacion solicitada
- Opciones de formato

Y produce:
- Datos procesados listos para renderizar
- Un PDF configurado dinamicamente

---

## 2. Componentes del motor

```
REPORTE
  |
  +-- CAMPO DEFINITION (campos.py)
  |     |
  |     +-- label, key, type, width, order, formatter
  |
  +-- DATA PROVIDER (reportes_data.py, existente)
  |     |
  |     +-- OBTENEDORES dict -> (datos, kpis)
  |
  +-- FIELD SELECTOR (nuevo)
  |     |
  |     +-- CAMPOS_DISPONIBLES[modulo] -> subset
  |     +-- COLUMNAS_DEFAULT[modulo] -> fallback
  |
  +-- FILTER ENGINE (existente, whitelist)
  |     |
  |     +-- FILTROS_PERMITIDOS + _filtros_del_request
  |
  +-- SORT ENGINE (existente, _ordenar_datos)
  |     |
  |     +-- campo + direccion
  |
  +-- GROUP ENGINE (nuevo)
  |     |
  |     +-- agrupar_por campo -> OrderedDict
  |     +-- subtotales numericos
  |     +-- total general
  |
  +-- PDF RENDERER (existente, ampliado)
        |
        +-- orientation dinamica
        +-- columnas dinamicas
        +-- anchos calculados
        +-- formateadores por tipo
```

---

## 3. Flujo de datos detallado

### Paso 1: Definicion de campos disponibles

```python
# reportes_campos.py

CAMPOS_DISPONIBLES = {
    '<modulo>': {
        '<campo_key>': {
            'label': str,       # Nombre para mostrar en UI y PDF
            'key': str,         # Clave en el dict de datos
            'type': str,        # Tipo para formateo
            'width': int,       # Ancho sugerido en puntos
            'order': int,       # Orden de aparicion
            'groupable': bool,  # Se puede agrupar por este campo
            'sortable': bool,   # Se puede ordenar por este campo
            'aggregate': str|None,  # Tipo de agregacion (suma, conteo, promedio)
        }
    }
}
```

### Paso 2: Seleccion de campos

El usuario interactua con checkboxes en el panel de filtros:

```
[x] Nombre          [x] Estado
[x] Tipo            [ ] Descripcion
[x] Fecha Compra    [x] Costo
[ ] ID
```

- Por defecto: `COLUMNAS_DEFAULT[modulo]` (las mismas que hoy)
- El usuario puede agregar/quitar campos
- Validacion: al menos 1 campo seleccionado

### Paso 3: Resolucion de columnas

```python
def _resolver_columnas(modulo, campos_seleccionados):
    """Convierte keys de campos en tuplas (label, key, width) para BaseReportGenerator."""
    disponibles = CAMPOS_DISPONIBLES[modulo]
    columnas = []
    for key in campos_seleccionados:
        if key in disponibles:
            campo = disponibles[key]
            columnas.append((campo['label'], campo['key'], campo['width']))
    # Ordenar por 'order'
    columnas.sort(key=lambda c: disponibles[c[1]]['order'])
    return columnas
```

### Paso 4: Calculo de anchos dinamicos

```python
def _calcular_anchos(columnas, orientacion='vertical'):
    """Calcula anchos proporcionales para caber en la pagina."""
    if orientacion == 'horizontal':
        disponible = 712  # landscape(letter) - margenes
    else:
        disponible = 532  # letter - margenes (40+40)

    total_sugerido = sum(c[2] for c in columnas)
    if total_sugerido <= disponible:
        return [c[2] for c in columnas]  # caben, usar anchos sugeridos

    # Escalar proporcionalmente
    factor = disponible / total_sugerido
    return [max(30, int(c[2] * factor)) for c in columnas]  # min 30pt
```

### Paso 5: Formateo de celdas

```python
def _formatear_celda(self, item, columna):
    """Formatea un valor segun el tipo de campo."""
    key = columna[1]
    value = item.get(key)
    tipo = self._obtener_tipo(key)  # desde CAMPOS_DISPONIBLES

    formatter = FORMATTERS.get(tipo, FORMATTERS['texto'])
    texto = formatter(value)

    # Truncar si es muy largo para el ancho de columna
    ancho = columna[2]
    if len(texto) > ancho // 5:  # estimacion ~5pt por caracter
        texto = texto[:ancho // 5 - 2] + '..'

    return Paragraph(texto, self.style_normal)
```

---

## 4. Agrupacion

### 4.1 Flujo

```
DATOS ORDENADOS
  |
  v
GROUP BY campo_agrupacion
  |
  v
Para cada grupo:
  |
  +-- Fila de grupo (encabezado)
  +-- Filas de datos del grupo
  +-- Fila de subtotal (suma de columnas numericas)
  |
  v
Fila de total general
```

### 4.2 Identificacion de columnas numericas

```python
CAMPOS_NUMERICOS = {'entero', 'moneda', 'decimal', 'porcentaje'}

def _columnas_agregables(columnas):
    """Retorna las columnas que pueden sumarse."""
    return [c for c in columnas if CAMPOS_DISPONIBLES[modulo][c[1]]['type'] in CAMPOS_NUMERICOS]
```

### 4.3 Subtotales

```python
def _calcular_subtotales(self, items_grupo, columnas):
    """Suma columnas numericas de un grupo."""
    agregables = _columnas_agregables(columnas)
    subtotales = {}
    for col in agregables:
        key = col[1]
        total = sum(float(item.get(key, 0) or 0) for item in items_grupo)
        subtotales[key] = total
    return subtotales
```

---

## 5. Ordenamiento

```python
# Ya existe: _ordenar_datos() en reportes_utils.py
# Se amplia para soportar ordenamiento por cualquier campo

def _ordenar_datos(datos, campo, direccion='asc'):
    """Ordena por campo, soportando strings, numeros, fechas."""
    def clave(item):
        val = item.get(campo)
        if val is None:
            return ''
        if isinstance(val, str):
            # Intentar parsear como numero (ej: "$12,000" -> 12000)
            limpio = val.replace('$', '').replace(',', '').strip()
            try:
                return float(limpio)
            except ValueError:
                return val.lower()
        return val
    return sorted(datos, key=clave, reverse=(direccion == 'desc'))
```

---

## 6. Orientacion automatica

```python
def _determinar_pagina(columnas_seleccionadas, orientacion_solicitada):
    """Determina tamano y orientacion de pagina."""
    from reportlab.lib.pagesizes import letter, landscape

    if orientacion_solicitada == 'horizontal':
        return landscape(letter)

    # Calcular ancho necesario
    total_width = sum(c[2] for c in columnas_seleccionadas)

    # Con 8+ columnas o ancho > 500pt, landscape automatico
    if len(columnas_seleccionadas) >= 8 or total_width > 500:
        return landscape(letter)

    return letter
```

---

## 7. Gestion de muchos campos

### Estrategia por cantidad de columnas:

| Columnas | Estrategia |
|----------|-----------|
| 1-5 | Portrait, anchos originales |
| 6-7 | Portrait, anchos escalados proporcionalmente |
| 8-10 | Landscape automatico, anchos escalados |
| 11-15 | Landscape, fuentes reducidas (7pt), texto truncado |
| 16-20 | Landscape, fuentes 6pt, texto truncado agresivo, sin descripcion larga |
| 20+ | Aviso "Demasiadas columnas para una pagina" + sugerencia de reducir |

### Implementacion:

```python
def _ajustar_estilo_segun_columnas(self, num_columnas):
    """Ajusta tamanos de fuente segun cantidad de columnas."""
    if num_columnas <= 7:
        return  # estilos default
    elif num_columnas <= 10:
        self.style_normal.fontSize = 7
        self.style_bold.fontSize = 7
    else:
        self.style_normal.fontSize = 6
        self.style_bold.fontSize = 6
```

---

*Documento de diseno del motor de reportes.*
