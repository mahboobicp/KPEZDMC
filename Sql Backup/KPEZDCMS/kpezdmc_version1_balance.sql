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
-- Table structure for table `balance`
--

DROP TABLE IF EXISTS `balance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `balance` (
  `balance_id` int NOT NULL AUTO_INCREMENT,
  `owner_id` int DEFAULT NULL,
  `plot_id` int DEFAULT NULL,
  `industry_id` int DEFAULT NULL,
  `budget_head_id` int DEFAULT NULL,
  `balance` decimal(10,2) DEFAULT NULL,
  `max_balance` decimal(10,2) DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  PRIMARY KEY (`balance_id`),
  KEY `fk_budget_head_id_balance` (`budget_head_id`),
  KEY `fk_owner_id_balance` (`owner_id`),
  KEY `fk_plot_id_balance` (`plot_id`),
  KEY `fk_industry_id_balance` (`industry_id`),
  CONSTRAINT `fk_budget_head_id_balance` FOREIGN KEY (`budget_head_id`) REFERENCES `budget_heads` (`budget_head_id`),
  CONSTRAINT `fk_industry_id_balance` FOREIGN KEY (`industry_id`) REFERENCES `industries` (`Id`),
  CONSTRAINT `fk_owner_id_balance` FOREIGN KEY (`owner_id`) REFERENCES `ownertable` (`id`),
  CONSTRAINT `fk_plot_id_balance` FOREIGN KEY (`plot_id`) REFERENCES `plots` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `balance`
--

LOCK TABLES `balance` WRITE;
/*!40000 ALTER TABLE `balance` DISABLE KEYS */;
INSERT INTO `balance` VALUES (1,102,102,104,100,-5500.00,0.00,'2024-09-09 10:28:14'),(2,102,102,104,102,-5000.00,0.00,'2024-09-09 10:29:34'),(3,101,101,102,102,-3000.00,0.00,'2024-09-09 10:30:03'),(4,115,115,100,101,-5000.00,0.00,'2024-09-09 10:36:37'),(5,115,115,100,102,-2000.00,0.00,'2024-09-09 10:36:50'),(6,115,115,100,103,-120000.00,0.00,'2024-09-09 10:39:26'),(7,101,101,102,103,-500000.00,0.00,'2024-09-09 10:51:46'),(8,104,104,103,100,-2000.00,0.00,'2024-09-09 12:45:45'),(9,101,101,102,100,-6000.00,0.00,'2024-09-09 13:45:13'),(10,104,104,103,101,-5000.00,0.00,'2024-09-09 13:49:16'),(11,104,104,103,103,-250000.00,0.00,'2024-09-09 13:49:57'),(12,105,105,105,101,-1000.00,0.00,'2024-09-09 16:11:55'),(13,105,105,105,102,-7000.00,0.00,'2024-09-09 16:12:05'),(14,105,105,105,100,-5000.00,0.00,'2024-09-09 16:12:15');
/*!40000 ALTER TABLE `balance` ENABLE KEYS */;
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
