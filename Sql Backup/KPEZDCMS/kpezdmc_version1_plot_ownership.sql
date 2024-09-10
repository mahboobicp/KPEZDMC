-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: kpezdmc_version1
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `plot_ownership`
--

DROP TABLE IF EXISTS `plot_ownership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plot_ownership` (
  `id` int NOT NULL,
  `plot_id` int NOT NULL,
  `owner_id` int NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `po_status` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_plot_id_plottable` (`plot_id`),
  KEY `fk_owner_id_ownertable` (`owner_id`),
  CONSTRAINT `fk_owner_id_ownertable` FOREIGN KEY (`owner_id`) REFERENCES `ownertable` (`id`),
  CONSTRAINT `fk_plot_id_plottable` FOREIGN KEY (`plot_id`) REFERENCES `plots` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plot_ownership`
--

LOCK TABLES `plot_ownership` WRITE;
/*!40000 ALTER TABLE `plot_ownership` DISABLE KEYS */;
INSERT INTO `plot_ownership` VALUES (100,101,101,'2019-09-05',NULL,'Alloted','2024-09-04 13:50:48',NULL),(101,102,102,'2024-09-04',NULL,'Alloted','2024-09-04 14:10:58',NULL),(103,104,104,'2021-09-08',NULL,'Alloted','2024-09-04 16:02:37',NULL),(104,105,105,'2024-09-12',NULL,'Alloted','2024-09-04 16:05:19',NULL),(105,106,106,'2021-09-08',NULL,'Alloted','2024-09-04 16:19:15',NULL),(106,107,107,'2021-09-15',NULL,'Alloted','2024-09-04 16:21:44',NULL),(107,108,108,'2018-09-12',NULL,'Alloted','2024-09-04 16:26:15',NULL),(108,109,109,'2022-09-06',NULL,'Alloted','2024-09-04 16:32:30',NULL),(109,110,110,'2024-09-10',NULL,'Alloted','2024-09-05 12:16:53',NULL),(110,111,111,'2024-09-05',NULL,'Alloted','2024-09-05 12:17:58',NULL),(111,112,112,'2024-09-05',NULL,'Alloted','2024-09-05 12:36:30',NULL),(112,113,113,'2024-09-05',NULL,'Alloted','2024-09-05 12:49:23',NULL),(113,114,114,'2024-09-06',NULL,'Alloted','2024-09-06 18:23:45',NULL),(114,115,115,'2021-09-16',NULL,'Alloted','2024-09-08 09:31:04',NULL),(115,116,116,'2024-09-10',NULL,'Alloted','2024-09-10 11:06:59',NULL);
/*!40000 ALTER TABLE `plot_ownership` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-10 12:45:19
