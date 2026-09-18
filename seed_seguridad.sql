-- ============================================================
-- SEED DATA: seguridad — Usuarios, roles y auditoría
-- Estadio Antonio Herrera Gutiérrez — Datos realistas
-- ============================================================

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- -----------------------------------------------------------
-- 1. ROLES
-- -----------------------------------------------------------
INSERT INTO `roles` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Superadmin',      'Acceso total al sistema'),
(2, 'Administrador',   'Acceso administrativo excepto roles'),
(3, 'Usuario',         'Acceso básico de lectura');

-- -----------------------------------------------------------
-- 2. PERMISOS (52 permisos del sistema)
-- -----------------------------------------------------------
INSERT INTO `permisos` (`id`, `nombre`, `codigo`, `modulo`, `descripcion`) VALUES
(1,  'Ver panel principal',                    'dashboard.view',           'Dashboard',   NULL),
(2,  'Ver lista de usuarios',                  'usuario.view',             'Usuarios',    NULL),
(3,  'Crear usuarios',                         'usuario.create',           'Usuarios',    NULL),
(4,  'Editar usuarios',                        'usuario.edit',             'Usuarios',    NULL),
(5,  'Eliminar usuarios',                      'usuario.delete',           'Usuarios',    NULL),
(6,  'Ver perfil propio',                      'usuario.perfil',           'Usuarios',    NULL),
(7,  'Ver guiones',                            'guion.view',               'Guión',       NULL),
(8,  'Crear guiones',                          'guion.create',             'Guión',       NULL),
(9,  'Editar guiones',                         'guion.edit',               'Guión',       NULL),
(10, 'Eliminar guiones',                       'guion.delete',             'Guión',       NULL),
(11, 'Publicar guiones',                       'guion.publish',            'Guión',       NULL),
(12, 'Previsualizar guiones',                  'guion.preview',            'Guión',       NULL),
(13, 'Ver pantalla en vivo',                   'envivo.view',              'En Vivo',     NULL),
(14, 'Controlar elementos en vivo',            'envivo.control',           'En Vivo',     NULL),
(15, 'Ver premios',                            'premio.view',              'Premios',     NULL),
(16, 'Crear premios',                          'premio.create',            'Premios',     NULL),
(17, 'Editar premios',                         'premio.edit',              'Premios',     NULL),
(18, 'Eliminar premios',                       'premio.delete',            'Premios',     NULL),
(19, 'Entregar premios',                       'premio.entregar',          'Premios',     NULL),
(20, 'Ver mantenimiento',                      'mantenimiento.view',       'Mantenimiento',NULL),
(21, 'Crear recursos',                         'mantenimiento.create',     'Mantenimiento',NULL),
(22, 'Editar recursos',                        'mantenimiento.edit',       'Mantenimiento',NULL),
(23, 'Eliminar recursos',                      'mantenimiento.delete',     'Mantenimiento',NULL),
(24, 'Ver roles y permisos',                   'rol.view',                 'Roles',       NULL),
(25, 'Editar permisos de usuarios',            'rol.edit',                 'Roles',       NULL),
(26, 'Ver tareas',                             'gestion_tarea.view',       'Tareas',      ''),
(27, 'Crear tareas',                           'gestion_tarea.create',     'Tareas',      ''),
(28, 'Editar tareas',                          'gestion_tarea.edit',       'Tareas',      ''),
(29, 'Eliminar tareas',                        'gestion_tarea.delete',     'Tareas',      ''),
(30, 'Completar tareas propias',               'gestion_tarea.complete',   'Tareas',      ''),
(31, 'Ver patrocinadores',                     'patrocinador.view',        'Patrocinadores',''),
(32, 'Crear patrocinadores',                   'patrocinador.create',      'Patrocinadores',''),
(33, 'Editar patrocinadores',                  'patrocinador.edit',        'Patrocinadores',''),
(34, 'Eliminar patrocinadores',                'patrocinador.delete',      'Patrocinadores',''),
(35, 'Ver contratos',                          'contrato.view',            'Contratos',   ''),
(36, 'Crear contratos',                        'contrato.create',          'Contratos',   ''),
(37, 'Editar contratos',                       'contrato.edit',            'Contratos',   ''),
(38, 'Eliminar contratos',                     'contrato.delete',          'Contratos',   ''),
(39, 'Ver balance',                            'balance.view',             'Balance',     ''),
(40, 'Registrar pagos',                        'balance.create',           'Balance',     ''),
(41, 'Editar pagos',                           'balance.edit',             'Balance',     ''),
(42, 'Eliminar pagos',                         'balance.delete',           'Balance',     ''),
(43, 'Ver inventario de recursos',             'inventario.view',          'Inventario',  ''),
(44, 'Crear recursos (inventario)',            'inventario.create',        'Inventario',  ''),
(45, 'Editar recursos (inventario)',           'inventario.edit',          'Inventario',  ''),
(46, 'Eliminar recursos (inventario)',         'inventario.delete',        'Inventario',  ''),
(47, 'Asignar y devolver recursos',            'inventario.assign',        'Inventario',  ''),
(48, 'Ver reels',                              'reels.view',               'Reels',       ''),
(49, 'Crear reels',                            'reels.create',             'Reels',       ''),
(50, 'Editar reels',                           'reels.edit',               'Reels',       ''),
(51, 'Eliminar reels',                         'reels.delete',             'Reels',       ''),
(52, 'Supervisar tareas de todos los usuarios','gestion_tarea.supervisar', 'Tareas',      '');

-- -----------------------------------------------------------
-- 3. ROL_PERMISO — Superadmin (rol 1): todos los permisos
-- -----------------------------------------------------------
DELETE FROM `rol_permiso`;

-- Superadmin: permisos 1-52
INSERT INTO `rol_permiso` (`id`, `rol_id`, `permiso_id`)
SELECT (@row_num := @row_num + 1) AS id, 1, permiso_id
FROM (
  SELECT 1 AS permiso_id UNION ALL SELECT 2  UNION ALL SELECT 3  UNION ALL SELECT 4  UNION ALL SELECT 5
  UNION ALL SELECT 6  UNION ALL SELECT 7  UNION ALL SELECT 8  UNION ALL SELECT 9  UNION ALL SELECT 10
  UNION ALL SELECT 11 UNION ALL SELECT 12 UNION ALL SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15
  UNION ALL SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL SELECT 19 UNION ALL SELECT 20
  UNION ALL SELECT 21 UNION ALL SELECT 22 UNION ALL SELECT 23 UNION ALL SELECT 24 UNION ALL SELECT 25
  UNION ALL SELECT 26 UNION ALL SELECT 27 UNION ALL SELECT 28 UNION ALL SELECT 29 UNION ALL SELECT 30
  UNION ALL SELECT 31 UNION ALL SELECT 32 UNION ALL SELECT 33 UNION ALL SELECT 34 UNION ALL SELECT 35
  UNION ALL SELECT 36 UNION ALL SELECT 37 UNION ALL SELECT 38 UNION ALL SELECT 39 UNION ALL SELECT 40
  UNION ALL SELECT 41 UNION ALL SELECT 42 UNION ALL SELECT 43 UNION ALL SELECT 44 UNION ALL SELECT 45
  UNION ALL SELECT 46 UNION ALL SELECT 47 UNION ALL SELECT 48 UNION ALL SELECT 49 UNION ALL SELECT 50
  UNION ALL SELECT 51 UNION ALL SELECT 52
) AS permisos
CROSS JOIN (SELECT @row_num := 0) AS init;

-- Administrador (rol 2): todo excepto rol.edit (25) y respaldo
INSERT INTO `rol_permiso` (`id`, `rol_id`, `permiso_id`)
SELECT (@row_num2 := @row_num2 + 1) + 52, 2, permiso_id
FROM (
  SELECT 1 AS permiso_id UNION ALL SELECT 2  UNION ALL SELECT 3  UNION ALL SELECT 4  UNION ALL SELECT 5
  UNION ALL SELECT 6  UNION ALL SELECT 7  UNION ALL SELECT 8  UNION ALL SELECT 9  UNION ALL SELECT 10
  UNION ALL SELECT 11 UNION ALL SELECT 12 UNION ALL SELECT 13 UNION ALL SELECT 14 UNION ALL SELECT 15
  UNION ALL SELECT 16 UNION ALL SELECT 17 UNION ALL SELECT 18 UNION ALL SELECT 19 UNION ALL SELECT 20
  UNION ALL SELECT 21 UNION ALL SELECT 22 UNION ALL SELECT 23 UNION ALL SELECT 24
  UNION ALL SELECT 26 UNION ALL SELECT 27 UNION ALL SELECT 28 UNION ALL SELECT 29 UNION ALL SELECT 30
  UNION ALL SELECT 31 UNION ALL SELECT 32 UNION ALL SELECT 33 UNION ALL SELECT 34 UNION ALL SELECT 35
  UNION ALL SELECT 36 UNION ALL SELECT 37 UNION ALL SELECT 38 UNION ALL SELECT 39 UNION ALL SELECT 40
  UNION ALL SELECT 41 UNION ALL SELECT 42 UNION ALL SELECT 43 UNION ALL SELECT 44 UNION ALL SELECT 45
  UNION ALL SELECT 46 UNION ALL SELECT 47 UNION ALL SELECT 48 UNION ALL SELECT 49 UNION ALL SELECT 50
  UNION ALL SELECT 51 UNION ALL SELECT 52
) AS permisos
CROSS JOIN (SELECT @row_num2 := 0) AS init;

-- Usuario (rol 3): solo lectura + tareas propias + reels
INSERT INTO `rol_permiso` (`id`, `rol_id`, `permiso_id`)
SELECT (@row_num3 := @row_num3 + 1) + 104, 3, permiso_id
FROM (
  SELECT 1  AS permiso_id UNION ALL SELECT 6  UNION ALL SELECT 7  UNION ALL SELECT 13
  UNION ALL SELECT 15 UNION ALL SELECT 26 UNION ALL SELECT 30 UNION ALL SELECT 48
) AS permisos
CROSS JOIN (SELECT @row_num3 := 0) AS init;

-- -----------------------------------------------------------
-- 4. USUARIOS — Contraseñas: "password123" hasheadas con scrypt
--    (mismas que tenían antes, conservadas para compatibilidad)
-- -----------------------------------------------------------
INSERT INTO `usuarios` (`id`, `nombre`, `email`, `password_hash`, `cedula`, `rol`, `departamento`, `telefono`, `activo`, `fecha_registro`, `ultimo_acceso`) VALUES
(1, 'Carlos Mendoza',    'carlos@mendoza.com',    'scrypt:32768:8:1$mDfRImpoWDtKGfhj$68fbff3ab8a29cad13e30f4356bace2eba29f42e98e612d2cbfaca58a60a5762e5e8ba6ae52778b3af83aaec93df20ab96b2f6752e0934aff4b9544c392dd2a9', '20123456', 'Superadmin',      'Palco de Operaciones', '0424-1234567', 1, '2026-01-05 08:00:00', '2026-07-10 18:00:00'),
(2, 'Ana Sofía Pérez',   'ana.perez@outlook.com', 'scrypt:32768:8:1$mDfRImpoWDtKGfhj$68fbff3ab8a29cad13e30f4356bace2eba29f42e98e612d2cbfaca58a60a5762e5e8ba6ae52778b3af83aaec93df20ab96b2f6752e0934aff4b9544c392dd2a9', '25489012', 'Administrador',   'Palco de Operaciones', '0412-3456789', 1, '2026-01-05 08:10:00', '2026-07-10 17:30:00'),
(3, 'Keiver Zamudia',    'keiver@cardenales.com',  'scrypt:32768:8:1$mDfRImpoWDtKGfhj$68fbff3ab8a29cad13e30f4356bace2eba29f42e98e612d2cbfaca58a60a5762e5e8ba6ae52778b3af83aaec93df20ab96b2f6752e0934aff4b9544c392dd2a9', '25469224', 'Superadmin',      'Medios',                '0412-3445901', 1, '2026-01-05 08:20:00', '2026-07-10 18:15:00'),
(4, 'Genesis Acosta',    'genesis@cardenales.com', 'scrypt:32768:8:1$mDfRImpoWDtKGfhj$68fbff3ab8a29cad13e30f4356bace2eba29f42e98e612d2cbfaca58a60a5762e5e8ba6ae52778b3af83aaec93df20ab96b2f6752e0934aff4b9544c392dd2a9', '26357326', 'Administrador',   'Palco de Operaciones', '0424-3455566', 1, '2026-01-05 08:30:00', '2026-07-10 16:45:00'),
(5, 'María González',    'maria.gonzalez@gmail.com','scrypt:32768:8:1$mDfRImpoWDtKGfhj$68fbff3ab8a29cad13e30f4356bace2eba29f42e98e612d2cbfaca58a60a5762e5e8ba6ae52778b3af83aaec93df20ab96b2f6752e0934aff4b9544c392dd2a9', '24789012', 'Usuario',         'Medios',                '0412-9876543', 1, '2026-01-10 09:00:00', '2026-07-10 14:00:00'),
(6, 'Roberto Díaz',      'roberto.diaz@hotmail.com','scrypt:32768:8:1$mDfRImpoWDtKGfhj$68fbff3ab8a29cad13e30f4356bace2eba29f42e98e612d2cbfaca58a60a5762e5e8ba6ae52778b3af83aaec93df20ab96b2f6752e0934aff4b9544c392dd2a9', '14598999', 'Usuario',         'Operaciones',          '0412-3455564', 1, '2026-01-10 09:10:00', '2026-07-10 15:30:00');

-- -----------------------------------------------------------
-- 5. USUARIO_PERMISO — Permisos directos por usuario
--    (Solo permisos extras fuera de rol, o los mismos del rol)
-- -----------------------------------------------------------
DELETE FROM `usuario_permiso`;

-- Carlos (Superadmin): permisos directos (ya tiene todo por rol)
-- Keiver (Superadmin): permisos directos (ya tiene todo por rol)
-- Genesis (Administrador): permisos directos extra
INSERT INTO `usuario_permiso` (`id`, `usuario_id`, `permiso_id`, `fecha_asignacion`) VALUES
(1,  3, 14, '2026-01-05 08:20:00'),
(2,  3, 25, '2026-01-05 08:20:00'),
(3,  3, 52, '2026-01-05 08:20:00'),
(4,  4, 14, '2026-01-05 08:30:00'),
(5,  4, 19, '2026-01-05 08:30:00'),
(6,  4, 27, '2026-01-05 08:30:00');

-- -----------------------------------------------------------
-- 6. DASHBOARD VISIBILIDAD
-- -----------------------------------------------------------
DELETE FROM `dashboard_visibilidad`;

-- Superadmin (rol 1): todo visible
INSERT INTO `dashboard_visibilidad` (`id`, `rol_id`, `modulo_key`, `visible`) VALUES
(1,  1, 'guion', 1), (2,  1, 'mantenimiento', 1), (3,  1, 'premio', 1),
(4,  1, 'contrato', 1), (5,  1, 'balance', 1), (6,  1, 'tarea', 1),
(7,  1, 'patrocinador', 1), (8,  1, 'usuario', 1), (9,  1, 'actividad', 1),
(10, 1, 'enlinea', 1);

-- Administrador (rol 2): lo mismo
INSERT INTO `dashboard_visibilidad` (`id`, `rol_id`, `modulo_key`, `visible`) VALUES
(11, 2, 'guion', 1), (12, 2, 'mantenimiento', 1), (13, 2, 'premio', 1),
(14, 2, 'contrato', 1), (15, 2, 'balance', 1), (16, 2, 'tarea', 1),
(17, 2, 'patrocinador', 1), (18, 2, 'usuario', 1);

-- Usuario (rol 3): solo guion, tarea, reels
INSERT INTO `dashboard_visibilidad` (`id`, `rol_id`, `modulo_key`, `visible`) VALUES
(19, 3, 'guion', 1), (20, 3, 'tarea', 1);

-- -----------------------------------------------------------
-- 7. USUARIO DASHBOARD VIS
-- -----------------------------------------------------------
DELETE FROM `usuario_dashboard_vis`;

-- Carlos: ve todo
INSERT INTO `usuario_dashboard_vis` (`id`, `usuario_id`, `modulo_key`, `visible`) VALUES
(1,  1, 'guion', 1), (2,  1, 'mantenimiento', 1), (3,  1, 'premio', 1),
(4,  1, 'contrato', 1), (5,  1, 'balance', 1), (6,  1, 'tarea', 1),
(7,  1, 'patrocinador', 1), (8,  1, 'usuario', 1);

-- Keiver: ve todo
INSERT INTO `usuario_dashboard_vis` (`id`, `usuario_id`, `modulo_key`, `visible`) VALUES
(9,  3, 'guion', 1), (10, 3, 'mantenimiento', 1), (11, 3, 'premio', 1),
(12, 3, 'contrato', 1), (13, 3, 'balance', 1), (14, 3, 'tarea', 1),
(15, 3, 'patrocinador', 1), (16, 3, 'usuario', 1);

-- -----------------------------------------------------------
-- 8. ACTIVIDAD USUARIO — Registros de ejemplo recientes
-- -----------------------------------------------------------
DELETE FROM `actividad_usuario`;

INSERT INTO `actividad_usuario` (`id`, `sesion_id`, `usuario_id`, `tipo_accion`, `modulo`, `accion`, `detalle`, `pagina`, `ip_address`, `created_at`) VALUES
(1,  NULL, 3, 'login',  'auth',   'Inicio de sesión',          '{"d": "Usuario keiver@cardenales.com inicio sesion"}',      '/auth/login',        '192.168.1.100', '2026-07-10 08:00:00'),
(2,  NULL, 3, 'create', 'guion',  'Crear guion',               '{"d": "Guion Cardenales vs Leones - 2026-07-10 creado"}', '/guiones/crear',     '192.168.1.100', '2026-07-01 09:00:00'),
(3,  NULL, 3, 'update', 'envivo', 'Iniciar guion en vivo',     '{"d": "Guion Cardenales vs Leones - 2026-07-10 iniciado en vivo"}', '/en-vivo/iniciar/1', '192.168.1.100', '2026-07-10 18:00:00'),
(4,  NULL, 3, 'update', 'envivo', 'Sincronizar elementos',     '{"d": "Guion Cardenales vs Leones - 2026-07-10: 16 elemento(s) sincronizado(s)"}', '/en-vivo/api/sincronizar/1', '192.168.1.100', '2026-07-10 18:05:00'),
(5,  NULL, 3, 'update', 'envivo', 'Finalizar guion en vivo',   '{"d": "Guion Cardenales vs Leones - 2026-07-10 finalizado"}', '/en-vivo/finalizar/1', '192.168.1.100', '2026-07-10 21:00:00'),
(6,  NULL, 4, 'create', 'patrocinador', 'Registrar patrocinador','{"d": "Patrocinador Maltin Polar registrado"}',         '/patrocinador/',     '192.168.1.101', '2026-01-15 10:00:00'),
(7,  NULL, 4, 'create', 'reels',  'Crear reel',                '{"d": "Reel Maltin Polar - Edicion Verano creado"}',      '/reels/crear',       '192.168.1.101', '2026-06-01 10:00:00'),
(8,  NULL, 2, 'create', 'usuario','Registrar usuario',         '{"d": "Usuario Keiver Zamudia registrado"}',              '/usuarios/',         '192.168.1.102', '2026-01-05 08:20:00'),
(9,  NULL, 2, 'update', 'tareas', 'Asignar tarea',             '{"d": "Tarea Verificar equipo de transmision asignada a Keiver Zamudia"}', '/gestion-tarea/', '192.168.1.102', '2026-07-01 14:00:00'),
(10, NULL, 3, 'update', 'tareas', 'Completar tarea',           '{"d": "Tarea Verificar equipo de transmision completada"}', '/gestion-tarea/completar', '192.168.1.100', '2026-07-10 16:00:00'),
(11, NULL, 2, 'create', 'balance','Pago registrado',            '{"d": "Pago de $21250 registrado para Maltin Polar"}',      '/balance/pagos',     '192.168.1.102', '2026-01-15 10:05:00'),
(12, NULL, 2, 'create', 'balance','Pago registrado',            '{"d": "Pago de $30000 registrado para Banesco"}',           '/balance/pagos',     '192.168.1.102', '2026-02-10 09:35:00'),
(13, NULL, 4, 'create', 'mantenimiento','Ingresar a mantenimiento','{"d": "Recurso Sony PXW-Z150 ingresado a mantenimiento"}', '/mantenimiento/ingresar/1', '192.168.1.101', '2026-07-10 17:44:46'),
(14, NULL, 4, 'update', 'mantenimiento','Reparar recurso',       '{"d": "Mantenimiento de Sony PXW-Z150: Reparado exitosamente"}', '/mantenimiento/reparar/1', '192.168.1.101', '2026-07-10 17:47:42'),
(15, NULL, 4, 'update', 'inventario','Asignar recurso',         '{"d": "Recurso iPad Pro 12.9 asignado a Genesis Acosta"}', '/inventario/asignar/10', '192.168.1.101', '2026-07-01 08:00:00');

-- -----------------------------------------------------------
-- 9. NOTIFICACIONES — De ejemplo
-- -----------------------------------------------------------
DELETE FROM `notificaciones`;

INSERT INTO `notificaciones` (`id`, `usuario_id`, `tipo`, `titulo`, `mensaje`, `url`, `leida`, `fecha_creacion`) VALUES
(1, 3, 'tarea_asignada',  'Nueva tarea asignada',     '"Verificar equipo de transmisión" te fue asignada por Carlos Mendoza', '/gestion-tarea/mis-tareas', 1, '2026-07-01 14:00:00'),
(2, 4, 'tarea_asignada',  'Nueva tarea asignada',     '"Preparar contenido Jumbotron" te fue asignada por Carlos Mendoza',  '/gestion-tarea/mis-tareas', 0, '2026-07-01 15:00:00'),
(3, 3, 'tarea_completada','Tarea completada',         'Keiver Zamudia completó "Verificar equipo de transmisión"',          '/gestion-tarea/seguimiento',0, '2026-07-10 16:00:00'),
(4, 2, 'tarea_asignada',  'Nueva tarea asignada',     '"Calibrar sonido del estadio" te fue asignada por Carlos Mendoza',   '/gestion-tarea/mis-tareas', 0, '2026-07-01 14:30:00');

-- -----------------------------------------------------------
-- 10. SESIONES USUARIO
-- -----------------------------------------------------------
DELETE FROM `sesiones_usuario`;

INSERT INTO `sesiones_usuario` (`id`, `usuario_id`, `inicio_sesion`, `fin_sesion`, `ip_address`, `user_agent`, `duracion_segundos`) VALUES
(1, 3, '2026-07-10 08:00:00', '2026-07-10 21:30:00', '192.168.1.100', NULL, 48600),
(2, 4, '2026-07-10 08:10:00', '2026-07-10 18:00:00', '192.168.1.101', NULL, 35400),
(3, 2, '2026-07-10 08:20:00', '2026-07-10 17:00:00', '192.168.1.102', NULL, 32400),
(4, 5, '2026-07-10 09:00:00', '2026-07-10 15:00:00', '192.168.1.103', NULL, 21600),
(5, 6, '2026-07-10 09:10:00', '2026-07-10 16:00:00', '192.168.1.104', NULL, 25200);

-- -----------------------------------------------------------
-- 11. SINCRONIZACIONES — De ejemplo
-- -----------------------------------------------------------
DELETE FROM `sincronizaciones`;

INSERT INTO `sincronizaciones` (`id`, `guion_id`, `usuario_id`, `nombre`, `descripcion`, `fecha_sincronizacion`, `hora_sincronizacion`, `estado`, `created_at`) VALUES
(1, 1, 3, 'iniciar',     'Iniciado',                                              '2026-07-10', '18:00:00', 'success', '2026-07-10 18:00:00'),
(2, 1, 3, 'sincronizar', '6:00 PM - Apertura de puertas completado',              '2026-07-10', '18:00:05', 'success', '2026-07-10 18:00:05'),
(3, 1, 3, 'sincronizar', '6:05 PM - Presentación de alineaciones completado',     '2026-07-10', '18:05:00', 'success', '2026-07-10 18:05:00'),
(4, 1, 3, 'sincronizar', '6:10 PM - Ceremonia de lanzamiento completado',         '2026-07-10', '18:10:00', 'success', '2026-07-10 18:10:00'),
(5, 1, 3, 'sincronizar', '6:15 PM - Himno Nacional completado',                   '2026-07-10', '18:15:00', 'success', '2026-07-10 18:15:00'),
(6, 1, 3, 'sincronizar', '1ro° Baja - Maltin Polar completado',                   '2026-07-10', '18:20:00', 'success', '2026-07-10 18:20:00'),
(7, 1, 3, 'sincronizar', '1ro° Alta - Pepsi completado',                          '2026-07-10', '18:20:30', 'success', '2026-07-10 18:20:30'),
(8, 1, 3, 'finalizar',   'Finalizado',                                            '2026-07-10', '21:00:00', 'success', '2026-07-10 21:00:00');

-- -----------------------------------------------------------
-- 12. REPORTES GENERADOS
-- -----------------------------------------------------------
DELETE FROM `reportes_generados`;

INSERT INTO `reportes_generados` (`id`, `usuario_id`, `modulo`, `tipo_reporte`, `filtros`, `archivo_ruta`, `archivo_nombre`, `archivo_tamano`, `creado_en`) VALUES
(1, 3, 'contratos',   'REPORTE DE CONTRATOS',   '{"fecha_inicio": "2026-01-01", "fecha_fin": "2026-07-10"}', '2026/07/contratos_20260710_180000.pdf', 'contratos_10-07-2026.pdf',  5200, '2026-07-10 18:00:00'),
(2, 3, 'guiones',     'REPORTE DE GUIONES',     '{"estado": "finalizado"}',                                    '2026/07/guiones_20260710_180000.pdf',   'guiones_10-07-2026.pdf',    3800, '2026-07-10 18:00:00'),
(3, 3, 'inventario',  'REPORTE DE INVENTARIO',  '{}',                                                         '2026/07/inventario_20260710_180000.pdf','inventario_10-07-2026.pdf',  6100, '2026-07-10 18:00:00');

-- -----------------------------------------------------------
-- 13. PASSWORD RESET TOKENS (vacío, sin tokens pendientes)
-- -----------------------------------------------------------
DELETE FROM `password_reset_tokens`;

-- -----------------------------------------------------------
-- 14. ERRORES APLICACIÓN (vacío)
-- -----------------------------------------------------------
DELETE FROM `errores_aplicacion`;

-- -----------------------------------------------------------
-- 15. CAMBIOS POR MÓDULO (vacío)
-- -----------------------------------------------------------
DELETE FROM `cambios_por_modulo`;

-- -----------------------------------------------------------
-- AUTO_INCREMENT resets
-- -----------------------------------------------------------
ALTER TABLE `actividad_usuario`      MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
ALTER TABLE `cambios_por_modulo`     MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `dashboard_visibilidad`  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
ALTER TABLE `errores_aplicacion`     MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `notificaciones`         MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
ALTER TABLE `password_reset_tokens`  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `permisos`               MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;
ALTER TABLE `reportes_generados`     MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
ALTER TABLE `roles`                  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
ALTER TABLE `rol_permiso`            MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=113;
ALTER TABLE `sesiones_usuario`       MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
ALTER TABLE `sincronizaciones`       MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
ALTER TABLE `usuarios`               MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
ALTER TABLE `usuario_dashboard_vis`  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
ALTER TABLE `usuario_permiso`        MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

-- -----------------------------------------------------------
-- Foreign Keys (ya existen en el esquema original)
-- -----------------------------------------------------------
-- Las foreign keys ya están creadas en seguridad.sql
-- No es necesario agregarlas de nuevo

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
