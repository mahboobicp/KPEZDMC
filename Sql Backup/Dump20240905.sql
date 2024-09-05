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
-- Table structure for table `industries`
--

DROP TABLE IF EXISTS `industries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `industries` (
  `Id` int NOT NULL,
  `Ind_Name` varchar(100) DEFAULT NULL,
  `Ind_Nature` varchar(100) DEFAULT NULL,
  `Ind_Status` varchar(50) DEFAULT NULL,
  `Ind_Mode` varchar(100) DEFAULT NULL,
  `Ind_Type` varchar(100) DEFAULT NULL,
  `Coverd_Area` decimal(2,2) DEFAULT NULL,
  `plot_ID` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `fk_plot_id_plot_table` (`plot_ID`),
  CONSTRAINT `fk_plot_id_plot_table` FOREIGN KEY (`plot_ID`) REFERENCES `plots` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `industries`
--

LOCK TABLES `industries` WRITE;
/*!40000 ALTER TABLE `industries` DISABLE KEYS */;
/*!40000 ALTER TABLE `industries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `industry_ownerships`
--

DROP TABLE IF EXISTS `industry_ownerships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `industry_ownerships` (
  `id` int NOT NULL,
  `industry_id` int NOT NULL,
  `owner_id` int NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `i0_status` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_industry_id_industries_table` (`industry_id`),
  KEY `fk_owner_id_owner_table` (`owner_id`),
  CONSTRAINT `fk_industry_id_industries_table` FOREIGN KEY (`industry_id`) REFERENCES `industries` (`Id`),
  CONSTRAINT `fk_owner_id_owner_table` FOREIGN KEY (`owner_id`) REFERENCES `ownertable` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `industry_ownerships`
--

LOCK TABLES `industry_ownerships` WRITE;
/*!40000 ALTER TABLE `industry_ownerships` DISABLE KEYS */;
/*!40000 ALTER TABLE `industry_ownerships` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ownertable`
--

DROP TABLE IF EXISTS `ownertable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ownertable` (
  `id` int NOT NULL,
  `CNIC` varchar(15) NOT NULL,
  `OwnName` varchar(100) NOT NULL,
  `Mobile` varchar(12) DEFAULT NULL,
  `Email` varchar(50) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ownertable`
--

LOCK TABLES `ownertable` WRITE;
/*!40000 ALTER TABLE `ownertable` DISABLE KEYS */;
INSERT INTO `ownertable` VALUES (100,'44','kk','44','jj','44','2024-09-04 13:48:53',NULL),(101,'1234568741','Asad','14523698','jazz@gmail.com','peshawa','2024-09-04 13:50:48',NULL),(102,'12345685465','Ahmad','12365478','ahmad@gmail.com','Swat','2024-09-04 14:10:58',NULL),(103,'','','','','','2024-09-04 15:51:15',NULL),(104,'12345687455','Shoaib khan','12365478','shab@gmail.com','Lahore','2024-09-04 16:02:37',NULL),(105,'1478562355','Sohail','456235','jadsdj','lahore','2024-09-04 16:05:19',NULL),(106,'145236987','Junaid','456321789','jsdfsdj','kalakoot','2024-09-04 16:19:15',NULL),(107,'4563218944','akbar','4562545555','jdsfksdkfh','mardan','2024-09-04 16:21:44',NULL),(108,'456231789','Sahil','147852369','jjjkhh','ghh','2024-09-04 16:26:15',NULL),(109,'123654897526','Ahmad','4523698','fsdjfhdjsk','Mardan','2024-09-04 16:32:30',NULL),(110,'123569871412','Bahar','123654895','jaml@gmail.com','mardan','2024-09-05 12:16:53',NULL),(111,'478562315','Abdul','45698726344','','dir','2024-09-05 12:17:58',NULL),(112,'456235879','Sardar Khan','456987123','','Sawat','2024-09-05 12:36:30',NULL),(113,'4568231656','Ahad','47562316','','Sawat','2024-09-05 12:49:23',NULL);
/*!40000 ALTER TABLE `ownertable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `id` int NOT NULL,
  `owner_id` int DEFAULT NULL,
  `plot_id` int DEFAULT NULL,
  `industry_id` int DEFAULT NULL,
  `payment_type` varchar(100) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_industry_id_industries_table_py` (`industry_id`),
  KEY `fk_owner_id_owner_table_py` (`owner_id`),
  KEY `fk_plot_id_plotstable` (`plot_id`),
  CONSTRAINT `fk_industry_id_industries_table_py` FOREIGN KEY (`industry_id`) REFERENCES `industries` (`Id`),
  CONSTRAINT `fk_owner_id_owner_table_py` FOREIGN KEY (`owner_id`) REFERENCES `ownertable` (`id`),
  CONSTRAINT `fk_plot_id_plotstable` FOREIGN KEY (`plot_id`) REFERENCES `plots` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

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
INSERT INTO `plot_ownership` VALUES (100,101,101,'2019-09-05',NULL,'Alloted','2024-09-04 13:50:48',NULL),(101,102,102,'2024-09-04',NULL,'Alloted','2024-09-04 14:10:58',NULL),(102,103,103,'2024-09-04',NULL,'Alloted','2024-09-04 15:51:15',NULL),(103,104,104,'2021-09-08',NULL,'Alloted','2024-09-04 16:02:37',NULL),(104,105,105,'2024-09-12',NULL,'Alloted','2024-09-04 16:05:19',NULL),(105,106,106,'2021-09-08',NULL,'Alloted','2024-09-04 16:19:15',NULL),(106,107,107,'2021-09-15',NULL,'Alloted','2024-09-04 16:21:44',NULL),(107,108,108,'2018-09-12',NULL,'Alloted','2024-09-04 16:26:15',NULL),(108,109,109,'2022-09-06',NULL,'Alloted','2024-09-04 16:32:30',NULL),(109,110,110,'2024-09-10',NULL,'Alloted','2024-09-05 12:16:53',NULL),(110,111,111,'2024-09-05',NULL,'Alloted','2024-09-05 12:17:58',NULL),(111,112,112,'2024-09-05',NULL,'Alloted','2024-09-05 12:36:30',NULL),(112,113,113,'2024-09-05',NULL,'Alloted','2024-09-05 12:49:23',NULL);
/*!40000 ALTER TABLE `plot_ownership` ENABLE KEYS */;
UNLOCK TABLES;

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

-- Dump completed on 2024-09-05 15:50:37
