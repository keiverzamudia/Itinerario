# Compatibilidad con el Sistema Existente

**Fecha:** 2026-09-01

---

## 1. Principio fundamental

> NO CAMBIAR LA VISTA ACTUAL. NO ROMPER EL SISTEMA EXISTENTE.

El usuario debe percibir la misma aplicacion. La diferencia esta en la potencia interna.

---

## 2. Que NO cambia

| Componente | Estado | Razon |
|------------|--------|-------|
| `MODULOS_DISPONIBLES` | Intacto | Ya funciona |
| Rutas `/reportes/*` | Intactas | Ya funcionan |
| `MODULE_CONFIG` (JS) | Intacto | Legado se conserva |
| `_filtros_*` handlers | Intactos | Se reutilizan |
| `OBTENEDORES` dict | Intacto | Legado se conserva |
| `BaseReportGenerator.save()` | Intacto | Registro en bitacora |
| Los 12 `<Modulo>Report` | Intactos | Default = comportamiento actual |
| `FILTROS_PERMITIDOS` | Intacto | Se amplia, no se reemplaza |
| `COLUMNAS_PREVIEW` (controller) | Intacto | Legado se conserva |
| Filtros progresivos AJAX | Intactos | Ya funcionan |
| KPIs del preview | Intactos | Ya funcionan |
| Panel de filtros | Intacto | Se agrega seccion de campos |
| Wizard del constructor | Intacto | Camino paralelo |
| `ReporteModel` | Intacto | Registro de PDFs |
| Permisos | Intactos | Sin cambios |
| CSRF | Intacto | Sin cambios |
| CSS/estilos | Intactos | Sin cambios visuales |

---

## 3. Que se AGREGA (sin modificar existente)

| Componente | Archivo | Tipo |
|------------|---------|------|
| `CAMPOS_DISPONIBLES` dict | `reportes_campos.py` | Nuevo archivo |
| `FORMATTERS` dict | `reportes_campos.py` | Nuevo en mismo archivo |
| `COLUMNAS_DEFAULT` dict | `reportes_campos.py` | Nuevo en mismo archivo |
| Endpoint `/campos/<modulo>` | `reportes_controller.py` | Nueva ruta |
| Parametro `columnas_seleccionadas` | `generar()` | Ampliacion |
| Parametro `orientacion` | `generar()` | Ampliacion |
| Parametro `agrupar_por` | `generar()` | Ampliacion |
| Panel de campos checkboxes | `dashboard.html` | Nuevo contenedor |
| Logica de campos | `GestionReportes.js` | Nuevas funciones |
| `_obtener_columnas()` | `base_report.py` | Nuevo metodo |
| `_calcular_anchos()` | `base_report.py` | Nuevo metodo |
| `_construir_tabla_agrupada()` | `base_report.py` | Nuevo metodo |

---

## 4. Compatibilidad con el Constructor

El constructor y el flujo clasico son **caminos paralelos** que no se interfieren:

```
USUARIO
  |
  +-- Click modulo clasico --> Filtros --> Preview --> PDF clasico (MEJORADO)
  |
  +-- Click "Constructor" --> Wizard --> Dataset --> ConstructorReport (INTACTO)
```

- El constructor usa `reportes_constructor.py` + `constructor_report.py`
- El clasico usa `reportes_data.py` + `<modulo>_report.py`
- No comparten estado ni se pisan

---

## 5. Compatibilidad con filtros existentes

Los filtros AJAX existentes siguen funcionando igual. El panel de campos es **adicional**:

```
Panel de filtros (existente):
  [Select estado] [Select encargado] [Rango elementos] [Fechas]

Seccion de campos (nueva, debajo de filtros):
  [x] Nombre  [x] Estado  [x] Tipo  [ ] Descripcion  [x] Costo

Botones (existentes):
  [Vista Previa]  [Descargar PDF]
```

---

## 6. Compatibilidad de datos

### 6.1 Preview

El preview muestra las columnas seleccionadas (o las default si no selecciona).

### 6.2 PDF

El PDF respeta las columnas seleccionadas. Sin seleccion = PDF identico al actual.

### 6.3 Registro

`reportes_generados` registra el PDF con las columnas usadas en `filtros` JSON.

---

## 7. Estrategia de migracion

```
FASE 1: Agregar CAMPOS_DISPONIBLES + endpoint /campos
  -> No afecta nada existente
  -> Solo se agrega infraestructura

FASE 2: Ampliar BaseReportGenerator
  -> Si no se envia columnas_seleccionadas, comportamiento identico al actual
  -> Zero regressions

FASE 3: Agregar panel de campos al frontend
  -> Por defecto muestra las columnas actuales
  -> El usuario puede cambiar o dejar como esta

FASE 4: Agregar agrupacion
  -> Sin agrupar_por = comportamiento identico al actual
  -> Solo se activa cuando el usuario lo pide
```

---

## 8. Testing de compatibilidad

Para cada fase, verificar:

1. Sin opciones nuevas: PDF generado es byte-a-byte identico al anterior
2. Con columnas_seleccionadas: PDF respeta la seleccion
3. Con agrupar_por: PDF muestra subtotales
4. Preview: respeta columnas seleccionadas
5. Filtros AJAX: siguen funcionando igual
6. KPIs: se calculan igual
7. save(): registra correctamente

---

*Documento de compatibilidad con el sistema existente.*
