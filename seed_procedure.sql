-- ============================================================
-- PROCEDIMIENTO ALMACENADO: sp_resumen_financiero
-- Estadio Antonio Herrera Gutiérrez
-- ============================================================
-- NOTA: Este procedimiento se crea por separado debido a
-- incompatibilidad de versión de MariaDB (mysql_upgrade
-- requiere permisos root que no están disponibles).
-- Ejecutar después de importar seed_estadio_db.sql
-- ============================================================

DROP PROCEDURE IF EXISTS `sp_resumen_financiero`;

DELIMITER //

CREATE PROCEDURE `sp_resumen_financiero`(
  IN p_fecha_inicio DATE,
  IN p_fecha_fin DATE
)
BEGIN
  -- 1. Resumen de contratos
  SELECT
    COUNT(*) AS total_contratos,
    SUM(CASE WHEN estatus = 'Vigente' THEN 1 ELSE 0 END) AS vigentes,
    SUM(CASE WHEN estatus = 'Vencido' THEN 1 ELSE 0 END) AS vencidos,
    SUM(monto_total) AS monto_total_contratos
  FROM contrato
  WHERE fecha_inicio <= p_fecha_fin AND fecha_fin >= p_fecha_inicio;

  -- 2. Pagos recibidos
  SELECT
    COUNT(*) AS total_pagos,
    SUM(monto) AS monto_total_pagado,
    ROUND(AVG(monto), 2) AS promedio_pago,
    MAX(monto) AS mayor_pago
  FROM pagos
  WHERE fecha_pago BETWEEN p_fecha_inicio AND p_fecha_fin
    AND estado = 1;

  -- 3. Top-10 patrocinadores por monto pagado
  SELECT
    p.nombre_empresa,
    COUNT(pg.id_pago) AS cantidad_pagos,
    SUM(pg.monto) AS monto_total_pagado
  FROM pagos pg
  JOIN contrato c ON pg.id_contrato = c.id_contrato
  JOIN patrocinadores p ON c.id_patrocinador = p.id_patrocinador
  WHERE pg.fecha_pago BETWEEN p_fecha_inicio AND p_fecha_fin
    AND pg.estado = 1
  GROUP BY p.id_patrocinador, p.nombre_empresa
  ORDER BY monto_total_pagado DESC
  LIMIT 10;

  -- 4. Contratos por vencer (próximos 30 días)
  SELECT
    c.id_contrato,
    p.nombre_empresa,
    c.monto_total,
    c.fecha_fin,
    DATEDIFF(c.fecha_fin, CURDATE()) AS dias_restantes
  FROM contrato c
  JOIN patrocinadores p ON c.id_patrocinador = p.id_patrocinador
  WHERE c.estatus = 'Vigente'
    AND c.fecha_fin BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
  ORDER BY c.fecha_fin ASC;
END //

DELIMITER ;
