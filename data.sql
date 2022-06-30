-- MySQL dump 10.13  Distrib 8.0.29, for Linux (x86_64)
--
-- Host: localhost    Database: data_anl
-- ------------------------------------------------------
-- Server version	8.0.29-0ubuntu0.20.04.3

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
-- Table structure for table `connection`
--

DROP TABLE IF EXISTS `connection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `connection` (
  `u_id` varchar(100) NOT NULL,
  `conn_name` varchar(100) NOT NULL,
  `host` varchar(100) NOT NULL,
  `port` int NOT NULL,
  `db_user` varchar(100) NOT NULL,
  `db_password` varchar(100) NOT NULL,
  `db_name` varchar(100) NOT NULL,
  `db_type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`u_id`,`conn_name`),
  CONSTRAINT `fk_connection` FOREIGN KEY (`u_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `connection`
--

LOCK TABLES `connection` WRITE;
/*!40000 ALTER TABLE `connection` DISABLE KEYS */;
INSERT INTO `connection` VALUES ('biter','conn_data_anl','127.0.0.1',3306,'root','root','data_anl','mysql'),('biter','CONN_DEMO','127.0.0.1',8086,'root','root','NOAA_water_database','influxdb'),('biter','数据分析数据库','127.0.0.1',3306,'root','root','data_anl','mysql');
/*!40000 ALTER TABLE `connection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `datasrc`
--

DROP TABLE IF EXISTS `datasrc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `datasrc` (
  `u_id` varchar(100) NOT NULL,
  `file_name` varchar(100) NOT NULL,
  `path` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`u_id`,`file_name`),
  CONSTRAINT `fk_datasrc` FOREIGN KEY (`u_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datasrc`
--

LOCK TABLES `datasrc` WRITE;
/*!40000 ALTER TABLE `datasrc` DISABLE KEYS */;
INSERT INTO `datasrc` VALUES ('biter','output_dataset.xlsx',NULL),('biter','PM2.5_pred.csv',NULL),('biter','PM2.5_train.csv',NULL),('biter','中国银行股价.csv',NULL),('biter','北京房价.csv',NULL),('biter','特斯拉股票2010-2020.csv',NULL),('biter','股票数据(含缺失值).xlsx',NULL),('biter','银行客户流失_1.csv',NULL),('biter','银行客户流失_2.csv',NULL),('user','bank_customer_churn_prd.csv',NULL),('user','bank_customer_churn.csv',NULL),('user','PM2.5_train.csv',NULL),('wangmingyu','高盛银行历史股价.csv',NULL);
/*!40000 ALTER TABLE `datasrc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `model`
--

DROP TABLE IF EXISTS `model`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `model` (
  `u_id` varchar(100) NOT NULL,
  `model_name` varchar(100) NOT NULL,
  `status` int NOT NULL,
  `path` varchar(200) DEFAULT NULL,
  `dataset` varchar(100) DEFAULT NULL,
  `dataset_size` varchar(100) DEFAULT NULL,
  `dataset_split` varchar(100) DEFAULT NULL,
  `model_desc` varchar(100) DEFAULT NULL,
  `fields` varchar(300) DEFAULT NULL,
  `label` varchar(100) DEFAULT NULL,
  `task` varchar(50) DEFAULT NULL,
  `fit_time` varchar(200) DEFAULT NULL,
  `eval_metric` varchar(200) DEFAULT NULL,
  `industry` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`u_id`,`model_name`),
  CONSTRAINT `fk_model` FOREIGN KEY (`u_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model`
--

LOCK TABLES `model` WRITE;
/*!40000 ALTER TABLE `model` DISABLE KEYS */;
INSERT INTO `model` VALUES ('biter','model1',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'智能数据分析'),('biter','model2',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'智能数据分析'),('biter','PM2.5',1,NULL,'PM2.5_train.csv','共3120行10列','训练集共2496行, 测试集共624行','PM2.5','1,2,3,4,5,6,7,8,9,10','10','回归','2022-06-08 22:44:04','R2(决定系数) = 0.8995861937851869','智能数据分析'),('biter','供应链风险预测',1,NULL,'output_dataset.csv','共1000行29列','训练集共800行, 测试集共200行','供应链风险预测','风险情况,发动机的系数,发动机的供应商指标1,发动机的供应商指标2,发动机的供应商指标3,驱动系统的系数,驱动系统的供应商指标1,驱动系统的供应商指标2,驱动系统的供应商指标3,转向系统的系数,转向系统的供应商指标1,转向系统的供应商指标2,转向系统的供应商指标3,空调的系数,空调的供应商指标1,空调的供应商指标2,空调的供应商指标3,车身的系数,车身的供应商指标1,车身的供应商指标2,车身的供应商指标3,玻璃的系数,玻璃的供应商指标1,玻璃的供应商指标2,玻璃的供应商指标3,其它的系数,其它的供应商指标1,其它的供应商指标2,其它的供应商指标3','风险情况','分类','2022-06-28 22:49:46','Accuracy(准确率) = 0.97125','智能数据分析'),('biter','流失预测模型',1,NULL,'银行客户流失_1.csv','共10000行15列','训练集共8000行, 测试集共2000行','银行客户流失预测','信用评分,年限,余额,购买的银行产品数量,薪资估计,是否退出','是否退出','分类','2022-06-25 21:32:23','Accuracy(准确率) = 0.914625','汽车行业数据分析'),('biter','特斯拉',1,NULL,'特斯拉股票2010-2020.csv','共2416行7列','训练集共1933行, 测试集共483行','特斯拉','开盘价,最高价,最低价,收盘价,调整后的收盘价','调整后的收盘价','回归','2022-07-01 01:04:24','R2(决定系数) = 0.9999054052660297','智能数据分析'),('biter','银行用户流失预测模型',1,NULL,'银行客户流失_1.csv','共10000行15列','训练集共8000行, 测试集共2000行','银行用户流失预测模型，预测用户是否流失','信用评分,地理位置,年限,余额,购买的银行产品数量,是否有信用卡,是否是活跃用户,薪资估计,是否退出','是否退出','分类','2022-05-03 12:30:56','Accuracy(准确率) = 0.86225','智能数据分析'),('user','预测',1,NULL,'bank_customer_churn.csv','共9000行14列','训练集共7200行, 测试集共1800行','预测','CreditScore,Age,Tenure,Balance,NumOfProducts,EstimatedSalary,Exited','Exited','分类','2022-06-30 19:01:27','Accuracy(准确率) = 0.8491666666666666','智能数据分析');
/*!40000 ALTER TABLE `model` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `processplatform`
--

DROP TABLE IF EXISTS `processplatform`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `processplatform` (
  `u_id` varchar(100) NOT NULL,
  `file_name` varchar(100) NOT NULL,
  `path` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`u_id`,`file_name`),
  CONSTRAINT `fk_processplatform` FOREIGN KEY (`u_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `processplatform`
--

LOCK TABLES `processplatform` WRITE;
/*!40000 ALTER TABLE `processplatform` DISABLE KEYS */;
INSERT INTO `processplatform` VALUES ('biter','output_dataset',NULL),('biter','PM2.5_pred',NULL),('biter','PM2.5_train',NULL),('biter','中国银行股价',NULL),('biter','北京房价',NULL),('biter','拆分',NULL),('biter','特斯拉股票2010-2020',NULL),('biter','银行客户流失_1',NULL),('biter','银行客户流失_2',NULL),('biter','高盛银行历史股价',NULL),('user','123',NULL),('user','bank_customer_churn',NULL),('user','bank_customer_churn_prd',NULL),('user','PM2.5_train',NULL),('user','test',NULL),('wangmingyu','高盛银行历史股价',NULL);
/*!40000 ALTER TABLE `processplatform` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report`
--

DROP TABLE IF EXISTS `report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report` (
  `u_id` varchar(100) NOT NULL,
  `report_name` varchar(100) NOT NULL,
  `path` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`u_id`,`report_name`),
  CONSTRAINT `fk_report` FOREIGN KEY (`u_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report`
--

LOCK TABLES `report` WRITE;
/*!40000 ALTER TABLE `report` DISABLE KEYS */;
INSERT INTO `report` VALUES ('biter','PM2.5分析报告',NULL),('biter','分析',NULL),('biter','高盛银行历史股价',NULL),('user','report',NULL);
/*!40000 ALTER TABLE `report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stat`
--

DROP TABLE IF EXISTS `stat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stat` (
  `u_id` varchar(100) NOT NULL,
  `stat_file_name` varchar(100) NOT NULL,
  `path` varchar(200) DEFAULT NULL,
  `industry` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`u_id`,`stat_file_name`),
  CONSTRAINT `fk_stat` FOREIGN KEY (`u_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stat`
--

LOCK TABLES `stat` WRITE;
/*!40000 ALTER TABLE `stat` DISABLE KEYS */;
INSERT INTO `stat` VALUES ('biter','PM2.5统计',NULL,'智能数据分析'),('biter','中国银行',NULL,'智能数据分析'),('biter','分析',NULL,'智能数据分析'),('biter','汽车统计',NULL,'汽车行业数据分析'),('biter','统计分析',NULL,'智能数据分析'),('user','stat',NULL,'智能数据分析');
/*!40000 ALTER TABLE `stat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` varchar(100) NOT NULL,
  `user_password` varchar(100) NOT NULL,
  `user_mail` varchar(100) NOT NULL,
  `user_status` int NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('000','000','000',0),('123','wmy','1120180298@qq.com',0),('123456','123456','123456',0),('biter','biter','1120180298@bit.edu.cn',1),('user','user','1120180298',0),('wangmingyu','wmy','2318852986@qq.com',0),('wmy','wmy','1120180298@qq.com',0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visual`
--

DROP TABLE IF EXISTS `visual`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `visual` (
  `u_id` varchar(100) NOT NULL,
  `visual_file_name` varchar(100) NOT NULL,
  `path` varchar(200) DEFAULT NULL,
  `industry` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`u_id`,`visual_file_name`),
  CONSTRAINT `fk_visual` FOREIGN KEY (`u_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visual`
--

LOCK TABLES `visual` WRITE;
/*!40000 ALTER TABLE `visual` DISABLE KEYS */;
INSERT INTO `visual` VALUES ('biter','PM2.5可视化',NULL,'智能数据分析'),('biter','中国银行',NULL,'智能数据分析'),('biter','股票',NULL,'汽车行业数据分析'),('biter','高盛银行',NULL,'智能数据分析'),('user','AGE',NULL,'智能数据分析');
/*!40000 ALTER TABLE `visual` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `worksheet`
--

DROP TABLE IF EXISTS `worksheet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `worksheet` (
  `u_id` varchar(100) NOT NULL,
  `file_name` varchar(100) NOT NULL,
  `path` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`u_id`,`file_name`),
  CONSTRAINT `fk_worksheet` FOREIGN KEY (`u_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `worksheet`
--

LOCK TABLES `worksheet` WRITE;
/*!40000 ALTER TABLE `worksheet` DISABLE KEYS */;
INSERT INTO `worksheet` VALUES ('biter','output_dataset',NULL),('biter','PM2.5_pred',NULL),('biter','PM2.5_train',NULL),('biter','中国银行股价',NULL),('biter','北京房价',NULL),('biter','水文数据',NULL),('biter','特斯拉股票2010-2020',NULL),('biter','股票数据(含缺失值)',NULL),('biter','银行客户流失_1',NULL),('biter','银行客户流失_2',NULL),('biter','高盛银行历史股价',NULL),('user','bank_customer_churn',NULL),('user','bank_customer_churn_prd',NULL),('user','PM2.5_train',NULL),('wangmingyu','高盛银行历史股价',NULL);
/*!40000 ALTER TABLE `worksheet` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-07-01  2:11:42
