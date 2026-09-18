-- MariaDB dump 10.19  Distrib 10.4.28-MariaDB, for osx10.10 (x86_64)
--
-- Host: localhost    Database: estadio_db
-- ------------------------------------------------------
-- Server version	10.4.28-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `asignaciones_recursos`
--

DROP TABLE IF EXISTS `asignaciones_recursos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `asignaciones_recursos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `recurso_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `fecha_asignacion` datetime DEFAULT current_timestamp(),
  `fecha_devolucion_esperada` date DEFAULT NULL,
  `fecha_devolucion_real` datetime DEFAULT NULL,
  `estado_asignacion_id` int(11) DEFAULT 1,
  `notas` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_asignaciones_recurso` (`recurso_id`),
  KEY `idx_asignaciones_estado` (`estado_asignacion_id`),
  CONSTRAINT `fk_asignaciones_estado_asig` FOREIGN KEY (`estado_asignacion_id`) REFERENCES `estado_asignacion` (`id`),
  CONSTRAINT `fk_asignaciones_recurso` FOREIGN KEY (`recurso_id`) REFERENCES `recursos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asignaciones_recursos`
--

LOCK TABLES `asignaciones_recursos` WRITE;
/*!40000 ALTER TABLE `asignaciones_recursos` DISABLE KEYS */;
INSERT INTO `asignaciones_recursos` VALUES (1,10,4,'2026-07-10 17:47:12','2026-07-10',NULL,1,'ejhfe');
/*!40000 ALTER TABLE `asignaciones_recursos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contrato`
--

DROP TABLE IF EXISTS `contrato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contrato` (
  `id_contrato` int(11) NOT NULL AUTO_INCREMENT,
  `id_patrocinador` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `estado` varchar(100) NOT NULL,
  `estatus` varchar(100) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `monto_total` decimal(12,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`id_contrato`),
  KEY `id_patrocinador` (`id_patrocinador`),
  CONSTRAINT `contrato_ibfk_1` FOREIGN KEY (`id_patrocinador`) REFERENCES `patrocinadores` (`id_patrocinador`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contrato`
--

LOCK TABLES `contrato` WRITE;
/*!40000 ALTER TABLE `contrato` DISABLE KEYS */;
INSERT INTO `contrato` VALUES (1,1,'2026-04-01','2026-10-31','1','Vigente','2',85000.00),(2,2,'2026-05-01','2026-09-30','1','Vigente','2',62000.00),(3,3,'2026-06-01','2026-08-31','1','Vigente','1',25000.00),(4,4,'2026-04-15','2026-07-15','0','Vencido','1',30000.00),(5,5,'2026-03-01','2026-12-31','1','Vigente','3',120000.00),(6,6,'2026-06-01','2026-09-30','1','Vigente','1',18000.00),(7,7,'2026-07-01','2026-09-30','1','Vigente','1',15000.00),(8,8,'2026-04-01','2026-11-30','1','Vigente','2',45000.00),(9,9,'2026-05-15','2026-08-15','1','Vigente','1',22000.00);
/*!40000 ALTER TABLE `contrato` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departamentos`
--

DROP TABLE IF EXISTS `departamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `departamentos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(200) DEFAULT NULL,
  `color` varchar(7) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departamentos`
--

LOCK TABLES `departamentos` WRITE;
/*!40000 ALTER TABLE `departamentos` DISABLE KEYS */;
INSERT INTO `departamentos` VALUES (1,'Producción','Puesta en escena, guiones y transmisión','#e74c3c'),(2,'Técnica','Soporte técnico, mantenimiento de equipos','#3498db'),(3,'Comercial','Gestión de patrocinadores y contratos','#2ecc71'),(4,'Administración','Gestión general del estadio','#9b59b6'),(5,'Operaciones','Operaciones en vivo y palco','#f39c12');
/*!40000 ALTER TABLE `departamentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elementos_guion`
--

DROP TABLE IF EXISTS `elementos_guion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `elementos_guion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
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
  `estado` varchar(20) DEFAULT NULL,
  `inicio_curso` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `guion_id` (`guion_id`),
  KEY `fecha_id` (`fecha_id`),
  CONSTRAINT `elementos_guion_ibfk_1` FOREIGN KEY (`guion_id`) REFERENCES `guiones` (`id`),
  CONSTRAINT `elementos_guion_ibfk_2` FOREIGN KEY (`fecha_id`) REFERENCES `guion_fechas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elementos_guion`
--

LOCK TABLES `elementos_guion` WRITE;
/*!40000 ALTER TABLE `elementos_guion` DISABLE KEYS */;
INSERT INTO `elementos_guion` VALUES (1,1,1,'pregame','17:00:00',NULL,NULL,'Apertura de puertas y bienvenida',300,'keiver',1,'2026-07-08 09:05:00','pendiente',NULL),(2,1,1,'pregame','17:30:00',NULL,NULL,'Presentación de alineaciones por pantallas',180,'Genesis',2,'2026-07-08 09:06:00','pendiente',NULL),(3,1,1,'pregame','18:00:00',NULL,NULL,'Ceremonia de lanzamiento inaugural',240,'keiver',3,'2026-07-08 09:07:00','pendiente',NULL),(4,1,1,'pregame','18:15:00',NULL,NULL,'Himno Nacional - Orquesta del Estado',180,'Genesis',4,'2026-07-08 09:08:00','pendiente',NULL),(5,1,1,'pregame','18:20:00',NULL,NULL,'Video bienvenida patrocinadores',60,'keiver',5,'2026-07-08 09:09:00','pendiente',NULL),(6,1,1,'game',NULL,1,'baja','Publicidad Maltin Polar - Jumbotron',30,'keiver',1,'2026-07-08 09:10:00','pendiente',NULL),(7,1,1,'game',NULL,1,'alta','Publicidad Pepsi - Bafles del estadio',30,'Genesis',2,'2026-07-08 09:11:00','pendiente',NULL),(8,1,1,'game',NULL,2,'baja','Concurso Maltin Polar - Lanzamiento de pelota',120,'keiver',3,'2026-07-08 09:12:00','pendiente',NULL),(9,1,1,'game',NULL,3,'alta','Publicidad Banesco - Finanzas personales',30,'Genesis',4,'2026-07-08 09:13:00','pendiente',NULL),(10,1,1,'game',NULL,4,'baja','Reels Café Flor de Arauca',25,'keiver',5,'2026-07-08 09:14:00','pendiente',NULL),(11,1,1,'game',NULL,5,'alta','Publicidad Movilnet - Plan datos beisbol',30,'Genesis',6,'2026-07-08 09:15:00','pendiente',NULL),(12,1,1,'game',NULL,6,'baja','Ceremonia de premiación fan del juego',180,'keiver',7,'2026-07-08 09:16:00','pendiente',NULL),(13,1,1,'game',NULL,7,'alta','Publicidad Farmatodo - Salud y bienestar',30,'Genesis',8,'2026-07-08 09:17:00','pendiente',NULL),(14,1,1,'game',NULL,8,'baja','Reels Cerveza Regional',25,'keiver',9,'2026-07-08 09:18:00','pendiente',NULL),(15,1,1,'postgame',NULL,NULL,NULL,'Entrega de premios a ganadores',300,'keiver',1,'2026-07-08 09:19:00','pendiente',NULL),(16,1,1,'postgame',NULL,NULL,NULL,'Entrevistas post-juego y agradecimientos',600,'Genesis',2,'2026-07-08 09:20:00','pendiente',NULL),(17,2,2,'pregame','17:00:00',NULL,NULL,'Apertura de puertas',300,'keiver',1,'2026-07-10 10:05:00','pendiente',NULL),(18,2,2,'pregame','17:30:00',NULL,NULL,'Presentación de alineaciones',180,'Genesis',2,'2026-07-10 10:06:00','pendiente',NULL),(19,2,2,'pregame','18:00:00',NULL,NULL,'Ceremonia de lanzamiento inaugural',240,'keiver',3,'2026-07-10 10:07:00','pendiente',NULL),(20,2,2,'pregame','18:15:00',NULL,NULL,'Himno Nacional',180,'Genesis',4,'2026-07-10 10:08:00','pendiente',NULL),(21,2,2,'game',NULL,1,'baja','Publicidad Maltin Polar',30,'keiver',1,'2026-07-10 10:10:00',NULL,NULL),(22,2,2,'game',NULL,2,'baja','Concurso Alimentos Mary - Sabor del juego',120,'keiver',2,'2026-07-10 10:11:00',NULL,NULL),(23,2,2,'game',NULL,3,'alta','Publicidad Tubrica',30,'Genesis',3,'2026-07-10 10:12:00',NULL,NULL),(24,2,2,'game',NULL,5,'baja','Reels Banesco',25,'keiver',4,'2026-07-10 10:13:00',NULL,NULL),(25,2,2,'game',NULL,7,'alta','Publicidad Pepsi',30,'Genesis',5,'2026-07-10 10:14:00',NULL,NULL),(26,3,3,'pregame','18:00:00',NULL,NULL,'Apertura de puertas y animación',300,'keiver',1,'2026-07-10 11:05:00','pendiente',NULL),(27,3,3,'pregame','18:30:00',NULL,NULL,'Himno Nacional y presentación',240,'Genesis',2,'2026-07-10 11:06:00','pendiente',NULL),(28,3,3,'game',NULL,1,'baja','Publicidad Movilnet',30,'keiver',1,'2026-07-10 11:08:00',NULL,NULL),(29,3,3,'game',NULL,3,'baja','Concurso Café Flor de Arauca',120,'keiver',2,'2026-07-10 11:09:00',NULL,NULL),(30,3,3,'game',NULL,5,'alta','Publicidad Farmatodo',30,'Genesis',3,'2026-07-10 11:10:00',NULL,NULL),(31,3,3,'game',NULL,7,'baja','Reels Cerveza Regional',25,'keiver',4,'2026-07-10 11:11:00',NULL,NULL),(32,6,NULL,'pregame','16:32:00',NULL,NULL,'eece',120,'Keiver Zamudia',1,'2026-07-10 16:32:43','pendiente',NULL),(33,6,NULL,'game',NULL,1,'baja','rvvvev',720,'Genesis Acosta',1,'2026-07-10 16:33:24','pendiente',NULL),(34,6,NULL,'pregame','16:36:00',NULL,NULL,'eber',120,'Naryibeth Alejos',2,'2026-07-10 16:33:42','pendiente',NULL),(35,7,NULL,'pregame','16:32:00',NULL,NULL,'eece',120,'Keiver Zamudia',1,'2026-07-10 17:39:12','pendiente',NULL),(36,7,NULL,'game',NULL,1,'baja','rvvvev',720,'Genesis Acosta',1,'2026-07-10 17:39:12','pendiente',NULL),(37,7,NULL,'pregame','16:36:00',NULL,NULL,'eber',120,'Naryibeth Alejos',2,'2026-07-10 17:39:12','pendiente',NULL),(38,7,NULL,'game',NULL,3,'baja','prueba',720,'Admin',2,'2026-08-23 15:50:04','pendiente',NULL);
/*!40000 ALTER TABLE `elementos_guion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estado_asignacion`
--

DROP TABLE IF EXISTS `estado_asignacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estado_asignacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estado_asignacion`
--

LOCK TABLES `estado_asignacion` WRITE;
/*!40000 ALTER TABLE `estado_asignacion` DISABLE KEYS */;
INSERT INTO `estado_asignacion` VALUES (1,'Pendiente','Asignación activa, pendiente de devolución'),(2,'Devuelto','Recurso devuelto exitosamente'),(3,'Vencido','Asignación vencida (no devuelto a tiempo)');
/*!40000 ALTER TABLE `estado_asignacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estado_recurso`
--

DROP TABLE IF EXISTS `estado_recurso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estado_recurso` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estado_recurso`
--

LOCK TABLES `estado_recurso` WRITE;
/*!40000 ALTER TABLE `estado_recurso` DISABLE KEYS */;
INSERT INTO `estado_recurso` VALUES (1,'Disponible','Recurso disponible para uso o asignación'),(2,'Asignado','Recurso actualmente asignado a un usuario'),(3,'En Mantenimiento','Recurso en proceso de mantenimiento o reparación'),(4,'Dañado','Recurso reportado como dañado'),(5,'Baja','Recurso dado de baja del inventario');
/*!40000 ALTER TABLE `estado_recurso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guion_fechas`
--

DROP TABLE IF EXISTS `guion_fechas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `guion_fechas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `guion_id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `guion_id` (`guion_id`),
  CONSTRAINT `guion_fechas_ibfk_1` FOREIGN KEY (`guion_id`) REFERENCES `guiones` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guion_fechas`
--

LOCK TABLES `guion_fechas` WRITE;
/*!40000 ALTER TABLE `guion_fechas` DISABLE KEYS */;
INSERT INTO `guion_fechas` VALUES (1,1,'2026-07-10'),(2,2,'2026-07-12'),(3,3,'2026-07-15'),(4,4,'2026-07-18'),(5,5,'2026-07-20'),(6,6,'2026-07-10'),(7,7,'2026-07-10'),(8,8,'2026-09-18'),(9,9,'2026-09-18');
/*!40000 ALTER TABLE `guion_fechas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guiones`
--

DROP TABLE IF EXISTS `guiones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `guiones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) NOT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `inicio_show` datetime DEFAULT NULL,
  `creado_en` datetime DEFAULT NULL,
  `modificado_en` datetime DEFAULT NULL,
  `tiempo_inning` int(11) DEFAULT NULL,
  `grupo_id` varchar(36) DEFAULT NULL,
  `status` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`),
  KEY `idx_grupo_id` (`grupo_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guiones`
--

LOCK TABLES `guiones` WRITE;
/*!40000 ALTER TABLE `guiones` DISABLE KEYS */;
INSERT INTO `guiones` VALUES (1,'Cardenales vs Leones - 2026-07-10','finalizado',NULL,'2026-07-08 09:00:00','2026-07-25 15:58:18',120,NULL,1),(2,'Cardenales vs Tiburones - 2026-07-12','borrador',NULL,'2026-07-10 10:00:00','2026-07-10 10:00:00',120,NULL,1),(3,'Cardenales vs Navegantes - 2026-07-15','borrador',NULL,'2026-07-10 11:00:00','2026-07-10 11:00:00',120,NULL,1),(4,'Cardenales vs Tigres - 2026-07-18','borrador',NULL,'2026-07-10 12:00:00','2026-07-10 12:00:00',120,NULL,1),(5,'Cardenales vs Águilas - 2026-07-20','borrador',NULL,'2026-07-10 13:00:00','2026-07-10 13:00:00',120,NULL,1),(6,'juego - 2026-07-10','finalizado',NULL,'2026-07-10 16:30:20','2026-08-23 15:50:18',720,NULL,1),(7,'juego 3 - 2026-07-10','finalizado',NULL,'2026-07-10 17:39:12','2026-09-18 06:26:48',720,NULL,1),(8,'prueba - 2026-09-18','borrador',NULL,'2026-09-18 06:12:12',NULL,180,NULL,1),(9,'prueba - 2026-09-18','borrador',NULL,'2026-09-18 06:12:16',NULL,180,NULL,1);
/*!40000 ALTER TABLE `guiones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historial_chat`
--

DROP TABLE IF EXISTS `historial_chat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `historial_chat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `mensaje_usuario` text NOT NULL,
  `respuesta_ia` text NOT NULL,
  `contexto` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`contexto`)),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_chat`
--

LOCK TABLES `historial_chat` WRITE;
/*!40000 ALTER TABLE `historial_chat` DISABLE KEYS */;
INSERT INTO `historial_chat` VALUES (1,3,'Hola','Buenos días, **Admin**. Soy **Aurora**, tu asistente del sistema Itinerario. Puedo ayudarte con información sobre los módulos, estados, conteos y guías de uso. ¿En qué te puedo ayudar?','{\"intencion\": \"saludo\", \"confianza\": 1.0}','2026-07-10 14:26:38'),(2,3,'Dime cuantos usuarios hay conectadas','No pude obtener los datos de **usuarios** en este momento. Intenta de nuevo.','{\"intencion\": \"error\", \"confianza\": 0.3}','2026-07-10 14:27:10'),(3,5,'¿Cuántos guiones hay?','Hay **5** guion(es) registrado(s) en el sistema.','{\"intencion\": \"contar_guiones\", \"confianza\": 0.95}','2026-07-10 14:53:19'),(4,4,'¿Cuántos guiones hay?','Hay **7** guion(es) registrado(s) en el sistema.','{\"intencion\": \"contar_guiones\", \"confianza\": 0.95}','2026-08-23 19:29:04');
/*!40000 ALTER TABLE `historial_chat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historial_mantenimiento`
--

DROP TABLE IF EXISTS `historial_mantenimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `historial_mantenimiento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mantenimiento_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `accion` varchar(50) NOT NULL,
  `descripcion` text NOT NULL,
  `creado_en` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `idx_historial_mantenimiento` (`mantenimiento_id`),
  CONSTRAINT `historial_mantenimiento_ibfk_1` FOREIGN KEY (`mantenimiento_id`) REFERENCES `mantenimientos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_mantenimiento`
--

LOCK TABLES `historial_mantenimiento` WRITE;
/*!40000 ALTER TABLE `historial_mantenimiento` DISABLE KEYS */;
INSERT INTO `historial_mantenimiento` VALUES (1,1,4,'ingreso','Ingreso a mantenimiento. Diagnóstico: no funciona','2026-07-10 17:44:46'),(2,1,4,'reparar','Se inició el proceso de reparación.','2026-07-10 17:45:38'),(3,1,4,'reparar','Recurso reparado exitosamente.','2026-07-10 17:47:42'),(4,1,4,'finalizar','Mantenimiento finalizado.','2026-07-10 17:47:52'),(5,2,4,'ingreso','Ingreso a mantenimiento. Diagnóstico: deefc','2026-07-10 17:48:32');
/*!40000 ALTER TABLE `historial_mantenimiento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mantenimientos`
--

DROP TABLE IF EXISTS `mantenimientos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mantenimientos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `recurso_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `estado` varchar(20) DEFAULT 'en_espera',
  `fecha_ingreso` date NOT NULL,
  `fecha_salida` date DEFAULT NULL,
  `diagnostico` text DEFAULT NULL,
  `observaciones` text DEFAULT NULL,
  `creado_en` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `idx_mantenimientos_estado` (`estado`),
  KEY `idx_mantenimientos_recurso` (`recurso_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mantenimientos`
--

LOCK TABLES `mantenimientos` WRITE;
/*!40000 ALTER TABLE `mantenimientos` DISABLE KEYS */;
INSERT INTO `mantenimientos` VALUES (1,1,4,'finalizado','2026-07-10','2026-07-10','no funciona','','2026-07-10 17:44:46'),(2,1,4,'en_espera','2026-07-10',NULL,'deefc','scxed','2026-07-10 17:48:32');
/*!40000 ALTER TABLE `mantenimientos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pagos`
--

DROP TABLE IF EXISTS `pagos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pagos` (
  `id_pago` int(11) NOT NULL AUTO_INCREMENT,
  `id_contrato` int(11) NOT NULL,
  `monto` decimal(12,2) NOT NULL,
  `tipo_pago` varchar(20) NOT NULL,
  `referencia` varchar(100) DEFAULT NULL,
  `fecha_pago` date NOT NULL,
  `hora_pago` time NOT NULL,
  `registrado_por` int(11) DEFAULT NULL,
  `Descripcion` text DEFAULT NULL,
  `fecha_registro` datetime DEFAULT current_timestamp(),
  `estado` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id_pago`),
  KEY `id_contrato` (`id_contrato`),
  CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`id_contrato`) REFERENCES `contrato` (`id_contrato`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagos`
--

LOCK TABLES `pagos` WRITE;
/*!40000 ALTER TABLE `pagos` DISABLE KEYS */;
INSERT INTO `pagos` VALUES (1,1,21250.00,'Transferencia','TRF-2026-001','2026-04-05','10:00:00',3,'Pago inicial contrato Maltin Polar - 25%','2026-04-05 10:05:00',1),(2,1,21250.00,'Transferencia','TRF-2026-002','2026-06-05','10:00:00',3,'Segundo abono contrato Maltin Polar - 25%','2026-06-05 10:05:00',1),(3,2,15500.00,'Transferencia','TRF-2026-003','2026-05-10','11:00:00',4,'Pago inicial contrato Pepsi - 25%','2026-05-10 11:05:00',1),(4,5,30000.00,'Transferencia','TRF-2026-004','2026-03-15','09:30:00',3,'Pago inicial contrato Banesco - 25%','2026-03-15 09:35:00',1),(5,5,30000.00,'Transferencia','TRF-2026-005','2026-06-15','09:30:00',3,'Segundo abono contrato Banesco - 25%','2026-06-15 09:35:00',1),(6,8,11250.00,'Efectivo','EFE-2026-001','2026-04-10','14:00:00',5,'Pago inicial contrato Farmatodo - 25%','2026-04-10 14:05:00',1),(7,3,6250.00,'Efectivo','EFE-2026-002','2026-06-10','15:00:00',5,'Pago inicial contrato Café Flor - 50%','2026-06-10 15:05:00',1),(8,9,5500.00,'Transferencia','TRF-2026-006','2026-05-20','16:00:00',6,'Pago inicial contrato Cerveza Regional - 25%','2026-05-20 16:05:00',1);
/*!40000 ALTER TABLE `pagos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patrocinadores`
--

DROP TABLE IF EXISTS `patrocinadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `patrocinadores` (
  `id_patrocinador` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_empresa` varchar(100) NOT NULL,
  `rif` varchar(20) NOT NULL,
  `tipo_contrato` int(11) NOT NULL,
  `nombre_contacto` text NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `estado` int(11) NOT NULL,
  `encargado_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_patrocinador`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patrocinadores`
--

LOCK TABLES `patrocinadores` WRITE;
/*!40000 ALTER TABLE `patrocinadores` DISABLE KEYS */;
INSERT INTO `patrocinadores` VALUES (1,'Maltin Polar','J-00005820-9',2,'José Luis Rodríguez','0212-4003000','jrodriguez@polar.com',1,3),(2,'Pepsi Venezuela','J-00028049-5',2,'María Fernanda López','0212-5002000','mlopez@pepsi.com',1,4),(3,'Café Flor de Arauca','J-40206831-0',1,'Carlos Mendoza','0251-2661100','cmendoza@cafeflor.com',1,5),(4,'Tubrica C.A','J-310284567',1,'Pedro Jiménez','0241-8581000','pjimenez@tubrica.com',1,6),(5,'Banesco Banco Universal','J-00078321-3',2,'Ana Sofía Pérez','0212-2064646','aperez@banesco.com',1,3),(6,'Movilnet C.A','J-30472189-0',1,'Roberto Díaz','0212-3001000','rdiaz@movilnet.com',1,4),(7,'Alimentos Mary','J-29587314-6',1,'Luis Hernández','0241-8782000','lhernandez@alimentosmary.com',1,5),(8,'Farmatodo C.A','J-00032815-8',2,'Gabriela Torres','0212-7003000','gtorres@farmatodo.com',1,6),(9,'Cerveza Regional','J-40157623-8',1,'Manuel Castillo','0261-7984000','mcastillo@regional.com',1,3),(10,'donitas Edg','j65151525',1,'donitas edg','0424-3577654','donitas@gmail.com',1,25),(11,'jean center','j-31388643',1,'jean center','04129656958','jeancenterbqto@gmail.com',1,25);
/*!40000 ALTER TABLE `patrocinadores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `premios`
--

DROP TABLE IF EXISTS `premios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `premios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_patrocinador` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` varchar(20) DEFAULT 'pendiente',
  `fecha_creacion` date NOT NULL DEFAULT current_timestamp(),
  `fecha_entrega` datetime DEFAULT NULL,
  `entregado_por` int(11) DEFAULT NULL,
  `hora_creacion` time NOT NULL,
  `foto` varchar(200) DEFAULT 'default-premio.png',
  `cantidad` int(11) NOT NULL DEFAULT 1,
  `cantidad_entregada` int(11) NOT NULL DEFAULT 0,
  `estatus` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `id_patrocinador` (`id_patrocinador`),
  CONSTRAINT `premios_ibfk_1` FOREIGN KEY (`id_patrocinador`) REFERENCES `patrocinadores` (`id_patrocinador`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `premios`
--

LOCK TABLES `premios` WRITE;
/*!40000 ALTER TABLE `premios` DISABLE KEYS */;
INSERT INTO `premios` VALUES (1,1,'6 Pack Maltin Polar','Caja de 6 latas de Maltin Polar 350ml','entregado','2026-06-15','2026-06-18 19:30:00',3,'10:00:00','default-premio.png',50,12,0),(2,2,'Pepsi Cola 2L x3','Tres botellas de Pepsi Cola 2 litros','entregado','2026-06-15','2026-06-18 20:15:00',4,'10:30:00','default-premio.png',30,8,0),(3,5,'Tarjeta Banesco $50','Tarjeta de regalo Banesco por 50$','pendiente','2026-07-01',NULL,NULL,'09:00:00','default-premio.png',10,0,1),(4,3,'Café Flor de Arauca 250g','Paquete de café premium tostado oscuro','entregado','2026-06-20','2026-06-22 18:45:00',5,'11:00:00','default-premio.png',20,5,0),(5,8,'Kit Farmatodo','Kit de productos de higiene personal','pendiente','2026-07-05',NULL,NULL,'14:00:00','default-premio.png',40,0,1),(6,6,'Camiseta Movilnet','Camiseta oficial Movilnet edición beisbol','entregado','2026-06-10','2026-06-12 19:00:00',3,'08:30:00','default-premio.png',100,25,0),(7,4,'Combo Tubrica','Kit de herramientas básicas Tubrica','pendiente','2026-07-08',NULL,NULL,'15:30:00','default-premio.png',15,0,1),(8,9,'Cerveza Regional 6 Pack','Caja de 6 latas de Cerveza Regional','pendiente','2026-07-10',NULL,NULL,'12:00:00','default-premio.png',25,0,1),(9,1,'Polar Pina 1L x2','Dos botellas de Polar Pina 1 litro','entregado','2026-06-25','2026-06-28 20:00:00',4,'09:30:00','default-premio.png',40,15,0),(10,7,'Caja Alimentos Mary','Caja de snacks y dulces variados','pendiente','2026-07-12',NULL,NULL,'16:00:00','default-premio.png',30,0,1),(11,1,'caja de malta polar','','pendiente','2026-07-10',NULL,NULL,'10:33:18','premio_1783693998.jpg',20,0,0),(12,4,'Gorra de cardenales','','pendiente','2026-07-10',NULL,NULL,'10:37:26','premio_1783694246.jpg',40,0,0),(13,3,'Cafe 500mg','Competencia','pendiente','2026-07-10',NULL,NULL,'10:38:03','premio_1783694570.jpg',10,0,0),(14,7,'Bolsa de comida Mary','Combo de 7 productos variados ','pendiente','2026-07-10',NULL,NULL,'10:42:07','premio_1783694527.jpg',10,0,0);
/*!40000 ALTER TABLE `premios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recursos`
--

DROP TABLE IF EXISTS `recursos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recursos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `tipo_id` int(11) NOT NULL,
  `estado_id` int(11) NOT NULL DEFAULT 1,
  `fecha_compra` date DEFAULT NULL,
  `costo` decimal(10,2) DEFAULT NULL,
  `eliminado` tinyint(1) NOT NULL DEFAULT 0,
  `creado_en` datetime DEFAULT current_timestamp(),
  `modificado_en` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_recursos_tipo` (`tipo_id`),
  KEY `idx_recursos_estado` (`estado_id`),
  CONSTRAINT `fk_recursos_estado` FOREIGN KEY (`estado_id`) REFERENCES `estado_recurso` (`id`),
  CONSTRAINT `fk_recursos_tipo` FOREIGN KEY (`tipo_id`) REFERENCES `tipo_recurso` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recursos`
--

LOCK TABLES `recursos` WRITE;
/*!40000 ALTER TABLE `recursos` DISABLE KEYS */;
INSERT INTO `recursos` VALUES (1,'Sony PXW-Z150','Cámara 4K profesional para transmisión en vivo',2,3,'2025-03-15',4500.00,0,'2026-07-10 14:24:44','2026-07-10 17:48:32'),(2,'Pantalla LED 55\"','Pantalla LED para sala de control y palco',2,1,'2025-06-20',3200.00,0,'2026-07-10 14:24:44','2026-07-10 14:24:44'),(3,'Yamaha TF3','Mezcladora digital 24 canales para audio en vivo',8,1,'2024-11-10',5800.00,0,'2026-07-10 14:24:44','2026-07-10 14:24:44'),(4,'Shure SM58 x4','Micrófonos dinámicos inalámbricos para presentadores',8,1,'2025-08-05',1200.00,0,'2026-07-10 14:24:44','2026-07-10 14:24:44'),(5,'Dell XPS 15','Laptop para control de guiones y presentaciones',1,1,'2025-09-01',2100.00,0,'2026-07-10 14:24:44','2026-07-10 14:24:44'),(6,'Epson EB-L615U','Proyector láser 6000 lúmenes para pantallas del estadio',2,1,'2025-01-20',3800.00,0,'2026-07-10 14:24:44','2026-07-10 14:24:44'),(7,'Mesa de iluminación DMX','Controlador de luces para escenario principal',3,1,'2024-12-05',2600.00,0,'2026-07-10 14:24:44','2026-07-10 14:24:44'),(8,'Sillas plegables x20','Set de sillas para área de producción',4,1,'2025-04-10',400.00,0,'2026-07-10 14:24:44','2026-07-10 14:24:44'),(9,'Bafle JBL PRX812W','Bafle inalámbrico 12\" para zona de transmisión',7,1,'2025-07-15',1800.00,0,'2026-07-10 14:24:44','2026-07-10 14:24:44'),(10,'iPad Pro 12.9\"','Tablet para control remoto de presentaciones',1,2,'2025-10-01',1100.00,0,'2026-07-10 14:24:44','2026-07-10 17:47:12');
/*!40000 ALTER TABLE `recursos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reels`
--

DROP TABLE IF EXISTS `reels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reels` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `id_patrocinador` int(11) DEFAULT NULL,
  `duracion_total` float DEFAULT 0,
  `creado_en` datetime DEFAULT current_timestamp(),
  `modificado_en` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `id_patrocinador` (`id_patrocinador`),
  CONSTRAINT `reels_ibfk_1` FOREIGN KEY (`id_patrocinador`) REFERENCES `patrocinadores` (`id_patrocinador`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reels`
--

LOCK TABLES `reels` WRITE;
/*!40000 ALTER TABLE `reels` DISABLE KEYS */;
INSERT INTO `reels` VALUES (1,'Maltin Polar - Edición Verano',1,2700,'2026-06-01 10:00:00','2026-09-18 06:50:35'),(2,'Pepsi - Noche de Beisbol',2,1800,'2026-06-05 11:00:00','2026-09-18 06:50:35'),(3,'Banesco - Finanzas Familiares',5,2100,'2026-06-10 09:00:00','2026-09-18 06:50:35'),(4,'Café Flor de Arauca - Momento Café',3,1500,'2026-06-15 14:00:00','2026-09-18 06:50:35'),(5,'Movilnet - Conectados al Juego',6,1200,'2026-06-20 10:00:00','2026-09-18 06:50:35'),(6,'Reels pruebas',NULL,180,'2026-09-18 06:40:12','2026-09-18 06:50:35');
/*!40000 ALTER TABLE `reels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tareas`
--

DROP TABLE IF EXISTS `tareas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tareas` (
  `id_tarea` int(11) NOT NULL AUTO_INCREMENT,
  `Nombre_Tarea` varchar(255) NOT NULL,
  `Instruccion` varchar(255) NOT NULL,
  `id_usuario_creador` int(11) DEFAULT NULL,
  `Estatus` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id_tarea`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tareas`
--

LOCK TABLES `tareas` WRITE;
/*!40000 ALTER TABLE `tareas` DISABLE KEYS */;
INSERT INTO `tareas` VALUES (1,'Verificar equipo de transmisión','Revisar estado de cámaras, mezcladora y pantallas antes del juego',3,1),(2,'Calibrar sonido del estadio','Ajustar niveles de audio en bafles principales y zonas secundarias',3,1),(3,'Preparar contenido Jumbotron','Cargar videos de patrocinadores y spots en el sistema de pantallas',4,1),(4,'Revisar iluminación del campo','Verificar focos principales, focos de juego y luz de emergencia',5,1),(5,'Entregar kits de premios','Preparar y entregar premios a zona de animación 2 horas antes del juego',6,1),(6,'Coordinar llegada de patrocinadores','Confirmar asistencia y asignar accesos a invitados especiales',3,1);
/*!40000 ALTER TABLE `tareas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tareas_asignadas`
--

DROP TABLE IF EXISTS `tareas_asignadas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tareas_asignadas` (
  `id_asignacion` int(11) NOT NULL AUTO_INCREMENT,
  `id_tarea` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `Estado` varchar(50) DEFAULT 'Pendiente',
  `fecha_asignacion_tarea` datetime DEFAULT NULL,
  `Estatus` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id_asignacion`),
  KEY `id_tarea` (`id_tarea`),
  CONSTRAINT `tareas_asignadas_ibfk_1` FOREIGN KEY (`id_tarea`) REFERENCES `tareas` (`id_tarea`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tareas_asignadas`
--

LOCK TABLES `tareas_asignadas` WRITE;
/*!40000 ALTER TABLE `tareas_asignadas` DISABLE KEYS */;
INSERT INTO `tareas_asignadas` VALUES (1,1,4,'Completada','2026-07-09 14:00:00',1),(2,2,5,'Completada','2026-07-09 14:30:00',1),(3,3,4,'Completada','2026-07-09 15:00:00',1),(4,4,6,'Pendiente','2026-07-10 08:00:00',1),(5,5,5,'Pendiente','2026-07-10 09:00:00',1),(6,6,3,'Pendiente','2026-07-10 10:00:00',1),(7,4,25,'Pendiente','2026-07-10 10:33:45',1),(8,5,25,'Pendiente','2026-07-10 10:33:55',1),(9,6,5,'Pendiente','2026-07-10 18:03:56',1),(10,6,4,'Completada','2026-08-23 20:56:59',1),(11,6,25,'Pendiente','2026-08-23 20:56:59',1),(12,2,4,'Completada','2026-08-23 23:11:06',1);
/*!40000 ALTER TABLE `tareas_asignadas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_recurso`
--

DROP TABLE IF EXISTS `tipo_recurso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_recurso` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_recurso`
--

LOCK TABLES `tipo_recurso` WRITE;
/*!40000 ALTER TABLE `tipo_recurso` DISABLE KEYS */;
INSERT INTO `tipo_recurso` VALUES (1,'Equipo de PC','Computadoras, laptops, tablets'),(2,'Equipo de Video','Cámaras, proyectores, monitores, pantallas LED'),(3,'Iluminación','Luces, reflectores, dimmers, mesas de luz'),(4,'Mobiliario','Mesas, sillas, stands, tarimas'),(5,'Instrumento','Instrumentos musicales, amplificadores'),(6,'Vehículo','Vehículos de producción y logística'),(7,'Otro','Otros tipos de recursos'),(8,'Microfono','Micrófonos inalámbricos y de solapa');
/*!40000 ALTER TABLE `tipo_recurso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `videos`
--

DROP TABLE IF EXISTS `videos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `videos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) NOT NULL,
  `duracion_segundos` int(11) DEFAULT 0,
  `orden` int(11) DEFAULT NULL,
  `reel_id` int(11) NOT NULL,
  `id_patrocinador` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_videos_reel` (`reel_id`),
  CONSTRAINT `fk_videos_reel` FOREIGN KEY (`reel_id`) REFERENCES `reels` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `videos`
--

LOCK TABLES `videos` WRITE;
/*!40000 ALTER TABLE `videos` DISABLE KEYS */;
INSERT INTO `videos` VALUES (1,'Maltin Polar - Spot 15s',15,1,1,1),(2,'Maltin Polar - Behind the scenes',15,2,1,1),(3,'Maltin Polar - Testimonios fans',15,3,1,1),(4,'Pepsi - Spot principal',15,1,2,2),(5,'Pepsi - Momento refresh',15,2,2,2),(6,'Banesco - Consejos financieros',20,1,3,5),(7,'Banesco - Beneficios tarjeta',15,2,3,5),(8,'Café Flor - Tueste artesanal',15,1,4,3),(9,'Café Flor - Recetas',10,2,4,3),(10,'Movilnet - Plan beisbol',10,1,5,6),(11,'Movilnet - Conectividad',10,2,5,6),(12,'prueba',15,1,6,5);
/*!40000 ALTER TABLE `videos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-18  9:03:22
