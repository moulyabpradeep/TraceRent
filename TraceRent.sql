CREATE DATABASE trace_rent_ai;

USE trace_rent_ai;


CREATE TABLE `tenant_personal_details` (
  `user_id` integer PRIMARY KEY,
  `name` varchar(255),
  `email` varchar(255),
  `phone` integer,
  `province` varchar(255),
  `dob` date
);

CREATE TABLE `tenant_preference_details` (
  `user_id` integer PRIMARY KEY,
  `tent_cat_id` integer,
  `province` varchar(255),
  `country` varchar(255),
  `pets_preference` varchar(255),
  `family_with_kids` varchar(255),
  `amenities` varchar(255)
);

CREATE TABLE `tenant_category` (
  `tent_cat_id` integer PRIMARY KEY,
  `tent_category` varchar(255)
);

CREATE TABLE `property_category` (
  `prop_cat_id` integer PRIMARY KEY,
  `prop_category` varchar(255)
);

CREATE TABLE `tenant_preferred_properties` (
  `id` integer PRIMARY KEY,
  `tent_cat_id` integer,
  `prop_cat_id` integer
);

CREATE TABLE `property_Data` (
  `prop_cat_id` integer,
  `unit_id` integer PRIMARY KEY,
  `prop_name` varchar(255),
  `prop_type` varchar(255),
  `no_of_rooms` varchar(255),
  `area_code` varchar(255),
  `province` varchar(255),
  `country` varchar(255),
  `address` varchar(255),
  `rent` decimal,
  `lease_length` varchar(255)
);

CREATE TABLE `behaviour_data` (
  `user_id` integer PRIMARY KEY,
  `prop_searched` integer,
  `prop_viewed` integer,
  `prop_saved` integer
);

CREATE TABLE `location` (
  `unit_id` INTEGER PRIMARY KEY,      -- Unique identifier for the unit
  `apt_unit_number` VARCHAR(50),      -- Apartment or Unit number
  `street_name` VARCHAR(255),         -- Street name
  `community` VARCHAR(255),           -- Community name
  `city` VARCHAR(255),                -- City name
  `province` VARCHAR(255),            -- Province or state
  `country` VARCHAR(255),             -- Country
  `latitude` VARCHAR(50),             -- Latitude coordinates
  `longitude` VARCHAR(50)             -- Longitude coordinates
);


CREATE TABLE `amenities` (
  `unit_id` integer PRIMARY KEY,
  `accessibility` varchar(255),
  `parking` integer,
  `gym` varchar(255),
  `kids_playarea` varchar(255),
  `party_hall` varchar(255),
  `backyard` varchar(255),
  `deck` varchar(255),
  `laundary` varchar(255),
  `visitor_parking` varchar(255),
  `pool` varchar(255)
);

CREATE TABLE `user` (
  `user_id` integer PRIMARY KEY,
  `username` varchar(255),
  `password` varchar(255)
);

CREATE TABLE `tenant_financial_preferences` (
  `user_id` integer PRIMARY KEY,
  `monthly_income` integer,
  `monthly_savings` integer,
  `monthly_debt` integer,
  `rent_percentage` integer
);

CREATE TABLE `areas` (
  `area_id` INTEGER PRIMARY KEY AUTO_INCREMENT,  -- Unique identifier for each area
  `community` VARCHAR(255),                      -- Community name
  `city` VARCHAR(255),                           -- City name
  `province` VARCHAR(255),                       -- Province or state
  `country` VARCHAR(255)                         -- Country
);


ALTER TABLE `tenant_personal_details` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

ALTER TABLE `tenant_preference_details` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

ALTER TABLE `tenant_preference_details` ADD FOREIGN KEY (`tent_cat_id`) REFERENCES `tenant_category` (`tent_cat_id`);

ALTER TABLE `tenant_preferred_properties` ADD FOREIGN KEY (`tent_cat_id`) REFERENCES `tenant_category` (`tent_cat_id`);

ALTER TABLE `tenant_preferred_properties` ADD FOREIGN KEY (`prop_cat_id`) REFERENCES `property_category` (`prop_cat_id`);

ALTER TABLE `property_Data` ADD FOREIGN KEY (`prop_cat_id`) REFERENCES `property_category` (`prop_cat_id`);

ALTER TABLE `behaviour_data` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

ALTER TABLE `behaviour_data` ADD FOREIGN KEY (`prop_searched`) REFERENCES `property_Data` (`unit_id`);

ALTER TABLE `behaviour_data` ADD FOREIGN KEY (`prop_viewed`) REFERENCES `property_Data` (`unit_id`);

ALTER TABLE `behaviour_data` ADD FOREIGN KEY (`prop_saved`) REFERENCES `property_Data` (`unit_id`);

ALTER TABLE `location` ADD FOREIGN KEY (`unit_id`) REFERENCES `property_Data` (`unit_id`);

ALTER TABLE `amenities` ADD FOREIGN KEY (`unit_id`) REFERENCES `property_Data` (`unit_id`);

ALTER TABLE `tenant_financial_preferences` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

-- Insert static data for tenant categories
INSERT INTO tenant_category (tent_cat_id, tent_category) 
VALUES 
  (1, 'Singles'),
  (2, 'Couple'),
  (3, 'Family'),
  (4, 'Roommates');
  
-- Insert static data for property categories
INSERT INTO property_category (prop_cat_id, prop_category) 
VALUES 
  (1, 'Studio apartment'),
  (2, '1-bedroom apartment'),
  (3, '2-bedroom apartment'),
  (4, '3-bedroom apartment');