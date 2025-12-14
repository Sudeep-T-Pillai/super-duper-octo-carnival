-- init.sql

CREATE DATABASE IF NOT EXISTS linkedin_insights_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'dev_user'@'%' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON linkedin_insights_db.* TO 'dev_user'@'%';

FLUSH PRIVILEGES;