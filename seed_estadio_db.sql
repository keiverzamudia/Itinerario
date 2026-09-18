-- ============================================================
-- SEED DATA: estadio_db — Estadio Antonio Herrera Gutiérrez
-- Cardenales de Lara — Datos realistas para defensa
-- ============================================================

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- -----------------------------------------------------------
-- 0. DEPARTAMENTOS (lookup)
-- -----------------------------------------------------------
INSERT INTO `departamentos` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Producción', 'Puesta en escena, guiones y transmisión'),
(2, 'Técnica', 'Soporte técnico, mantenimiento de equipos'),
(3, 'Comercial', 'Gestión de patrocinadores y contratos'),
(4, 'Administración', 'Gestión general del estadio'),
(5, 'Operaciones', 'Operaciones en vivo y palco');

-- -----------------------------------------------------------
-- 1. PATROCINADORES — Empresas venezolanas reales
-- -----------------------------------------------------------
INSERT INTO `patrocinadores` (`id_patrocinador`, `nombre_empresa`, `rif`, `tipo_contrato`, `nombre_contacto`, `telefono`, `email`, `estado`, `encargado_id`) VALUES
(1,  'Maltin Polar',            'J-00005820-9',  2, 'José Luis Rodríguez',    '0212-4003000', 'jrodriguez@polar.com',        1, NULL),
(2,  'Pepsi Venezuela',         'J-00028049-5',  2, 'María Fernanda López',    '0212-5002000', 'mlopez@pepsi.com',            1, NULL),
(3,  'Café Flor de Arauca',     'J-40206831-0',  1, 'Carlos Mendoza',          '0251-2661100', 'cmendoza@cafeflor.com',       1, NULL),
(4,  'Tubrica C.A',             'J-310284567',   1, 'Pedro Jiménez',           '0241-8581000', 'pjimenez@tubrica.com',        1, NULL),
(5,  'Banesco Banco Universal', 'J-00078321-3',  2, 'Ana Sofía Pérez',         '0212-2064646', 'aperez@banesco.com',          1, NULL),
(6,  'Movilnet C.A',            'J-30472189-0',  1, 'Roberto Díaz',            '0212-3001000', 'rdiaz@movilnet.com',          1, NULL),
(7,  'Alimentos Mary',          'J-29587314-6',  1, 'Luis Hernández',          '0241-8782000', 'lhernandez@alimentosmary.com',1, NULL),
(8,  'Farmatodo C.A',           'J-00032815-8',  2, 'Gabriela Torres',         '0212-7003000', 'gtorres@farmatodo.com',       1, NULL),
(9,  'Cerveza Regional',        'J-40157623-8',  1, 'Manuel Castillo',         '0261-7984000', 'mcastillo@regional.com',      1, NULL),
(10, 'Empresas Polar',          'J-00005804-7',  2, 'Lorenzo Mendoza',         '0212-4003000', 'lmendoza@polar.com',          1, NULL);

-- -----------------------------------------------------------
-- 2. CONTRATOS — Con fechas y montos realistas
-- -----------------------------------------------------------
INSERT INTO `contrato` (`id_contrato`, `id_patrocinador`, `monto_total`, `fecha_inicio`, `fecha_fin`, `estado`, `estatus`, `tipo`) VALUES
(1,  1,  85000.00,  '2026-01-01', '2026-12-31', 'Activo', 'Vigente',  'Patrocinio Principal'),
(2,  2,  62000.00,  '2026-03-01', '2026-12-31', 'Activo', 'Vigente',  'Patrocinio TV'),
(3,  3,  12500.00,  '2026-04-01', '2026-09-30', 'Activo', 'Vigente',  'Patrocinio Evento'),
(4,  4,   8000.00,  '2026-05-15', '2026-11-15', 'Activo', 'Vigente',  'Patrocinio Técnico'),
(5,  5, 120000.00,  '2026-02-01', '2027-01-31', 'Activo', 'Vigente',  'Naming Rights'),
(6,  6,  45000.00,  '2026-06-01', '2026-12-31', 'Activo', 'Vigente',  'Patrocinio Digital'),
(7,  7,  18000.00,  '2026-04-01', '2026-08-31', 'Activo', 'Vigente',  'Patrocinio Alimentos'),
(8,  8,  45000.00,  '2026-01-15', '2026-12-31', 'Activo', 'Vigente',  'Patrocinio Salud'),
(9,  9,  22000.00,  '2026-05-01', '2026-10-31', 'Activo', 'Vigente',  'Patrocinio Bebidas'),
(10, 10, 150000.00, '2026-01-01', '2026-12-31', 'Activo', 'Vigente',  'Patrocinio General');

-- -----------------------------------------------------------
-- 3. PAGOS — Pagos parciales (estado=1 = activo)
-- -----------------------------------------------------------
INSERT INTO `pagos` (`id_pago`, `id_contrato`, `monto`, `tipo_pago`, `referencia`, `fecha_pago`, `hora_pago`, `registrado_por`, `Descripcion`, `fecha_registro`, `estado`) VALUES
(1,  1,  21250.00, 'Transferencia', 'TRF-2026-001', '2026-01-15', '10:00:00', NULL, 'Pago inicial Maltin Polar 25%',  '2026-01-15 10:05:00', 1),
(2,  1,  21250.00, 'Transferencia', 'TRF-2026-002', '2026-04-15', '10:00:00', NULL, 'Segundo abono Maltin Polar 25%', '2026-04-15 10:05:00', 1),
(3,  2,  15500.00, 'Transferencia', 'TRF-2026-003', '2026-03-15', '11:00:00', NULL, 'Pago inicial Pepsi 25%',         '2026-03-15 11:05:00', 1),
(4,  2,  15500.00, 'Transferencia', 'TRF-2026-004', '2026-06-15', '11:00:00', NULL, 'Segundo abono Pepsi 25%',        '2026-06-15 11:05:00', 1),
(5,  3,   6250.00, 'Efectivo',      'EFE-2026-001', '2026-04-20', '15:00:00', NULL, 'Pago inicial Café Flor 50%',     '2026-04-20 15:05:00', 1),
(6,  4,   4000.00, 'Transferencia', 'TRF-2026-005', '2026-05-20', '09:30:00', NULL, 'Pago inicial Tubrica 50%',       '2026-05-20 09:35:00', 1),
(7,  5,  30000.00, 'Transferencia', 'TRF-2026-006', '2026-02-10', '09:30:00', NULL, 'Pago inicial Banesco 25%',       '2026-02-10 09:35:00', 1),
(8,  5,  30000.00, 'Transferencia', 'TRF-2026-007', '2026-05-10', '09:30:00', NULL, 'Segundo abono Banesco 25%',      '2026-05-10 09:35:00', 1),
(9,  6,  11250.00, 'Transferencia', 'TRF-2026-008', '2026-06-10', '14:00:00', NULL, 'Pago inicial Movilnet 25%',      '2026-06-10 14:05:00', 1),
(10, 7,   9000.00, 'Efectivo',      'EFE-2026-002', '2026-04-15', '16:00:00', NULL, 'Pago inicial Alimentos Mary 50%','2026-04-15 16:05:00', 1),
(11, 8,  11250.00, 'Transferencia', 'TRF-2026-009', '2026-02-20', '10:00:00', NULL, 'Pago inicial Farmatodo 25%',     '2026-02-20 10:05:00', 1),
(12, 9,   5500.00, 'Transferencia', 'TRF-2026-010', '2026-05-15', '16:00:00', NULL, 'Pago inicial Cerveza 25%',       '2026-05-15 16:05:00', 1),
(13, 10, 37500.00, 'Transferencia', 'TRF-2026-011', '2026-01-10', '09:00:00', NULL, 'Pago inicial Polar 25%',         '2026-01-10 09:05:00', 1),
(14, 10, 37500.00, 'Transferencia', 'TRF-2026-012', '2026-04-10', '09:00:00', NULL, 'Segundo abono Polar 25%',        '2026-04-10 09:05:00', 1);

-- -----------------------------------------------------------
-- 4. TIPO RECURSO + ESTADO RECURSO + ESTADO ASIGNACIÓN (lookup)
-- -----------------------------------------------------------
INSERT INTO `tipo_recurso` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Equipo de PC',     'Computadoras, laptops, tablets'),
(2, 'Equipo de Video',  'Cámaras, proyectores, monitores, pantallas LED'),
(3, 'Iluminación',      'Luces, reflectores, dimmers, mesas de luz'),
(4, 'Mobiliario',       'Mesas, sillas, stands, tarimas'),
(5, 'Instrumento',      'Instrumentos musicales, amplificadores'),
(6, 'Vehículo',         'Vehículos de producción y logística'),
(7, 'Otro',             'Otros tipos de recursos'),
(8, 'Microfono',        'Micrófonos inalámbricos y de solapa');

INSERT INTO `estado_recurso` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Disponible',       'Recurso disponible para uso o asignación'),
(2, 'Asignado',         'Recurso actualmente asignado a un usuario'),
(3, 'En Mantenimiento', 'Recurso en proceso de mantenimiento o reparación'),
(4, 'Dañado',           'Recurso reportado como dañado'),
(5, 'Baja',             'Recurso dado de baja del inventario');

INSERT INTO `estado_asignacion` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Pendiente',  'Asignación activa, pendiente de devolución'),
(2, 'Devuelto',   'Recurso devuelto exitosamente'),
(3, 'Vencido',    'Asignación vencida (no devuelto a tiempo)');

-- -----------------------------------------------------------
-- 5. RECURSOS — Equipos del estadio
-- -----------------------------------------------------------
INSERT INTO `recursos` (`id`, `nombre`, `descripcion`, `tipo_id`, `estado_id`, `fecha_compra`, `costo`, `eliminado`, `creado_en`, `modificado_en`) VALUES
(1,  'Sony PXW-Z150',           'Cámara 4K profesional para transmisión en vivo',   2, 1, '2025-03-15',  4500.00, 0, '2026-01-10 14:24:44', '2026-01-10 14:24:44'),
(2,  'Pantalla LED 55"',        'Pantalla LED para sala de control y palco',        2, 1, '2025-06-20',  3200.00, 0, '2026-01-10 14:24:44', '2026-01-10 14:24:44'),
(3,  'Yamaha TF3',              'Mezcladora digital 24 canales para audio en vivo',  8, 1, '2024-11-10',  5800.00, 0, '2026-01-10 14:24:44', '2026-01-10 14:24:44'),
(4,  'Shure SM58 x4',          'Micrófonos dinámicos inalámbricos para presentadores',8, 1, '2025-08-05', 1200.00, 0, '2026-01-10 14:24:44', '2026-01-10 14:24:44'),
(5,  'Dell XPS 15',             'Laptop para control de guiones y presentaciones',   1, 1, '2025-09-01',  2100.00, 0, '2026-01-10 14:24:44', '2026-01-10 14:24:44'),
(6,  'Epson EB-L615U',          'Proyector láser 6000 lúmenes para pantallas',      2, 1, '2025-01-20',  3800.00, 0, '2026-01-10 14:24:44', '2026-01-10 14:24:44'),
(7,  'Mesa de iluminación DMX', 'Controlador de luces para escenario principal',     3, 1, '2024-12-05',  2600.00, 0, '2026-01-10 14:24:44', '2026-01-10 14:24:44'),
(8,  'Sillas plegables x20',    'Set de sillas para área de producción',             4, 1, '2025-04-10',   400.00, 0, '2026-01-10 14:24:44', '2026-01-10 14:24:44'),
(9,  'Bafle JBL PRX812W',       'Bafle inalámbrico 12" para zona de transmisión',   7, 1, '2025-07-15',  1800.00, 0, '2026-01-10 14:24:44', '2026-01-10 14:24:44'),
(10, 'iPad Pro 12.9"',          'Tablet para control remoto de presentaciones',      1, 1, '2025-10-01',  1100.00, 0, '2026-01-10 14:24:44', '2026-01-10 14:24:44'),
(11, 'Cable HDMI 15m x3',      'Cables HDMI largos para conexión de cámaras',        7, 1, '2025-02-10',   120.00, 0, '2026-02-01 14:24:44', '2026-02-01 14:24:44'),
(12, 'Switcher ATEM Mini',      'Conmutador de video para transmisión en vivo',       2, 1, '2025-05-20',   850.00, 0, '2026-02-01 14:24:44', '2026-02-01 14:24:44');

-- -----------------------------------------------------------
-- 6. ASIGNACIONES DE RECURSOS
-- -----------------------------------------------------------
INSERT INTO `asignaciones_recursos` (`id`, `recurso_id`, `usuario_id`, `fecha_asignacion`, `fecha_devolucion_esperada`, `fecha_devolucion_real`, `estado_asignacion_id`, `notas`) VALUES
(1, 1, 4, '2026-07-01 08:00:00', '2026-07-15', NULL, 1, 'Cámara asignada para transmisión del juego'),
(2, 5, 4, '2026-07-01 08:00:00', '2026-07-15', NULL, 1, 'Laptop para control de guiones'),
(3, 10, 6, '2026-07-01 09:00:00', '2026-07-05', '2026-07-05 17:00:00', 2, 'iPad devuelto después de evento VIP'),
(4, 3, 4, '2026-07-01 08:00:00', '2026-07-15', NULL, 1, 'Mezcladora para sala de control'),
(5, 12, 4, '2026-07-01 08:00:00', '2026-07-15', NULL, 1, 'Switcher para transmisión');

-- -----------------------------------------------------------
-- 7. REELS — Contenido de patrocinadores
-- -----------------------------------------------------------
INSERT INTO `reels` (`id`, `nombre`, `id_patrocinador`, `duracion_total`, `creado_en`, `modificado_en`) VALUES
(1, 'Maltin Polar - Edición Verano',     1, 2700, '2026-06-01 10:00:00', '2026-06-01 10:00:00'),
(2, 'Pepsi - Noche de Béisbol',           2, 1800, '2026-06-05 11:00:00', '2026-06-05 11:00:00'),
(3, 'Banesco - Finanzas Familiares',      5, 2100, '2026-06-10 09:00:00', '2026-06-10 09:00:00'),
(4, 'Café Flor de Arauca - Momento Café', 3, 1500, '2026-06-15 14:00:00', '2026-06-15 14:00:00'),
(5, 'Movilnet - Conectados al Juego',      6, 1200, '2026-06-20 10:00:00', '2026-06-20 10:00:00'),
(6, 'Farmatodo - Salud y Bienestar',       8, 900,  '2026-06-22 11:00:00', '2026-06-22 11:00:00');

-- -----------------------------------------------------------
-- 8. VIDEOS — Contenido de cada reel
-- -----------------------------------------------------------
INSERT INTO `videos` (`id`, `nombre`, `duracion_segundos`, `orden`, `reel_id`, `id_patrocinador`) VALUES
(1,  'Maltin Polar - Spot 15s',            15, 1, 1, 1),
(2,  'Maltin Polar - Behind the scenes',   15, 2, 1, 1),
(3,  'Maltin Polar - Testimonios fans',    15, 3, 1, 1),
(4,  'Maltin Polar - Promoción verano',    20, 4, 1, 1),
(5,  'Pepsi - Spot principal',             15, 1, 2, 2),
(6,  'Pepsi - Momento refresh',            15, 2, 2, 2),
(7,  'Pepsi - Noche de juego',             15, 3, 2, 2),
(8,  'Banesco - Consejos financieros',     20, 1, 3, 5),
(9,  'Banesco - Beneficios tarjeta',       15, 2, 3, 5),
(10, 'Banesco - Inversiones deportivas',   15, 3, 3, 5),
(11, 'Café Flor - Tueste artesanal',       15, 1, 4, 3),
(12, 'Café Flor - Recetas',                10, 2, 4, 3),
(13, 'Movilnet - Plan beisbol',            10, 1, 5, 6),
(14, 'Movilnet - Conectividad',            10, 2, 5, 6),
(15, 'Farmatodo - Tips de salud',          15, 1, 6, 8);

-- -----------------------------------------------------------
-- 9. PREMIOS — De patrocinadores
-- -----------------------------------------------------------
INSERT INTO `premios` (`id`, `id_patrocinador`, `nombre`, `descripcion`, `estado`, `fecha_creacion`, `fecha_entrega`, `entregado_por`, `hora_creacion`, `foto`, `cantidad`, `cantidad_entregada`, `estatus`) VALUES
(1,  1, '6 Pack Maltin Polar',      'Caja de 6 latas de Maltin Polar 350ml',           'entregado', '2026-06-15', '2026-06-18 19:30:00', NULL, '10:00:00', 'default-premio.png', 50, 12, 0),
(2,  2, 'Pepsi Cola 2L x3',        'Tres botellas de Pepsi Cola 2 litros',             'entregado', '2026-06-15', '2026-06-18 20:15:00', NULL, '10:30:00', 'default-premio.png', 30,  8, 0),
(3,  5, 'Tarjeta Banesco $50',      'Tarjeta de regalo Banesco por 50$',                'pendiente', '2026-07-01', NULL, NULL, '09:00:00', 'default-premio.png', 10,  0, 1),
(4,  3, 'Café Flor de Arauca 250g', 'Paquete de café premium tostado oscuro',           'entregado', '2026-06-20', '2026-06-22 18:45:00', NULL, '11:00:00', 'default-premio.png', 20,  5, 0),
(5,  8, 'Kit Farmatodo',            'Kit de productos de higiene personal',             'pendiente', '2026-07-05', NULL, NULL, '14:00:00', 'default-premio.png', 40,  0, 1),
(6,  6, 'Camiseta Movilnet',        'Camiseta oficial Movilnet edición béisbol',        'entregado', '2026-06-10', '2026-06-12 19:00:00', NULL, '08:30:00', 'default-premio.png',100, 25, 0),
(7,  4, 'Combo Tubrica',            'Kit de herramientas básicas Tubrica',              'pendiente', '2026-07-08', NULL, NULL, '15:30:00', 'default-premio.png', 15,  0, 1),
(8,  9, 'Cerveza Regional 6 Pack',  'Caja de 6 latas de Cerveza Regional',             'pendiente', '2026-07-10', NULL, NULL, '12:00:00', 'default-premio.png', 25,  0, 1),
(9,  1, 'Polar Piña 1L x2',         'Dos botellas de Polar Piña 1 litro',               'entregado', '2026-06-25', '2026-06-28 20:00:00', NULL, '09:30:00', 'default-premio.png', 40, 15, 0),
(10, 7, 'Caja Alimentos Mary',       'Caja de snacks y dulces variados',                'pendiente', '2026-07-12', NULL, NULL, '16:00:00', 'default-premio.png', 30,  0, 1);

-- -----------------------------------------------------------
-- 10. TAREAS — Preparativos de juego
-- -----------------------------------------------------------
INSERT INTO `tareas` (`id_tarea`, `Nombre_Tarea`, `Instruccion`, `id_usuario_creador`, `Estatus`) VALUES
(1, 'Verificar equipo de transmisión',     'Revisar estado de cámaras, mezcladora y pantallas antes del juego',      3, 1),
(2, 'Calibrar sonido del estadio',         'Ajustar niveles de audio en bafles principales y zonas secundarias',    3, 1),
(3, 'Preparar contenido Jumbotron',        'Cargar videos de patrocinadores y spots en el sistema de pantallas',    4, 1),
(4, 'Revisar iluminación del campo',       'Verificar focos principales, focos de juego y luz de emergencia',       5, 1),
(5, 'Entregar kits de premios',            'Preparar y entregar premios a zona de animación 2 horas antes del juego',6, 1),
(6, 'Coordinar llegada de patrocinadores', 'Confirmar asistencia y asignar accesos a invitados especiales',         3, 1);

-- -----------------------------------------------------------
-- 11. TAREAS ASIGNADAS
-- -----------------------------------------------------------
INSERT INTO `tareas_asignadas` (`id_asignacion`, `id_tarea`, `id_usuario`, `Estado`, `fecha_asignacion_tarea`, `Estatus`) VALUES
(1, 1, 4, 'Completada', '2026-07-01 14:00:00', 1),
(2, 2, 5, 'Completada', '2026-07-01 14:30:00', 1),
(3, 3, 4, 'Completada', '2026-07-01 15:00:00', 1),
(4, 4, 6, 'Pendiente',  '2026-07-01 08:00:00', 1),
(5, 5, 5, 'Pendiente',  '2026-07-01 09:00:00', 1),
(6, 6, 3, 'Pendiente',  '2026-07-01 10:00:00', 1);

-- -----------------------------------------------------------
-- 12. GUIONES — Programación de juegos
-- -----------------------------------------------------------
INSERT INTO `guiones` (`id`, `nombre`, `estado`, `inicio_show`, `creado_en`, `modificado_en`, `tiempo_inning`, `grupo_id`, `status`) VALUES
(1, 'Cardenales vs Leones - 2026-07-10',     'finalizado', '2026-07-10 18:00:00', '2026-07-01 09:00:00', '2026-07-10 19:00:00', 120, NULL, 1),
(2, 'Cardenales vs Tiburones - 2026-07-12',   'borrador',   NULL, '2026-07-05 10:00:00', '2026-07-05 10:00:00', 120, NULL, 1),
(3, 'Cardenales vs Navegantes - 2026-07-15',  'borrador',   NULL, '2026-07-08 11:00:00', '2026-07-08 11:00:00', 120, NULL, 1),
(4, 'Cardenales vs Tigres - 2026-07-18',      'borrador',   NULL, '2026-07-10 12:00:00', '2026-07-10 12:00:00', 120, NULL, 1),
(5, 'Cardenales vs Águilas - 2026-07-20',     'borrador',   NULL, '2026-07-12 13:00:00', '2026-07-12 13:00:00', 120, NULL, 1),
(6, 'Cardenales vs Caribes - 2026-07-22',     'borrador',   NULL, '2026-07-14 14:00:00', '2026-07-14 14:00:00', 120, NULL, 1);

-- -----------------------------------------------------------
-- 13. GUION FECHAS
-- -----------------------------------------------------------
INSERT INTO `guion_fechas` (`id`, `guion_id`, `fecha`) VALUES
(1, 1, '2026-07-10'),
(2, 2, '2026-07-12'),
(3, 3, '2026-07-15'),
(4, 4, '2026-07-18'),
(5, 5, '2026-07-20'),
(6, 6, '2026-07-22');

-- -----------------------------------------------------------
-- 14. ELEMENTOS GUION — Programación detallada del juego 1
-- -----------------------------------------------------------
INSERT INTO `elementos_guion` (`id`, `guion_id`, `fecha_id`, `tipo`, `hora`, `inning`, `medio_inning`, `contenido`, `duracion_estimada`, `encargado`, `orden`, `creado_en`, `estado`, `inicio_curso`) VALUES
-- Pregame
(1,  1, 1, 'pregame',  '17:00:00', NULL, NULL, 'Apertura de puertas y bienvenida',                   300, 'Keiver Zamudia',  1, '2026-07-01 09:05:00', 'pendiente', NULL),
(2,  1, 1, 'pregame',  '17:30:00', NULL, NULL, 'Presentación de alineaciones por pantallas',          180, 'Genesis Acosta',  2, '2026-07-01 09:06:00', 'pendiente', NULL),
(3,  1, 1, 'pregame',  '18:00:00', NULL, NULL, 'Ceremonia de lanzamiento inaugural',                  240, 'Keiver Zamudia',  3, '2026-07-01 09:07:00', 'pendiente', NULL),
(4,  1, 1, 'pregame',  '18:15:00', NULL, NULL, 'Himno Nacional - Orquesta del Estado Lara',           180, 'Genesis Acosta',  4, '2026-07-01 09:08:00', 'pendiente', NULL),
(5,  1, 1, 'pregame',  '18:20:00', NULL, NULL, 'Video bienvenida patrocinadores',                     60, 'Keiver Zamudia',  5, '2026-07-01 09:09:00', 'pendiente', NULL),
-- Game - Innings
(6,  1, 1, 'game',     NULL, 1, 'baja', 'Publicidad Maltin Polar - Jumbotron',                       30, 'Keiver Zamudia',  1, '2026-07-01 09:10:00', 'pendiente', NULL),
(7,  1, 1, 'game',     NULL, 1, 'alta', 'Publicidad Pepsi - Bafles del estadio',                     30, 'Genesis Acosta',  2, '2026-07-01 09:11:00', 'pendiente', NULL),
(8,  1, 1, 'game',     NULL, 2, 'baja', 'Concurso Maltin Polar - Lanzamiento de pelota',            120, 'Keiver Zamudia',  3, '2026-07-01 09:12:00', 'pendiente', NULL),
(9,  1, 1, 'game',     NULL, 3, 'alta', 'Publicidad Banesco - Finanzas personales',                  30, 'Genesis Acosta',  4, '2026-07-01 09:13:00', 'pendiente', NULL),
(10, 1, 1, 'game',     NULL, 4, 'baja', 'Reels Café Flor de Arauca',                                25, 'Keiver Zamudia',  5, '2026-07-01 09:14:00', 'pendiente', NULL),
(11, 1, 1, 'game',     NULL, 5, 'alta', 'Publicidad Movilnet - Plan datos béisbol',                  30, 'Genesis Acosta',  6, '2026-07-01 09:15:00', 'pendiente', NULL),
(12, 1, 1, 'game',     NULL, 6, 'baja', 'Ceremonia de premiación fan del juego',                    180, 'Keiver Zamudia',  7, '2026-07-01 09:16:00', 'pendiente', NULL),
(13, 1, 1, 'game',     NULL, 7, 'alta', 'Publicidad Farmatodo - Salud y bienestar',                  30, 'Genesis Acosta',  8, '2026-07-01 09:17:00', 'pendiente', NULL),
(14, 1, 1, 'game',     NULL, 8, 'baja', 'Reels Cerveza Regional',                                   25, 'Keiver Zamudia',  9, '2026-07-01 09:18:00', 'pendiente', NULL),
-- Postgame
(15, 1, 1, 'postgame', NULL, NULL, NULL, 'Entrega de premios a ganadores',                           300, 'Keiver Zamudia',  1, '2026-07-01 09:19:00', 'pendiente', NULL),
(16, 1, 1, 'postgame', NULL, NULL, NULL, 'Entrevistas post-juego y agradecimientos',                 600, 'Genesis Acosta',  2, '2026-07-01 09:20:00', 'pendiente', NULL),
-- Guion 2
(17, 2, 2, 'pregame',  '17:00:00', NULL, NULL, 'Apertura de puertas',                                300, 'Keiver Zamudia',  1, '2026-07-05 10:05:00', 'pendiente', NULL),
(18, 2, 2, 'pregame',  '17:30:00', NULL, NULL, 'Presentación de alineaciones',                        180, 'Genesis Acosta',  2, '2026-07-05 10:06:00', 'pendiente', NULL),
(19, 2, 2, 'pregame',  '18:00:00', NULL, NULL, 'Ceremonia de lanzamiento inaugural',                  240, 'Keiver Zamudia',  3, '2026-07-05 10:07:00', 'pendiente', NULL),
(20, 2, 2, 'game',     NULL, 1, 'baja', 'Publicidad Maltin Polar',                                   30, 'Keiver Zamudia',  1, '2026-07-05 10:10:00', 'pendiente', NULL),
(21, 2, 2, 'game',     NULL, 2, 'baja', 'Concurso Alimentos Mary - Sabor del juego',                 120, 'Keiver Zamudia',  2, '2026-07-05 10:11:00', 'pendiente', NULL),
(22, 2, 2, 'game',     NULL, 3, 'alta', 'Publicidad Tubrica',                                        30, 'Genesis Acosta',  3, '2026-07-05 10:12:00', 'pendiente', NULL),
(23, 2, 2, 'game',     NULL, 5, 'baja', 'Reels Banesco',                                             25, 'Keiver Zamudia',  4, '2026-07-05 10:13:00', 'pendiente', NULL),
(24, 2, 2, 'game',     NULL, 7, 'alta', 'Publicidad Pepsi',                                          30, 'Genesis Acosta',  5, '2026-07-05 10:14:00', 'pendiente', NULL),
-- Guion 3
(25, 3, 3, 'pregame',  '18:00:00', NULL, NULL, 'Apertura de puertas y animación',                     300, 'Keiver Zamudia',  1, '2026-07-08 11:05:00', 'pendiente', NULL),
(26, 3, 3, 'pregame',  '18:30:00', NULL, NULL, 'Himno Nacional y presentación',                       240, 'Genesis Acosta',  2, '2026-07-08 11:06:00', 'pendiente', NULL),
(27, 3, 3, 'game',     NULL, 1, 'baja', 'Publicidad Movilnet',                                       30, 'Keiver Zamudia',  1, '2026-07-08 11:08:00', 'pendiente', NULL),
(28, 3, 3, 'game',     NULL, 3, 'baja', 'Concurso Café Flor de Arauca',                             120, 'Keiver Zamudia',  2, '2026-07-08 11:09:00', 'pendiente', NULL),
(29, 3, 3, 'game',     NULL, 5, 'alta', 'Publicidad Farmatodo',                                      30, 'Genesis Acosta',  3, '2026-07-08 11:10:00', 'pendiente', NULL),
(30, 3, 3, 'game',     NULL, 7, 'baja', 'Reels Cerveza Regional',                                    25, 'Keiver Zamudia',  4, '2026-07-08 11:11:00', 'pendiente', NULL);

-- -----------------------------------------------------------
-- 15. HISTORIAL DE MANTENIMIENTO
-- -----------------------------------------------------------
INSERT INTO `mantenimientos` (`id`, `recurso_id`, `usuario_id`, `estado`, `fecha_ingreso`, `fecha_salida`, `diagnostico`, `observaciones`, `creado_en`) VALUES
(1, 1, 4, 'finalizado', '2026-07-10', '2026-07-10', 'Autofocus no responde en modo manual', 'Se reemplazó actuador de lente', '2026-07-10 17:44:46'),
(2, 9, 4, 'en_espera',  '2026-07-15', NULL,          'Sonido distorsionado a volumen alto',   'Revisar amplificador interno',    '2026-07-15 10:30:00');

INSERT INTO `historial_mantenimiento` (`id`, `mantenimiento_id`, `usuario_id`, `accion`, `descripcion`, `creado_en`) VALUES
(1, 1, 4, 'ingreso',  'Ingreso a mantenimiento. Diagnóstico: Autofocus no responde en modo manual',  '2026-07-10 17:44:46'),
(2, 1, 4, 'reparar',  'Se inició el proceso de reparación.',                                        '2026-07-10 17:45:38'),
(3, 1, 4, 'reparar',  'Reparado exitosamente. Se reemplazó actuador de lente.',                      '2026-07-10 17:47:42'),
(4, 1, 4, 'finalizar','Mantenimiento finalizado.',                                                   '2026-07-10 17:47:52'),
(5, 2, 4, 'ingreso',  'Ingreso a mantenimiento. Diagnóstico: Sonido distorsionado a volumen alto',   '2026-07-15 10:30:00');

-- -----------------------------------------------------------
-- 16. HISTORIAL CHAT
-- -----------------------------------------------------------
INSERT INTO `historial_chat` (`id`, `usuario_id`, `mensaje_usuario`, `respuesta_ia`, `contexto`, `created_at`) VALUES
(1, 3, '¿Cuántos guiones hay?',     'Hay **6** guion(es) registrado(s) en el sistema.', '{"intencion": "contar_guiones", "confianza": 0.95}', '2026-07-10 14:26:38'),
(2, 3, '¿Cuántos patrocinadores?',  'Hay **10** patrocinador(es) registrado(s) en el sistema.', '{"intencion": "contar_patrocinadores", "confianza": 0.95}', '2026-07-10 14:27:10'),
(3, 4, '¿Cuántos usuarios hay?',    'Hay **6** usuario(s) registrado(s) en el sistema.', '{"intencion": "contar_usuarios", "confianza": 0.95}', '2026-07-10 14:53:19'),
(4, 4, '¿Cuántas tareas hay?',      'Hay **6** tarea(s) registrada(s) en el sistema.', '{"intencion": "contar_tareas", "confianza": 0.95}', '2026-08-23 19:29:04');

-- -----------------------------------------------------------
-- OBJETOS SQL PARA LA DEFENSA
-- -----------------------------------------------------------

-- 17. VISTA: v_balance_contratos
-- ============================================================
DROP VIEW IF EXISTS `v_balance_contratos`;
CREATE VIEW `v_balance_contratos` AS
SELECT
  c.id_contrato,
  p.nombre_empresa,
  p.rif,
  c.monto_total,
  COALESCE(SUM(pg.monto), 0) AS monto_pagado,
  c.monto_total - COALESCE(SUM(pg.monto), 0) AS saldo_pendiente,
  ROUND(COALESCE(SUM(pg.monto), 0) / c.monto_total * 100, 2) AS porcentaje_pagado,
  COUNT(pg.id_pago) AS cantidad_pagos,
  c.fecha_inicio,
  c.fecha_fin,
  c.estatus AS estatus_contrato
FROM contrato c
JOIN patrocinadores p ON c.id_patrocinador = p.id_patrocinador
LEFT JOIN pagos pg ON c.id_contrato = pg.id_contrato AND pg.estado = 1
GROUP BY c.id_contrato, p.nombre_empresa, p.rif, c.monto_total, c.fecha_inicio, c.fecha_fin, c.estatus;

-- 18. TRIGGERS: Auditoría financiera en pagos
-- ============================================================
DROP TRIGGER IF EXISTS `trg_pagos_after_insert`;
DELIMITER //
CREATE TRIGGER `trg_pagos_after_insert`
AFTER INSERT ON `pagos`
FOR EACH ROW
BEGIN
  INSERT INTO `seguridad`.`actividad_usuario`
    (usuario_id, tipo_accion, modulo, accion, detalle, pagina, ip_address, created_at)
  VALUES
    (NEW.registrado_por, 'create', 'balance',
     'Pago registrado',
     JSON_OBJECT(
       'pago_id', NEW.id_pago,
       'contrato_id', NEW.id_contrato,
       'monto', NEW.monto,
       'tipo_pago', NEW.tipo_pago,
       'referencia', NEW.referencia,
       'fecha_pago', NEW.fecha_pago
     ),
     '/balance/pagos', NULL, NOW());
END //
DELIMITER ;

DROP TRIGGER IF EXISTS `trg_pagos_after_update`;
DELIMITER //
CREATE TRIGGER `trg_pagos_after_update`
AFTER UPDATE ON `pagos`
FOR EACH ROW
BEGIN
  IF OLD.monto <> NEW.monto OR OLD.estado <> NEW.estado OR OLD.referencia <> NEW.referencia THEN
    INSERT INTO `seguridad`.`actividad_usuario`
      (usuario_id, tipo_accion, modulo, accion, detalle, pagina, ip_address, created_at)
    VALUES
      (NEW.registrado_por, 'update', 'balance',
       'Pago modificado',
       JSON_OBJECT(
         'pago_id', NEW.id_pago,
         'antes', JSON_OBJECT('monto', OLD.monto, 'estado', OLD.estado, 'referencia', OLD.referencia),
         'despues', JSON_OBJECT('monto', NEW.monto, 'estado', NEW.estado, 'referencia', NEW.referencia)
       ),
       '/balance/pagos', NULL, NOW());
  END IF;
END //
DELIMITER ;

-- 19. PROCEDIMIENTO: sp_resumen_financiero
-- ============================================================
-- NOTA: El procedimiento se crea por separado debido a
-- incompatibilidad de versión de MariaDB (mysql_upgrade requiere permisos root)
-- Ver: seed_procedure.sql

-- -----------------------------------------------------------
-- ÍNDICES
-- -----------------------------------------------------------
ALTER TABLE `asignaciones_recursos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_asignaciones_recurso` (`recurso_id`),
  ADD KEY `idx_asignaciones_estado` (`estado_asignacion_id`);

ALTER TABLE `contrato`
  ADD PRIMARY KEY (`id_contrato`),
  ADD KEY `id_patrocinador` (`id_patrocinador`);

ALTER TABLE `departamentos`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `elementos_guion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `guion_id` (`guion_id`),
  ADD KEY `fecha_id` (`fecha_id`);

ALTER TABLE `estado_asignacion`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

ALTER TABLE `estado_recurso`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

ALTER TABLE `guiones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_grupo_id` (`grupo_id`);

ALTER TABLE `guion_fechas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `guion_id` (`guion_id`);

ALTER TABLE `historial_chat`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `historial_mantenimiento`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `idx_historial_mantenimiento` (`mantenimiento_id`);

ALTER TABLE `mantenimientos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `idx_mantenimientos_estado` (`estado`),
  ADD KEY `idx_mantenimientos_recurso` (`recurso_id`);

ALTER TABLE `pagos`
  ADD PRIMARY KEY (`id_pago`),
  ADD KEY `id_contrato` (`id_contrato`);

ALTER TABLE `patrocinadores`
  ADD PRIMARY KEY (`id_patrocinador`);

ALTER TABLE `premios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_patrocinador` (`id_patrocinador`);

ALTER TABLE `recursos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_recursos_tipo` (`tipo_id`),
  ADD KEY `idx_recursos_estado` (`estado_id`);

ALTER TABLE `reels`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_patrocinador` (`id_patrocinador`);

ALTER TABLE `tareas`
  ADD PRIMARY KEY (`id_tarea`);

ALTER TABLE `tareas_asignadas`
  ADD PRIMARY KEY (`id_asignacion`),
  ADD KEY `id_tarea` (`id_tarea`);

ALTER TABLE `tipo_recurso`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

ALTER TABLE `videos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_videos_reel` (`reel_id`);

-- AUTO_INCREMENT
ALTER TABLE `asignaciones_recursos` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
ALTER TABLE `contrato`             MODIFY `id_contrato` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
ALTER TABLE `departamentos`        MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
ALTER TABLE `elementos_guion`      MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;
ALTER TABLE `estado_asignacion`    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
ALTER TABLE `estado_recurso`       MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
ALTER TABLE `guiones`              MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
ALTER TABLE `guion_fechas`         MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
ALTER TABLE `historial_chat`       MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
ALTER TABLE `historial_mantenimiento` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
ALTER TABLE `mantenimientos`       MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
ALTER TABLE `pagos`                MODIFY `id_pago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
ALTER TABLE `patrocinadores`       MODIFY `id_patrocinador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
ALTER TABLE `premios`              MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
ALTER TABLE `recursos`             MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
ALTER TABLE `reels`                MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
ALTER TABLE `tareas`               MODIFY `id_tarea` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
ALTER TABLE `tareas_asignadas`     MODIFY `id_asignacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
ALTER TABLE `tipo_recurso`         MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
ALTER TABLE `videos`               MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

-- Foreign Keys
ALTER TABLE `asignaciones_recursos`
  ADD CONSTRAINT `fk_asignaciones_estado_asig` FOREIGN KEY (`estado_asignacion_id`) REFERENCES `estado_asignacion` (`id`),
  ADD CONSTRAINT `fk_asignaciones_recurso` FOREIGN KEY (`recurso_id`) REFERENCES `recursos` (`id`);

ALTER TABLE `contrato`
  ADD CONSTRAINT `contrato_ibfk_1` FOREIGN KEY (`id_patrocinador`) REFERENCES `patrocinadores` (`id_patrocinador`);

ALTER TABLE `elementos_guion`
  ADD CONSTRAINT `elementos_guion_ibfk_1` FOREIGN KEY (`guion_id`) REFERENCES `guiones` (`id`),
  ADD CONSTRAINT `elementos_guion_ibfk_2` FOREIGN KEY (`fecha_id`) REFERENCES `guion_fechas` (`id`);

ALTER TABLE `guion_fechas`
  ADD CONSTRAINT `guion_fechas_ibfk_1` FOREIGN KEY (`guion_id`) REFERENCES `guiones` (`id`);

ALTER TABLE `historial_mantenimiento`
  ADD CONSTRAINT `historial_mantenimiento_ibfk_1` FOREIGN KEY (`mantenimiento_id`) REFERENCES `mantenimientos` (`id`) ON DELETE CASCADE;

ALTER TABLE `pagos`
  ADD CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`id_contrato`) REFERENCES `contrato` (`id_contrato`);

ALTER TABLE `premios`
  ADD CONSTRAINT `premios_ibfk_1` FOREIGN KEY (`id_patrocinador`) REFERENCES `patrocinadores` (`id_patrocinador`);

ALTER TABLE `recursos`
  ADD CONSTRAINT `fk_recursos_estado` FOREIGN KEY (`estado_id`) REFERENCES `estado_recurso` (`id`),
  ADD CONSTRAINT `fk_recursos_tipo` FOREIGN KEY (`tipo_id`) REFERENCES `tipo_recurso` (`id`);

ALTER TABLE `reels`
  ADD CONSTRAINT `reels_ibfk_1` FOREIGN KEY (`id_patrocinador`) REFERENCES `patrocinadores` (`id_patrocinador`);

ALTER TABLE `tareas_asignadas`
  ADD CONSTRAINT `tareas_asignadas_ibfk_1` FOREIGN KEY (`id_tarea`) REFERENCES `tareas` (`id_tarea`);

ALTER TABLE `videos`
  ADD CONSTRAINT `fk_videos_reel` FOREIGN KEY (`reel_id`) REFERENCES `reels` (`id`) ON DELETE CASCADE;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
