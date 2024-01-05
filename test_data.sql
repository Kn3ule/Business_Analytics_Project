-- Einfügen von 10 Genera mit deutschen Namen
INSERT INTO genus (species_name) VALUES 
('Rotfuchs'),          -- Vulpes vulpes
('Reh'),               -- Capreolus capreolus
('Wildschwein'),       -- Sus scrofa
('Dachs'),             -- Meles meles
('Elch'),              -- Alces alces
('Wolf'),              -- Canis lupus
('Braunbär'),          -- Ursus arctos
('Luchs'),             -- Lynx lynx
('Baummarder'),        -- Martes martes
('Biber');             -- Castor fiber

-- Einfügen von 5 Standorten
INSERT INTO locations (short_title, description) VALUES 
('BayerWald', 'Bayerischer Wald'),
('Schwarzwald', 'Schwarzwald'),
('Harz', 'Harzgebirge'),
('SächsSchweiz', 'Sächsische Schweiz'),
('Eifel', 'Eifel');

-- Einfügen von Tieren (3-5 pro Genus)
-- Einfügen von Beobachtungen (mindestens 1 pro Tier)

-- Rotfuchs
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(1, 'Männlich', 'Rotes Fell, buschiger Schwanz', 4, 8, 0.6),
(1, 'Weiblich', 'Kleiner, dunkleres Fell', 3, 6, 0.5),
(1, 'Männlich', 'Helles Fell, große Ohren', 5, 9, 0.65);
-- Beobachtungen für Rotfüchse
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(1, 1, '2023-02-01 07:00:00', '2023-02-01 07:30:00'),
(2, 2, '2023-02-03 08:00:00', '2023-02-03 08:45:00'),
(3, 3, '2023-02-05 06:00:00', '2023-02-05 06:30:00');

-- Reh
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(2, 'Weiblich', 'Schlank, helles Fell', 2, 30, 1.3),
(2, 'Männlich', 'Dunkles Fell, kleines Geweih', 3, 35, 1.4),
(2, 'Weiblich', 'Jung, gepunktetes Fell', 1, 25, 1.2);
-- Beobachtungen für Rehe
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(4, 4, '2023-02-10 09:00:00', '2023-02-10 09:30:00'),
(5, 5, '2023-02-12 10:00:00', '2023-02-12 10:45:00'),
(6, 1, '2023-02-14 08:00:00', '2023-02-14 08:30:00');

-- Wildschwein
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(3, 'Weiblich', 'Groß, dunkles Fell', 4, 60, 0.7),
(3, 'Männlich', 'Stark, lange Hauer', 5, 75, 0.8),
(3, 'Weiblich', 'Jung, gestreiftes Fell', 1, 30, 0.5);
-- Beobachtungen für Wildschweine
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(7, 2, '2023-02-16 07:00:00', '2023-02-16 07:30:00'),
(8, 3, '2023-02-18 06:00:00', '2023-02-18 06:45:00'),
(9, 4, '2023-02-20 05:00:00', '2023-02-20 05:30:00');

-- Dachs
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(4, 'Männlich', 'Schwarz-weißes Fell, kurz', 3, 12, 0.75),
(4, 'Weiblich', 'Graues Fell, lang', 4, 10, 0.7),
(4, 'Männlich', 'Jung, kleines Größe', 1, 8, 0.6);
-- Beobachtungen für Dachse
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(10, 5, '2023-02-22 08:00:00', '2023-02-22 08:30:00'),
(11, 1, '2023-02-24 09:00:00', '2023-02-24 09:45:00'),
(12, 2, '2023-02-26 07:00:00', '2023-02-26 07:30:00');

-- Elch
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(5, 'Männlich', 'Großes Geweih, dunkelbraunes Fell', 7, 700, 2.1),
(5, 'Weiblich', 'Ohne Geweih, helle Färbung', 6, 600, 1.9),
(5, 'Männlich', 'Jungtier, schlank, kleines Geweih', 2, 400, 1.5);
-- Beobachtungen für Elche
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(13, 3, '2023-03-01 07:00:00', '2023-03-01 07:45:00'),
(14, 4, '2023-03-03 08:00:00', '2023-03-03 08:30:00'),
(15, 5, '2023-03-05 06:00:00', '2023-03-05 06:45:00');

-- Wolf
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(6, 'Männlich', 'Dichtes graues Fell, große Ohren', 5, 45, 1.2),
(6, 'Weiblich', 'Schlanker Körperbau, hellgraues Fell', 4, 40, 1.1),
(6, 'Männlich', 'Jungtier, spielerisch, kleiner Körper', 1, 25, 0.8);
-- Beobachtungen für Wölfe
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(16, 1, '2023-03-07 07:00:00', '2023-03-07 07:45:00'),
(17, 2, '2023-03-09 08:00:00', '2023-03-09 08:30:00'),
(18, 3, '2023-03-11 06:00:00', '2023-03-11 06:45:00');

-- Braunbär
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(7, 'Männlich', 'Dunkelbraunes Fell, große Pranken', 8, 350, 2.2),
(7, 'Weiblich', 'Mittleres Braun, weniger massiv', 6, 250, 1.8),
(7, 'Weiblich', 'Jungtier, verspielt, helles Fell', 2, 100, 1.2);
-- Beobachtungen für Braunbären
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(19, 4, '2023-03-13 07:00:00', '2023-03-13 07:45:00'),
(20, 5, '2023-03-15 08:00:00', '2023-03-15 08:30:00'),
(21, 1, '2023-03-17 06:00:00', '2023-03-17 06:45:00');

-- Luchs
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(8, 'Männlich', 'Gestreiftes Fell, kurzer Schwanz', 6, 30, 1.0),
(8, 'Weiblich', 'Kleiner, unauffälliges Fell', 5, 25, 0.9),
(8, 'Männlich', 'Jungtier, spielerisch, helles Fell', 2, 15, 0.6);
-- Beobachtungen für Luchse
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(22, 2, '2023-03-19 07:00:00', '2023-03-19 07:45:00'),
(23, 3, '2023-03-21 08:00:00', '2023-03-21 08:30:00'),
(24, 4, '2023-03-23 06:00:00', '2023-03-23 06:45:00');

-- Baummarder
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(9, 'Männlich', 'Dunkles Fell, agil', 4, 2, 0.45),
(9, 'Weiblich', 'Helles Kehlfell, schlank', 3, 1.8, 0.4),
(9, 'Männlich', 'Jungtier, neugierig, kleiner Körper', 1, 1, 0.3);
-- Beobachtungen für Baummarder
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(25, 5, '2023-03-25 07:00:00', '2023-03-25 07:45:00'),
(26, 1, '2023-03-27 08:00:00', '2023-03-27 08:30:00'),
(27, 2, '2023-03-29 06:00:00', '2023-03-29 06:45:00');

-- Biber
INSERT INTO animals (genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size) VALUES 
(10, 'Männlich', 'Breiter Körper, großer flacher Schwanz', 7, 30, 1.0),
(10, 'Weiblich', 'Kompakter Körperbau, dunkles Fell', 6, 28, 0.95),
(10, 'Weiblich', 'Jungtier, kleiner Körper', 2, 15, 0.5);
-- Beobachtungen für Biber
INSERT INTO observations (animal_id, location_id, start_time, end_time) VALUES 
(28, 3, '2023-03-31 07:00:00', '2023-03-31 07:45:00'),
(29, 4, '2023-04-02 08:00:00', '2023-04-02 08:30:00'),
(30, 5, '2023-04-04 06:00:00', '2023-04-04 06:45:00');