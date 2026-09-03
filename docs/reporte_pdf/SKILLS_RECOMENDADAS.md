# Skills Recomendadas

**Fecha:** 2026-09-01

---

## 1. Skills ya disponibles y utilizadas

| Skill | Uso actual | Relevancia para reportes PDF |
|-------|-----------|----------------------------|
| `reportes-pdf` | Guia de personalizacion PDF con `opciones` dict | **ALTA** - Define contrato de opciones (orientacion, columnas, top_n, etc.) |
| `reportes-detallados` | Patron "efecto bitacora" para filtros progresivos | **ALTA** - Define como cargar datos desde BD real |
| `db-transacciones` | Reglas de acceso a datos PyMySQL | **ALTA** - Parametros %s, transaction(), DictCursor |
| `refactor-controladores` | Patrones de refactor de controllers Flask | **MEDIA** - Para dividir reportes_controller si crece |
| `ponytail` | Anti-sobreeningenieria, YAGNI | **MEDIA** - Recordatorio constante de no sobre-disenar |

### 1.1 reportes-pdf (CRITICA)

Ya define:
- Contrato `opciones` en `generate()`
- Orientacion, titulo/subtitulo, columnas, top_n, agrupar_por
- Gráficos con reportlab nativo (sin deps nuevas)
- Orden de construccion recomendado

**Esta skill ES la base del diseno propuesto.** La propuesta la implementa.

### 1.2 reportes-detallados (CRITICA)

Ya define:
- Filtros AJAX cargados desde BD real
- Progresividad progressive/dependsOn
- KPIs server-side con lo filtrado
- Receta por modulo

**Se reutiliza para nuevos filtros si se agregan campos calculados.**

---

## 2. Skills disponibles pero no necesarias para esta fase

| Skill | Por que no |
|-------|-----------|
| `envivo-*` (9 skills) | Son del modulo EN VIVO, no de reportes |
| `interface-design` | No se esta disenando UI nueva |
| `accessibility` | No se esta cambiando la vista |
| `ponytail-audit` | Ya se hizo internamente |
| `ponytail-review` | Aplicado durante el diseno |
| `security-and-hardening` | Ya cubierto por skills de reportes + db-transacciones |
| `tdd` | Util para testing pero no critico para diseno |
| `code-review` | Util post-implementacion |
| `diagnosing-bugs` | No hay bugs que diagnosticar |

---

## 3. Skills faltantes recomendadas

### 3.1 `reportes-pdf-dynamic` (CRITICA)

**Proposito:** Guia especializada en generacion de PDFs con columnas dinamicas, anchos proporcionales, paginacion inteligente y manejo de muchos campos.

**Problema que resolveria:**
- No hay guia para calcular anchos de columna dinamicamente
- No hay patron para paginacion con encabezados repetidos
- No hay estrategia documentada para 10+ columnas en una pagina
- No hay formateo estandarizado por tipo de dato

**Que parte mejoraria:**
- `base_report.py`: generacion de tablas dinamicas
- `reportes_campos.py`: formateadores
- Calidad del PDF con muchas columnas

**Prioridad:** CRITICA

**Vale la pena?** SI. Es el corazon de la funcionalidad nueva. Sin ella, cada implementador tendra que resolver los mismos problemas de layout PDF desde cero.

**Contenido sugerido:**
- Algoritmo de calculo de anchos proporcionales
- Patron para `colWidths` dinamicos en reportlab
- Estrategia de truncado de texto por ancho de columna
- Encabezados repetidos en `onFirstPage`/`onLaterPages`
- Deteccion automatica portrait/landscape
- Formateo de celdas por tipo
- Manejo de subtotales en tabla
- Manejo de texto largo (WrappedParagraph)
- Limites praticos (max columnas, max filas)

---

### 3.2 `reportes-data-optimization` (ALTA)

**Proposito:** Guia para mover filtros de Python a SQL, optimizar consultas, y manejar grandes volumenes en el contexto de Itinerario.

**Problema que resolveria:**
- La mayoria de modulos cargan TODO y filtran en Python
- No hay patron para construir queries parametrizadas con filtros dinamicos
- No hay estrategia para 10K+ registros

**Que parte mejoraria:**
- `reportes_data.py`: funciones de datos por modulo
- Rendimiento con filtros activos
- Consistencia con `reportes_constructor.py` (que SI filtra en SQL)

**Prioridad:** ALTA

**Vale la pena?** SI, pero solo si se detecta que el rendimiento actual es insuficiente. Para ~30 usuarios y max 2000 registros, el enfoque actual funciona. La skill seria mas valiosa si el sistema crece.

---

### 3.3 `reportes-testing` (MEDIA)

**Proposito:** Suite de tests especifica para el motor de reportes dinamico.

**Problema que resolveria:**
- Los tests actuales (`test_reportes_filtros.py`, `test_reportes_pdf.py`) prueban el flujo clasico
- No hay tests para columnas dinamicas, agrupacion, subtotales
- No hay tests de rendimiento

**Que parte mejoraria:**
- Cobertura de tests del nuevo motor
- Regresion: PDF sin opciones sigue igual
- Validacion de columnas seleccionadas

**Prioridad:** MEDIA

**Vale la pena?** SI, pero se puede construir con las convenciones de `tests-pytest` existente. No necesita una skill dedicada.

---

## 4. Skills que NO vale la pena instalar

| Skill | Razon |
|-------|-------|
| `emil-design-eng` | Filosofia UI/animaciones. No aplica a PDFs estaticos |
| `interface-design` | Para dashboards/paneles interactivos. El PDF no es interactivo |
| `ponytail-gain` | Scoreboards de impacto. Util pero no critico |
| `ponytail-debt` | Ledger de deuda. Util pero no critico |
| `webapp-testing` | Playwright para UI web. Los tests de PDF son diferentes |

---

## 5. Resumen

| Skill | Prioridad | Instalar? |
|-------|-----------|-----------|
| reportes-pdf (existente) | CRITICA | Ya instalada, reutilizar |
| reportes-detallados (existente) | CRITICA | Ya instalada, reutilizar |
| db-transacciones (existente) | ALTA | Ya instalada, reutilizar |
| reportes-pdf-dynamic (NUEVA) | CRITICA | **SI instalar** |
| reportes-data-optimization (NUEVA) | ALTA | Instalar si rendimiento es problema |
| reportes-testing (NUEVA) | MEDIA | Opcional, cubierto por tests-pytest |

**Decision final:** Instalar SOLO `reportes-pdf-dynamic`. Las demas son opcionales o ya existen.

---

*Documento de analisis de skills.*
