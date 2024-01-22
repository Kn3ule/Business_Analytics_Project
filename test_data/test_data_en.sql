-- Insert 10 genera with German names
INSERT INTO genus (species_name) VALUES 
('red fox'), -- Vulpes vulpes
('roe deer'), -- Capreolus capreolus
('wild boar'), -- Sus scrofa
('badger'), -- Meles meles
('elk'), -- Alces alces
('wolf'), -- Canis lupus
('brown bear'), -- Ursus arctos
('lynx'), -- Lynx lynx
('pine marten'), -- Martes martes
('beaver'); -- Castor fiber

-- Insert 5 locations
INSERT INTO locations (short_title, description) VALUES 
('BayerWald', 'Bavarian Forest'),
('Black Forest', 'Schwarzwald'),
('Harz', 'Harzgebirge'),
('SächsSchweiz', 'Sächsische Schweiz'),
('Eifel', 'Eifel');

-- Insert animals (3-5 per genus)
-- Insert observations (at least 1 per animal)

-- Red fox
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(1, 'Male', 'Red fur, bushy tail', 4, 8, 60),
(1, 'Female', 'Smaller, darker fur', 3, 6, 50),
(1, 'Male', 'Light fur, large ears', 5, 9, 65);
-- Observations for red foxes
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(1, 1, '2023-02-01 07:00:00', '2023-02-01 07:30:00'),
(2, 2, '2023-02-03 08:00:00', '2023-02-03 08:45:00'),
(3, 3, '2023-02-05 06:00:00', '2023-02-05 06:30:00');

-- deer
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(2, 'Female', 'Slim, light coat', 2, 30, 130),
(2, 'Male', 'Dark coat, small antlers', 3, 35, 140),
(2, 'Female', 'Young, spotted coat', 1, 25, 120);
-- Observations for deer
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(4, 4, '2023-02-10 09:00:00', '2023-02-10 09:30:00'),
(5, 5, '2023-02-12 10:00:00', '2023-02-12 10:45:00'),
(6, 1, '2023-02-14 08:00:00', '2023-02-14 08:30:00');

-- wild boar
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(3, 'Female', 'Large, dark fur', 4, 60, 70),
(3, 'Male', 'Strong, long tusks', 5, 75, 80),
(3, 'Female', 'Young, striped coat', 1, 30, 50);
-- Observations for wild boar
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(7, 2, '2023-02-16 07:00:00', '2023-02-16 07:30:00'),
(8, 3, '2023-02-18 06:00:00', '2023-02-18 06:45:00'),
(9, 4, '2023-02-20 05:00:00', '2023-02-20 05:30:00');

-- badger
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(4, 'Male', 'Black and white fur, short', 3, 12, 75),
(4, 'Female', 'Gray fur, long', 4, 10, 75),
(4, 'Male', 'Young, small size', 1, 8, 60);
-- Observations for badgers
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(10, 5, '2023-02-22 08:00:00', '2023-02-22 08:30:00'),
(11, 1, '2023-02-24 09:00:00', '2023-02-24 09:45:00'),
(12, 2, '2023-02-26 07:00:00', '2023-02-26 07:30:00');

-- moose
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(5, 'Male', 'Large antlers, dark brown fur', 7, 700, 210),
(5, 'Female', 'No antlers, light coloration', 6, 600, 190),
(5, 'Male', 'young animal, slender, small antlers', 2, 400, 150);
-- Observations for moose
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(13, 3, '2023-03-01 07:00:00', '2023-03-01 07:45:00'),
(14, 4, '2023-03-03 08:00:00', '2023-03-03 08:30:00'),
(15, 5, '2023-03-05 06:00:00', '2023-03-05 06:45:00');

-- wolf
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(6, 'Male', 'Dense gray fur, large ears', 5, 45, 120),
(6, 'Female', 'Slender build, light gray fur', 4, 40, 110),
(6, 'Male', 'Young, playful, small body', 1, 25, 80);
-- Observations for wolves
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(16, 1, '2023-03-07 07:00:00', '2023-03-07 07:45:00'),
(17, 2, '2023-03-09 08:00:00', '2023-03-09 08:30:00'),
(18, 3, '2023-03-11 06:00:00', '2023-03-11 06:45:00');

-- brown bear
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(7, 'Male', 'Dark brown fur, large paws', 8, 350, 220),
(7, 'Female', 'Medium brown, less massive', 6, 250, 180),
(7, 'Female', 'Young, playful, light-colored fur', 2, 100, 120);
-- Observations for brown bears
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(19, 4, '2023-03-13 07:00:00', '2023-03-13 07:45:00'),
(20, 5, '2023-03-15 08:00:00', '2023-03-15 08:30:00'),
(21, 1, '2023-03-17 06:00:00', '2023-03-17 06:45:00');

-- lynx
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(8, 'Male', 'Striped fur, short tail', 6, 30, 10),
(8, 'Female', 'Smaller, inconspicuous coat', 5, 25, 90),
(8, 'Male', 'Young, playful, light-colored fur', 2, 15, 60);
-- Observations for lynxes
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(22, 2, '2023-03-19 07:00:00', '2023-03-19 07:45:00'),
(23, 3, '2023-03-21 08:00:00', '2023-03-21 08:30:00'),
(24, 4, '2023-03-23 06:00:00', '2023-03-23 06:45:00');

-- pine marten
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(9, 'Male', 'Dark fur, agile', 4, 2, 45),
(9, 'Female', 'Light throat coat, slender', 3, 1.8, 40),
(9, 'Male', 'Young, curious, small body', 1, 1, 30);
-- Observations for pine marten
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(25, 5, '2023-03-25 07:00:00', '2023-03-25 07:45:00'),
(26, 1, '2023-03-27 08:00:00', '2023-03-27 08:30:00'),
(27, 2, '2023-03-29 06:00:00', '2023-03-29 06:45:00');

-- Beaver
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(10, 'Male', 'Wide body, large flat tail', 7, 30, 100),
(10, 'Female', 'Compact build, dark coat', 6, 28, 95),
(10, 'Female', 'Juvenile, small body', 2, 15, 50);
-- Observations for beaver
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(28, 3, '2023-03-31 07:00:00', '2023-03-31 07:45:00'),
(29, 4, '2023-04-02 08:00:00', '2023-04-02 08:30:00'),
(30, 5, '2023-04-04 06:00:00', '2023-04-04 06:45:00');