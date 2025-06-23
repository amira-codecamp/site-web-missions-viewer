
ALTER DATABASE db
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

SET SESSION lc_time_names = 'en_US'; -- date format : yyyy-mm-dd

/* TABLES */

CREATE TABLE Status (
    status_name VARCHAR(50) PRIMARY KEY
);

CREATE TABLE Transports (
    transport_name VARCHAR(50) PRIMARY KEY
);

CREATE TABLE Employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (status) REFERENCES Status(status_name)
);

CREATE TABLE Missions (
    mission_id INT AUTO_INCREMENT PRIMARY KEY,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    mission_desc VARCHAR(255) NOT NULL UNIQUE,
    employee INT NOT NULL,
    FOREIGN KEY (employee) REFERENCES Employees(employee_id)
);

CREATE TABLE Trips (
    trip_id INT AUTO_INCREMENT PRIMARY KEY,
    departure_city VARCHAR(255) NOT NULL,
    departure_country VARCHAR(255) NOT NULL,
    destination_city VARCHAR(255) NOT NULL,
    destination_country VARCHAR(255) NOT NULL,
    is_round_trip BOOLEAN NOT NULL,
    carpooling INT NOT NULL,
    transport VARCHAR(50) NOT NULL,
    mission INT NOT NULL,
    carbon_footprint DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (mission) REFERENCES Missions(mission_id),
    FOREIGN KEY (transport) REFERENCES Transports(transport_name)
);

CREATE TABLE Permissions (
    permission_name VARCHAR(50) PRIMARY KEY,
    permission_desc VARCHAR(255) NOT NULL
);

CREATE TABLE `Groups` (
    group_name VARCHAR(50) PRIMARY KEY
);

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    date_joined DATE NOT NULL,
    last_login DATETIME NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    `group` VARCHAR(50) NOT NULL,
    employee INT NOT NULL,
    FOREIGN KEY (employee) REFERENCES Employees(employee_id),
    FOREIGN KEY (`group`) REFERENCES `Groups`(group_name)
);

CREATE TABLE Groups_permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    permission VARCHAR(50) NOT NULL,
    `group` VARCHAR(50) NOT NULL,
    FOREIGN KEY (permission) REFERENCES Permissions(permission_name),
    FOREIGN KEY (`group`) REFERENCES `Groups`(group_name)
);

/* TRIGGERS */

DELIMITER $$

CREATE TRIGGER validate_lipn_email
BEFORE INSERT ON Employees
FOR EACH ROW
BEGIN
    IF NEW.email NOT REGEXP '^[^@]+@lipn\\.fr$'
    AND NEW.email NOT REGEXP '^[^@]+@lipn\\.univ-paris13\\.fr$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid email address. Only members of LIPN are allowed!';
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER check_mission_date
BEFORE INSERT ON Missions
FOR EACH ROW
BEGIN
    IF NEW.start_date > CURDATE() AND NEW.end_date > CURDATE() THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Mission date must be at most today (or earlier, of course!)';
    END IF;
    IF NEW.end_date < NEW.start_date THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Mission end date must be after or the same as the start date !';
    END IF;
END$$

DELIMITER ;

/* DATA */

INSERT INTO Status (status_name) VALUES 
('researcher'),
('doctorant'),
('intern'),
('technician');

INSERT INTO Employees (first_name, last_name, email, `status`) VALUES 
('Mathieu', 'LACROIX', 'lacroix@lipn.fr', 'researcher'),
('Étienne', 'ANDRÉ', 'Etienne.Andre@lipn.univ-paris13.fr', 'researcher'),
('Amira', 'HAMMADI', 'hammadi@lipn.univ-paris13.fr', 'intern'),
('missionmanager', 'missionmanager', 'missionmanager@lipn.fr', 'technician'),
('admin', 'admin', 'admin@lipn.fr', 'technician');

INSERT INTO `Groups` (group_name) VALUES 
('admin'),
('missionmanager'),
('standard');

INSERT INTO `Permissions` (permission_name, permission_desc) VALUES
('view_trip', 'Can view trip'),
('add_trip', 'Can add trip'),
('change_trip', 'Can modify trip'),
('delete_trip', 'Can delete trip'),
('view_mission', 'Can view mission'),
('add_mission', 'Can add mission'),
('change_mission', 'Can modify mission'),
('delete_mission', 'Can delete mission'),
('view_employee', 'Can view employee'),
('add_employee', 'Can add employee'),
('change_employee', 'Can modify employee'),
('delete_employee', 'Can delete employee'),
('view_status', 'Can view status'),
('add_status', 'Can add status'),
('change_status', 'Can modify status'),
('delete_status', 'Can delete status'),
('view_transport', 'Can view transport'),
('add_transport', 'Can add transport'),
('change_transport', 'Can modify transport'),
('delete_transport', 'Can delete transport'),
('view_user', 'Can view user'),
('add_user', 'Can add user'),
('change_user', 'Can modify user'),
('delete_user', 'Can delete user'),
('view_group', 'Can view group'),
('add_group', 'Can add group'),
('change_group', 'Can modify group'),
('delete_group', 'Can delete group'),
('view_permission', 'Can view permission'),
('add_permission', 'Can add permission'),
('change_permission', 'Can modify permission'),
('delete_permission', 'Can delete permission');

INSERT INTO Groups_permissions (permission, `group`) VALUES 
('view_trip', 'missionmanager'),
('add_trip', 'missionmanager'),
('delete_trip', 'missionmanager'),
('change_trip', 'missionmanager'),
('view_mission', 'missionmanager'),
('add_mission', 'missionmanager'),
('delete_mission', 'missionmanager'),
('change_mission', 'missionmanager'),
('view_employee', 'missionmanager'),
('view_user', 'admin'),
('delete_user', 'admin'),
('add_user', 'admin'),
('change_user', 'admin'),
('view_employee', 'admin'),
('change_employee', 'admin'),
('view_trip', 'standard');

INSERT INTO Users (login, password, date_joined, last_login, is_active, `group`, employee) VALUES 
('lacroix', 'pbkdf2_sha256$1000000$ev7fOcB3Rx1M8Av90qSSGm$BoDD/YWq4bpGPv9O+eOoAL0vHFdreGJpeI/WGBjoYpM=', '2010/03/10', '2025/05/08', TRUE, 'standard', 1),
('andre', 'pbkdf2_sha256$1000000$MYtyO8gaelf05aMTQnH3fV$5e+u4HywJ+bR5tk5sn1+/6if9MX/a1gm0FFnp6GaDZs=', '2010/03/10', '2025/05/08', TRUE, 'standard', 2),
('hammadi', 'pbkdf2_sha256$1000000$3ouINtYqNiJL8dcXFqm6gU$LVMxjbrPwrmgy2e91EFOc8ZQWGa/0B7aguQPgNcegyE=', '2024/04/14', '2025/05/08', TRUE, 'standard', 3),
('missionmanager', 'pbkdf2_sha256$1000000$OQaPzaE6XDkRBKVvm0vZ3J$vFCCD5p8Gl1IlbhMFB5J1aXK7vo36DSVhOmWPsx8kKc=', '2024/04/14', '2025/05/08', TRUE, 'missionmanager', 4),
('admin', 'pbkdf2_sha256$1000000$yx7t1QvvROIWZjN6XrguZs$RveAVbvCsU1wCcNNp8TlaV0vHwmdd5PksfLDqQqHNEQ=', '2024/04/14', '2025/05/08', TRUE, 'admin', 5);

INSERT INTO Transports (transport_name) VALUES 
('car'),
('plane'),
('train'),
('bus'),
('cab'),
('tram'),
('rer'),
('subway'),
('ferry');

INSERT INTO Missions (start_date, end_date, mission_desc, employee) VALUES
('2024-04-01', '2024-04-05', 'PRJ-lacroix-042024', 1),
('2024-05-01', '2024-05-05', 'PRJ-andre-052024', 2),
('2024-06-02', '2024-06-06', 'CONF-lacroix-062024', 1),
('2024-06-03', '2024-06-07', 'CONF-andre-062024', 2);

-- 5 Trips within France using Train
INSERT INTO Trips (departure_city, departure_country, destination_city, destination_country, is_round_trip, carpooling, transport, mission, carbon_footprint) VALUES
('Paris', 'France', 'Lyon', 'France', TRUE, 1, 'train', 1, 2.0),
('Paris', 'France', 'Marseille', 'France', FALSE, 1, 'train', 1, 1.5),
('Lyon', 'France', 'Toulouse', 'France', FALSE, 1, 'train', 2, 2.2),
('Marseille', 'France', 'Paris', 'France', TRUE, 1, 'train', 2, 1.9);

-- 9 Trips between Different Countries using Plane
INSERT INTO Trips (departure_city, departure_country, destination_city, destination_country, is_round_trip, carpooling, transport, mission, carbon_footprint) VALUES
('Bordeaux', 'France', 'Berlin', 'Germany', TRUE, 1, 'plane', 3, 2.1),
('Bordeaux', 'France', 'Tokyo', 'Japan', FALSE, 1, 'plane', 2, 2.1),
('Paris', 'France', 'Berlin', 'Germany', TRUE, 1, 'plane', 1, 2.1),
('Paris', 'France', 'Frankfort', 'Germany', FALSE, 1, 'plane', 1, 2.1),
('Lyon', 'France', 'New York', 'USA', TRUE, 1, 'plane', 4, 1.7),
('Paris', 'France', 'Berlin', 'Germany', TRUE, 1, 'plane', 3, 1.6),
('Marseille', 'France', 'Berlin', 'Germany', FALSE, 1, 'plane', 4, 2.3),
('Lyon', 'France', 'Madrid', 'Spain', TRUE, 1, 'plane', 4, 1.7),
('Nantes', 'France', 'Berlin', 'Germany', TRUE, 1, 'plane', 2, 1.8),
('Paris', 'France', 'Nancy', 'France', FALSE, 1, 'car', 3, 1.9);

-- 3 Trips between Two Regions of Paris using Car
INSERT INTO Trips (departure_city, departure_country, destination_city, destination_country, is_round_trip, carpooling, transport, mission, carbon_footprint) VALUES
('Paris', 'France', 'Versailles', 'France', TRUE, 1, 'car', 2, 2.0),
('Paris', 'France', 'Boulogne-Billancourt', 'France', FALSE, 1, 'car', 1, 1.9);