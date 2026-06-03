-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 01-06-2026 a las 06:44:29
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
-- Base de datos: `no_funcional`
--
CREATE DATABASE IF NOT EXISTS `no_funcional` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `no_funcional`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actividad_usuario`
--

CREATE TABLE `actividad_usuario` (
  `id` int(11) NOT NULL,
  `sesion_id` int(11) DEFAULT NULL,
  `usuario_id` int(11) NOT NULL,
  `tipo_accion` varchar(30) NOT NULL,
  `modulo` varchar(50) NOT NULL,
  `accion` text DEFAULT NULL,
  `detalle` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`detalle`)),
  `pagina` varchar(200) DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `actividad_usuario`
--

INSERT INTO `actividad_usuario` (`id`, `sesion_id`, `usuario_id`, `tipo_accion`, `modulo`, `accion`, `detalle`, `pagina`, `ip_address`, `created_at`) VALUES
(11, NULL, 4, 'logout', 'auth', 'Cierre de sesión', '\"Usuario keiberzamudia14@gmail.com cerr\\u00f3 sesi\\u00f3n\"', '/auth/logout', '127.0.0.1', '2026-05-26 04:40:36'),
(12, NULL, 3, 'logout', 'auth', 'Cierre de sesión', '\"Usuario admin@admin.com cerr\\u00f3 sesi\\u00f3n\"', '/auth/logout', '127.0.0.1', '2026-05-26 04:41:28'),
(13, NULL, 4, 'login', 'auth', 'Inicio de sesión', '\"Usuario keiberzamudia14@gmail.com inici\\u00f3 sesi\\u00f3n\"', '/auth/login', '127.0.0.1', '2026-05-26 04:41:28'),
(14, NULL, 3, 'login', 'auth', 'Inicio de sesión', '\"Usuario admin@admin.com inici\\u00f3 sesi\\u00f3n\"', '/auth/login', '127.0.0.1', '2026-05-26 04:41:36'),
(15, NULL, 4, 'create', 'guion', 'Agregar elemento', '\"Elemento game agregado a gui\\u00f3n #2\"', '/guiones/agregar-elemento/2', '127.0.0.1', '2026-05-26 04:42:38'),
(16, NULL, 4, 'create', 'mantenimiento', 'Crear recurso', '\"Recurso \\\"Lapto MacBook Pro m3\\\" creado\"', '/mantenimiento/recursos/crear', '127.0.0.1', '2026-05-26 04:45:34'),
(17, NULL, 4, 'create', 'mantenimiento', 'Ingresar a mantenimiento', '\"Recurso \\\"Lapto MacBook Pro m3\\\" ingresado a mantenimiento\"', '/mantenimiento/ingresar/2', '127.0.0.1', '2026-05-26 04:56:25'),
(18, NULL, 4, 'update', 'mantenimiento', 'Agregar nota', '\"Nota a mantenimiento #1: Prueba de bitacora\"', '/mantenimiento/agregar-nota/1', '127.0.0.1', '2026-05-26 04:56:41'),
(20, NULL, 3, 'logout', 'auth', 'Cierre de sesión', '\"Usuario admin@admin.com cerr\\u00f3 sesi\\u00f3n\"', '/auth/logout', '127.0.0.1', '2026-05-31 18:02:09'),
(21, NULL, 3, 'login', 'auth', 'Inicio de sesión', '\"Usuario admin@admin.com inici\\u00f3 sesi\\u00f3n\"', '/auth/login', '127.0.0.1', '2026-05-31 18:02:18'),
(22, NULL, 3, 'create', 'usuarios', 'Crear usuario', '\"Usuario \\\"Yolianna\\\" (yolianna14@gmail.com) creado\"', '/usuarios/crear', '127.0.0.1', '2026-05-31 18:02:46'),
(23, NULL, 3, 'update', 'usuarios', 'Editar usuario', '\"Usuario #18 editado\"', '/usuarios/editar/18', '127.0.0.1', '2026-05-31 18:03:31'),
(24, NULL, 3, 'logout', 'auth', 'Cierre de sesión', '\"Usuario admin@admin.com cerr\\u00f3 sesi\\u00f3n\"', '/auth/logout', '127.0.0.1', '2026-05-31 18:10:40'),
(25, NULL, 3, 'login', 'auth', 'Inicio de sesión', '\"Usuario admin@admin.com inici\\u00f3 sesi\\u00f3n\"', '/auth/login', '127.0.0.1', '2026-05-31 18:10:49'),
(26, NULL, 3, 'create', 'usuarios', 'Crear usuario', '\"Usuario \\\"Prueba\\\" (prueba@gmail.com) creado\"', '/usuarios/crear', '127.0.0.1', '2026-05-31 18:13:23'),
(27, NULL, 3, 'update', 'usuarios', 'Editar usuario', '\"Usuario #19 editado\"', '/usuarios/editar/19', '127.0.0.1', '2026-05-31 18:14:18'),
(28, NULL, 3, 'update', 'usuarios', 'Editar usuario', '\"Usuario #19 editado\"', '/usuarios/editar/19', '127.0.0.1', '2026-05-31 18:14:44'),
(29, NULL, 3, 'update', 'usuarios', 'Editar usuario', '\"Usuario #18 editado\"', '/usuarios/editar/18', '127.0.0.1', '2026-05-31 18:19:01'),
(30, NULL, 3, 'delete', 'usuarios', 'Eliminar usuario', '\"Usuario \\\"Prueba\\\" (prueba@gmail.com) eliminado\"', '/usuarios/eliminar/19', '127.0.0.1', '2026-05-31 18:19:16'),
(31, NULL, 3, 'delete', 'guion', 'Eliminar guión', '\"Gui\\u00f3n \\\"sxdsDAS\\\" eliminado\"', '/guiones/eliminar/2', '127.0.0.1', '2026-05-31 18:36:45'),
(32, NULL, 3, 'update', 'guion', 'Editar elemento', '\"Elemento #1 de gui\\u00f3n #1 editado\"', '/guiones/editar-elemento/1/1', '127.0.0.1', '2026-05-31 18:46:55'),
(33, NULL, 3, 'create', 'guion', 'Agregar elemento', '\"Elemento game agregado a gui\\u00f3n #1\"', '/guiones/agregar-elemento/1', '127.0.0.1', '2026-05-31 18:57:24'),
(34, NULL, 3, 'create', 'guion', 'Crear guión', '\"Gui\\u00f3n \\\"Cardenales General\\\" creado\"', '/guiones/crear', '127.0.0.1', '2026-05-31 19:13:10'),
(35, NULL, 3, 'create', 'guion', 'Agregar elemento', '\"Elemento pregame agregado a gui\\u00f3n #3\"', '/guiones/agregar-elemento/3', '127.0.0.1', '2026-05-31 19:14:01'),
(36, NULL, 3, 'update', 'guion', 'Editar elemento', '\"Elemento #6 de gui\\u00f3n #3 editado\"', '/guiones/editar-elemento/3/6', '127.0.0.1', '2026-05-31 19:14:47'),
(37, NULL, 3, 'create', 'guion', 'Agregar elemento', '\"Elemento pregame agregado a gui\\u00f3n #3\"', '/guiones/agregar-elemento/3', '127.0.0.1', '2026-05-31 19:15:36'),
(38, NULL, 3, 'update', 'guion', 'Editar elemento', '\"Elemento #6 de gui\\u00f3n #3 editado\"', '/guiones/editar-elemento/3/6', '127.0.0.1', '2026-05-31 19:15:45'),
(39, NULL, 3, 'create', 'guion', 'Agregar elemento', '\"Elemento game agregado a gui\\u00f3n #3\"', '/guiones/agregar-elemento/3', '127.0.0.1', '2026-05-31 19:16:13'),
(40, NULL, 3, 'update', 'guion', 'Publicar guión', '\"Gui\\u00f3n \\\"Cardenales General\\\" publicado\"', '/guiones/publicar/3', '127.0.0.1', '2026-05-31 19:16:22'),
(41, NULL, 3, 'delete', 'guion', 'Eliminar guión', '\"Gui\\u00f3n \\\"Cardenales General\\\" eliminado\"', '/guiones/eliminar/3', '127.0.0.1', '2026-05-31 19:17:21'),
(42, NULL, 3, 'delete', 'guion', 'Eliminar guión', '\"Gui\\u00f3n \\\"Guion de Producci\\u00f3n\\\" eliminado\"', '/guiones/eliminar/1', '127.0.0.1', '2026-05-31 19:35:05'),
(43, NULL, 3, 'create', 'guion', 'Crear guión', '\"Gui\\u00f3n \\\"Cardenales General\\\" creado\"', '/guiones/crear', '127.0.0.1', '2026-05-31 19:41:10'),
(44, NULL, 3, 'create', 'guion', 'Agregar elemento', '\"Elemento pregame agregado a gui\\u00f3n #4\"', '/guiones/agregar-elemento/4', '127.0.0.1', '2026-05-31 19:41:33'),
(45, NULL, 3, 'delete', 'guion', 'Eliminar guión', '\"Gui\\u00f3n \\\"Cardenales General\\\" eliminado\"', '/guiones/eliminar/4', '127.0.0.1', '2026-05-31 19:41:37'),
(46, NULL, 3, 'create', 'guion', 'Crear guión', '\"Gui\\u00f3n \\\"Cardenales General\\\" creado\"', '/guiones/crear', '127.0.0.1', '2026-05-31 19:41:53'),
(47, NULL, 3, 'create', 'guion', 'Agregar elemento', '\"Elemento pregame agregado a gui\\u00f3n #5\"', '/guiones/agregar-elemento/5', '127.0.0.1', '2026-05-31 19:42:09'),
(48, NULL, 3, 'login', 'auth', 'Inicio de sesión', '\"Usuario admin@admin.com inici\\u00f3 sesi\\u00f3n\"', '/auth/login', '127.0.0.1', '2026-05-31 19:42:30'),
(49, NULL, 3, 'delete', 'guion', 'Eliminar guión', '\"Gui\\u00f3n \\\"Cardenales General\\\" eliminado\"', '/guiones/eliminar/5', '127.0.0.1', '2026-05-31 19:42:40'),
(50, NULL, 3, 'create', 'guion', 'Crear guión', '\"Gui\\u00f3n \\\"Cardenales General\\\" creado\"', '/guiones/crear', '127.0.0.1', '2026-05-31 19:46:35'),
(51, NULL, 3, 'create', 'guion', 'Agregar elemento', '\"Elemento pregame agregado a gui\\u00f3n #6\"', '/guiones/agregar-elemento/6', '127.0.0.1', '2026-05-31 19:46:51'),
(52, NULL, 3, 'update', 'guion', 'Publicar guión', '\"Gui\\u00f3n \\\"Cardenales General\\\" publicado\"', '/guiones/publicar/6', '127.0.0.1', '2026-05-31 19:53:36'),
(53, NULL, 3, 'create', 'guion', 'Agregar elemento', '\"Elemento pregame agregado a gui\\u00f3n #6\"', '/guiones/agregar-elemento/6', '127.0.0.1', '2026-05-31 20:11:39'),
(54, NULL, 18, 'login', 'auth', 'Inicio de sesión', '\"Usuario yolianna14@gmail.com inici\\u00f3 sesi\\u00f3n\"', '/auth/login', '127.0.0.1', '2026-05-31 20:52:32'),
(55, NULL, 3, 'login', 'auth', 'Inicio de sesión', '\"Usuario admin@admin.com inici\\u00f3 sesi\\u00f3n\"', '/auth/login', '127.0.0.1', '2026-05-31 21:11:57'),
(56, NULL, 3, 'update', 'roles', 'Actualizar permisos del rol', '\"Permisos del rol #2 actualizados\"', '/roles/editar-rol/2', '127.0.0.1', '2026-05-31 21:13:30'),
(57, NULL, 3, 'update', 'roles', 'Actualizar permisos del rol', '\"Permisos del rol #3 actualizados\"', '/roles/editar-rol/3', '127.0.0.1', '2026-05-31 21:13:54'),
(58, NULL, 18, 'logout', 'auth', 'Cierre de sesión', '\"Usuario yolianna14@gmail.com cerr\\u00f3 sesi\\u00f3n\"', '/auth/logout', '127.0.0.1', '2026-05-31 21:14:57'),
(59, NULL, 18, 'login', 'auth', 'Inicio de sesión', '\"Usuario yolianna14@gmail.com inici\\u00f3 sesi\\u00f3n\"', '/auth/login', '127.0.0.1', '2026-05-31 21:15:22'),
(60, NULL, 18, 'login', 'auth', 'Inicio de sesión', '\"Usuario yolianna14@gmail.com inici\\u00f3 sesi\\u00f3n\"', '/auth/login', '127.0.0.1', '2026-05-31 21:23:50'),
(61, NULL, 3, 'update', 'roles', 'Actualizar permisos del rol', '\"Permisos del rol #3 actualizados\"', '/roles/editar-rol/3', '127.0.0.1', '2026-05-31 21:24:11'),
(62, NULL, 3, 'update', 'roles', 'Actualizar permisos del rol', '\"Permisos del rol #3 actualizados\"', '/roles/editar-rol/3', '127.0.0.1', '2026-05-31 21:26:17'),
(63, NULL, 3, 'update', 'roles', 'Actualizar permisos del rol', '\"Permisos del rol #3 actualizados\"', '/roles/editar-rol/3', '127.0.0.1', '2026-05-31 21:35:32'),
(64, NULL, 3, 'delete', 'contrato', 'Eliminar contrato', '\"Contrato #5 eliminado\"', '/contratos/', '127.0.0.1', '2026-05-31 21:39:53'),
(65, NULL, 3, 'delete', 'contrato', 'Eliminar contrato', '\"Contrato #4 eliminado\"', '/contratos/', '127.0.0.1', '2026-05-31 21:39:55'),
(66, NULL, 3, 'delete', 'contrato', 'Eliminar contrato', '\"Contrato #3 eliminado\"', '/contratos/', '127.0.0.1', '2026-05-31 21:39:59'),
(67, NULL, 3, 'create', 'patrocinadores', 'Crear patrocinador', '\"Patrocinador \\\"keiver C.A\\\" creado\"', '/patrocinadores/', '127.0.0.1', '2026-05-31 21:49:46'),
(68, NULL, 3, 'login', 'auth', 'Inicio de sesión', '\"Usuario admin@admin.com inici\\u00f3 sesi\\u00f3n\"', '/auth/login', '127.0.0.1', '2026-05-31 22:01:39'),
(69, NULL, 3, 'create', 'patrocinadores', 'Crear patrocinador', '\"Patrocinador \\\"Tubrica\\\" creado\"', '/patrocinadores/', '127.0.0.1', '2026-05-31 22:02:39'),
(70, NULL, 3, 'update', 'patrocinadores', 'Editar patrocinador', '\"Patrocinador #6 editado\"', '/patrocinadores/', '127.0.0.1', '2026-05-31 22:02:47'),
(71, NULL, 3, 'update', 'patrocinadores', 'Editar patrocinador', '\"Patrocinador #6 editado\"', '/patrocinadores/', '127.0.0.1', '2026-05-31 22:03:01'),
(72, NULL, 3, 'login', 'auth', 'Inicio de sesión', '\"Usuario admin@admin.com inici\\u00f3 sesi\\u00f3n\"', '/auth/login', '127.0.0.1', '2026-05-31 22:11:53'),
(73, NULL, 3, 'create', 'contrato', 'Crear contrato', '\"Contrato con patrocinador #6 creado\"', '/contratos/', '127.0.0.1', '2026-05-31 22:12:17'),
(74, NULL, 3, 'update', 'contrato', 'Editar contrato', '\"Contrato #6 editado\"', '/contratos/', '127.0.0.1', '2026-05-31 22:12:26'),
(75, NULL, 3, 'create', 'premios', 'Crear premio', '\"Premio \\\"Programador JR\\\" creado\"', '/premios/', '127.0.0.1', '2026-05-31 22:13:36'),
(76, NULL, 3, 'delete', 'patrocinadores', 'Eliminar patrocinador', '\"Patrocinador \\\"keiver C.A\\\" eliminado\"', '/patrocinadores/', '127.0.0.1', '2026-05-31 22:14:00'),
(77, NULL, 3, 'delete', 'contrato', 'Eliminar contrato', '\"Contrato #6 eliminado\"', '/contratos/', '127.0.0.1', '2026-05-31 22:14:10'),
(78, NULL, 3, 'login', 'auth', 'Inicio de sesión', '\"Usuario admin@admin.com inici\\u00f3 sesi\\u00f3n\"', '/auth/login', '127.0.0.1', '2026-05-31 22:20:54'),
(79, NULL, 3, 'update', 'premios', 'Entregar premio existente', '\"Premio #50 entregado\"', '/premios/', '127.0.0.1', '2026-05-31 22:21:52'),
(80, NULL, 3, 'login', 'auth', 'Inicio de sesión', '\"Usuario admin@admin.com inici\\u00f3 sesi\\u00f3n\"', '/auth/login', '127.0.0.1', '2026-05-31 22:24:07'),
(81, NULL, 3, 'create', 'inventario', 'Crear recurso', '\"Recurso \\\"Camara\\\" creado\"', '/inventario/crear', '127.0.0.1', '2026-05-31 23:31:06'),
(82, NULL, 3, 'create', 'inventario', 'Asignar recurso', '\"Recurso #1 asignado\"', '/inventario/asignar_desde_gestion', '127.0.0.1', '2026-05-31 23:31:44'),
(83, NULL, 3, 'update', 'inventario', 'Devolver recurso', '\"Asignaci\\u00f3n #1 devuelta\"', '/inventario/devolver/1', '127.0.0.1', '2026-05-31 23:32:05'),
(84, NULL, 3, 'create', 'inventario', 'Asignar recurso', '\"Recurso #1 asignado\"', '/inventario/asignar_desde_gestion', '127.0.0.1', '2026-05-31 23:32:21'),
(85, NULL, 3, 'update', 'inventario', 'Devolver recurso', '\"Asignaci\\u00f3n #2 devuelta\"', '/inventario/devolver/2', '127.0.0.1', '2026-05-31 23:43:57'),
(86, NULL, 3, 'update', 'inventario', 'Editar tipo de recurso', '\"Tipo \\\"Equipo de PC\\\" editado\"', '/inventario/api/tipos/editar/1', '127.0.0.1', '2026-05-31 23:50:27'),
(87, NULL, 3, 'create', 'inventario', 'Crear tipo de recurso', '\"Tipo \\\"Microfonos\\\" creado\"', '/inventario/api/tipos/crear', '127.0.0.1', '2026-05-31 23:58:33'),
(88, NULL, 3, 'update', 'inventario', 'Editar recurso', '\"Recurso \\\"Camara\\\" editado\"', '/inventario/editar/1', '127.0.0.1', '2026-05-31 23:58:44'),
(89, NULL, 3, 'update', 'inventario', 'Editar recurso', '\"Recurso \\\"Camara\\\" editado\"', '/inventario/editar/1', '127.0.0.1', '2026-06-01 00:03:10'),
(90, NULL, 3, 'update', 'inventario', 'Editar tipo de recurso', '\"Tipo \\\"Microfono\\\" editado\"', '/inventario/api/tipos/editar/8', '127.0.0.1', '2026-06-01 00:03:24'),
(91, NULL, 3, 'create', 'inventario', 'Asignar recurso', '\"Recurso #1 asignado\"', '/inventario/asignar_desde_gestion', '127.0.0.1', '2026-06-01 00:04:31'),
(92, NULL, 3, 'update', 'inventario', 'Editar recurso', '\"Recurso \\\"Camara\\\" editado\"', '/inventario/editar/1', '127.0.0.1', '2026-06-01 00:08:09'),
(93, NULL, 3, 'delete', 'guion', 'Eliminar guión', '\"Gui\\u00f3n \\\"sxdsDAS\\\" eliminado\"', '/guiones/eliminar/2', '127.0.0.1', '2026-06-01 00:15:54'),
(94, NULL, 3, 'delete', 'guion', 'Eliminar guión', '\"Gui\\u00f3n \\\"Guion de Producci\\u00f3n\\\" eliminado\"', '/guiones/eliminar/1', '127.0.0.1', '2026-06-01 00:16:06'),
(95, NULL, 3, 'create', 'reels', 'Crear reel', '\"Reel \\\"Reels 1\\\" creado\"', '/reels/crear', '127.0.0.1', '2026-06-01 00:20:43'),
(96, NULL, 3, 'create', 'tareas', 'Crear tarea', '\"Tarea \\\"revisar la iluminacion\\\" creada\"', '/gestion-tareas/', '127.0.0.1', '2026-06-01 00:23:21'),
(97, NULL, 3, 'create', 'tareas', 'Asignar tarea', '\"Tarea #1 asignada a usuario #3\"', '/gestion-tareas/asignar', '127.0.0.1', '2026-06-01 00:23:29'),
(98, NULL, 3, 'update', 'tareas', 'Completar tarea', '\"Asignaci\\u00f3n #1 completada por usuario #3\"', '/gestion-tareas/completar', '127.0.0.1', '2026-06-01 00:41:18');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cambios_por_modulo`
--

CREATE TABLE `cambios_por_modulo` (
  `id` int(11) NOT NULL,
  `actividad_id` int(11) NOT NULL,
  `tabla_afectada` varchar(50) NOT NULL,
  `registro_id` int(11) DEFAULT NULL,
  `campo` varchar(100) NOT NULL,
  `valor_anterior` text DEFAULT NULL,
  `valor_nuevo` text DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dashboard_visibilidad`
--

CREATE TABLE `dashboard_visibilidad` (
  `id` int(11) NOT NULL,
  `rol_id` int(11) NOT NULL,
  `modulo_key` varchar(50) NOT NULL,
  `visible` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `dashboard_visibilidad`
--

INSERT INTO `dashboard_visibilidad` (`id`, `rol_id`, `modulo_key`, `visible`) VALUES
(1, 2, 'guion', 1),
(2, 2, 'mantenimiento', 1),
(3, 2, 'premio', 1),
(4, 2, 'contrato', 1),
(5, 2, 'balance', 1),
(6, 2, 'tarea', 1),
(7, 2, 'patrocinador', 1),
(8, 2, 'usuario', 1),
(35, 3, 'guion', 1),
(36, 3, 'mantenimiento', 0),
(37, 3, 'premio', 0),
(38, 3, 'contrato', 0),
(39, 3, 'balance', 0),
(40, 3, 'tarea', 1),
(41, 3, 'patrocinador', 0),
(42, 3, 'usuario', 0),
(43, 3, 'actividad', 0),
(44, 3, 'enlinea', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `errores_aplicacion`
--

CREATE TABLE `errores_aplicacion` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `tipo_error` varchar(50) DEFAULT NULL,
  `mensaje` text DEFAULT NULL,
  `traceback` text DEFAULT NULL,
  `pagina` varchar(200) DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permisos`
--

CREATE TABLE `permisos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `codigo` varchar(100) NOT NULL,
  `modulo` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `permisos`
--

INSERT INTO `permisos` (`id`, `nombre`, `codigo`, `modulo`, `descripcion`) VALUES
(1, 'Ver panel principal', 'dashboard.view', 'Dashboard', NULL),
(2, 'Ver lista de usuarios', 'usuario.view', 'Usuarios', NULL),
(3, 'Crear usuarios', 'usuario.create', 'Usuarios', NULL),
(4, 'Editar usuarios', 'usuario.edit', 'Usuarios', NULL),
(5, 'Eliminar usuarios', 'usuario.delete', 'Usuarios', NULL),
(6, 'Ver perfil propio', 'usuario.perfil', 'Usuarios', NULL),
(7, 'Ver guiones', 'guion.view', 'Guión', NULL),
(8, 'Crear guiones', 'guion.create', 'Guión', NULL),
(9, 'Editar guiones', 'guion.edit', 'Guión', NULL),
(10, 'Eliminar guiones', 'guion.delete', 'Guión', NULL),
(11, 'Publicar guiones', 'guion.publish', 'Guión', NULL),
(12, 'Previsualizar guiones', 'guion.preview', 'Guión', NULL),
(13, 'Ver pantalla en vivo', 'envivo.view', 'En Vivo', NULL),
(14, 'Controlar elementos en vivo', 'envivo.control', 'En Vivo', NULL),
(15, 'Ver premios', 'premio.view', 'Premios', NULL),
(16, 'Crear premios', 'premio.create', 'Premios', NULL),
(17, 'Editar premios', 'premio.edit', 'Premios', NULL),
(18, 'Eliminar premios', 'premio.delete', 'Premios', NULL),
(19, 'Entregar premios', 'premio.entregar', 'Premios', NULL),
(20, 'Ver mantenimiento', 'mantenimiento.view', 'Mantenimiento', NULL),
(21, 'Crear recursos', 'mantenimiento.create', 'Mantenimiento', NULL),
(22, 'Editar recursos', 'mantenimiento.edit', 'Mantenimiento', NULL),
(23, 'Eliminar recursos', 'mantenimiento.delete', 'Mantenimiento', NULL),
(24, 'Ver roles y permisos', 'rol.view', 'Roles', NULL),
(25, 'Editar permisos de usuarios', 'rol.edit', 'Roles', NULL),
(26, 'Ver tareas', 'gestion_tarea.view', 'Tareas', NULL),
(27, 'Crear tareas', 'gestion_tarea.create', 'Tareas', NULL),
(28, 'Editar tareas', 'gestion_tarea.edit', 'Tareas', NULL),
(29, 'Eliminar tareas', 'gestion_tarea.delete', 'Tareas', NULL),
(30, 'Completar tareas propias', 'gestion_tarea.complete', 'Tareas', NULL),
(31, 'Ver patrocinadores', 'patrocinador.view', 'Patrocinadores', NULL),
(32, 'Crear patrocinadores', 'patrocinador.create', 'Patrocinadores', NULL),
(33, 'Editar patrocinadores', 'patrocinador.edit', 'Patrocinadores', NULL),
(34, 'Eliminar patrocinadores', 'patrocinador.delete', 'Patrocinadores', NULL),
(35, 'Ver contratos', 'contrato.view', 'Contratos', NULL),
(36, 'Crear contratos', 'contrato.create', 'Contratos', NULL),
(37, 'Editar contratos', 'contrato.edit', 'Contratos', NULL),
(38, 'Eliminar contratos', 'contrato.delete', 'Contratos', NULL),
(39, 'Ver balance', 'balance.view', 'Balance', NULL),
(40, 'Registrar pagos', 'balance.create', 'Balance', NULL),
(41, 'Editar pagos', 'balance.edit', 'Balance', NULL),
(42, 'Eliminar pagos', 'balance.delete', 'Balance', NULL),
(43, 'Ver inventario de recursos', 'inventario.view', 'Inventario', NULL),
(44, 'Crear recursos', 'inventario.create', 'Inventario', NULL),
(45, 'Editar recursos', 'inventario.edit', 'Inventario', NULL),
(46, 'Eliminar recursos', 'inventario.delete', 'Inventario', NULL),
(47, 'Asignar y devolver recursos', 'inventario.assign', 'Inventario', NULL),
(48, 'Ver reels', 'reels.view', 'Reels', NULL),
(49, 'Crear reels', 'reels.create', 'Reels', NULL),
(50, 'Editar reels', 'reels.edit', 'Reels', NULL),
(51, 'Eliminar reels', 'reels.delete', 'Reels', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Superadmin', 'Acceso total al sistema'),
(2, 'Administrador', 'Acceso administrativo excepto roles'),
(3, 'Usuario', 'Acceso básico de lectura');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol_permiso`
--

CREATE TABLE `rol_permiso` (
  `id` int(11) NOT NULL,
  `rol_id` int(11) NOT NULL,
  `permiso_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `rol_permiso`
--

INSERT INTO `rol_permiso` (`id`, `rol_id`, `permiso_id`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(4, 1, 4),
(5, 1, 5),
(6, 1, 6),
(7, 1, 7),
(8, 1, 8),
(9, 1, 9),
(10, 1, 10),
(11, 1, 11),
(12, 1, 12),
(13, 1, 13),
(14, 1, 14),
(15, 1, 15),
(16, 1, 16),
(17, 1, 17),
(18, 1, 18),
(19, 1, 19),
(20, 1, 20),
(21, 1, 21),
(22, 1, 22),
(23, 1, 23),
(24, 1, 24),
(25, 1, 25),
(169, 2, 1),
(191, 2, 2),
(188, 2, 3),
(189, 2, 4),
(190, 2, 5),
(192, 2, 6),
(177, 2, 7),
(172, 2, 8),
(173, 2, 9),
(174, 2, 10),
(176, 2, 11),
(175, 2, 12),
(171, 2, 13),
(170, 2, 14),
(186, 2, 15),
(182, 2, 16),
(183, 2, 17),
(184, 2, 18),
(185, 2, 19),
(181, 2, 20),
(178, 2, 21),
(179, 2, 22),
(180, 2, 23),
(187, 2, 24),
(205, 3, 1),
(208, 3, 6),
(206, 3, 13),
(207, 3, 15),
(209, 1, 26),
(210, 1, 27),
(211, 1, 28),
(212, 1, 29),
(213, 1, 30),
(214, 1, 31),
(215, 1, 32),
(216, 1, 33),
(217, 1, 34),
(218, 1, 35),
(219, 1, 36),
(220, 1, 37),
(221, 1, 38),
(222, 1, 39),
(223, 1, 40),
(224, 1, 41),
(225, 1, 42),
(226, 1, 43),
(227, 1, 44),
(228, 1, 45),
(229, 1, 46),
(230, 1, 47),
(231, 1, 48),
(232, 1, 49),
(233, 1, 50),
(234, 1, 51),
(235, 2, 26),
(236, 2, 27),
(237, 2, 28),
(238, 2, 29),
(239, 2, 30),
(240, 2, 31),
(241, 2, 32),
(242, 2, 33),
(243, 2, 34),
(244, 2, 35),
(245, 2, 36),
(246, 2, 37),
(247, 2, 38),
(248, 2, 39),
(249, 2, 40),
(250, 2, 41),
(251, 2, 42),
(252, 2, 43),
(253, 2, 44),
(254, 2, 45),
(255, 2, 46),
(256, 2, 47),
(257, 2, 48),
(258, 2, 49),
(259, 2, 50),
(260, 2, 51),
(261, 3, 2),
(262, 3, 7),
(263, 3, 20),
(264, 3, 26),
(265, 3, 31),
(266, 3, 35),
(267, 3, 39),
(268, 3, 43),
(269, 3, 48);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sesiones_usuario`
--

CREATE TABLE `sesiones_usuario` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `inicio_sesion` datetime DEFAULT NULL,
  `fin_sesion` datetime DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` varchar(500) DEFAULT NULL,
  `duracion_segundos` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sesiones_usuario`
--

INSERT INTO `sesiones_usuario` (`id`, `usuario_id`, `inicio_sesion`, `fin_sesion`, `ip_address`, `user_agent`, `duracion_segundos`) VALUES
(4, 4, '2026-05-26 04:41:28', NULL, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Safari/605.1.15', NULL),
(5, 3, '2026-05-26 04:41:36', NULL, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', NULL),
(11, 3, '2026-05-31 18:02:18', '2026-05-31 22:10:40', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', 14902),
(12, 3, '2026-05-31 18:10:49', NULL, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', NULL),
(13, 3, '2026-05-31 19:42:30', NULL, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', NULL),
(14, 18, '2026-05-31 20:52:32', '2026-06-01 01:14:57', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Safari/605.1.15', 15745),
(15, 3, '2026-05-31 21:11:57', NULL, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', NULL),
(16, 18, '2026-05-31 21:15:22', NULL, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Safari/605.1.15', NULL),
(17, 18, '2026-05-31 21:23:50', NULL, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Safari/605.1.15', NULL),
(18, 3, '2026-05-31 22:01:39', NULL, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', NULL),
(19, 3, '2026-05-31 22:11:53', NULL, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', NULL),
(20, 3, '2026-05-31 22:20:54', NULL, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', NULL),
(21, 3, '2026-05-31 22:24:07', NULL, '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(200) NOT NULL,
  `cedula` varchar(20) NOT NULL,
  `rol` varchar(20) DEFAULT 'Usuario',
  `departamento` varchar(50) DEFAULT 'Medios',
  `telefono` varchar(20) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `fecha_registro` datetime DEFAULT NULL,
  `ultimo_acceso` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `email`, `password_hash`, `cedula`, `rol`, `departamento`, `telefono`, `activo`, `fecha_registro`, `ultimo_acceso`) VALUES
(3, 'Admin', 'admin@admin.com', 'scrypt:32768:8:1$VImiJ1cWMig3OJN6$66e6543200f85e636bf90eb21b174b6d22ceea892b52ecb277a9d878b41447879ad382b1e29418e473d6df392a991d827e214a96d411f0b3ae71f3ec7642dc11', '12345678', 'Superadmin', 'Palco de Operaciones', '0422345981', 1, '2026-05-05 21:34:59', '2026-05-31 22:24:07'),
(4, 'keiver', 'keiberzamudia14@gmail.com', 'scrypt:32768:8:1$Ja5EZ2d8z6RDtluV$21bbb2479653cb8914c283ba440713c18a32ad731791dd2a2187af34dac22370e55e2f85e8b92688f1587b59b009e003ee65ee62d42928dca52b0da2a2771ef0', '25469224', 'Administrador', 'Medios', '0412344590', 1, '2026-05-05 23:44:26', NULL),
(5, 'Genesis', 'genesis94@gmail.com', 'scrypt:32768:8:1$kuxi8DGW2YZ3lUpv$64ca25908b6cfe3c60ba9a50969a703ef14b7291365d0eade9e696dc08046383f6d183d22037dec774450586f49be3a398af7f1c75774d5996690b3780f44aa3', '26330334', 'Administrador', 'Palco de Operaciones', '04243455566', 1, '2026-05-05 23:49:50', NULL),
(6, 'naryi', 'naryi30@gmail.com', 'scrypt:32768:8:1$m6IBDa49H8GPNhHw$04486b03ba43534e514ea5c4f4cde1bda35abdadc1d42b82ce8e19ab2b4bcb1ca08dc71d8005f6e3c3296a74f003b2c17d0cf92be1b9296d8fc7be207daa54a6', '14598999', 'Usuario', 'Medios', '04123455564', 1, '2026-05-06 19:58:32', NULL),
(18, 'Yolianna', 'yolianna14@gmail.com', 'scrypt:32768:8:1$bA30tHfEi8KMvDxE$ba997862b9784b253cb148727099874f6c207278f71b4135e074fc7fe9a1b1a4688bb270d1ef823d9e314ec13a0d4b83ba3108c4d76c4e2380ca5e2048d136e8', '25894881', 'Usuario', 'Medios', '02512661166', 1, '2026-05-31 18:02:46', '2026-05-31 21:23:50');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_dashboard_vis`
--

CREATE TABLE `usuario_dashboard_vis` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `modulo_key` varchar(50) NOT NULL,
  `visible` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_permiso`
--

CREATE TABLE `usuario_permiso` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `permiso_id` int(11) NOT NULL,
  `fecha_asignacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `actividad_usuario`
--
ALTER TABLE `actividad_usuario`
  ADD PRIMARY KEY (`id`),
  ADD KEY `au_fk_sesion` (`sesion_id`),
  ADD KEY `au_fk_usuario` (`usuario_id`);

--
-- Indices de la tabla `cambios_por_modulo`
--
ALTER TABLE `cambios_por_modulo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cm_fk_actividad` (`actividad_id`);

--
-- Indices de la tabla `dashboard_visibilidad`
--
ALTER TABLE `dashboard_visibilidad`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_rol_modulo` (`rol_id`,`modulo_key`);

--
-- Indices de la tabla `errores_aplicacion`
--
ALTER TABLE `errores_aplicacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ea_fk_usuario` (`usuario_id`);

--
-- Indices de la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo` (`codigo`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `rol_permiso`
--
ALTER TABLE `rol_permiso`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `rol_permiso_unique` (`rol_id`,`permiso_id`),
  ADD KEY `rp_fk_permiso` (`permiso_id`);

--
-- Indices de la tabla `sesiones_usuario`
--
ALTER TABLE `sesiones_usuario`
  ADD PRIMARY KEY (`id`),
  ADD KEY `su_fk_usuario` (`usuario_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `cedula` (`cedula`);

--
-- Indices de la tabla `usuario_dashboard_vis`
--
ALTER TABLE `usuario_dashboard_vis`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_user_modulo` (`usuario_id`,`modulo_key`);

--
-- Indices de la tabla `usuario_permiso`
--
ALTER TABLE `usuario_permiso`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario_permiso_unique` (`usuario_id`,`permiso_id`),
  ADD KEY `up_fk_permiso` (`permiso_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `actividad_usuario`
--
ALTER TABLE `actividad_usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=99;

--
-- AUTO_INCREMENT de la tabla `cambios_por_modulo`
--
ALTER TABLE `cambios_por_modulo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `dashboard_visibilidad`
--
ALTER TABLE `dashboard_visibilidad`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT de la tabla `errores_aplicacion`
--
ALTER TABLE `errores_aplicacion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `permisos`
--
ALTER TABLE `permisos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `rol_permiso`
--
ALTER TABLE `rol_permiso`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=270;

--
-- AUTO_INCREMENT de la tabla `sesiones_usuario`
--
ALTER TABLE `sesiones_usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `usuario_dashboard_vis`
--
ALTER TABLE `usuario_dashboard_vis`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario_permiso`
--
ALTER TABLE `usuario_permiso`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `actividad_usuario`
--
ALTER TABLE `actividad_usuario`
  ADD CONSTRAINT `au_fk_sesion` FOREIGN KEY (`sesion_id`) REFERENCES `sesiones_usuario` (`id`),
  ADD CONSTRAINT `au_fk_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `cambios_por_modulo`
--
ALTER TABLE `cambios_por_modulo`
  ADD CONSTRAINT `cm_fk_actividad` FOREIGN KEY (`actividad_id`) REFERENCES `actividad_usuario` (`id`);

--
-- Filtros para la tabla `errores_aplicacion`
--
ALTER TABLE `errores_aplicacion`
  ADD CONSTRAINT `ea_fk_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `rol_permiso`
--
ALTER TABLE `rol_permiso`
  ADD CONSTRAINT `rp_fk_permiso` FOREIGN KEY (`permiso_id`) REFERENCES `permisos` (`id`),
  ADD CONSTRAINT `rp_fk_rol` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`);

--
-- Filtros para la tabla `sesiones_usuario`
--
ALTER TABLE `sesiones_usuario`
  ADD CONSTRAINT `su_fk_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `usuario_permiso`
--
ALTER TABLE `usuario_permiso`
  ADD CONSTRAINT `up_fk_permiso` FOREIGN KEY (`permiso_id`) REFERENCES `permisos` (`id`),
  ADD CONSTRAINT `up_fk_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
