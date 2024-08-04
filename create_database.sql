-- -----------------------------------------------------
-- Schema TreeTalk
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS login;
CREATE SCHEMA login;
USE login;

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
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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

