-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: publications
-- ------------------------------------------------------
-- Server version	5.1.73

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
-- Table structure for table `document`
--

DROP TABLE IF EXISTS `document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `document` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `date_created` date NOT NULL,
  `filename` varchar(255) NOT NULL,
  `common_id` int(11) DEFAULT NULL,
  `section_id` int(11) DEFAULT NULL,
  `num_access` int(11) NOT NULL,
  `agency` enum('Aging','Buildings','Campaign Finance','Children''s Services','City Council','City Clerk','City Planning','Citywide Admin Svcs','Civilian Complaint','Comm - Police Corr','Community Assistance','Comptroller','Conflicts of Interest','Consumer Affairs','Contracts','Correction','Criminal Justice Coordinator','Cultural Affairs','DOI - Investigation','Design/Construction','Disabilities','District Atty, NY County','Districting Commission','Domestic Violence','Economic Development','Education, Dept. of','Elections, Board of','Emergency Mgmt.','Employment','Empowerment Zone','Environmental - DEP','Environmental - OEC','Environmental - ECB','Equal Employment','Film/Theatre','Finance','Fire','FISA','Health and Mental Hyg.','HealthStat','Homeless Services','Hospitals - HHC','Housing - HPD','Human Rights','Human Rsrcs - HRA','Immigrant Affairs','Independent Budget','Info. Tech. and Telecom.','Intergovernmental','International Affairs','Judiciary Committee','Juvenile Justice','Labor Relations','Landmarks','Law Department','Library - Brooklyn','Library - New York','Library - Queens','Loft Board','Management and Budget','Mayor','Metropolitan Transportation Authority','NYCERS','Operations','Parks and Recreation','Payroll Administration','Police','Police Pension Fund','Probation','Public Advocate','Public Health','Public Housing-NYCHA','Records','Rent Guidelines','Sanitation','School Construction','Small Business Svcs','Sports Commission','Standards and Appeal','Tax Appeals Tribunal','Tax Commission','Taxi and Limousine','Transportation','Trials and Hearings','Veterans - Military','Volunteer Center','Voter Assistance','Youth & Community') NOT NULL,
  `category` enum('Business and Consumers','Cultural/Entertainment','Education','Environment','Finance and Budget','Government Policy','Health','Housing and Buildings','Human Services','Labor Relations','Public Safety','Recreation/Parks','Sanitation','Technology','Transportation') NOT NULL,
  `type` enum('Annual Report','Audit Report','Bond Offering - Official Statements','Budget Report','Consultant Report','Guide - Manual','Hearing - Minutes','Legislative Document','Memoranda - Directive','Press Release','Serial Publication','Staff Report','Report') NOT NULL,
  `url` varchar(255) NOT NULL,
  `pub_or_foil` enum('Publication','FOIL') NOT NULL,
  `docText` mediumtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9578 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `document`
--
-- WHERE:  id < 11

LOCK TABLES `document` WRITE;
/*!40000 ALTER TABLE `document` DISABLE KEYS */;
INSERT INTO `document` VALUES (1,'Network NYC: Building the Broadband City','Telecommunications report from the New York City Council\'s Select Committee on Technology in Government','2003-05-19','1_Network NYC: Building the Broadband City',NULL,NULL,1,'City Council','Government Policy','Report','','Publication',NULL),(2,'Fiscal 2003 Preliminary Mayor\'s Management Report','The Mayor\'s Management Report (MMR), which is mandated by the City Charter, serves as a public report card on City services affecting the lives of New Yorkers. The MMR is released twice a year.','2003-02-24','2_Fiscal 2003 Preliminary Mayor\'s Management Report',NULL,NULL,0,'Operations','Government Policy','Serial Publication','http://nyc.gov/html/ops/pdf/2003_mmr/0203_mmr.pdf','Publication',NULL),(3,'The Comptroller\'s Comments On The Economic Assumptions Underlying The Executive Budget For Fiscal Year 2003','The Comptroller\'s Comments On The Economic Assumptions Underlying The Executive Budget For Fiscal Year 2003','2002-05-01','3_The Comptroller\'s Comments On The Economic Assumptions Underlying The Executive Budget For Fiscal Year 2003',NULL,NULL,0,'Comptroller','Finance and Budget','Budget Report','/static/data/gppPdfs/3_The Comptroller\'s Comments On The Economic Assumptions Underlying The Executive Budget For Fiscal Year 2003.pdf','Publication',NULL),(4,'Comptroller\'s Comments on The Preliminary Budget For Fiscal Year 2002 and Fiscal Plan for Fiscal Years 2002 -2006','The city is on course toward FY2002 budget balance but faces budget gaps beginning with 2003 fiscal year. FY 2002 is projected to end with a $260 million surplus, which will help the FY 2003 budget, which has a budget deficit greater than $4.5 billion. Therefore, they must borrow from the NYCTFA, about $1.5 billion. The city also faces problems such as deteriorating city infrastructure, which leads to debt service growing at twice the rate of revenues. However, despite all efforts, the FY2006 budget gap can exceed $5.5 billon.','2002-03-20','4_Comptroller\'s Comments on The Preliminary Budget For Fiscal Year 2002 and Fiscal Plan for Fiscal Years 2002 -2006',NULL,NULL,0,'Comptroller','Finance and Budget','Budget Report','/static/data/gppPdfs/4_Comptroller\'s Comments on The Preliminary Budget For Fiscal Year 2002 and Fiscal Plan for Fiscal Years 2002  2006.pdf','Publication',NULL),(5,'Report on Audit Operations for Fiscal Year 2002','Comptroller Report on Audit Operations for Fiscal Year 2002','2003-03-01','5_Report on Audit Operations for Fiscal Year 2002',NULL,NULL,0,'Comptroller','Finance and Budget','Annual Report','/static/data/gppPdfs/5_Report on Audit Operations for Fiscal Year 2002.pdf','Publication',NULL),(6,'Economic Notes Fourth Quarter 2002','Economic Notes: \n Fourth Quarter of 2002 Continues City Decline NYC RECESSION PERSISTS INTO EIGHTH CONSECUTIVE QUARTER\n Vol. XI, No. 1, March 2003','2003-03-11','6_Economic Notes Fourth Quarter 2002',NULL,NULL,0,'Comptroller','Finance and Budget','Serial Publication','/static/data/gppPdfs/6_Economic Notes Fourth Quarter 2002.pdf','Publication',NULL),(7,'Quarterly Cash Report: October - December 2002','Quarterly Cash Report \n October - December 2002','2003-03-03','7_Quarterly Cash Report: October - December 2002',NULL,NULL,0,'Comptroller','Finance and Budget','Serial Publication','/static/data/gppPdfs/7_Quarterly Cash Report  October   December 2002.pdf','Publication',NULL),(8,'Audit Report on the Internal Controls Of the Fire Department Over Billing and Collection of Inspection Fees','The FDNY has adequate controls over the billing and collection of inspection fees and whether it charges the correct fees. The FDNY billed $35.6 million in BFP inspection fees and collected $34.6 million.The FDNY has not changed its fee schedule in more than a decade. FDNY has a number of internal control weaknesses that can affect billing and collection practices.','2003-06-18','8_Audit Report on the Internal Controls Of the Fire Department Over Billing and Collection of Inspection Fees',NULL,NULL,0,'Comptroller','Finance and Budget','Audit Report','/static/data/gppPdfs/8_Audit Report on the Internal Controls Of the Fire Department Over Billing and Collection of Inspection Fees.pdf','Publication',NULL),(9,'Audit Report on the Development and Implementation Of the Housing Preservation and Development Information System','The Housing Preservation and Development Information System has become a multi-module system with a central repository of information on private and City-owned residential properties and registered property owners. The system design allowed for future enhancements and upgrades. It also met overall goals as stated in the original system justification. However, it did not follow a formal system methodology.A user satisfaction survey revealed that 57 percent of respondents would like to see changes made to HPDInfo.Lastly, the Department does not have procedures in place to ensure that security violations are recorded, documented, and reviewed.','2003-06-17','9_Audit Report on the Development and Implementation Of the Housing Preservation and Development Information System',NULL,NULL,0,'Comptroller','Finance and Budget','Audit Report','/static/data/gppPdfs/9_Audit Report on the Development and Implementation Of the Housing Preservation and Development Information System.pdf','Publication',NULL),(10,'Follow-up Audit Report on the Collection Practices and Procedures of the Health and Hospitals Corporation Related Medicaid Managed Care/ Heath Mainten','This follow-up audit report is to determine whether the NYC Health and Hospitals Corporation(HHC) implemented the recommendations made in an earlier audit. The previous audit made 22 recommendations to HHC. Of the 22, only 11 were implemented, three were partially implemented, one was not implemented, and seven were no longer applicable. This audit found that HHC has improved its billing and collection procedures. HHC still needs to improve its posting of initial payments into its computer system and the timliness of its initial billings to HMOs. Several recommendations are listed to address the problems noted in this report.','2003-06-17','10_Follow-up Audit Report on the Collection Practices and Procedures of the Health and Hospitals Corporation Related Medicaid Managed Care/ Heath Mainten',NULL,NULL,0,'Comptroller','Finance and Budget','Audit Report','/static/data/gppPdfs/10_Follow up Audit Report on the Collection Practices and Procedures of the Health and Hospitals Corporation Related Medicaid Managed Care  Heath Mainten.pdf','Publication',NULL);
/*!40000 ALTER TABLE `document` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-01-13 13:53:38
