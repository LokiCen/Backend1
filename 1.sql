-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: retrievalsystem
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `backuprecord`
--

DROP TABLE IF EXISTS `backuprecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `backuprecord` (
  `id` int NOT NULL AUTO_INCREMENT,
  `admin_id` int DEFAULT NULL,
  `backup_date` datetime DEFAULT NULL,
  `backup_filename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  CONSTRAINT `backuprecord_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backuprecord`
--

LOCK TABLES `backuprecord` WRITE;
/*!40000 ALTER TABLE `backuprecord` DISABLE KEYS */;
INSERT INTO `backuprecord` VALUES (12,10,'2024-09-05 10:31:54','backup_20240905_103153.sql'),(13,10,'2024-09-05 10:33:37','backup_20240905_103336.sql'),(14,10,'2024-09-05 10:36:21','backup_20240905_103620.sql'),(15,10,'2024-09-05 10:37:33','backup_20240905_103733.sql'),(16,10,'2024-09-05 10:39:13','backup_20240905_103912.sql'),(17,10,'2024-09-05 10:39:38','backup_20240905_103937.sql'),(18,10,'2024-09-06 09:30:06','backup_20240906_093005.sql'),(19,10,'2024-09-06 15:41:15','backup_20240906_154114.sql');
/*!40000 ALTER TABLE `backuprecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backupsettings`
--

DROP TABLE IF EXISTS `backupsettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `backupsettings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `admin_id` int DEFAULT NULL,
  `backup_frequency` varchar(255) DEFAULT NULL,
  `backup_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  CONSTRAINT `backupsettings_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backupsettings`
--

LOCK TABLES `backupsettings` WRITE;
/*!40000 ALTER TABLE `backupsettings` DISABLE KEYS */;
INSERT INTO `backupsettings` VALUES (1,10,'month','D:/code/RetrievalSystemBackend/backup/');
/*!40000 ALTER TABLE `backupsettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faq`
--

DROP TABLE IF EXISTS `faq`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faq` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question` text,
  `answer` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faq`
--

LOCK TABLES `faq` WRITE;
/*!40000 ALTER TABLE `faq` DISABLE KEYS */;
/*!40000 ALTER TABLE `faq` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedbackandsuggestion`
--

DROP TABLE IF EXISTS `feedbackandsuggestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedbackandsuggestion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `content` text,
  `date` datetime DEFAULT NULL,
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'pending-待处理状态; in_progress-正在处理中; resolved-问题已解决; closed-不再处理',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `feedbackandsuggestion_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedbackandsuggestion`
--

LOCK TABLES `feedbackandsuggestion` WRITE;
/*!40000 ALTER TABLE `feedbackandsuggestion` DISABLE KEYS */;
INSERT INTO `feedbackandsuggestion` VALUES (1,1,'后端还没做完','2024-08-30 07:05:13','pending'),(2,1,'df','2024-08-30 07:24:06','pending'),(7,1,'hello','2024-09-03 02:39:04','pending'),(8,1,'你好','2024-09-03 03:24:48','pending'),(9,5,'11111313432425red','2024-09-03 07:13:52','pending'),(10,5,'1225w4t4wfwfse','2024-09-03 07:16:05','pending'),(11,5,'asfafaega','2024-09-03 07:52:37','pending'),(12,5,'qwdqw','2024-09-03 07:54:31','pending'),(13,5,'acfasdfsa','2024-09-03 07:56:10','pending'),(14,5,'acfasdfsaggg','2024-09-03 07:56:44','pending'),(15,5,'acfasdfsagggefdcf','2024-09-03 07:57:07','pending'),(16,5,'dsgsfc','2024-09-03 08:04:52','pending'),(17,5,'dsgsfcsef','2024-09-03 08:05:04','pending'),(18,5,'dsgsfcsef;,ll,p','2024-09-03 08:06:21','pending'),(19,5,'dsgsfcsef;,ll,p121','2024-09-03 08:06:46','pending'),(20,5,'sdsrvgf4we','2024-09-03 08:23:52','pending'),(21,1,'efgdhr','2024-09-04 03:51:47','pending'),(22,1,'gsgrh','2024-09-04 03:53:54','pending'),(23,12,'eaeghbtejsqasessdfhfddfff','2024-09-06 01:16:15','pending'),(24,1,'shrgdd','2024-09-06 07:39:33','pending'),(25,1,'hihello','2024-09-09 06:50:25','pending'),(26,14,'hihello','2024-09-09 08:23:47','pending');
/*!40000 ALTER TABLE `feedbackandsuggestion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `image`
--

DROP TABLE IF EXISTS `image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `image` (
  `id` int NOT NULL AUTO_INCREMENT,
  `path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `format` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `resolution` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40456 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image`
--

LOCK TABLES `image` WRITE;
/*!40000 ALTER TABLE `image` DISABLE KEYS */;
INSERT INTO `image` VALUES (1,'D:\\code\\RetrievalSystemBackend\\pictures\\1000268201_693b08cb0e.jpg','A child in a pink dress is climbing up a set of stairs in an entry way .',NULL,NULL,NULL)

/*!40000 ALTER TABLE `searchhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `smartqa`
--

DROP TABLE IF EXISTS `smartqa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `smartqa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `question` text,
  `answer` text,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `smartqa_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `smartqa`
--

LOCK TABLES `smartqa` WRITE;
/*!40000 ALTER TABLE `smartqa` DISABLE KEYS */;
INSERT INTO `smartqa` VALUES (1,1,'hi','Hello 👋! I\'m ChatGLM（智谱清言）, the artificial intelligence assistant, nice to meet you. Feel free to ask me any questions.','2024-09-09 14:34:39'),(2,1,'{    \"code\": 0,    \"data\": null,    \"message\": \"Hello 👋! I\'m ChatGLM（智谱清言）, the artificial intelligence assistant, nice to meet you. Feel free to ask me any questions.\"}这是什么','这是一个JSON格式的数据，通常用于在网络上传输数据。具体来说，这个JSON对象包含三个键（key）：\n\n- `\"code\"`: 表示一个状态码，在这里它的值是 `0`。通常，状态码用来表示请求的结果，例如成功或错误。在这个例子中，`0` 可能意味着成功或者是一个没有具体错误代码的状态。\n\n- `\"data\"`: 通常用于存放实际的数据内容。在这个例子中，它的值是 `null`，意味着没有要返回的数据。\n\n- `\"message\"`: 包含了一个文本消息，这里是用来向用户传达信息的。在这个例子中，消息表示一个友好的问候，并介绍了自己是ChatGLM（智谱清言），是一个人工智能助手，还鼓励用户提问。\n\n这样的JSON数据通常是由一个服务器或API返回的，作为对客户端请求的响应。在这个例子中，它可能是作为一个交互式API的“欢迎”响应，告知用户该服务可用并邀请他们进行交互。','2024-09-09 14:35:42');
/*!40000 ALTER TABLE `smartqa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `text`
--

DROP TABLE IF EXISTS `text`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `text` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `content` text,
  `source` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `text`
--

LOCK TABLES `text` WRITE;
/*!40000 ALTER TABLE `text` DISABLE KEYS */;
/*!40000 ALTER TABLE `text` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `nickname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `permission_level` int(1) unsigned zerofill DEFAULT '1',
  `balance` decimal(10,2) unsigned zerofill DEFAULT NULL,
  `search_condition_id` int(10) unsigned zerofill DEFAULT NULL,
  `filter_condition_id` int(10) unsigned zerofill DEFAULT NULL,
  `delete_flag` tinyint DEFAULT '0',
  `birthday` date DEFAULT NULL,
  `sex` int DEFAULT NULL,
  `description` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'xm','11423','D:/code/RetrievalSystemBackend/avatar/1725518177.png','weg','123',1,00000000.00,0000000000,0000000000,0,'2024-09-12',1,'1q2t3'),(2,'xmq','0','0','12@qq.com','123',1,00000000.00,0000000000,0000000000,0,NULL,NULL,NULL),(5,'111','114',NULL,'1@1.222','333',1,NULL,NULL,NULL,0,'2024-09-19',NULL,'22'),(6,'1112','sss',NULL,'1@1.3','11111111a',1,NULL,NULL,NULL,0,NULL,NULL,NULL),(7,'114514','114514',NULL,'1@1.114514','1145141919810a',1,NULL,NULL,NULL,0,NULL,NULL,NULL),(8,'sss','22',NULL,'1@1.8','11111111a',1,NULL,NULL,NULL,0,NULL,NULL,NULL),(9,'333','sdhfbsfr',NULL,'214235@1.11','2222222221a',1,NULL,NULL,NULL,0,NULL,NULL,NULL),(10,'admin',NULL,NULL,NULL,'123',0,NULL,NULL,NULL,0,NULL,NULL,NULL),(11,'sssss','rehr',NULL,'12143@1.fd','5555555a',1,NULL,NULL,NULL,0,NULL,NULL,NULL),(12,'test111','afrfr',NULL,'adsdvsr@1fde.1','7777777a',1,NULL,NULL,NULL,0,NULL,NULL,NULL),(13,'test222','aqgte','D:/code/RetrievalSystemBackend/avatar/1725584787.png','szdh','222',1,NULL,NULL,NULL,0,'2024-09-12',NULL,'dsg'),(14,'www','www',NULL,'www','123',1,00000011.00,NULL,NULL,0,NULL,NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-09 16:53:14
