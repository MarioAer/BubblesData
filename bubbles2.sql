-- MySQL dump 10.13  Distrib 5.6.24, for Win64 (x86_64)
--
-- Host: localhost    Database: bubbles
-- ------------------------------------------------------
-- Server version	5.6.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bubbles_bubbles`
--

DROP TABLE IF EXISTS `bubbles_bubbles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bubbles_bubbles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data` mediumtext,
  `project_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `type` varchar(45) DEFAULT 'bubble',
  `order` int(11) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bubbles_bubbles`
--

LOCK TABLES `bubbles_bubbles` WRITE;
/*!40000 ALTER TABLE `bubbles_bubbles` DISABLE KEYS */;
INSERT INTO `bubbles_bubbles` VALUES (1,'Hello first Bubble',NULL,1,'bubble',1),(2,'Hello second Bubble',NULL,1,'bubble',2);
/*!40000 ALTER TABLE `bubbles_bubbles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bubbles_meta_global`
--

DROP TABLE IF EXISTS `bubbles_meta_global`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bubbles_meta_global` (
  `name` varchar(100) NOT NULL,
  `content` varchar(100) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bubbles_meta_global`
--

LOCK TABLES `bubbles_meta_global` WRITE;
/*!40000 ALTER TABLE `bubbles_meta_global` DISABLE KEYS */;
INSERT INTO `bubbles_meta_global` VALUES ('author','Patrick Münster'),('robots','all');
/*!40000 ALTER TABLE `bubbles_meta_global` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bubbles_meta_local`
--

DROP TABLE IF EXISTS `bubbles_meta_local`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bubbles_meta_local` (
  `name` varchar(100) NOT NULL,
  `page` int(11) NOT NULL,
  `content` varchar(100) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bubbles_meta_local`
--

LOCK TABLES `bubbles_meta_local` WRITE;
/*!40000 ALTER TABLE `bubbles_meta_local` DISABLE KEYS */;
INSERT INTO `bubbles_meta_local` VALUES ('decription',1,'Dies ist eine Testseite'),('keywords',1,'Test');
/*!40000 ALTER TABLE `bubbles_meta_local` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bubbles_pages`
--

DROP TABLE IF EXISTS `bubbles_pages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bubbles_pages` (
  `id` int(8) NOT NULL AUTO_INCREMENT,
  `alias` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bubbles_pages`
--

LOCK TABLES `bubbles_pages` WRITE;
/*!40000 ALTER TABLE `bubbles_pages` DISABLE KEYS */;
INSERT INTO `bubbles_pages` VALUES (1,'testseite','Testseite'),(2,'landingbubbles','Welcome'),(3,'userbubbles','MyBubbles'),(4,'usersettings','MySettings'),(5,'content-bubbles','Bubbles'),(6,'logout','Goodbye');
/*!40000 ALTER TABLE `bubbles_pages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bubbles_projects`
--

DROP TABLE IF EXISTS `bubbles_projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bubbles_projects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` mediumtext,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bubbles_projects`
--

LOCK TABLES `bubbles_projects` WRITE;
/*!40000 ALTER TABLE `bubbles_projects` DISABLE KEYS */;
/*!40000 ALTER TABLE `bubbles_projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bubbles_projects_resources`
--

DROP TABLE IF EXISTS `bubbles_projects_resources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bubbles_projects_resources` (
  `project_id` int(11) NOT NULL,
  `resources_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Descriptes the relationship between a project and its resources.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bubbles_projects_resources`
--

LOCK TABLES `bubbles_projects_resources` WRITE;
/*!40000 ALTER TABLE `bubbles_projects_resources` DISABLE KEYS */;
/*!40000 ALTER TABLE `bubbles_projects_resources` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bubbles_quests`
--

DROP TABLE IF EXISTS `bubbles_quests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bubbles_quests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `description` mediumtext,
  `auther_id` int(11) NOT NULL,
  `editor_id` varchar(255) DEFAULT NULL,
  `state` varchar(45) NOT NULL,
  `resource` varchar(255) DEFAULT NULL,
  `language` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bubbles_quests`
--

LOCK TABLES `bubbles_quests` WRITE;
/*!40000 ALTER TABLE `bubbles_quests` DISABLE KEYS */;
/*!40000 ALTER TABLE `bubbles_quests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bubbles_resources`
--

DROP TABLE IF EXISTS `bubbles_resources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bubbles_resources` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(45) NOT NULL,
  `data` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bubbles_resources`
--

LOCK TABLES `bubbles_resources` WRITE;
/*!40000 ALTER TABLE `bubbles_resources` DISABLE KEYS */;
/*!40000 ALTER TABLE `bubbles_resources` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bubbles_settings`
--

DROP TABLE IF EXISTS `bubbles_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bubbles_settings` (
  `property` varchar(255) NOT NULL,
  `value` varchar(255) NOT NULL,
  `activated` int(1) NOT NULL DEFAULT '1',
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`property`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bubbles_settings`
--

LOCK TABLES `bubbles_settings` WRITE;
/*!40000 ALTER TABLE `bubbles_settings` DISABLE KEYS */;
INSERT INTO `bubbles_settings` VALUES ('selectedskin','1',1,''),('title','Bubbles',1,'');
/*!40000 ALTER TABLE `bubbles_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bubbles_skins`
--

DROP TABLE IF EXISTS `bubbles_skins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bubbles_skins` (
  `id` int(3) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bubbles_skins`
--

LOCK TABLES `bubbles_skins` WRITE;
/*!40000 ALTER TABLE `bubbles_skins` DISABLE KEYS */;
INSERT INTO `bubbles_skins` VALUES (1,'default');
/*!40000 ALTER TABLE `bubbles_skins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bubbles_user`
--

DROP TABLE IF EXISTS `bubbles_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bubbles_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `mail` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `role` varchar(50) NOT NULL,
  PRIMARY KEY (`id`,`name`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COMMENT='Use "MyISAM" engine because of high frequently access';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bubbles_user`
--

LOCK TABLES `bubbles_user` WRITE;
/*!40000 ALTER TABLE `bubbles_user` DISABLE KEYS */;
INSERT INTO `bubbles_user` VALUES (1,'admin','16ed28bc4745f31fc138047fec6b2c19','muenster@hdm-stuttgart.de','Web Developer / Software engineer at HdM Stuttgart','admin'),(2,'Andy','16ed28bc4745f31fc138047fec6b2c19','stiegler@hdm-stuttgart.de','Big Boss','admin'),(3,'Patrick','df3847b2a3066d37056ec462984997a4','pat.muenster@outlook.de','I am just taking a look around','user');
/*!40000 ALTER TABLE `bubbles_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-10-29 15:19:58
