# Decisiones Arquitectonicas

**Fecha:** 2026-09-01

---

## D1: Evolucionar el clasico vs reemplazar

**Alternativas:**
- A) Reemplazar todo por el constructor
- B) Evolucionar solo el clasico
- C) Unificar ambos en un solo flujo

**Ventajas A:** Un solo camino, menos codigo.
**Desventajas A:** Rompe la UX existente, el usuario perderia el flujo conocido.

**Ventajas B:** Zero regressions, el usuario no nota el cambio.
**Desventajas B:** Dos caminos paralelos (ya existe).

**Ventajas C:** Consistencia total.
**Desventajas C:** Complejidad enorme, requiere reescribir 12 generadores.

**Decision:** B - Evolucionar solo el clasico.

**Motivo:** El usuario pidio explicitamente NO CAMBIAR LA VISTA ACTUAL. El constructor ya funciona como camino alternativo. La mejora es sobre el clasico.

---

## D2: Donde vive la definicion de campos

**Alternativas:**
- A) En Python (`reportes_campos.py`)
- B) En JavaScript (`MODULE_CONFIG`)
- C) En la BD (tabla nueva)

**Ventajas A:** Seguridad (whitelist server-side), testeable, coherente con `reportes_catalogo.py`.
**Desventajas A:** Un archivo nuevo.

**Ventajas B:** Rapido de prototipar.
**Desventajas B:** Inseguro (el cliente puede enviar cualquier cosa), duplicado con backend.

**Ventajas C:** Maximum flexibilidad.
**Desventajas C:** Requiere migracion, complejidad innecesaria.

**Decision:** A - Python dict.

**Motivo:** Ya existe el patron en `reportes_catalogo.py`. Seguridad: whitelist server-side.

---

## D3: Cambiar BaseReportGenerator vs crear subclase

**Alternativas:**
- A) Modificar `generate()` en la clase base
- B) Crear `DynamicReportGenerator` que hereda
- C) Crear mixin `DynamicColumnsMixin`

**Ventajas A:** Un solo lugar, todos los generadores heredan gratis.
**Desventajas A:** Riesgo de regresion si se hace mal.

**Ventajas B:** Cero riesgo de regresion.
**Desventajas B:** Duplicacion de logica de header/kpis/save.

**Ventajas C:** Composicion limpia.
**Desventajas C:** Complejidad de herencia multiple.

**Decision:** A - Modificar la clase base, con proteccion `if columnas_seleccionadas`.

**Motivo:** El patron `opciones` ya existe en `generate()`. La proteccion `if` garantiza que sin opciones nuevas, el comportamiento es identico. Los 12 generadores no se tocan.

---

## D4: Agrupacion en Python vs SQL

**Alternativas:**
- A) GROUP BY en SQL (como el constructor)
- B) Agrupacion en Python (OrderedDict)
- C) Ambas, elegir segun volumen

**Ventajas A:** Eficiente para datos grandes.
**Desventajas A:** Requiere modificar las funciones de datos para soportar GROUP BY.

**Ventajas B:** Simple, funciona con los datos ya cargados.
**Desventajas B:** Lento con muchos registros.

**Ventajas C:** Optimo en ambos casos.
**Desventajas C:** Complejidad de decidir.

**Decision:** B - Agrupacion en Python.

**Motivo:** El flujo clasico ya carga los datos en Python. La agrupacion es sobre esos datos. Para el volumen actual (max 2000 registros), Python es suficiente. Si se necesita SQL GROUP BY, el constructor ya lo hace.

---

## D5: Orientacion automatica vs manual

**Alternativas:**
- A) Siempre portrait, el usuario elige landscape
- B) Automatica segun cantidad de columnas
- C) Manual con sugerencia automatica

**Ventajas A:** Control total del usuario.
**Desventajas A:** El usuario puede elegir mal.

**Ventajas B:** Siempre optimo.
**Desventajas B:** El usuario pierde control.

**Ventajas C:** Mejor de ambos mundos.
**Desventajas C:** Mas complejo de implementar.

**Decision:** B - Automatica.

**Motivo:** El usuario no sabe cuantos puntos ocupan 10 columnas. La automatica produce mejor resultado. Si el usuario quiere forzar, puede cambiar la opcion.

---

## D6: Panel de campos como checkbox vs dropdown

**Alternativas:**
- A) Checkboxes (seleccion multiple)
- B) Dropdown con multi-select
- C) Drag-and-drop para ordenar

**Ventajas A:** Visible, intuitivo, rapido.
**Desventajas A:** Ocupa espacio vertical.

**Ventajas B:** Compacto.
**Desventajas B:** Menos intuitivo para seleccion multiple.

**Ventajas C:** Control total de orden.
**Desventajas C:** Complejidad de implementacion.

**Decision:** A - Checkboxes.

**Motivo:** El usuario necesita ver TODOS los campos disponibles y seleccionar cuales quiere. Checkboxes es el patron mas directo para esto.

---

## D7: Defaults de columnas

**Alternativas:**
- A) Mismas columnas que el generador actual
- B) Todas las columnas disponibles
- C) Columnas "populares" (las mas usadas)

**Ventajas A:** Zero regressions, el usuario ve lo mismo de siempre.
**Desventajas A:** No muestra que hay mas campos disponibles.

**Ventajas B:** Muestra todo, el usuario quita lo que no quiere.
**Desventajas B:** PDF potencialmente largo.

**Ventajas C:** Balance.
**Desventajas C:** Requiere tracking de uso.

**Decision:** A - Mismas columnas que el generador actual.

**Motivo:** El usuario pidio NO CAMBIAR LA VISTA ACTUAL. Defaults = comportamiento actual. El usuario descubre los campos adicionales en el panel.

---

*Documento de decisiones arquitectonicas.*
