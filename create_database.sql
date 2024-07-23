-- -----------------------------------------------------
-- Schema login
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS login;
CREATE SCHEMA login;
USE login;

-- -----------------------------------------------------
-- Table login.users
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS login.users (
  user_id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(20) NOT NULL UNIQUE,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(320) NOT NULL COMMENT 'Maximum email address length according to RFC5321 section 4.5.3.1 is 320 characters (64 for local-part, 1 for at sign, 255 for domain)',
  password_hash CHAR(64) NOT NULL COMMENT 'SHA256 password hash stored in hexadecimal (64 characters)',
  date_of_birth DATE NOT NULL,
  location VARCHAR(100) NOT NULL,
  profile_pic VARCHAR(100) DEFAULT 'default.png',
  role ENUM('user', 'staff', 'admin') NOT NULL,
  PRIMARY KEY (user_id));

-- -----------------------------------------------------
-- Table login.staffs
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS login.staffs (
  user_id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(20) NOT NULL UNIQUE,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(320) NOT NULL COMMENT 'Maximum email address length according to RFC5321 section 4.5.3.1 is 320 characters (64 for local-part, 1 for at sign, 255 for domain)',
  password_hash CHAR(64) NOT NULL COMMENT 'SHA256 password hash stored in hexadecimal (64 characters)',
  date_of_birth DATE NOT NULL,
  location VARCHAR(100) NOT NULL,
  profile_pic VARCHAR(100) DEFAULT 'default.png',
  role ENUM('user', 'staff', 'admin') NOT NULL,
  PRIMARY KEY (user_id));

-- -----------------------------------------------------
-- Table login.admins
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS login.admins (
  user_id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(20) NOT NULL UNIQUE,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(320) NOT NULL COMMENT 'Maximum email address length according to RFC5321 section 4.5.3.1 is 320 characters (64 for local-part, 1 for at sign, 255 for domain)',
  password_hash CHAR(64) NOT NULL COMMENT 'SHA256 password hash stored in hexadecimal (64 characters)',
  date_of_birth DATE NOT NULL,
  location VARCHAR(100) NOT NULL,
  profile_pic VARCHAR(100) DEFAULT 'default.png',
  role ENUM('user', 'staff', 'admin') NOT NULL,
  PRIMARY KEY (user_id));