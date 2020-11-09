/*
Navicat MariaDB Data Transfer

Source Server         : Txy
Source Server Version : 50556
Source Host           : 115.159.101.208:3306
Source Database       : article_spider

Target Server Type    : MariaDB
Target Server Version : 50556
File Encoding         : 65001

Date: 2018-01-26 15:00:37
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for article
-- ----------------------------
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article` (
  `title` varchar(255) NOT NULL,
  `create_date` date DEFAULT NULL,
  `url` varchar(300) NOT NULL,
  `url_object_id` varchar(50) NOT NULL,
  `front_image_url` varchar(300) DEFAULT NULL,
  `front_image_path` varchar(200) DEFAULT NULL,
  `comment_nums` int(11) NOT NULL,
  `fav_nums` int(11) NOT NULL,
  `parise_nums` int(11) NOT NULL,
  `tags` varchar(200) DEFAULT NULL,
  `content` longtext NOT NULL,
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of article
-- ----------------------------

-- ----------------------------
-- Table structure for jobbole_article
-- ----------------------------
DROP TABLE IF EXISTS `jobbole_article`;
CREATE TABLE `jobbole_article` (
  `title` varchar(255) NOT NULL,
  `create_date` date DEFAULT NULL,
  `url` varchar(300) NOT NULL,
  `url_object_id` varchar(50) NOT NULL,
  `front_image_url` varchar(300) DEFAULT NULL,
  `front_image_path` varchar(200) DEFAULT NULL,
  `comment_nums` int(11) DEFAULT NULL,
  `fav_nums` int(11) DEFAULT NULL,
  `parise_nums` int(11) DEFAULT NULL,
  `tags` varchar(200) DEFAULT NULL,
  `content` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of jobbole_article
-- ----------------------------
INSERT INTO `jobbole_article` VALUES ('汇编语言入门教程', '2018-01-21', 'http://blog.jobbole.com/113509/', '', null, null, null, '1', null, null, '');
INSERT INTO `jobbole_article` VALUES ('汇编语言入门教程', '2018-01-21', 'http://blog.jobbole.com/113509/', '', null, null, null, '1', null, null, '');
INSERT INTO `jobbole_article` VALUES ('汇编语言入门教程', '2018-01-21', 'http://blog.jobbole.com/113509/', '', null, null, null, '1', null, null, '');
INSERT INTO `jobbole_article` VALUES ('Linux 的 fmt 命令用法与案例', '2018-01-22', 'http://blog.jobbole.com/113479/', '', null, null, null, '0', null, null, '');
INSERT INTO `jobbole_article` VALUES ('在 Linux 的终端上伪造一个好莱坞黑客的屏幕', '2018-01-22', 'http://blog.jobbole.com/113471/', '', null, null, null, '1', null, null, '');
INSERT INTO `jobbole_article` VALUES ('汇编语言入门教程', '2018-01-22', 'http://blog.jobbole.com/113509/', '', null, null, null, '1', null, null, '');
INSERT INTO `jobbole_article` VALUES ('AI 玩跳一跳的正确姿势，跳一跳 Auto-Jump 算法详解', '2018-01-22', 'http://blog.jobbole.com/113493/', '', null, null, null, '1', null, null, '');
INSERT INTO `jobbole_article` VALUES ('10 个用于 AI 开发的框架和库', '2018-01-22', 'http://blog.jobbole.com/113499/', '', null, null, null, '1', null, null, '');
INSERT INTO `jobbole_article` VALUES ('请停止结对编程', '2018-01-22', 'http://blog.jobbole.com/113474/', '', null, null, null, '0', null, null, '');
INSERT INTO `jobbole_article` VALUES ('当你在 Linux 上启动一个进程时会发生什么？', '2018-01-22', 'http://blog.jobbole.com/113506/', '', null, null, null, '1', null, null, '');
INSERT INTO `jobbole_article` VALUES ('为小白准备的重要 Docker 命令说明', '2018-01-22', 'http://blog.jobbole.com/113490/', '', null, null, null, '2', null, null, '');
INSERT INTO `jobbole_article` VALUES ('Pick：一款 Linux 上的命令行模糊搜索工具', '2018-01-22', 'http://blog.jobbole.com/113480/', '', null, null, null, '0', null, null, '');
INSERT INTO `jobbole_article` VALUES ('回顾 2017 年发布的 10 个新数据库系统', '2018-01-22', 'http://blog.jobbole.com/113486/', '', null, null, null, '1', null, null, '');
INSERT INTO `jobbole_article` VALUES ('区块链初学者指南', '2018-01-22', 'http://blog.jobbole.com/113467/', '', null, null, null, '0', null, null, '');
INSERT INTO `jobbole_article` VALUES ('加密货币的本质', '2018-01-22', 'http://blog.jobbole.com/113463/', '', null, null, null, '1', null, null, '');
INSERT INTO `jobbole_article` VALUES ('操作系统级虚拟化概述', '2018-01-22', 'http://blog.jobbole.com/113459/', '', null, null, null, '1', null, null, '');
INSERT INTO `jobbole_article` VALUES ('把docker镜像当作桌面系统来用', '2018-01-22', 'http://blog.jobbole.com/113448/', '', null, null, null, '2', null, null, '');
INSERT INTO `jobbole_article` VALUES ('利用副项目找 IT 工作，需要满足这 3 个原则', '2018-01-22', 'http://blog.jobbole.com/113443/', '', null, null, null, '1', null, null, '');
INSERT INTO `jobbole_article` VALUES ('比特币入门教程', '2018-01-22', 'http://blog.jobbole.com/113429/', '', null, null, null, '5', null, null, '');
INSERT INTO `jobbole_article` VALUES ('绝不要用的 Linux 命令 ！', '2018-01-22', 'http://blog.jobbole.com/113437/', '', null, null, null, '5', null, null, '');
INSERT INTO `jobbole_article` VALUES ('12 条用于 Linux 的 MySQL/MariaDB 安全最佳实践', '2018-01-22', 'http://blog.jobbole.com/113422/', '', null, null, null, '2', null, null, '');
INSERT INTO `jobbole_article` VALUES ('通过实例学习 tcpdump 命令', '2018-01-22', 'http://blog.jobbole.com/113452/', '', null, null, null, '2', null, null, '');
INSERT INTO `jobbole_article` VALUES ('区块链入门教程', '2018-01-22', 'http://blog.jobbole.com/113428/', '', null, null, null, '6', null, null, '');
