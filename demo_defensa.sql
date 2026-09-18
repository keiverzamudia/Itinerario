-- ============================================================
-- SCRIPT DE DEMOSTRACION — OBJETOS SQL
-- Para la defensa de Itinerario — Estadio Antonio Herrera Gutierrez
-- ============================================================

-- ============================================================
-- 1. VISTA: v_balance_contratos
-- ============================================================
-- Que hace: Une contratos + patrocinadores + pagos
-- Resultado: monto_total, monto_pagado, saldo_pendiente, porcentaje_pagado

USE estadio_db;

SELECT * FROM v_balance_contratos;

-- Solo contratos vigentes
SELECT * FROM v_balance_contratos WHERE estatus_contrato = 'Vigente';

-- Ver el saldo pendiente de cada patrocinador
SELECT 
    patrocinador,
    monto_total,
    monto_pagado,
    saldo_pendiente,
    porcentaje_pagado
FROM v_balance_contratos
ORDER BY saldo_pendiente DESC;


-- ============================================================
-- 2. TRIGGERS: Auditoria en pagos
-- ============================================================
-- trg_pagos_after_insert: Cuando creas un pago, registra en bitacora
-- trg_pagos_after_update: Cuando modificas un pago, guarda antes/despues

-- Ver los triggers existentes
SHOW TRIGGERS WHERE `Table` = 'pagos';

-- Insertar un pago de prueba (esto activa el trigger automaticamente)
INSERT INTO pagos (contrato_id, monto, fecha_pago, metodo_pago, referencia, estado)
VALUES (1, 5000.00, '2026-09-18', 'Transferencia', 'DEMO-001', 1);

-- Ver que el trigger registro el pago en la bitacora
SELECT * FROM seguridad.actividad_usuario 
WHERE modulo = 'pagos' 
ORDER BY timestamp DESC 
LIMIT 5;


-- ============================================================
-- 3. PROCEDIMIENTO: sp_resumen_financiero
-- ============================================================
-- Un solo llamado genera 4 result sets:
--   Result 1: Resumen de contratos
--   Result 2: Pagos recibidos
--   Result 3: Top-10 patrocinadores
--   Result 4: Contratos por vencer

CALL sp_resumen_financiero('2026-01-01', '2026-12-31');

-- Para ver los resultados, ejecutar en phpMyAdmin o MySQL Workbench
-- Cada CALL genera 4 tablas separadas


-- ============================================================
-- 4. VERIFICACION DE OBJETOS
-- ============================================================

-- Ver todas las vistas
SHOW FULL TABLES WHERE Table_type = 'VIEW';

-- Ver todos los triggers
SHOW TRIGGERS;

-- Ver todos los procedimientos
SHOW PROCEDURE STATUS WHERE Db = 'estadio_db';

-- Ver la estructura de la vista
SHOW CREATE VIEW v_balance_contratos;

-- Ver la estructura del procedimiento
SHOW CREATE PROCEDURE sp_resumen_financiero;
