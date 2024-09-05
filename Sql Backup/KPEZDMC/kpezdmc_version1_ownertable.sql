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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-05 15:50:23
