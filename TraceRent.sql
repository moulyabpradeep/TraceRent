-- Create the database and use it
CREATE DATABASE IF NOT EXISTS trace_rent_ai;
USE trace_rent_ai;

-- Create Users Table
CREATE TABLE `users` (
  `user_id` INT PRIMARY KEY,
  `username` VARCHAR(255),
  `password` VARCHAR(255)
);

-- Create Tenant Personal Details Table
CREATE TABLE `tenant_personal_details` (
  `user_id` INT PRIMARY KEY,
  `name` VARCHAR(255),
  `email` VARCHAR(255),
  `phone` VARCHAR(15),
  `province` VARCHAR(255),
  `dob` DATE,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
);

-- Create Tenant Category Table
CREATE TABLE `tenant_category` (
  `tent_cat_id` INT PRIMARY KEY,
  `tent_category` VARCHAR(255)
);

-- Create Property Category Table
CREATE TABLE `property_category` (
  `prop_cat_id` INT PRIMARY KEY,
  `prop_category` VARCHAR(255)
);

-- Create Tenant Preferred Properties Table
CREATE TABLE `tenant_preferred_properties` (
  `tent_cat_id` INT,
  `prop_cat_id` INT,
  FOREIGN KEY (`tent_cat_id`) REFERENCES `tenant_category` (`tent_cat_id`),
  FOREIGN KEY (`prop_cat_id`) REFERENCES `property_category` (`prop_cat_id`)
);

-- Create Property Data Table
CREATE TABLE `property_data` (
  `prop_cat_id` INT,
  `unit_id` INT PRIMARY KEY,
  `prop_name` VARCHAR(255),
  `prop_type` VARCHAR(255),
  `no_of_rooms` VARCHAR(255),
  `area_code` VARCHAR(255),
  `province` VARCHAR(255),
  `country` VARCHAR(255),
  `address` VARCHAR(255),
  `rent` DECIMAL(10, 2),
  `lease_length` VARCHAR(255),
  FOREIGN KEY (`prop_cat_id`) REFERENCES `property_category` (`prop_cat_id`)
);

-- Create Behaviour Data Table
CREATE TABLE `behaviour_data` (
  `user_id` INT PRIMARY KEY,
  `prop_searched` INT,
  `prop_viewed` INT,
  `prop_saved` INT,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  FOREIGN KEY (`prop_searched`) REFERENCES `property_data` (`unit_id`),
  FOREIGN KEY (`prop_viewed`) REFERENCES `property_data` (`unit_id`),
  FOREIGN KEY (`prop_saved`) REFERENCES `property_data` (`unit_id`)
);

-- Create Location Table
CREATE TABLE `location` (
  `unit_id` INT PRIMARY KEY,
  `apt_unit_number` VARCHAR(50),
  `street_name` VARCHAR(255),
  `community` VARCHAR(255),
  `city` VARCHAR(255),
  `province` VARCHAR(255),
  `country` VARCHAR(255),
  `latitude` VARCHAR(50),
  `longitude` VARCHAR(50),
  FOREIGN KEY (`unit_id`) REFERENCES `property_data` (`unit_id`)
);

-- Create Amenities Table
CREATE TABLE `amenities` (
  `unit_id` INT PRIMARY KEY,
  `accessibility` VARCHAR(255),
  `parking` INT,
  `gym` BOOLEAN,
  `kids_playarea` BOOLEAN,
  `party_hall` BOOLEAN,
  `backyard` BOOLEAN,
  `deck` BOOLEAN,
  `in_house_laundry` BOOLEAN,
  `visitor_parking` BOOLEAN,
  `pool` BOOLEAN,
  `pet_friendly` BOOLEAN,
  FOREIGN KEY (`unit_id`) REFERENCES `property_data` (`unit_id`)
);

-- Create Tenant Financial Preferences Table
CREATE TABLE `tenant_financial_preferences` (
  `user_id` INT PRIMARY KEY,
  `monthly_income` INT,
  `monthly_savings` INT,
  `monthly_debt` INT,
  `rent_percentage` INT,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
);

-- Create Areas Table
CREATE TABLE `areas` (
  `area_id` INT PRIMARY KEY AUTO_INCREMENT,
  `community` VARCHAR(255),
  `city` VARCHAR(255),
  `province` VARCHAR(255),
  `country` VARCHAR(255)
);

-- Create Temporary User Sessions Table
CREATE TABLE `temp_user_sessions` (
  `session_id` CHAR(36) PRIMARY KEY,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `expires_at` TIMESTAMP
);

-- Create Tenant Preference Details Table
CREATE TABLE `tenant_preference_details` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `user_id` INT,
  `session_id` CHAR(36),
  `tenant_category_id` INT,
  `location_category_id` INT,
  `budget_category_id` INT,
  `school_proximity` INT,
  `hospital_proximity` INT,
  `transit_proximity` INT,
  `laundry` BOOLEAN,
  `gym` BOOLEAN,
  `pet_friendly` BOOLEAN,
  `pool` BOOLEAN,
  `is_logged_in` BOOLEAN,
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  FOREIGN KEY (`session_id`) REFERENCES `temp_user_sessions` (`session_id`),
  FOREIGN KEY (`tenant_category_id`) REFERENCES `tenant_category` (`tent_cat_id`)
);

-- Create an index for fast lookups by session ID or user ID
CREATE INDEX idx_user_or_session ON `tenant_preference_details` (`user_id`, `session_id`);

-- Insert static data for tenant categories
INSERT INTO `tenant_category` (`tent_cat_id`, `tent_category`) 
VALUES 
  (1, 'Singles'),
  (2, 'Couple'),
  (3, 'Family'),
  (4, 'Roommates');
  
-- Insert static data for property categories
INSERT INTO `property_category` (`prop_cat_id`, `prop_category`) 
VALUES 
  (1, 'Studio apartment'),
  (2, '1-bedroom apartment'),
  (3, '2-bedroom apartment'),
  (4, '3-bedroom apartment');



-- Insert statements for tenant preferred properties
INSERT INTO `tenant_preferred_properties` (`tent_cat_id`, `prop_cat_id`) 
VALUES 
  -- Singles preferences
  (1, 1),  -- Singles - Studio apartment
  (1, 2),  -- Singles - 1-bedroom apartment
  
  -- Couple preferences
  (2, 2),  -- Couple - 1-bedroom apartment
 --  (2, 1),  -- Couple - Studio apartment (if economy)

  -- Family preferences
  (3, 3),  -- Family - 2-bedroom apartment
  (3, 4),  -- Family - 3-bedroom apartment

  -- Roommates preferences
  (4, 2),  -- Roommates - 1-bedroom apartment
  (4, 3);  -- Roommates - 2-bedroom apartment
