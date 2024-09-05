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
-- Table structure for table `plots`
--

DROP TABLE IF EXISTS `plots`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plots` (
  `ID` int NOT NULL,
  `Plot_Number` varchar(50) NOT NULL,
  `zone` varchar(100) DEFAULT NULL,
  `Location` varchar(255) DEFAULT NULL,
  `Plot_Status` varchar(100) DEFAULT NULL,
  `Land_Type` varchar(50) DEFAULT NULL,
  `Area` decimal(10,2) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plots`
--

LOCK TABLES `plots` WRITE;
/*!40000 ALTER TABLE `plots` DISABLE KEYS */;
INSERT INTO `plots` VALUES (100,'4','NEZ','kk','Industrial','Acquired',4.00,'2024-09-04 13:48:53',NULL),(101,'20C','NEZ','Road 2','Industrial','Acquired',1.00,'2024-09-04 13:50:48',NULL),(102,'10A','Extension','Road 3','Industrial','Acquired',0.50,'2024-09-04 14:10:58',NULL),(103,'','NEZ','','Industrial','Acquired',0.00,'2024-09-04 15:51:14',NULL),(104,'10B','NEZ','Road 5','Industrial','Acquired',1.00,'2024-09-04 16:02:37',NULL),(105,'11A','NEZ','Road 4','Industrial','Acquired',1.00,'2024-09-04 16:05:19',NULL),(106,'23','NEZ','Road 5','Industrial','Acquired',2.00,'2024-09-04 16:19:15',NULL),(107,'12A','Extension','Road 4','Industrial','Acquired',1.50,'2024-09-04 16:21:44',NULL),(108,'68','NEZ','Road 12','Industrial','Acquired',0.40,'2024-09-04 16:26:15',NULL),(109,'99','NEZ','Branch 1','Industrial','Acquired',0.50,'2024-09-04 16:32:30',NULL),(110,'1','Nowshera Econoic Zone Ext.','Road 3','Industrial','Acquired',0.10,'2024-09-05 12:16:53',NULL),(111,'2','Nowshera Econoic Zone','Road 2','Industerial','Acquired',1.00,'2024-09-05 12:17:58',NULL),(112,'3','Nowshera Econoic Zone','Branch 2','Industrial','Acquired',2.00,'2024-09-05 12:36:30',NULL),(113,'4','Nowshera Econoic Zone','Road 5','Industrial','Acquired',4.00,'2024-09-05 12:49:23',NULL);
/*!40000 ALTER TABLE `plots` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-05 15:50:23
