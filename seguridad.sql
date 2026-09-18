-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 18-09-2026 a las 15:50:08
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
-- Base de datos: `seguridad`
--
CREATE DATABASE IF NOT EXISTS `seguridad` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `seguridad`;

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
(1, NULL, 4, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-07-10 10:25:27'),
(2, NULL, 5, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario gene@admin.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-07-10 10:25:51'),
(3, NULL, 6, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario naryi@admin.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-07-10 10:26:03'),
(4, NULL, 3, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario admin@admin.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-07-10 10:26:05'),
(5, NULL, 5, 'update', 'usuario', 'Editar usuario', '{\"d\": \"Usuario \\\"Genesis Acosta\\\" actualizado\"}', '/usuarios/', '127.0.0.1', '2026-07-10 10:27:54'),
(6, NULL, 5, 'update', 'usuario', 'Editar usuario', '{\"d\": \"Usuario \\\"Naryibeth Alejos\\\" actualizado\"}', '/usuarios/', '127.0.0.1', '2026-07-10 10:28:10'),
(7, NULL, 5, 'update', 'usuario', 'Editar usuario', '{\"d\": \"Usuario \\\"Yolianna Angulo\\\" actualizado\"}', '/usuarios/', '127.0.0.1', '2026-07-10 10:28:27'),
(8, NULL, 4, 'update', 'usuario', 'Editar usuario', '{\"d\": \"Usuario \\\"Maria Alvarez\\\" actualizado\"}', '/usuarios/', '127.0.0.1', '2026-07-10 10:28:40'),
(9, NULL, 5, 'update', 'usuario', 'Editar usuario', '{\"d\": \"Usuario \\\"Keiver Zamudia\\\" actualizado\"}', '/usuarios/', '127.0.0.1', '2026-07-10 10:29:32'),
(10, NULL, 3, 'create', 'usuario', 'Registrar usuario', '{\"d\": \"Usuario \\\"Edgardo Torrealba\\\" registrado\"}', '/usuarios/', '127.0.0.1', '2026-07-10 10:30:53'),
(11, NULL, 24, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario maria@admin.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-07-10 10:31:04'),
(12, NULL, 24, 'create', 'premio', 'Registrar premio', '{\"d\": \"Premio \\\"caja de malta polar\\\" registrado\"}', '/premio/', '127.0.0.1', '2026-07-10 10:33:18'),
(13, NULL, 3, 'update', 'tareas', 'Asignar tarea', '{\"d\": \"Tarea \\\"Revisar iluminación del campo\\\" asignada a usuario #25\"}', '/gestion-tarea/', '127.0.0.1', '2026-07-10 10:33:45'),
(14, NULL, 3, 'update', 'tareas', 'Asignar tarea', '{\"d\": \"Tarea \\\"Entregar kits de premios\\\" asignada a usuario #25\"}', '/gestion-tarea/', '127.0.0.1', '2026-07-10 10:33:55'),
(15, NULL, 24, 'create', 'premio', 'Registrar premio', '{\"d\": \"Premio \\\"Gorra de cardenales\\\" registrado\"}', '/premio/', '127.0.0.1', '2026-07-10 10:37:26'),
(16, NULL, 5, 'create', 'premio', 'Registrar premio', '{\"d\": \"Premio \\\"Cafe 500mg\\\" registrado\"}', '/premio/', '127.0.0.1', '2026-07-10 10:38:03'),
(17, NULL, 5, 'create', 'premio', 'Registrar premio', '{\"d\": \"Premio \\\"Bolsa de comida Mary\\\" registrado\"}', '/premio/', '127.0.0.1', '2026-07-10 10:42:07'),
(18, NULL, 24, 'update', 'premio', 'Editar premio', '{\"d\": \"Premio \\\"Cafe 500mg\\\" actualizado\"}', '/premio/', '127.0.0.1', '2026-07-10 10:42:50'),
(19, NULL, 5, 'create', 'patrocinador', 'Registrar patrocinador', '{\"d\": \"Patrocinador \\\"aaaaaaaa\\\" registrado\"}', '/patrocinador/', '127.0.0.1', '2026-07-10 10:48:21'),
(20, NULL, 5, 'update', 'patrocinador', 'Editar patrocinador', '{\"d\": \"Patrocinador \\\"aaaaaaaa\\\" actualizado\"}', '/patrocinador/', '127.0.0.1', '2026-07-10 10:49:53'),
(21, NULL, 6, 'update', 'patrocinador', 'Editar patrocinador', '{\"d\": \"Patrocinador \\\"donitas Edg\\\" actualizado\"}', '/patrocinador/', '127.0.0.1', '2026-07-10 10:50:13'),
(22, NULL, 4, 'update', 'patrocinador', 'Editar patrocinador', '{\"d\": \"Patrocinador \\\"Tubrica C.A\\\" actualizado\"}', '/patrocinador/', '127.0.0.1', '2026-07-10 10:50:57'),
(23, NULL, 3, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario admin@admin.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-07-10 10:52:09'),
(24, NULL, 5, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario gene@admin.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-07-10 10:52:11'),
(25, NULL, 6, 'create', 'patrocinador', 'Registrar patrocinador', '{\"d\": \"Patrocinador \\\"jean center\\\" registrado\"}', '/patrocinador/', '127.0.0.1', '2026-07-10 10:52:18'),
(26, NULL, 3, 'logout', 'auth', 'Cierre de sesión', '{\"d\": \"Usuario admin@admin.com cerró sesión\"}', '/auth/logout', '127.0.0.1', '2026-07-10 10:52:52'),
(27, NULL, 25, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario edgardo@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-07-10 10:53:02'),
(28, NULL, 4, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-07-10 16:13:53'),
(29, NULL, 4, 'create', 'usuario', 'Registrar usuario', '{\"d\": \"Usuario \\\"dsffddfgdfgffgfggggggggggggggggggggggghhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh\\\" registrado\"}', '/usuarios/', '127.0.0.1', '2026-07-10 16:20:29'),
(30, NULL, 4, 'update', 'envivo', 'Iniciar guion en vivo', '{\"d\": \"Guión \\\"Cardenales vs Leones - 2026-07-10\\\" iniciado en vivo\"}', '/en-vivo/iniciar/1', '127.0.0.1', '2026-07-10 16:29:15'),
(31, NULL, 4, 'update', 'envivo', 'Finalizar guion en vivo', '{\"d\": \"Guión \\\"Cardenales vs Leones - 2026-07-10\\\" finalizado\"}', '/en-vivo/finalizar/1', '127.0.0.1', '2026-07-10 16:29:29'),
(32, NULL, 4, 'create', 'guion', 'Crear guion', '{\"d\": \"Guion \\\"juego - 2026-07-10\\\" creado\"}', '/guiones/crear', '127.0.0.1', '2026-07-10 16:30:20'),
(33, NULL, 4, 'create', 'guion', 'Agregar elemento', '{\"d\": \"Elemento pregame agregado a guion \\\"juego - 2026-07-10\\\"\"}', '/guiones/agregar-elemento/6', '127.0.0.1', '2026-07-10 16:32:43'),
(34, NULL, 4, 'create', 'guion', 'Agregar elemento', '{\"d\": \"Elemento game agregado a guion \\\"juego - 2026-07-10\\\"\"}', '/guiones/agregar-elemento/6', '127.0.0.1', '2026-07-10 16:33:24'),
(35, NULL, 4, 'create', 'guion', 'Agregar elemento', '{\"d\": \"Elemento pregame agregado a guion \\\"juego - 2026-07-10\\\"\"}', '/guiones/agregar-elemento/6', '127.0.0.1', '2026-07-10 16:33:42'),
(36, NULL, 4, 'update', 'guion', 'Publicar guión', '{\"d\": \"Guión \\\"juego - 2026-07-10\\\" publicado\"}', '/guiones/publicar/6', '127.0.0.1', '2026-07-10 16:34:05'),
(37, NULL, 4, 'update', 'envivo', 'Iniciar guion en vivo', '{\"d\": \"Guión \\\"Cardenales vs Leones - 2026-07-10\\\" iniciado en vivo\"}', '/en-vivo/iniciar/1', '127.0.0.1', '2026-07-10 16:40:03'),
(38, NULL, 4, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-07-10 17:38:45'),
(39, NULL, 4, 'create', 'guion', 'Replicar guión', '{\"d\": \"Guión \\\"juego - 2026-07-10\\\" replicado a 1 fecha(s)\"}', '/guiones/replicar/6', '127.0.0.1', '2026-07-10 17:39:12'),
(40, NULL, 4, 'create', 'mantenimiento', 'Ingresar a mantenimiento', '{\"d\": \"Recurso \\\"Sony PXW-Z150\\\" ingresado a mantenimiento\"}', '/mantenimiento/ingresar/1', '127.0.0.1', '2026-07-10 17:44:46'),
(41, NULL, 4, 'update', 'mantenimiento', 'Reparar recurso', '{\"d\": \"Mantenimiento de \\\"Sony PXW-Z150\\\": Se inició el proceso de reparación.\"}', '/mantenimiento/reparar/1', '127.0.0.1', '2026-07-10 17:45:38'),
(42, NULL, 4, 'update', 'inventario', 'Asignar recurso', '{\"d\": \"Recurso \\\"iPad Pro 12.9\\\"\\\" asignado a usuario #4\"}', '/inventario/asignar/10', '127.0.0.1', '2026-07-10 17:47:12'),
(43, NULL, 4, 'update', 'mantenimiento', 'Reparar recurso', '{\"d\": \"Mantenimiento de \\\"Sony PXW-Z150\\\": Recurso reparado exitosamente.\"}', '/mantenimiento/reparar/1', '127.0.0.1', '2026-07-10 17:47:42'),
(44, NULL, 4, 'update', 'mantenimiento', 'Finalizar mantenimiento', '{\"d\": \"Mantenimiento de \\\"Sony PXW-Z150\\\" finalizado\"}', '/mantenimiento/finalizar/1', '127.0.0.1', '2026-07-10 17:47:52'),
(45, NULL, 4, 'create', 'mantenimiento', 'Ingresar a mantenimiento', '{\"d\": \"Recurso \\\"Sony PXW-Z150\\\" ingresado a mantenimiento\"}', '/mantenimiento/ingresar/1', '127.0.0.1', '2026-07-10 17:48:32'),
(46, NULL, 4, 'update', 'tareas', 'Asignar tarea', '{\"d\": \"Tarea \\\"Coordinar llegada de patrocinadores\\\" asignada a usuario #5\"}', '/gestion-tarea/', '127.0.0.1', '2026-07-10 18:03:56'),
(47, NULL, 4, 'logout', 'auth', 'Cierre de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com cerró sesión\"}', '/auth/logout', '127.0.0.1', '2026-07-10 18:07:56'),
(48, NULL, 4, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-07-25 14:00:00'),
(49, NULL, 4, 'logout', 'auth', 'Cierre de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com cerró sesión\"}', '/auth/logout', '127.0.0.1', '2026-07-25 14:00:11'),
(50, NULL, 4, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-07-25 14:10:26'),
(51, NULL, 4, 'logout', 'auth', 'Cierre de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com cerró sesión\"}', '/auth/logout', '127.0.0.1', '2026-07-25 14:10:34'),
(52, NULL, 4, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-07-25 14:14:16'),
(53, NULL, 4, 'logout', 'auth', 'Cierre de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com cerró sesión\"}', '/auth/logout', '127.0.0.1', '2026-07-25 14:14:23'),
(54, NULL, 4, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-07-25 14:15:31'),
(55, NULL, 4, 'delete', 'usuario', 'Eliminar usuario', '{\"d\": \"Usuario \\\"dsffddfgdfgffgfggggggggggggggggggggggghhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh\\\" eliminado\"}', '/usuarios/', '127.0.0.1', '2026-07-25 14:16:21'),
(56, NULL, 4, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-07-25 15:02:33'),
(57, NULL, 4, 'update', 'envivo', 'Finalizar guion en vivo', '{\"d\": \"Guión \\\"Cardenales vs Leones - 2026-07-10\\\" finalizado\"}', '/en-vivo/finalizar/1', '127.0.0.1', '2026-07-25 15:58:18'),
(58, NULL, 4, 'logout', 'auth', 'Cierre de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com cerró sesión\"}', '/auth/logout', '127.0.0.1', '2026-07-27 17:51:13'),
(59, NULL, 4, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-07-27 17:52:19'),
(60, NULL, 4, 'logout', 'auth', 'Cierre de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com cerró sesión\"}', '/auth/logout', '127.0.0.1', '2026-08-23 12:31:28'),
(61, NULL, 4, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-08-23 12:32:47'),
(62, NULL, 4, 'update', 'envivo', 'Iniciar guion en vivo', '{\"d\": \"Guión \\\"juego - 2026-07-10\\\" iniciado en vivo\"}', '/en-vivo/iniciar/6', '127.0.0.1', '2026-08-23 14:04:23'),
(63, NULL, 4, 'create', 'guion', 'Agregar elemento', '{\"d\": \"Elemento game agregado a guion \\\"juego 3 - 2026-07-10\\\"\"}', '/guiones/agregar-elemento/7', '127.0.0.1', '2026-08-23 15:50:04'),
(64, NULL, 4, 'update', 'guion', 'Publicar guión', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\" publicado\"}', '/guiones/publicar/7', '127.0.0.1', '2026-08-23 15:50:13'),
(65, NULL, 4, 'update', 'envivo', 'Finalizar guion en vivo', '{\"d\": \"Guión \\\"juego - 2026-07-10\\\" finalizado\"}', '/en-vivo/finalizar/6', '127.0.0.1', '2026-08-23 15:50:18'),
(66, NULL, 4, 'update', 'envivo', 'Iniciar guion en vivo', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\" iniciado en vivo\"}', '/en-vivo/iniciar/7', '127.0.0.1', '2026-08-23 15:50:20'),
(67, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 0 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:07:17'),
(68, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 0 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:07:20'),
(69, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 0 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:07:26'),
(70, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 0 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:07:31'),
(71, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 0 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:07:34'),
(72, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 0 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:07:37'),
(73, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 0 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:07:47'),
(74, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 0 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:07:54'),
(75, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 0 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:07:59'),
(76, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 0 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:08:01'),
(77, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 0 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:08:04'),
(78, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 0 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:08:07'),
(79, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 0 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:18:37'),
(80, NULL, 4, 'update', 'envivo', 'Finalizar guion en vivo', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\" finalizado\"}', '/en-vivo/finalizar/7', '127.0.0.1', '2026-08-23 16:18:49'),
(81, NULL, 4, 'update', 'envivo', 'Iniciar guion en vivo', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\" iniciado en vivo\"}', '/en-vivo/iniciar/7', '127.0.0.1', '2026-08-23 16:18:50'),
(82, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:18:54'),
(83, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 2 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:18:57'),
(84, NULL, 3, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario admin@admin.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-08-23 16:19:31'),
(85, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:19:54'),
(86, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:21:06'),
(87, NULL, 3, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:21:35'),
(88, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 2 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:22:07'),
(89, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 2 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:22:09'),
(90, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 2 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:22:10'),
(91, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:54:12'),
(92, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 2 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:54:14'),
(93, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:54:50'),
(94, NULL, 3, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 2 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:54:56'),
(95, NULL, 3, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 16:57:56'),
(96, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 17:25:12'),
(97, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 2 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 17:25:16'),
(98, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 2 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 17:25:20'),
(99, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 17:25:28'),
(100, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 17:25:45'),
(101, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 17:25:48'),
(102, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 17:26:00'),
(103, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 17:26:07'),
(104, NULL, 4, 'update', 'envivo', 'Finalizar guion en vivo', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\" finalizado\"}', '/en-vivo/finalizar/7', '127.0.0.1', '2026-08-23 18:35:50'),
(105, NULL, 4, 'update', 'envivo', 'Iniciar guion en vivo', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\" iniciado en vivo\"}', '/en-vivo/iniciar/7', '127.0.0.1', '2026-08-23 18:35:53'),
(106, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 18:35:54'),
(107, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 2 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 18:35:58'),
(108, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 18:35:59'),
(109, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 18:36:00'),
(110, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 18:36:02'),
(111, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 18:36:03'),
(112, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 18:36:08'),
(113, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 18:36:09'),
(114, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 18:53:26'),
(115, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-23 18:53:32'),
(116, NULL, 4, 'update', 'envivo', 'Finalizar guion en vivo', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\" finalizado\"}', '/en-vivo/finalizar/7', '127.0.0.1', '2026-08-23 18:53:38'),
(117, NULL, 4, 'update', 'tareas', 'Asignar tarea', '{\"d\": \"Tarea \\\"Coordinar llegada de patrocinadores\\\" asignada a 2 usuario(s); 1 ya la tenían\"}', '/gestion-tarea/', '127.0.0.1', '2026-08-23 20:56:59'),
(118, NULL, 4, 'update', 'tareas', 'Completar tarea', '{\"d\": \"Tarea \\\"Coordinar llegada de patrocinadores\\\" completada\"}', '/gestion-tarea/completar', '127.0.0.1', '2026-08-23 20:57:11'),
(119, NULL, 4, 'update', 'tareas', 'Completar tarea', '{\"d\": \"Tarea \\\"Preparar contenido Jumbotron\\\" completada\"}', '/gestion-tarea/completar', '127.0.0.1', '2026-08-23 22:52:21'),
(120, NULL, 4, 'update', 'tareas', 'Asignar tarea', '{\"d\": \"Tarea \\\"Calibrar sonido del estadio\\\" asignada a 1 usuario(s)\"}', '/gestion-tarea/', '127.0.0.1', '2026-08-23 23:11:06'),
(121, NULL, 4, 'update', 'tareas', 'Completar tarea', '{\"d\": \"Tarea \\\"Calibrar sonido del estadio\\\" completada\"}', '/gestion-tarea/completar', '127.0.0.1', '2026-08-23 23:11:14'),
(122, NULL, 4, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-08-25 19:34:19'),
(123, NULL, 4, 'update', 'envivo', 'Iniciar guion en vivo', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\" iniciado en vivo\"}', '/en-vivo/iniciar/7', '127.0.0.1', '2026-08-25 19:34:30'),
(124, NULL, 4, 'update', 'envivo', 'Sincronizar elementos', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\": 1 elemento(s) sincronizado(s)\"}', '/en-vivo/api/sincronizar/7', '127.0.0.1', '2026-08-25 19:34:36'),
(125, NULL, 4, 'logout', 'auth', 'Cierre de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com cerró sesión\"}', '/auth/logout', '127.0.0.1', '2026-08-25 20:47:20'),
(126, NULL, 4, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-08-25 20:52:21'),
(127, NULL, 4, 'update', 'usuario', 'Editar usuario', '{\"d\": \"Usuario \\\"Yolianna Angulo\\\" actualizado\"}', '/usuarios/', '127.0.0.1', '2026-08-25 21:41:20'),
(128, NULL, 4, 'logout', 'auth', 'Cierre de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com cerró sesión\"}', '/auth/logout', '127.0.0.1', '2026-08-25 21:41:34'),
(129, NULL, 18, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario yolianna14@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-08-25 21:41:51'),
(130, NULL, 3, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario admin@admin.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-08-25 21:42:47'),
(131, NULL, 18, 'logout', 'auth', 'Cierre de sesión', '{\"d\": \"Usuario yolianna14@gmail.com cerró sesión\"}', '/auth/logout', '127.0.0.1', '2026-08-26 00:21:10'),
(132, NULL, 4, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-08-26 00:21:29'),
(133, NULL, 4, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-09-02 20:27:44'),
(134, NULL, 4, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-09-04 19:50:30'),
(135, NULL, 4, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-09-17 21:10:00'),
(136, NULL, 4, 'create', 'rol', 'Respaldar BD', '{\"d\": \"Respaldo completo de estadio_db solicitado\"}', '/roles/respaldo', '127.0.0.1', '2026-09-17 22:17:41'),
(137, NULL, 4, 'create', 'guion', 'Crear guion', '{\"d\": \"Guion \\\"prueba - 2026-09-18\\\" creado\"}', '/guiones/crear', '127.0.0.1', '2026-09-18 06:12:12'),
(138, NULL, 4, 'create', 'guion', 'Crear guion', '{\"d\": \"Guion \\\"prueba - 2026-09-18\\\" creado\"}', '/guiones/crear', '127.0.0.1', '2026-09-18 06:12:16'),
(139, NULL, 4, 'update', 'envivo', 'Finalizar guion en vivo', '{\"d\": \"Guión \\\"juego 3 - 2026-07-10\\\" finalizado\"}', '/en-vivo/finalizar/7', '127.0.0.1', '2026-09-18 06:26:48'),
(140, NULL, 4, 'create', 'reels', 'Crear reel', '{\"d\": \"Reel \\\"Reels pruebas\\\" creado\"}', '/reels/crear', '127.0.0.1', '2026-09-18 06:40:13'),
(141, NULL, 4, 'create', 'rol', 'Respaldar BD', '{\"d\": \"Respaldo completo de estadio_db solicitado\"}', '/roles/respaldo', '127.0.0.1', '2026-09-18 09:03:22'),
(142, NULL, 4, 'create', 'reels', 'Crear reel', '{\"d\": \"Reel \\\"Reels 12\\\" creado\"}', '/reels/crear', '127.0.0.1', '2026-09-18 09:27:59'),
(143, NULL, 4, 'logout', 'auth', 'Cierre de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com cerró sesión\"}', '/auth/logout', '127.0.0.1', '2026-09-18 09:46:07'),
(144, NULL, 4, 'login', 'auth', 'Inicio de sesión', '{\"d\": \"Usuario keiberzamudia14@gmail.com inició sesión\"}', '/auth/login', '127.0.0.1', '2026-09-18 09:47:31');

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
(45, 1, 'guion', 1),
(46, 1, 'mantenimiento', 1),
(47, 1, 'premio', 1),
(48, 1, 'contrato', 1),
(49, 1, 'balance', 1),
(50, 1, 'tarea', 1),
(51, 1, 'patrocinador', 1),
(52, 1, 'usuario', 1),
(53, 1, 'actividad', 1),
(54, 1, 'enlinea', 1),
(65, 3, 'guion', 1),
(66, 3, 'mantenimiento', 0),
(67, 3, 'premio', 0),
(68, 3, 'contrato', 0),
(69, 3, 'balance', 0),
(70, 3, 'tarea', 1),
(71, 3, 'patrocinador', 0),
(72, 3, 'usuario', 0),
(73, 3, 'actividad', 0),
(74, 3, 'enlinea', 0);

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
-- Estructura de tabla para la tabla `notificaciones`
--

CREATE TABLE `notificaciones` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `tipo` varchar(40) NOT NULL DEFAULT 'tarea_asignada',
  `titulo` varchar(120) NOT NULL,
  `mensaje` varchar(255) NOT NULL,
  `url` varchar(200) DEFAULT NULL,
  `leida` tinyint(1) DEFAULT 0,
  `fecha_creacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `notificaciones`
--

INSERT INTO `notificaciones` (`id`, `usuario_id`, `tipo`, `titulo`, `mensaje`, `url`, `leida`, `fecha_creacion`) VALUES
(3, 4, 'tarea_asignada', 'Nueva tarea asignada', '\"Tarea de prueba\" te fue asignada por Usuario Prueba', '/gestion-tarea/mis-tareas', 1, '2026-08-23 20:01:15'),
(4, 6, 'tarea_asignada', 'Nueva tarea asignada', '\"Tarea de prueba\" te fue asignada por Usuario Prueba', '/gestion-tarea/mis-tareas', 0, '2026-08-23 20:01:15'),
(5, 18, 'tarea_asignada', 'Nueva tarea asignada', '\"Tarea de prueba\" te fue asignada por Usuario Prueba', '/gestion-tarea/mis-tareas', 0, '2026-08-23 20:01:15'),
(6, 24, 'tarea_asignada', 'Nueva tarea asignada', '\"Tarea de prueba\" te fue asignada por Usuario Prueba', '/gestion-tarea/mis-tareas', 0, '2026-08-23 20:01:15'),
(7, 25, 'tarea_asignada', 'Nueva tarea asignada', '\"Tarea de prueba\" te fue asignada por Usuario Prueba', '/gestion-tarea/mis-tareas', 0, '2026-08-23 20:01:15'),
(13, 4, 'tarea_asignada', 'Nueva tarea asignada', '\"Tarea de prueba\" te fue asignada por Usuario Prueba', '/gestion-tarea/mis-tareas', 1, '2026-08-23 20:01:15'),
(14, 6, 'tarea_asignada', 'Nueva tarea asignada', '\"Tarea de prueba\" te fue asignada por Usuario Prueba', '/gestion-tarea/mis-tareas', 0, '2026-08-23 20:01:15'),
(15, 18, 'tarea_asignada', 'Nueva tarea asignada', '\"Tarea de prueba\" te fue asignada por Usuario Prueba', '/gestion-tarea/mis-tareas', 0, '2026-08-23 20:01:15'),
(16, 24, 'tarea_asignada', 'Nueva tarea asignada', '\"Tarea de prueba\" te fue asignada por Usuario Prueba', '/gestion-tarea/mis-tareas', 0, '2026-08-23 20:01:15'),
(17, 25, 'tarea_asignada', 'Nueva tarea asignada', '\"Tarea de prueba\" te fue asignada por Usuario Prueba', '/gestion-tarea/mis-tareas', 0, '2026-08-23 20:01:15'),
(29, 4, 'tarea_asignada', 'Nueva tarea asignada', '\"Coordinar llegada de patrocinadores\" te fue asignada por Keiver Zamudia', '/gestion-tarea/mis-tareas', 1, '2026-08-23 20:56:59'),
(30, 25, 'tarea_asignada', 'Nueva tarea asignada', '\"Coordinar llegada de patrocinadores\" te fue asignada por Keiver Zamudia', '/gestion-tarea/mis-tareas', 0, '2026-08-23 20:56:59'),
(31, 3, 'tarea_completada', 'Tarea completada', 'Keiver Zamudia completó \"Coordinar llegada de patrocinadores\"', '/gestion-tarea/seguimiento', 0, '2026-08-23 20:57:11'),
(32, 4, 'tarea_asignada', 'Nueva tarea asignada', '\"Calibrar sonido del estadio\" te fue asignada por Keiver Zamudia', '/gestion-tarea/mis-tareas', 1, '2026-08-23 23:11:06'),
(33, 3, 'tarea_completada', 'Tarea completada', 'Keiver Zamudia completó \"Calibrar sonido del estadio\"', '/gestion-tarea/seguimiento', 0, '2026-08-23 23:11:14');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `password_reset_tokens`
--

CREATE TABLE `password_reset_tokens` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `token` varchar(64) NOT NULL,
  `expires_at` datetime NOT NULL,
  `used` tinyint(1) DEFAULT 0,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `password_reset_tokens`
--

INSERT INTO `password_reset_tokens` (`id`, `usuario_id`, `token`, `expires_at`, `used`, `created_at`) VALUES
(1, 4, 'f161a7b8e9e038f6b75e11b53e888a62379e33912484989b7134dd465c819fed', '2026-07-26 13:06:38', 0, '2026-07-25 13:06:38'),
(2, 4, '5288343296741976d9e2d3d73a507683f783783a9fb402a7d5882a1bfc7a7694', '2026-07-26 13:11:47', 0, '2026-07-25 13:11:47'),
(3, 4, 'dcbbc818e6b0f24cce83cec9af3fd5f535f4e220c0b3cf24b5ca5fef76acceee', '2026-07-26 14:13:20', 1, '2026-07-25 14:13:20');

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
(26, 'Ver tareas', 'gestion_tarea.view', 'Tareas', ''),
(27, 'Crear tareas', 'gestion_tarea.create', 'Tareas', ''),
(28, 'Editar tareas', 'gestion_tarea.edit', 'Tareas', ''),
(29, 'Eliminar tareas', 'gestion_tarea.delete', 'Tareas', ''),
(30, 'Completar tareas propias', 'gestion_tarea.complete', 'Tareas', ''),
(31, 'Ver patrocinadores', 'patrocinador.view', 'Patrocinadores', ''),
(32, 'Crear patrocinadores', 'patrocinador.create', 'Patrocinadores', ''),
(33, 'Editar patrocinadores', 'patrocinador.edit', 'Patrocinadores', ''),
(34, 'Eliminar patrocinadores', 'patrocinador.delete', 'Patrocinadores', ''),
(35, 'Ver contratos', 'contrato.view', 'Contratos', ''),
(36, 'Crear contratos', 'contrato.create', 'Contratos', ''),
(37, 'Editar contratos', 'contrato.edit', 'Contratos', ''),
(38, 'Eliminar contratos', 'contrato.delete', 'Contratos', ''),
(39, 'Ver balance', 'balance.view', 'Balance', ''),
(40, 'Registrar pagos', 'balance.create', 'Balance', ''),
(41, 'Editar pagos', 'balance.edit', 'Balance', ''),
(42, 'Eliminar pagos', 'balance.delete', 'Balance', ''),
(43, 'Ver inventario de recursos', 'inventario.view', 'Inventario', ''),
(44, 'Crear recursos', 'inventario.create', 'Inventario', ''),
(45, 'Editar recursos', 'inventario.edit', 'Inventario', ''),
(46, 'Eliminar recursos', 'inventario.delete', 'Inventario', ''),
(47, 'Asignar y devolver recursos', 'inventario.assign', 'Inventario', ''),
(48, 'Ver reels', 'reels.view', 'Reels', ''),
(49, 'Crear reels', 'reels.create', 'Reels', ''),
(50, 'Editar reels', 'reels.edit', 'Reels', ''),
(51, 'Eliminar reels', 'reels.delete', 'Reels', ''),
(52, 'Supervisar tareas de todos los usuarios', 'gestion_tarea.supervisar', 'Tareas', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reportes_generados`
--

CREATE TABLE `reportes_generados` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `modulo` varchar(50) NOT NULL,
  `tipo_reporte` varchar(100) NOT NULL,
  `filtros` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`filtros`)),
  `archivo_ruta` varchar(300) NOT NULL,
  `archivo_nombre` varchar(200) NOT NULL,
  `archivo_tamano` int(11) DEFAULT 0,
  `creado_en` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `reportes_generados`
--

INSERT INTO `reportes_generados` (`id`, `usuario_id`, `modulo`, `tipo_reporte`, `filtros`, `archivo_ruta`, `archivo_nombre`, `archivo_tamano`, `creado_en`) VALUES
(1, 4, 'contratos', 'REPORTE DE CONTRATOS', '{\"fecha_inicio\": \"2026-03-01\", \"fecha_fin\": \"2026-07-27\"}', '2026/07/contratos_20260727_181052.pdf', 'contratos_27-07-2026.pdf', 4527, '2026-07-27 18:10:52'),
(2, 4, 'contratos', 'REPORTE DE CONTRATOS', '{\"monto_max\": \"20000\", \"fecha_inicio\": \"2026-03-01\", \"fecha_fin\": \"2026-07-27\"}', '2026/07/contratos_20260727_182401.pdf', 'contratos_27-07-2026.pdf', 3259, '2026-07-27 18:24:01'),
(3, 4, 'guiones', 'REPORTE DE GUIONES', '{\"estado\": \"borrador\", \"fecha_inicio\": \"2026-07-08\", \"fecha_fin\": \"2026-08-23\"}', '2026/08/guiones_20260823_144834.pdf', 'guiones_23-08-2026.pdf', 4353, '2026-08-23 14:48:34'),
(4, 4, 'premios', 'REPORTE DE PREMIOS', '{\"fecha_inicio\": \"2026-07-10\", \"fecha_fin\": \"2026-08-23\"}', '2026/08/premios_20260823_152759.pdf', 'premios_23-08-2026.pdf', 3734, '2026-08-23 15:27:59'),
(5, 4, 'guiones_personalizado', 'REPORTE PERSONALIZADO', '{}', '2026/08/guiones_personalizado_20260826_002949.pdf', 'guiones_personalizado_26-08-2026.pdf', 2811, '2026-08-26 00:29:49'),
(6, 4, 'inventario', 'REPORTE DE INVENTARIO', '{\"fecha_inicio\": \"2024-11-10\", \"fecha_fin\": \"2026-09-04\"}', '2026/09/inventario_20260904_231657.pdf', 'inventario_04-09-2026.pdf', 8976, '2026-09-04 23:16:57'),
(7, 4, 'guiones', 'REPORTE DE GUIONES', '{\"fecha_inicio\": \"2026-07-08\", \"fecha_fin\": \"2026-09-04\"}', '2026/09/guiones_20260904_232341.pdf', 'guiones_04-09-2026.pdf', 5688, '2026-09-04 23:23:41'),
(8, 4, 'guiones_personalizado', 'REPORTE PERSONALIZADO', '{}', '2026/09/guiones_personalizado_20260917_221823.pdf', 'guiones_personalizado_17-09-2026.pdf', 2651, '2026-09-17 22:18:23'),
(9, 4, 'inventario_personalizado', 'REPORTE PERSONALIZADO', '{}', '2026/09/inventario_personalizado_20260918_085733.pdf', 'inventario_personalizado_18-09-2026.pdf', 2569, '2026-09-18 08:57:33');

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
(434, 1, 1),
(475, 1, 2),
(472, 1, 3),
(473, 1, 4),
(474, 1, 5),
(476, 1, 6),
(442, 1, 7),
(437, 1, 8),
(438, 1, 9),
(439, 1, 10),
(441, 1, 11),
(440, 1, 12),
(436, 1, 13),
(435, 1, 14),
(460, 1, 15),
(456, 1, 16),
(457, 1, 17),
(458, 1, 18),
(459, 1, 19),
(451, 1, 20),
(448, 1, 21),
(449, 1, 22),
(450, 1, 23),
(466, 1, 24),
(465, 1, 25),
(471, 1, 26),
(468, 1, 27),
(469, 1, 28),
(470, 1, 29),
(467, 1, 30),
(455, 1, 31),
(452, 1, 32),
(453, 1, 33),
(454, 1, 34),
(433, 1, 35),
(430, 1, 36),
(431, 1, 37),
(432, 1, 38),
(429, 1, 39),
(428, 1, 40),
(426, 1, 41),
(427, 1, 42),
(447, 1, 43),
(444, 1, 44),
(445, 1, 45),
(446, 1, 46),
(443, 1, 47),
(464, 1, 48),
(461, 1, 49),
(462, 1, 50),
(463, 1, 51),
(534, 1, 52),
(485, 2, 1),
(525, 2, 2),
(522, 2, 3),
(523, 2, 4),
(524, 2, 5),
(526, 2, 6),
(493, 2, 7),
(488, 2, 8),
(489, 2, 9),
(490, 2, 10),
(492, 2, 11),
(491, 2, 12),
(487, 2, 13),
(486, 2, 14),
(511, 2, 15),
(507, 2, 16),
(508, 2, 17),
(509, 2, 18),
(510, 2, 19),
(502, 2, 20),
(499, 2, 21),
(500, 2, 22),
(501, 2, 23),
(516, 2, 24),
(521, 2, 26),
(518, 2, 27),
(519, 2, 28),
(520, 2, 29),
(517, 2, 30),
(506, 2, 31),
(503, 2, 32),
(504, 2, 33),
(505, 2, 34),
(484, 2, 35),
(481, 2, 36),
(482, 2, 37),
(483, 2, 38),
(480, 2, 39),
(479, 2, 40),
(477, 2, 41),
(478, 2, 42),
(498, 2, 43),
(495, 2, 44),
(496, 2, 45),
(497, 2, 46),
(494, 2, 47),
(515, 2, 48),
(512, 2, 49),
(513, 2, 50),
(514, 2, 51),
(533, 2, 52),
(535, 3, 1),
(541, 3, 6),
(536, 3, 13),
(537, 3, 15),
(540, 3, 26),
(539, 3, 30),
(538, 3, 48);

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
(1, 4, '2026-07-10 10:25:27', '2026-07-10 20:13:53', '127.0.0.1', NULL, 35306),
(2, 5, '2026-07-10 10:25:51', '2026-07-10 14:52:11', '127.0.0.1', NULL, 15980),
(3, 6, '2026-07-10 10:26:03', NULL, '127.0.0.1', NULL, NULL),
(4, 3, '2026-07-10 10:26:05', '2026-07-10 14:52:09', '127.0.0.1', NULL, 15964),
(5, 24, '2026-07-10 10:31:04', NULL, '127.0.0.1', NULL, NULL),
(6, 3, '2026-07-10 10:52:09', '2026-07-10 14:52:52', '127.0.0.1', NULL, 14443),
(7, 5, '2026-07-10 10:52:11', NULL, '127.0.0.1', NULL, NULL),
(8, 25, '2026-07-10 10:53:02', NULL, '127.0.0.1', NULL, NULL),
(9, 4, '2026-07-10 16:13:53', '2026-07-10 21:38:45', '127.0.0.1', NULL, 19492),
(10, 4, '2026-07-10 17:38:45', '2026-07-10 22:07:56', '127.0.0.1', NULL, 16151),
(11, 4, '2026-07-25 14:00:00', '2026-07-25 18:00:11', '127.0.0.1', NULL, 14411),
(12, 4, '2026-07-25 14:10:26', '2026-07-25 18:10:34', '127.0.0.1', NULL, 14408),
(13, 4, '2026-07-25 14:14:16', '2026-07-25 18:14:23', '127.0.0.1', NULL, 14407),
(14, 4, '2026-07-25 14:15:31', '2026-07-25 19:02:32', '127.0.0.1', NULL, 17221),
(15, 4, '2026-07-25 15:02:33', '2026-07-27 21:51:13', '127.0.0.1', NULL, 197320),
(16, 4, '2026-07-27 17:52:19', '2026-08-23 16:32:47', '127.0.0.1', NULL, 2328028),
(17, 4, '2026-08-23 12:32:47', '2026-08-25 23:34:19', '127.0.0.1', NULL, 212492),
(18, 3, '2026-08-23 16:19:31', '2026-08-26 01:42:47', '127.0.0.1', NULL, 206596),
(19, 4, '2026-08-25 19:34:19', '2026-08-26 00:52:21', '127.0.0.1', NULL, 19082),
(20, 4, '2026-08-25 20:52:21', '2026-08-26 01:41:34', '127.0.0.1', NULL, 17353),
(21, 18, '2026-08-25 21:41:51', '2026-08-26 04:21:10', '127.0.0.1', NULL, 23959),
(22, 3, '2026-08-25 21:42:47', NULL, '127.0.0.1', NULL, NULL),
(23, 4, '2026-08-26 00:21:29', '2026-09-03 00:27:44', '127.0.0.1', NULL, 691575),
(24, 4, '2026-09-02 20:27:44', '2026-09-04 23:50:30', '127.0.0.1', NULL, 184966),
(25, 4, '2026-09-04 19:50:30', '2026-09-18 01:10:00', '127.0.0.1', NULL, 1142370),
(26, 4, '2026-09-17 21:10:00', '2026-09-18 13:47:31', '127.0.0.1', NULL, 59851),
(27, 4, '2026-09-18 09:47:31', NULL, '127.0.0.1', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sincronizaciones`
--

CREATE TABLE `sincronizaciones` (
  `id` int(11) NOT NULL,
  `guion_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(200) DEFAULT NULL,
  `fecha_sincronizacion` date NOT NULL,
  `hora_sincronizacion` time NOT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sincronizaciones`
--

INSERT INTO `sincronizaciones` (`id`, `guion_id`, `usuario_id`, `nombre`, `descripcion`, `fecha_sincronizacion`, `hora_sincronizacion`, `estado`, `created_at`) VALUES
(1, 1, 4, 'iniciar', 'Iniciado', '2026-07-10', '16:29:15', 'success', '2026-07-10 16:29:15'),
(2, 1, 4, 'finalizar', 'Finalizado', '2026-07-10', '16:29:29', 'success', '2026-07-10 16:29:29'),
(3, 1, 4, 'iniciar', 'Iniciado', '2026-07-10', '16:40:03', 'success', '2026-07-10 16:40:03'),
(4, 1, 4, 'finalizar', 'Finalizado', '2026-07-25', '15:58:18', 'success', '2026-07-25 15:58:18'),
(5, 6, 4, 'iniciar', 'Iniciado', '2026-08-23', '14:04:23', 'success', '2026-08-23 14:04:23'),
(6, 6, 4, 'finalizar', 'Finalizado', '2026-08-23', '15:50:18', 'success', '2026-08-23 15:50:18'),
(7, 7, 4, 'iniciar', 'Iniciado', '2026-08-23', '15:50:20', 'success', '2026-08-23 15:50:20'),
(8, 7, 4, 'finalizar', 'Finalizado', '2026-08-23', '16:18:49', 'success', '2026-08-23 16:18:49'),
(9, 7, 4, 'iniciar', 'Iniciado', '2026-08-23', '16:18:50', 'success', '2026-08-23 16:18:50'),
(10, 7, 4, 'sincronizar', '4:32 PM - eece completado', '2026-08-23', '16:18:54', 'success', '2026-08-23 16:18:54'),
(11, 7, 4, 'sincronizar', '4:32 PM - eece reiniciado', '2026-08-23', '16:18:57', 'success', '2026-08-23 16:18:57'),
(12, 7, 4, 'sincronizar', '4:36 PM - eber reiniciado', '2026-08-23', '16:18:57', 'success', '2026-08-23 16:18:57'),
(13, 7, 4, 'sincronizar', '4:32 PM - eece completado', '2026-08-23', '16:19:54', 'success', '2026-08-23 16:19:54'),
(14, 7, 4, 'sincronizar', '4:36 PM - eber completado', '2026-08-23', '16:21:06', 'success', '2026-08-23 16:21:06'),
(15, 7, 3, 'sincronizar', '1ro° Baja - rvvvev completado', '2026-08-23', '16:21:35', 'success', '2026-08-23 16:21:35'),
(16, 7, 4, 'sincronizar', '1ro° Baja - rvvvev reiniciado', '2026-08-23', '16:22:07', 'success', '2026-08-23 16:22:07'),
(17, 7, 4, 'sincronizar', '3ro° Baja - prueba reiniciado', '2026-08-23', '16:22:07', 'success', '2026-08-23 16:22:07'),
(18, 7, 4, 'sincronizar', '4:36 PM - eber reiniciado', '2026-08-23', '16:22:09', 'success', '2026-08-23 16:22:09'),
(19, 7, 4, 'sincronizar', '1ro° Baja - rvvvev reiniciado', '2026-08-23', '16:22:09', 'success', '2026-08-23 16:22:09'),
(20, 7, 4, 'sincronizar', '4:32 PM - eece reiniciado', '2026-08-23', '16:22:10', 'success', '2026-08-23 16:22:10'),
(21, 7, 4, 'sincronizar', '4:36 PM - eber reiniciado', '2026-08-23', '16:22:10', 'success', '2026-08-23 16:22:10'),
(22, 7, 4, 'sincronizar', '4:32 PM - eece completado', '2026-08-23', '16:54:12', 'success', '2026-08-23 16:54:12'),
(23, 7, 4, 'sincronizar', '4:36 PM - eber reiniciado', '2026-08-23', '16:54:14', 'success', '2026-08-23 16:54:14'),
(24, 7, 4, 'sincronizar', '4:32 PM - eece reiniciado', '2026-08-23', '16:54:14', 'success', '2026-08-23 16:54:14'),
(25, 7, 4, 'sincronizar', '4:32 PM - eece completado', '2026-08-23', '16:54:50', 'success', '2026-08-23 16:54:50'),
(26, 7, 3, 'sincronizar', '4:36 PM - eber reiniciado', '2026-08-23', '16:54:56', 'success', '2026-08-23 16:54:56'),
(27, 7, 3, 'sincronizar', '4:32 PM - eece reiniciado', '2026-08-23', '16:54:56', 'success', '2026-08-23 16:54:56'),
(28, 7, 3, 'sincronizar', '4:32 PM - eece completado', '2026-08-23', '16:57:56', 'success', '2026-08-23 16:57:56'),
(29, 7, 4, 'sincronizar', '4:36 PM - eber completado', '2026-08-23', '17:25:12', 'success', '2026-08-23 17:25:12'),
(30, 7, 4, 'sincronizar', '4:36 PM - eber reiniciado', '2026-08-23', '17:25:16', 'success', '2026-08-23 17:25:16'),
(31, 7, 4, 'sincronizar', '1ro° Baja - rvvvev reiniciado', '2026-08-23', '17:25:16', 'success', '2026-08-23 17:25:16'),
(32, 7, 4, 'sincronizar', '4:32 PM - eece reiniciado', '2026-08-23', '17:25:20', 'success', '2026-08-23 17:25:20'),
(33, 7, 4, 'sincronizar', '4:36 PM - eber reiniciado', '2026-08-23', '17:25:20', 'success', '2026-08-23 17:25:20'),
(34, 7, 4, 'sincronizar', '4:32 PM - eece reiniciado', '2026-08-23', '17:25:28', 'success', '2026-08-23 17:25:28'),
(35, 7, 4, 'sincronizar', '4:32 PM - eece reiniciado', '2026-08-23', '17:25:45', 'success', '2026-08-23 17:25:45'),
(36, 7, 4, 'sincronizar', '4:32 PM - eece reiniciado', '2026-08-23', '17:25:48', 'success', '2026-08-23 17:25:48'),
(37, 7, 4, 'sincronizar', '4:32 PM - eece reiniciado', '2026-08-23', '17:26:00', 'success', '2026-08-23 17:26:00'),
(38, 7, 4, 'sincronizar', '4:32 PM - eece reiniciado', '2026-08-23', '17:26:07', 'success', '2026-08-23 17:26:07'),
(39, 7, 4, 'finalizar', 'Finalizado', '2026-08-23', '18:35:50', 'success', '2026-08-23 18:35:50'),
(40, 7, 4, 'iniciar', 'Iniciado', '2026-08-23', '18:35:53', 'success', '2026-08-23 18:35:53'),
(41, 7, 4, 'sincronizar', '4:32 PM - eece completado', '2026-08-23', '18:35:54', 'success', '2026-08-23 18:35:54'),
(42, 7, 4, 'sincronizar', '4:32 PM - eece reiniciado', '2026-08-23', '18:35:58', 'success', '2026-08-23 18:35:58'),
(43, 7, 4, 'sincronizar', '4:36 PM - eber reiniciado', '2026-08-23', '18:35:58', 'success', '2026-08-23 18:35:58'),
(44, 7, 4, 'sincronizar', '4:32 PM - eece reiniciado', '2026-08-23', '18:35:59', 'success', '2026-08-23 18:35:59'),
(45, 7, 4, 'sincronizar', '4:32 PM - eece reiniciado', '2026-08-23', '18:36:00', 'success', '2026-08-23 18:36:00'),
(46, 7, 4, 'sincronizar', '4:32 PM - eece reiniciado', '2026-08-23', '18:36:02', 'success', '2026-08-23 18:36:02'),
(47, 7, 4, 'sincronizar', '4:32 PM - eece reiniciado', '2026-08-23', '18:36:03', 'success', '2026-08-23 18:36:03'),
(48, 7, 4, 'sincronizar', '4:32 PM - eece completado', '2026-08-23', '18:36:08', 'success', '2026-08-23 18:36:08'),
(49, 7, 4, 'sincronizar', '4:36 PM - eber completado', '2026-08-23', '18:36:09', 'success', '2026-08-23 18:36:09'),
(50, 7, 4, 'sincronizar', '1ro° Baja - rvvvev completado', '2026-08-23', '18:53:26', 'success', '2026-08-23 18:53:26'),
(51, 7, 4, 'sincronizar', '3ro° Baja - prueba completado', '2026-08-23', '18:53:32', 'success', '2026-08-23 18:53:32'),
(52, 7, 4, 'finalizar', 'Finalizado', '2026-08-23', '18:53:38', 'success', '2026-08-23 18:53:38'),
(53, 7, 4, 'iniciar', 'Iniciado', '2026-08-25', '19:34:30', 'success', '2026-08-25 19:34:30'),
(54, 7, 4, 'sincronizar', '4:32 PM - eece completado', '2026-08-25', '19:34:36', 'success', '2026-08-25 19:34:36'),
(55, 7, 4, 'finalizar', 'Finalizado', '2026-09-18', '06:26:48', 'success', '2026-09-18 06:26:48');

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
(3, 'Admin', 'admin@admin.com', 'scrypt:32768:8:1$VImiJ1cWMig3OJN6$66e6543200f85e636bf90eb21b174b6d22ceea892b52ecb277a9d878b41447879ad382b1e29418e473d6df392a991d827e214a96d411f0b3ae71f3ec7642dc11', '12345678', 'Superadmin', 'Palco de Operaciones', '0422345981', 1, '2026-05-05 21:34:59', '2026-08-25 21:42:47'),
(4, 'Keiver Zamudia', 'keiberzamudia14@gmail.com', 'scrypt:32768:8:1$RsrejHhJyqXdwCfX$1d2caad090fc6ed90fd4034480a7f60ddb4f15dd34630ea1bbba0d8f9c13bf2ec4fca908a89dd2d20f831065eb717f3b432af4f350b8a5a2be98aae9cc43f72f', '25469224', 'Superadmin', 'Medios', '0412344590', 1, '2026-05-05 23:44:26', '2026-09-18 09:47:31'),
(5, 'Genesis Acosta', 'gene@admin.com', 'scrypt:32768:8:1$coTXZEDqTjuXvG0Q$4b3453edd3c49f45f11e728ffa2565b9b34d8b52d7ab2b25fb2a8c8a626c3b7a8210c3b85da9362f95f5a0ccd86338bb6920bf1b7351cea6c4dd39184019ce22', '26357326', 'Administrador', 'Palco de Operaciones', '04243455566', 1, '2026-05-05 23:49:50', '2026-07-10 10:52:11'),
(6, 'Naryibeth Alejos', 'naryi@admin.com', 'scrypt:32768:8:1$msjmk9hpl7gJNoQR$548780bb655c20abc0f30e5957b3168cb67fdd9c34c8d7999c1c9b07e0ea5de9e559caf6b101b35d8308e04dcec589bfc0b8112f047ca66b96f9e7c6f9b193b2', '14598999', 'Administrador', 'Medios', '04123455564', 1, '2026-05-06 19:58:32', '2026-07-10 10:26:03'),
(18, 'Yolianna Angulo', 'yolianna14@gmail.com', 'scrypt:32768:8:1$a41DiLn8n1zp6yGS$eef3be026d19e67487bdf33b9bb0bfe846820ce8218cd3452cef3a6c194cb0a227a2c859a7a28c4435023d81cb58b3a2f2d3e2ad129a72930131b5c782d35c16', '25894881', 'Usuario', 'Medios', '+5802512661166', 1, '2026-05-31 18:02:46', '2026-08-25 21:41:51'),
(24, 'Maria Alvarez', 'maria@admin.com', 'scrypt:32768:8:1$JwKu9i5KXzJhB0YR$36d209fbd8c9d500e4536163f86ccc815d637dff1bd28802ee0ed9778ecefbaa851fdf2856a7f02d460833ba6d36de616746f951ab6fed559475ca285a244733', '26480334', 'Superadmin', 'Medios', '6776367376', 1, '2026-06-27 10:13:29', '2026-07-10 10:31:04'),
(25, 'Edgardo Torrealba', 'edgardo@gmail.com', 'scrypt:32768:8:1$HnXLXUQez7zbRY7y$14575362f7cd5a380fc0aec62d8922591aba8298908b580c34701d87a3e612e6444ff650c3ec78c639bd12fbd0e287eb9fd1441765b2e10bde3fb80d0da2761f', '31388643', 'Superadmin', 'Medios', '04129656958', 1, '2026-07-10 10:30:53', '2026-07-10 10:53:02');

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

--
-- Volcado de datos para la tabla `usuario_dashboard_vis`
--

INSERT INTO `usuario_dashboard_vis` (`id`, `usuario_id`, `modulo_key`, `visible`) VALUES
(1, 4, 'guion', 0),
(2, 4, 'mantenimiento', 0),
(3, 4, 'premio', 0),
(4, 4, 'contrato', 0),
(5, 4, 'balance', 0),
(6, 4, 'tarea', 0),
(7, 4, 'patrocinador', 0),
(8, 4, 'usuario', 0),
(9, 4, 'actividad', 1),
(10, 4, 'enlinea', 1);

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
-- Volcado de datos para la tabla `usuario_permiso`
--

INSERT INTO `usuario_permiso` (`id`, `usuario_id`, `permiso_id`, `fecha_asignacion`) VALUES
(1, 4, 25, '2026-06-03 12:31:56'),
(2, 4, 26, '2026-06-03 12:31:56'),
(3, 4, 27, '2026-06-03 12:31:56'),
(4, 4, 28, '2026-06-03 12:31:56'),
(5, 4, 29, '2026-06-03 12:31:56'),
(6, 4, 30, '2026-06-03 12:31:56'),
(7, 4, 31, '2026-06-03 12:31:56'),
(8, 4, 32, '2026-06-03 12:31:56'),
(9, 4, 33, '2026-06-03 12:31:56'),
(10, 4, 34, '2026-06-03 12:31:56'),
(11, 4, 35, '2026-06-03 12:31:56'),
(12, 4, 36, '2026-06-03 12:31:56'),
(13, 4, 37, '2026-06-03 12:31:56'),
(14, 4, 38, '2026-06-03 12:31:56'),
(15, 4, 39, '2026-06-03 12:31:56'),
(16, 4, 40, '2026-06-03 12:31:56'),
(17, 4, 41, '2026-06-03 12:31:56'),
(18, 4, 42, '2026-06-03 12:31:56'),
(19, 4, 43, '2026-06-03 12:31:56'),
(20, 4, 44, '2026-06-03 12:31:56'),
(21, 4, 45, '2026-06-03 12:31:56'),
(22, 4, 46, '2026-06-03 12:31:56'),
(23, 4, 47, '2026-06-03 12:31:56'),
(24, 4, 48, '2026-06-03 12:31:56'),
(25, 4, 49, '2026-06-03 12:31:56'),
(26, 4, 50, '2026-06-03 12:31:57'),
(27, 4, 51, '2026-06-03 12:31:57');

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
-- Indices de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_usuario_leida` (`usuario_id`,`leida`);

--
-- Indices de la tabla `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token` (`token`),
  ADD KEY `prt_fk_usuario` (`usuario_id`);

--
-- Indices de la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo` (`codigo`);

--
-- Indices de la tabla `reportes_generados`
--
ALTER TABLE `reportes_generados`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_usuario` (`usuario_id`),
  ADD KEY `idx_modulo` (`modulo`),
  ADD KEY `idx_creado` (`creado_en`);

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
-- Indices de la tabla `sincronizaciones`
--
ALTER TABLE `sincronizaciones`
  ADD PRIMARY KEY (`id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=145;

--
-- AUTO_INCREMENT de la tabla `cambios_por_modulo`
--
ALTER TABLE `cambios_por_modulo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `dashboard_visibilidad`
--
ALTER TABLE `dashboard_visibilidad`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=75;

--
-- AUTO_INCREMENT de la tabla `errores_aplicacion`
--
ALTER TABLE `errores_aplicacion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT de la tabla `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `permisos`
--
ALTER TABLE `permisos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT de la tabla `reportes_generados`
--
ALTER TABLE `reportes_generados`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `rol_permiso`
--
ALTER TABLE `rol_permiso`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=542;

--
-- AUTO_INCREMENT de la tabla `sesiones_usuario`
--
ALTER TABLE `sesiones_usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `sincronizaciones`
--
ALTER TABLE `sincronizaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `usuario_dashboard_vis`
--
ALTER TABLE `usuario_dashboard_vis`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `usuario_permiso`
--
ALTER TABLE `usuario_permiso`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

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
-- Filtros para la tabla `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD CONSTRAINT `prt_fk_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

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
