-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 01-06-2026 a las 06:44:04
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `estadio_db`
--
CREATE DATABASE IF NOT EXISTS `estadio_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `estadio_db`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asignaciones_recursos`
--

CREATE TABLE `asignaciones_recursos` (
  `id` int(11) NOT NULL,
  `recurso_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `fecha_asignacion` datetime DEFAULT current_timestamp(),
  `fecha_devolucion_esperada` date DEFAULT NULL,
  `fecha_devolucion_real` datetime DEFAULT NULL,
  `estado_asignacion_id` int(11) DEFAULT 1,
  `notas` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `asignaciones_recursos`
--

INSERT INTO `asignaciones_recursos` (`id`, `recurso_id`, `usuario_id`, `fecha_asignacion`, `fecha_devolucion_esperada`, `fecha_devolucion_real`, `estado_asignacion_id`, `notas`) VALUES
(1, 1, 4, '2026-05-31 23:31:44', '2026-05-31', '2026-05-31 23:32:05', 2, 'por su uso'),
(2, 1, 4, '2026-05-31 23:32:21', '2026-05-31', '2026-05-31 23:43:57', 2, 'axa'),
(3, 1, 18, '2026-06-01 00:04:31', '2026-06-01', NULL, 1, 'ergwr');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contrato`
--

CREATE TABLE `contrato` (
  `id_contrato` int(11) NOT NULL,
  `id_patrocinador` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `estado` varchar(100) NOT NULL,
  `estatus` varchar(100) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `monto_total` decimal(12,2) NOT NULL DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `contrato`
--

INSERT INTO `contrato` (`id_contrato`, `id_patrocinador`, `fecha_inicio`, `fecha_fin`, `estado`, `estatus`, `tipo`, `monto_total`) VALUES
(2, 1, '2026-05-01', '2026-05-31', '1', 'Vigente', '2', 150.00),
(3, 12, '2026-05-06', '2026-05-12', '0', 'Vencido', '2', 350.00),
(4, 10, '2026-05-13', '2026-05-18', '0', 'Vigente', '3', 450.00),
(5, 12, '2026-05-24', '2026-05-31', '0', 'Borrador', '3', 600.00),
(6, 6, '2026-05-31', '2026-08-30', '0', 'Vigente', '2', 150000.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `departamentos`
--

CREATE TABLE `departamentos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(200) DEFAULT NULL,
  `color` varchar(7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `elementos_guion`
--

CREATE TABLE `elementos_guion` (
  `id` int(11) NOT NULL,
  `guion_id` int(11) NOT NULL,
  `fecha_id` int(11) DEFAULT NULL,
  `tipo` varchar(20) NOT NULL,
  `hora` time DEFAULT NULL,
  `inning` int(11) DEFAULT NULL,
  `medio_inning` varchar(10) DEFAULT NULL,
  `contenido` text NOT NULL,
  `duracion_estimada` int(11) NOT NULL,
  `encargado` varchar(100) NOT NULL,
  `orden` int(11) DEFAULT NULL,
  `creado_en` datetime DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `elementos_guion`
--

INSERT INTO `elementos_guion` (`id`, `guion_id`, `fecha_id`, `tipo`, `hora`, `inning`, `medio_inning`, `contenido`, `duracion_estimada`, `encargado`, `orden`, `creado_en`, `estado`) VALUES
(11, 6, NULL, 'pregame', '19:46:00', NULL, NULL, 'warnning song', 150, 'Admin', 1, '2026-05-31 19:46:51', 'completado'),
(12, 6, NULL, 'pregame', '20:11:00', NULL, NULL, 'Salidas de las mascotas', 180, 'Admin', 2, '2026-05-31 20:11:39', 'en_curso');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estado_asignacion`
--

CREATE TABLE `estado_asignacion` (
  `id` int(11) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `estado_asignacion`
--

INSERT INTO `estado_asignacion` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Pendiente', 'Asignación activa, pendiente de devolución'),
(2, 'Devuelto', 'Recurso devuelto exitosamente'),
(3, 'Vencido', 'Asignación vencida (no devuelto a tiempo)');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estado_recurso`
--

CREATE TABLE `estado_recurso` (
  `id` int(11) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `estado_recurso`
--

INSERT INTO `estado_recurso` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Disponible', 'Recurso disponible para uso o asignación'),
(2, 'Asignado', 'Recurso actualmente asignado a un usuario'),
(3, 'En Mantenimiento', 'Recurso en proceso de mantenimiento o reparación'),
(4, 'Dañado', 'Recurso reportado como dañado'),
(5, 'Baja', 'Recurso dado de baja del inventario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `eventos`
--

CREATE TABLE `eventos` (
  `id` int(11) NOT NULL,
  `titulo` varchar(100) NOT NULL,
  `descripcion` varchar(500) DEFAULT NULL,
  `fecha` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `duracion_minutos` int(11) DEFAULT NULL,
  `departamento_id` int(11) NOT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `guion` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `eventos_sincronizados`
--

CREATE TABLE `eventos_sincronizados` (
  `id` int(11) NOT NULL,
  `sincronizacion_id` int(11) NOT NULL,
  `evento_id` int(11) NOT NULL,
  `orden` int(11) DEFAULT NULL,
  `ejecutado` tinyint(1) DEFAULT NULL,
  `ejecutado_en` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `guiones`
--

CREATE TABLE `guiones` (
  `id` int(11) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `creado_en` datetime DEFAULT NULL,
  `modificado_en` datetime DEFAULT NULL,
  `tiempo_inning` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `guiones`
--

INSERT INTO `guiones` (`id`, `nombre`, `estado`, `creado_en`, `modificado_en`, `tiempo_inning`) VALUES
(6, 'Cardenales General', 'en_vivo', '2026-05-31 19:46:35', '2026-06-01 00:16:30', 150);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `guion_fechas`
--

CREATE TABLE `guion_fechas` (
  `id` int(11) NOT NULL,
  `guion_id` int(11) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `guion_fechas`
--

INSERT INTO `guion_fechas` (`id`, `guion_id`, `fecha`) VALUES
(7, 6, '2026-05-31');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial_mantenimiento`
--

CREATE TABLE `historial_mantenimiento` (
  `id` int(11) NOT NULL,
  `mantenimiento_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `accion` varchar(50) NOT NULL,
  `descripcion` text NOT NULL,
  `creado_en` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `historial_mantenimiento`
--

INSERT INTO `historial_mantenimiento` (`id`, `mantenimiento_id`, `usuario_id`, `accion`, `descripcion`, `creado_en`) VALUES
(1, 1, 4, 'ingreso', 'Ingreso a mantenimiento. Diagnóstico: problemas de luz focal', '2026-05-22 22:59:58'),
(6, 4, 4, 'ingreso', 'Ingreso a mantenimiento. Diagnóstico: \r\nNo da imagen', '2026-05-26 04:56:25'),
(7, 1, 4, 'nota', 'Prueba de bitacora', '2026-05-26 04:56:41');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mantenimientos`
--

CREATE TABLE `mantenimientos` (
  `id` int(11) NOT NULL,
  `recurso_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `estado` varchar(20) DEFAULT 'en_espera',
  `fecha_ingreso` date NOT NULL,
  `fecha_salida` date DEFAULT NULL,
  `diagnostico` text DEFAULT NULL,
  `observaciones` text DEFAULT NULL,
  `creado_en` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `mantenimientos`
--

INSERT INTO `mantenimientos` (`id`, `recurso_id`, `usuario_id`, `estado`, `fecha_ingreso`, `fecha_salida`, `diagnostico`, `observaciones`, `creado_en`) VALUES
(1, 1, 4, 'en_espera', '2026-05-22', NULL, 'problemas de luz focal', '', '2026-05-22 22:59:58'),
(4, 2, 4, 'en_espera', '2026-05-26', NULL, '\r\nNo da imagen', '', '2026-05-26 04:56:25');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos`
--

CREATE TABLE `pagos` (
  `id_pago` int(11) NOT NULL,
  `id_contrato` int(11) NOT NULL,
  `monto` decimal(12,2) NOT NULL,
  `tipo_pago` varchar(20) NOT NULL,
  `referencia` varchar(100) DEFAULT NULL,
  `fecha_pago` date NOT NULL,
  `hora_pago` time NOT NULL,
  `registrado_por` int(11) DEFAULT NULL,
  `Descripción` text DEFAULT NULL,
  `fecha_registro` datetime DEFAULT current_timestamp(),
  `estado` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pagos`
--

INSERT INTO `pagos` (`id_pago`, `id_contrato`, `monto`, `tipo_pago`, `referencia`, `fecha_pago`, `hora_pago`, `registrado_por`, `Descripción`, `fecha_registro`, `estado`) VALUES
(1, 1, 50.00, 'Transferencia', '04004004', '2026-05-24', '11:17:00', 3, '', '2026-05-24 15:20:40', 1),
(2, 2, 10.00, 'Transferencia', '04004004', '2026-05-24', '14:12:00', 3, NULL, '2026-05-24 18:13:57', 1),
(3, 1, 50.00, 'Transferencia', '55555005', '2026-05-24', '14:23:00', 3, NULL, '2026-05-24 18:24:25', 1),
(4, 2, 10.00, 'Transferencia', '555005', '2026-05-24', '14:58:00', 3, 'si debe', '2026-05-24 19:00:30', 0),
(5, 2, 10.00, 'Transferencia', '55555005', '2026-05-17', '15:55:00', 3, '', '2026-05-24 19:59:08', 1),
(6, 1, 90.00, 'Depósito', '04004', '2026-05-24', '16:57:00', 3, '', '2026-05-24 21:00:38', 1),
(7, 2, 5.00, 'Cheque', '34433', '2026-05-24', '19:35:00', 3, 'sdqede2d2', '2026-05-24 23:36:45', 1),
(8, 2, 10.00, 'Transferencia', '555006', '2026-05-26', '21:46:00', 3, 'pago', '2026-05-27 01:48:00', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `patrocinadores`
--

CREATE TABLE `patrocinadores` (
  `id_patrocinador` int(11) NOT NULL,
  `nombre_empresa` varchar(100) NOT NULL,
  `rif` varchar(20) NOT NULL,
  `tipo_contrato` int(11) NOT NULL,
  `nombre_contacto` text NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `estado` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `patrocinadores`
--

INSERT INTO `patrocinadores` (`id_patrocinador`, `nombre_empresa`, `rif`, `tipo_contrato`, `nombre_contacto`, `telefono`, `email`, `estado`) VALUES
(1, 'Pepsi', 'j-03003', 1, 'Deportivo', '4128492014', 'daniel12@gmail.com', 1),
(2, 'Maltin polar', 'J-84566', 2, 'torneos', '04227658976', 'genaro23@gmail.com', 1),
(5, 'keiver C.A', 'V-25469224', 1, 'Plan Keiver', '0412344590', 'keiberzamudia14@gmail.com', 0),
(6, 'Tubrica C.A', 'J-83736545', 1, 'Tubrica', '0251-2661166', 'dwjdewjd@gmail.com', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `premios`
--

CREATE TABLE `premios` (
  `id` int(11) NOT NULL,
  `id_patrocinador` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` varchar(20) DEFAULT 'pendiente',
  `fecha_creacion` date NOT NULL DEFAULT current_timestamp(),
  `fecha_entrega` datetime DEFAULT NULL,
  `entregado_por` int(11) DEFAULT NULL,
  `hora_creacion` time NOT NULL,
  `foto` varchar(200) DEFAULT 'default-premio.png',
  `estatus` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `premios`
--

INSERT INTO `premios` (`id`, `id_patrocinador`, `nombre`, `descripcion`, `estado`, `fecha_creacion`, `fecha_entrega`, `entregado_por`, `hora_creacion`, `foto`, `estatus`) VALUES
(30, 1, 'ewdcdw', 'kkkk', 'entregado', '2026-05-19', '2026-05-19 19:12:43', NULL, '16:02:00', '20260519_150309_premio.png', 0),
(31, 2, 'Camisas deportivas', 'talla XL para caballeross', 'entregado', '2026-05-19', '2026-05-23 00:12:00', NULL, '16:13:00', '20260519_152537_premio.png', 0),
(32, 2, 'bolso de comida', '26 productos', 'entregado', '2026-05-19', '2026-05-23 00:25:54', NULL, '15:26:00', '20260519_155614_arichuna.png', 0),
(33, 2, 'playera', 'sdddw', 'entregado', '2026-05-19', '2026-05-19 19:58:40', NULL, '17:57:00', '20260519_155824_premio.png', 0),
(34, 2, 'Bebidas Ron', 'El que gane la carrera de la pollada', 'entregado', '2026-05-19', '2026-05-23 00:25:31', NULL, '16:05:00', '20260519_160518_chocolate.png', 0),
(35, 1, 'keiver Zamudia', 'SII', 'entregado', '2026-05-19', '2026-05-19 23:56:42', NULL, '19:56:00', 'default-premio.png', 0),
(37, 2, 'Genesis', 'qjsxqjsxjq', 'entregado', '2026-05-20', '2026-05-20 22:21:56', NULL, '18:21:00', '20260520_182145_chocolate.png', 0),
(39, 2, 'Pley', 'cantidad 6', 'pendiente', '2026-05-21', NULL, NULL, '14:57:00', 'default-premio.png', 1),
(40, 2, 'mariajose', 'djdjsj', 'pendiente', '2026-05-21', NULL, NULL, '14:58:00', 'default-premio.png', 1),
(41, 1, 'camisas doradas', 'grande talla s', 'entregado', '2026-05-21', '2026-05-21 18:18:15', NULL, '14:18:00', 'default-premio.png', 0),
(42, 2, 'Pley', 'eeeeee', 'pendiente', '2026-05-21', NULL, NULL, '20:20:59', 'default-premio.png', 1),
(43, 2, 'fsvsa', 'ffvv', 'pendiente', '2026-05-22', NULL, NULL, '20:35:13', 'default-premio.png', 1),
(44, 2, 'aaaa', '', 'pendiente', '2026-05-21', NULL, NULL, '21:05:52', 'default-premio.png', 1),
(45, 2, 'playsoy', '234', 'entregado', '2026-05-22', '2026-05-22 12:29:26', NULL, '09:27:00', '20260522_082903_cajitafeliz.png', 0),
(46, 2, 'cajita feliz', 'jdqdnqnjd', 'entregado', '2026-05-22', '2026-05-22 12:32:16', NULL, '08:30:00', '20260522_083122_cajitafeliz.png', 0),
(47, 2, 'vefe', 'rfr3f4f4', 'entregado', '2026-05-22', '2026-05-22 13:35:06', NULL, '09:34:00', '20260522_093453_cajitafeliz.png', 0),
(48, 2, 'mariajose', 'nnjhxjaxk', 'pendiente', '2026-04-27', NULL, NULL, '20:46:00', '20260522_204413_cajitafeliz.png', 0),
(49, 2, 'Play5', 'Ps5 1TB', 'entregado', '2026-05-22', '2026-05-26 04:24:45', NULL, '20:44:00', '20260522_204508_ps5.png', 0),
(50, 5, 'Programador JR', 'programador junior', 'entregado', '2026-05-31', '2026-06-01 02:21:52', 3, '22:12:00', '20260531_221336_IMG_8395.PNG', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recursos`
--

CREATE TABLE `recursos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `tipo_id` int(11) NOT NULL,
  `estado_id` int(11) NOT NULL DEFAULT 1,
  `fecha_compra` date DEFAULT NULL,
  `costo` decimal(10,2) DEFAULT NULL,
  `eliminado` tinyint(1) NOT NULL DEFAULT 0,
  `creado_en` datetime DEFAULT current_timestamp(),
  `modificado_en` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `recursos`
--

INSERT INTO `recursos` (`id`, `nombre`, `descripcion`, `tipo_id`, `estado_id`, `fecha_compra`, `costo`, `eliminado`, `creado_en`, `modificado_en`) VALUES
(1, 'Camara', 'camara 16mb', 2, 2, '2026-05-31', 100.00, 0, '2026-05-31 23:31:06', '2026-06-01 00:08:09');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reels`
--

CREATE TABLE `reels` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `patrocinado` varchar(100) DEFAULT NULL,
  `duracion_total` float DEFAULT 0,
  `creado_en` datetime DEFAULT current_timestamp(),
  `modificado_en` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `reels`
--

INSERT INTO `reels` (`id`, `nombre`, `patrocinado`, `duracion_total`, `creado_en`, `modificado_en`) VALUES
(1, 'Reels 1', 'Maltin polar', 0.25, '2026-06-01 00:20:43', '2026-06-01 00:20:43');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sincronizaciones`
--

CREATE TABLE `sincronizaciones` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(200) DEFAULT NULL,
  `fecha_sincronizacion` date NOT NULL,
  `hora_sincronizacion` time NOT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tareas`
--

CREATE TABLE `tareas` (
  `id_tarea` int(11) NOT NULL,
  `Nombre_Tarea` varchar(255) NOT NULL,
  `Instruccion` varchar(255) NOT NULL,
  `id_usuario_creador` int(11) DEFAULT NULL,
  `Estatus` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tareas`
--

INSERT INTO `tareas` (`id_tarea`, `Nombre_Tarea`, `Instruccion`, `id_usuario_creador`, `Estatus`) VALUES
(1, 'revisar la iluminacion', 'revisar la luces ', NULL, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tareas_asignadas`
--

CREATE TABLE `tareas_asignadas` (
  `id_asignacion` int(11) NOT NULL,
  `id_tarea` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `Estado` varchar(50) DEFAULT 'Pendiente',
  `fecha_asignacion_tarea` datetime DEFAULT NULL,
  `Estatus` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tareas_asignadas`
--

INSERT INTO `tareas_asignadas` (`id_asignacion`, `id_tarea`, `id_usuario`, `Estado`, `fecha_asignacion_tarea`, `Estatus`) VALUES
(1, 1, 3, 'Completada', '2026-06-01 00:23:29', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_recurso`
--

CREATE TABLE `tipo_recurso` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `tipo_recurso`
--

INSERT INTO `tipo_recurso` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Equipo de PC', 'pcs'),
(2, 'Equipo de Video', 'Cámaras, proyectores, monitores, etc.'),
(3, 'Iluminación', 'Luces, reflectores, dimmers, etc.'),
(4, 'Mobiliario', 'Mesas, sillas, stands, etc.'),
(5, 'Instrumento', 'Instrumentos musicales'),
(6, 'Vehículo', 'Vehículos de producción'),
(7, 'Otro', 'Otros tipos de recursos'),
(8, 'Microfono', 'microfonos');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `videos`
--

CREATE TABLE `videos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `duracion_segundos` int(11) DEFAULT 0,
  `orden` int(11) DEFAULT NULL,
  `reel_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `videos`
--

INSERT INTO `videos` (`id`, `nombre`, `duracion_segundos`, `orden`, `reel_id`) VALUES
(1, 'La Pollera', 15, 1, 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `asignaciones_recursos`
--
ALTER TABLE `asignaciones_recursos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_asignaciones_recurso` (`recurso_id`),
  ADD KEY `idx_asignaciones_estado` (`estado_asignacion_id`);

--
-- Indices de la tabla `contrato`
--
ALTER TABLE `contrato`
  ADD PRIMARY KEY (`id_contrato`),
  ADD KEY `id_patrocinador` (`id_patrocinador`);

--
-- Indices de la tabla `departamentos`
--
ALTER TABLE `departamentos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `elementos_guion`
--
ALTER TABLE `elementos_guion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `guion_id` (`guion_id`),
  ADD KEY `fecha_id` (`fecha_id`);

--
-- Indices de la tabla `estado_asignacion`
--
ALTER TABLE `estado_asignacion`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `estado_recurso`
--
ALTER TABLE `estado_recurso`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `eventos`
--
ALTER TABLE `eventos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `departamento_id` (`departamento_id`);

--
-- Indices de la tabla `eventos_sincronizados`
--
ALTER TABLE `eventos_sincronizados`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sincronizacion_id` (`sincronizacion_id`),
  ADD KEY `evento_id` (`evento_id`);

--
-- Indices de la tabla `guiones`
--
ALTER TABLE `guiones`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `guion_fechas`
--
ALTER TABLE `guion_fechas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `guion_id` (`guion_id`);

--
-- Indices de la tabla `historial_mantenimiento`
--
ALTER TABLE `historial_mantenimiento`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `idx_historial_mantenimiento` (`mantenimiento_id`);

--
-- Indices de la tabla `mantenimientos`
--
ALTER TABLE `mantenimientos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `idx_mantenimientos_estado` (`estado`),
  ADD KEY `idx_mantenimientos_recurso` (`recurso_id`);

--
-- Indices de la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD PRIMARY KEY (`id_pago`),
  ADD KEY `id_contrato` (`id_contrato`);

--
-- Indices de la tabla `patrocinadores`
--
ALTER TABLE `patrocinadores`
  ADD PRIMARY KEY (`id_patrocinador`);

--
-- Indices de la tabla `premios`
--
ALTER TABLE `premios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_patrocinador` (`id_patrocinador`);

--
-- Indices de la tabla `recursos`
--
ALTER TABLE `recursos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_recursos_tipo` (`tipo_id`),
  ADD KEY `idx_recursos_estado` (`estado_id`);

--
-- Indices de la tabla `reels`
--
ALTER TABLE `reels`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `sincronizaciones`
--
ALTER TABLE `sincronizaciones`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD PRIMARY KEY (`id_tarea`);

--
-- Indices de la tabla `tareas_asignadas`
--
ALTER TABLE `tareas_asignadas`
  ADD PRIMARY KEY (`id_asignacion`),
  ADD KEY `id_tarea` (`id_tarea`);

--
-- Indices de la tabla `tipo_recurso`
--
ALTER TABLE `tipo_recurso`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `videos`
--
ALTER TABLE `videos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_videos_reel` (`reel_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `asignaciones_recursos`
--
ALTER TABLE `asignaciones_recursos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `contrato`
--
ALTER TABLE `contrato`
  MODIFY `id_contrato` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `departamentos`
--
ALTER TABLE `departamentos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `elementos_guion`
--
ALTER TABLE `elementos_guion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `estado_asignacion`
--
ALTER TABLE `estado_asignacion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `estado_recurso`
--
ALTER TABLE `estado_recurso`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `eventos`
--
ALTER TABLE `eventos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `eventos_sincronizados`
--
ALTER TABLE `eventos_sincronizados`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `guiones`
--
ALTER TABLE `guiones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `guion_fechas`
--
ALTER TABLE `guion_fechas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `historial_mantenimiento`
--
ALTER TABLE `historial_mantenimiento`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `mantenimientos`
--
ALTER TABLE `mantenimientos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `pagos`
--
ALTER TABLE `pagos`
  MODIFY `id_pago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `patrocinadores`
--
ALTER TABLE `patrocinadores`
  MODIFY `id_patrocinador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `premios`
--
ALTER TABLE `premios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT de la tabla `recursos`
--
ALTER TABLE `recursos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `reels`
--
ALTER TABLE `reels`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `sincronizaciones`
--
ALTER TABLE `sincronizaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tareas`
--
ALTER TABLE `tareas`
  MODIFY `id_tarea` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `tareas_asignadas`
--
ALTER TABLE `tareas_asignadas`
  MODIFY `id_asignacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `tipo_recurso`
--
ALTER TABLE `tipo_recurso`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `videos`
--
ALTER TABLE `videos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asignaciones_recursos`
--
ALTER TABLE `asignaciones_recursos`
  ADD CONSTRAINT `fk_asignaciones_estado_asig` FOREIGN KEY (`estado_asignacion_id`) REFERENCES `estado_asignacion` (`id`),
  ADD CONSTRAINT `fk_asignaciones_recurso` FOREIGN KEY (`recurso_id`) REFERENCES `recursos` (`id`);

--
-- Filtros para la tabla `elementos_guion`
--
ALTER TABLE `elementos_guion`
  ADD CONSTRAINT `elementos_guion_ibfk_1` FOREIGN KEY (`guion_id`) REFERENCES `guiones` (`id`),
  ADD CONSTRAINT `elementos_guion_ibfk_2` FOREIGN KEY (`fecha_id`) REFERENCES `guion_fechas` (`id`);

--
-- Filtros para la tabla `eventos`
--
ALTER TABLE `eventos`
  ADD CONSTRAINT `eventos_ibfk_1` FOREIGN KEY (`departamento_id`) REFERENCES `departamentos` (`id`);

--
-- Filtros para la tabla `eventos_sincronizados`
--
ALTER TABLE `eventos_sincronizados`
  ADD CONSTRAINT `eventos_sincronizados_ibfk_1` FOREIGN KEY (`sincronizacion_id`) REFERENCES `sincronizaciones` (`id`),
  ADD CONSTRAINT `eventos_sincronizados_ibfk_2` FOREIGN KEY (`evento_id`) REFERENCES `eventos` (`id`);

--
-- Filtros para la tabla `guion_fechas`
--
ALTER TABLE `guion_fechas`
  ADD CONSTRAINT `guion_fechas_ibfk_1` FOREIGN KEY (`guion_id`) REFERENCES `guiones` (`id`);

--
-- Filtros para la tabla `historial_mantenimiento`
--
ALTER TABLE `historial_mantenimiento`
  ADD CONSTRAINT `historial_mantenimiento_ibfk_1` FOREIGN KEY (`mantenimiento_id`) REFERENCES `mantenimientos` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `recursos`
--
ALTER TABLE `recursos`
  ADD CONSTRAINT `fk_recursos_estado` FOREIGN KEY (`estado_id`) REFERENCES `estado_recurso` (`id`),
  ADD CONSTRAINT `fk_recursos_tipo` FOREIGN KEY (`tipo_id`) REFERENCES `tipo_recurso` (`id`);

--
-- Filtros para la tabla `tareas_asignadas`
--
ALTER TABLE `tareas_asignadas`
  ADD CONSTRAINT `tareas_asignadas_ibfk_1` FOREIGN KEY (`id_tarea`) REFERENCES `tareas` (`id_tarea`);

--
-- Filtros para la tabla `videos`
--
ALTER TABLE `videos`
  ADD CONSTRAINT `fk_videos_reel` FOREIGN KEY (`reel_id`) REFERENCES `reels` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
