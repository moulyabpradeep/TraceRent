-- Create the database and use it
CREATE DATABASE IF NOT EXISTS trace_rent_ai;
USE trace_rent_ai;

CREATE TABLE `user` (
  `user_id` INT PRIMARY KEY AUTO_INCREMENT,
  `username` VARCHAR(255) UNIQUE,
  `password` VARCHAR(255),
  `name` VARCHAR(255),
  `email` VARCHAR(255) UNIQUE,
  `phone` VARCHAR(15)
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
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `tent_cat_id` INT,
  `prop_cat_id` INT,
  FOREIGN KEY (`tent_cat_id`) REFERENCES `tenant_category` (`tent_cat_id`),
  FOREIGN KEY (`prop_cat_id`) REFERENCES `property_category` (`prop_cat_id`)
);
-- Create Property Data Table
CREATE TABLE `property_data` (
  `unit_id` INT PRIMARY KEY,
  `unit_number` INT,
  `prop_cat_id` INT,
  `prop_name` VARCHAR(255),
  `prop_description` VARCHAR(255),
  `prop_type` VARCHAR(255),
  `no_of_rooms` VARCHAR(255),
  `no_of_baths` VARCHAR(255),
  `rent` INT,
  `area_sq_ft` DECIMAL(10, 2),
  `lease_length` VARCHAR(255),
  FOREIGN KEY (`prop_cat_id`) 
    REFERENCES `property_category` (`prop_cat_id`) 
    ON DELETE CASCADE  -- Add this line for cascading delete
);

CREATE TABLE `property_media` (
  `media_id` INT AUTO_INCREMENT PRIMARY KEY,
  `unit_id` INT,  -- Foreign Key referencing property_data
  `category` ENUM('front', 'living_room', 'bedroom', 'kitchen', 'bathroom', 'balcony', 'garden', 'backyard', 'pool', 'misc') DEFAULT 'front' NOT NULL,
  `photo_url` VARCHAR(255) NOT NULL,  -- URL for the photo
  `sequence` INT NOT NULL,  -- Sequence of the photo within the category
  FOREIGN KEY (`unit_id`) 
    REFERENCES `property_data` (`unit_id`) 
    ON DELETE CASCADE
);


-- Create Location Table
CREATE TABLE `location` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `unit_id` INT,
  `location_cat_id` INT,
  `apt_unit_number` VARCHAR(50) NOT NULL,
  `street_name` VARCHAR(255) NOT NULL,
  `community` VARCHAR(255),
  `city` VARCHAR(255) NOT NULL,
  `province` VARCHAR(255),
  `country` VARCHAR(255),
  `zip_code` VARCHAR(255),
  `latitude` DECIMAL(10,7) NOT NULL,
  `longitude` DECIMAL(10,7) NOT NULL,
  `school_proximity` INT NOT NULL, -- in METERS
  `transit_proximity` INT NOT NULL, -- in METERS
  `hospital_proximity` INT NOT NULL, -- in METERS
  FOREIGN KEY (`unit_id`) 
    REFERENCES `property_data` (`unit_id`) 
    ON DELETE CASCADE  -- Add this line for cascading delete
);


-- Create Amenities Table
CREATE TABLE `amenities` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `unit_id` INT,
  `parking` INT,
  `wheelchair_accessibility` BOOLEAN DEFAULT 0,
  `gym` BOOLEAN DEFAULT 0,
  `kids_playarea` BOOLEAN DEFAULT 0,
  `party_hall` BOOLEAN DEFAULT 0,
  `backyard` BOOLEAN DEFAULT 0,
  `deck` BOOLEAN DEFAULT 0,
  `in_house_laundry` BOOLEAN DEFAULT 0,
  `visitor_parking` BOOLEAN DEFAULT 0,
  `pool` BOOLEAN DEFAULT 0,
  `pet_friendly` BOOLEAN DEFAULT 0,
 FOREIGN KEY (`unit_id`) 
    REFERENCES `property_data` (`unit_id`) 
    ON DELETE CASCADE  -- Add this line for cascading delete
);

-- Create Tenant Financial Preferences Table
CREATE TABLE `tenant_financial_preferences` (
  `user_id` INT PRIMARY KEY,
  `monthly_income` INT,
  `monthly_savings` INT,
  `monthly_debt` INT,
  `rent_percentage` INT,
  FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
);

CREATE TABLE `tenant_preference_details` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `session_id` VARCHAR(255) UNIQUE,
  `user_id` INT NULL,
  `tenant_category_id` INT,
  `location_category_id` INT,
  `budget_category_id` INT,
  `school_proximity` INT,
  `hospital_proximity` INT,
  `transit_proximity` INT,
  `in_house_laundry` BOOLEAN,
  `gym` BOOLEAN,
  `pet_friendly` BOOLEAN,
  `pool` BOOLEAN,
  `is_logged_in` BOOLEAN,
  FOREIGN KEY (`tenant_category_id`) REFERENCES `tenant_category` (`tent_cat_id`)
);

-- Optional index on `user_id` for faster lookups by user
CREATE INDEX idx_user_id ON `tenant_preference_details` (`user_id`);

-- Create Tenant Actions Table
CREATE TABLE `tenant_actions` (
  `action_id` INT AUTO_INCREMENT PRIMARY KEY,
  `tenant_preference_details_id` INT,
  `unit_id` INT,
  `is_liked` BOOLEAN DEFAULT NULL,    -- NULL for neutral, TRUE for liked, FALSE for disliked
  `is_contacted` BOOLEAN DEFAULT NULL,
  FOREIGN KEY (`tenant_preference_details_id`) REFERENCES `tenant_preference_details` (`id`),
  FOREIGN KEY (`unit_id`) REFERENCES `property_data` (`unit_id`) ON DELETE CASCADE
);

CREATE TABLE property_owner_info (
    owner_id INT AUTO_INCREMENT PRIMARY KEY,
    unit_id INT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    address VARCHAR(255),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (unit_id) REFERENCES property_data(unit_id) ON DELETE CASCADE
);


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
  
  -- Create location Category Table
CREATE TABLE `location_category` (
  `location_cat_id` INT PRIMARY KEY,
  `location_category` VARCHAR(255)
);
  -- Insert static data for location categories
INSERT INTO `location_category` (`location_cat_id`, `location_category`) 
VALUES 
  (1, 'Downtown'),
  (2, 'Suburb'),
  (3, 'Rural');



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
