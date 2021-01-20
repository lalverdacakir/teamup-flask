SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `faculty`;
DROP TABLE IF EXISTS `course`;
DROP TABLE IF EXISTS `department`;
DROP TABLE IF EXISTS `university`;
DROP TABLE IF EXISTS `userdetail`;
DROP TABLE IF EXISTS `application`;
DROP TABLE IF EXISTS `likes`;
DROP TABLE IF EXISTS `teamlist`;
DROP TABLE IF EXISTS `team`;
DROP TABLE IF EXISTS `user`;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `faculty` (
  `facId` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `facName` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`facId`),
  UNIQUE KEY `facName` (`facName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `course` (
  `courseId` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `courseName` varchar(500) NOT NULL,
  `courseCode` varchar(100) NOT NULL,
  `courseCRN` char(20) DEFAULT NULL,
  PRIMARY KEY (`courseId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;





CREATE TABLE `department` (
  `depId` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `depName` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`depId`),
  UNIQUE KEY `depName` (`depName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;





CREATE TABLE `university` (
  `uniId` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `uniName` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`uniId`),
  UNIQUE KEY `uniName` (`uniName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;





CREATE TABLE `user` (
  `userId` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(500) NOT NULL,
  `email` varchar(500) NOT NULL,
  `password` varchar(1000) NOT NULL,
  `enterDate` datetime DEFAULT NULL,
  PRIMARY KEY (`userId`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;






CREATE TABLE `userdetail` (
  `userDetailId` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `userId` int(20) unsigned NOT NULL,
  `fullName` varchar(1000) DEFAULT NULL,
  `linkCV` varchar(1000) DEFAULT NULL,
  `linkGithub` varchar(1000) DEFAULT NULL,
  `linkPhoto` varchar(1000) DEFAULT 'img/profile_img/dummy.jpg',
  `facId` int(20) unsigned DEFAULT '1',
  `depId` int(20) unsigned DEFAULT '1',
  `uniId` int(20) unsigned DEFAULT '1',
  `yearOfStudy` int(11) DEFAULT NULL,
  `gpa` float DEFAULT NULL,
  `bio` varchar(255) DEFAULT NULL,
  `likeCount` int(10) unsigned DEFAULT '0',
  PRIMARY KEY (`userDetailId`),
  KEY `userdetail_ibfk_1` (`userId`),
  KEY `userdetail_ibfk_2` (`facId`),
  KEY `userdetail_ibfk_3` (`depId`),
  KEY `userdetail_ibfk_4` (`uniId`),
  CONSTRAINT `userdetail_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `user` (`userId`) ON DELETE CASCADE,
  CONSTRAINT `userdetail_ibfk_2` FOREIGN KEY (`facId`) REFERENCES `faculty` (`facId`) ON DELETE SET NULL,
  CONSTRAINT `userdetail_ibfk_3` FOREIGN KEY (`depId`) REFERENCES `department` (`depId`) ON DELETE SET NULL,
  CONSTRAINT `userdetail_ibfk_4` FOREIGN KEY (`uniId`) REFERENCES `university` (`uniId`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `team` (
  `teamId` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `adminUserId` int(20) unsigned DEFAULT NULL,
  `teamName` varchar(500) NOT NULL,
  `courseId` int(20) unsigned DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `openSpots` int(11) NOT NULL,
  `isAccepting` tinyint(1) DEFAULT '1',
  `createDate` datetime DEFAULT NULL,
  `linkPhoto` varchar(255) DEFAULT 'img/team_img/dummy.jpeg',
  PRIMARY KEY (`teamId`),
  KEY `team_ibfk_1` (`courseId`),
  KEY `team_ibfk_2` (`adminUserId`),
  CONSTRAINT `team_ibfk_1` FOREIGN KEY (`courseId`) REFERENCES `course` (`courseId`) ON DELETE SET NULL,
  CONSTRAINT `team_ibfk_2` FOREIGN KEY (`adminUserId`) REFERENCES `user` (`userId`) ON DELETE SET NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;


CREATE TABLE `teamlist` (
  `teamListId` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `userId` int(20) unsigned NOT NULL,
  `teamId` int(20) unsigned NOT NULL,
  `enterDate` datetime DEFAULT NULL,
  `status` varchar(255) DEFAULT 'Up-to-date',
  `endDate` datetime DEFAULT NULL,
  PRIMARY KEY (`teamListId`),
  KEY `teamlist_ibfk_1` (`userId`),
  KEY `teamlist_ibfk_2` (`teamId`),
  CONSTRAINT `teamlist_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `user` (`userId`) ON DELETE CASCADE,
  CONSTRAINT `teamlist_ibfk_2` FOREIGN KEY (`teamId`) REFERENCES `team` (`teamId`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;





CREATE TABLE `application` (
  `applicationId` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `teamId` int(20) unsigned NOT NULL,
  `userId` int(20) unsigned NOT NULL,
  `content` varchar(255) DEFAULT NULL,
  `applyDate` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`applicationId`),
  KEY `application_ibfk_1` (`teamId`),
  KEY `application_ibfk_2` (`userId`),
  CONSTRAINT `application_ibfk_1` FOREIGN KEY (`teamId`) REFERENCES `team` (`teamId`) ON DELETE CASCADE,
  CONSTRAINT `application_ibfk_2` FOREIGN KEY (`userId`) REFERENCES `user` (`userId`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




CREATE TABLE `likes` (
  `likeId` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `likedUserId` int(20) unsigned NOT NULL,
  `userId` int(20) unsigned NOT NULL,
  PRIMARY KEY (`likeId`),
  KEY `likes_ibfk_1` (`likedUserId`),
  KEY `likes_ibfk_2` (`userId`),
  CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`likedUserId`) REFERENCES `user` (`userId`) ON DELETE CASCADE,
  CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`userId`) REFERENCES `user` (`userId`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




