-- -----------------------------------------------------
-- Schema TreeTalk
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Table TreeTalk.moderator_admin
-- -----------------------------------------------------


-- CREATE TABLE IF NOT EXISTS `moderator_admin`
-- (
-- `staff_id` INT auto_increment PRIMARY KEY NOT NULL,
-- `first_name` varchar(25),
-- `last_name` varchar(25) not null,
-- `email` varchar(320) not null,
-- `username` varchar(100) NOT NULL,
-- `password` varchar(255) NOT NULL,
-- `address` varchar(320) not null,
-- `work_phone_number` varchar(15) not null,
-- `hire_date` date NOT NULL,
-- `position` varchar(25) not null,
-- `department` varchar(25) not null,
-- `status` tinyint default 1
-- );


-- -----------------------------------------------------
-- Table TreeTalk.users
-- -----------------------------------------------------

CREATE DATABASE IF NOT EXISTS TreeTalk;
USE TreeTalk;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(320) NOT NULL,
    password CHAR(64) NOT NULL,
    birth_date DATE NOT NULL,
    location VARCHAR(50) NOT NULL,
    profile_image VARCHAR(255) DEFAULT 'default.png',
    role ENUM('member', 'moderator', 'admin') NOT NULL DEFAULT 'member',
    status ENUM('active', 'inactive') NOT NULL DEFAULT 'active'
);



-- -----------------------------------------------------
-- Table TreeTalk.messages
-- -----------------------------------------------------

CREATE TABLE messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) DEFAULT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_path VARCHAR(255) DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


-- -----------------------------------------------------
-- Table TreeTalk.replies
-- -----------------------------------------------------

CREATE TABLE replies (
    reply_id INT AUTO_INCREMENT PRIMARY KEY,
    message_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    parent_id INT NULL,
    FOREIGN KEY (message_id) REFERENCES messages(message_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (parent_id) REFERENCES replies(reply_id) -- This allows replies to reference other replies
);

-- -----------------------------------------------------
-- Table TreeTalk.likes
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS likes (
    like_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message_id INT NOT NULL,
    type ENUM('like', 'dislike') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    count INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (message_id) REFERENCES messages(message_id)
);

-- -----------------------------------------------------
-- Table TreeTalk.media
-- -----------------------------------------------------
CREATE TABLE `media` (
    `media_id` INT AUTO_INCREMENT PRIMARY KEY,
    `message_id` INT,
    `filename` VARCHAR(255),
    `uploaded_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`message_id`) REFERENCES `messages`(`message_id`) ON DELETE CASCADE
);

