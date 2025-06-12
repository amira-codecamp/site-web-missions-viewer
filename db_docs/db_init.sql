
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
    email VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (status) REFERENCES Status(status_name)
);

CREATE TABLE Missions (
    mission_num VARCHAR(50) PRIMARY KEY,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    mission_desc VARCHAR(255) NOT NULL
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
    mission VARCHAR(50) NOT NULL,
    employee INT NOT NULL,
    carbon_footprint DECIMAL(10, 2),
    FOREIGN KEY (mission) REFERENCES Missions(mission_num),
    FOREIGN KEY (transport) REFERENCES Transports(transport_name),
    FOREIGN KEY (employee) REFERENCES Employees(employee_id)
);

CREATE TABLE Permissions (
    permission_name VARCHAR(50) PRIMARY KEY,
    permission_desc VARCHAR(255) NOT NULL
);

CREATE TABLE `Groups` (
    group_name VARCHAR(50) PRIMARY KEY
);

CREATE TABLE Users (
    login VARCHAR(50) PRIMARY KEY,
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
('YYY', 'YYYYY', 'yyyyy@lipn.fr', 'technician'),
('XXX', 'XXXXX', 'xxxxx@lipn.fr', 'technician');

INSERT INTO `Groups` (group_name) VALUES 
('admin'),
('missionmanager'),
('standard');

INSERT INTO `Permissions` (permission_name, permission_desc) VALUES
('view_trip', 'Can view trip'),
('add_trip', 'Can add trip'),
('change_trip', 'Can modify trip'),
('delete_trip', 'Can delete trip'),
('view_all_trip', 'Can view all trips'),
('view_mission', 'Can view mission'),
('add_mission', 'Can add mission'),
('change_mission', 'Can modify mission'),
('delete_mission', 'Can delete mission'),
('view_all_mission', 'Can view all missions'),
('view_employee', 'Can view employee'),
('view_all_employee', 'Can view all employees'),
('add_employee', 'Can add employee'),
('change_employee', 'Can modify employee'),
('delete_employee', 'Can delete employee'),
('view_user', 'Can view user'),
('add_user', 'Can add user'),
('change_user', 'Can modify user'),
('delete_user', 'Can delete user'),
('view_status', 'Can view status'),
('add_status', 'Can add status'),
('change_status', 'Can modify status'),
('delete_status', 'Can delete status'),
('view_transport', 'Can view transport'),
('add_transport', 'Can add transport'),
('change_transport', 'Can modify transport'),
('delete_transport', 'Can delete transport'),
('view_all_transport', 'Can view all transports'),
('view_group', 'Can view group'),
('add_group', 'Can add group'),
('change_group', 'Can modify group'),
('delete_group', 'Can delete group'),
('view_permission', 'Can view permission'),
('add_permission', 'Can add permission'),
('change_permission', 'Can modify permission'),
('delete_permission', 'Can delete permission');

INSERT INTO Groups_permissions (permission, `group`) VALUES 
('view_trip', 'standard'),
('view_all_trip', 'admin'),
('view_all_trip', 'missionmanager'),
('add_trip', 'missionmanager'),
('view_all_mission', 'missionmanager'),
('add_mission', 'missionmanager'),
('view_all_transport', 'missionmanager'),
('view_all_employee', 'missionmanager'),
('delete_trip', 'missionmanager'),
('change_trip', 'missionmanager');

INSERT INTO Users (login, password, date_joined, last_login, is_active, `group`, employee) VALUES 
('lacroix', 'pbkdf2_sha256$1000000$ev7fOcB3Rx1M8Av90qSSGm$BoDD/YWq4bpGPv9O+eOoAL0vHFdreGJpeI/WGBjoYpM=', '2010/03/10', '2025/05/08', TRUE, 'standard', 1),
('andre', 'pbkdf2_sha256$1000000$MYtyO8gaelf05aMTQnH3fV$5e+u4HywJ+bR5tk5sn1+/6if9MX/a1gm0FFnp6GaDZs=', '2010/03/10', '2025/05/08', TRUE, 'standard', 2),
('hammadi', 'pbkdf2_sha256$1000000$3ouINtYqNiJL8dcXFqm6gU$LVMxjbrPwrmgy2e91EFOc8ZQWGa/0B7aguQPgNcegyE=', '2024/04/14', '2025/05/08', TRUE, 'standard', 3),
('xxxxx', 'pbkdf2_sha256$1000000$c1ilG4NoJ6VS9hE3GB9v1S$D9SGGM56KKI0OfKAOoc2IbxRk3oyI/OvGnxFdxGjcGQ=', '2020/04/14', '2025/05/08', TRUE, 'admin', 5),
('yyyyy', 'pbkdf2_sha256$1000000$kzUVVFpiiRKzY42qSotTrO$jraq9nPC+BwcVV22D+No6qsr4IqKnT2zYeTP69Jk17E=', '2017/04/14', '2025/05/08', TRUE, 'missionmanager', 4);

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

INSERT INTO Missions (mission_num, start_date, end_date, mission_desc) VALUES
('M-001', '2024-06-01', '2024-06-05', 'Research Project'),
('M-002', '2024-06-02', '2024-06-06', 'Conference'),
('M-003', '2024-06-03', '2024-06-07', 'Conference');

-- 5 Trips within France using Train
INSERT INTO Trips (employee, departure_city, departure_country, destination_city, destination_country, is_round_trip, carpooling, transport, mission, carbon_footprint) VALUES
(1, 'Paris', 'France', 'Lyon', 'France', TRUE, 0, 'train', 'M-001', 2.0),
(2, 'Paris', 'France', 'Marseille', 'France', FALSE, 0, 'train', 'M-002', 1.5),
(1, 'Lyon', 'France', 'Toulouse', 'France', FALSE, 0, 'train', 'M-003', 2.2),
(1, 'Marseille', 'France', 'Paris', 'France', TRUE, 0, 'train', 'M-002', 1.9);

-- 9 Trips between Different Countries using Plane
INSERT INTO Trips (employee, departure_city, departure_country, destination_city, destination_country, is_round_trip, carpooling, transport, mission, carbon_footprint) VALUES
(1, 'Bordeaux', 'France', 'Berlin', 'Germany', TRUE, 0, 'plane', 'M-001', 2.1),
(1, 'Bordeaux', 'France', 'Tokyo', 'Japan', FALSE, 0, 'plane', 'M-001', 2.1),
(1, 'Paris', 'France', 'Berlin', 'Germany', TRUE, 0, 'plane', 'M-001', 2.1),
(1, 'Paris', 'France', 'Frankfort', 'Germany', FALSE, 0, 'plane', 'M-002', 2.1),
(1, 'Bordeaux', 'France', 'Berlin', 'Germany', FALSE, 0, 'plane', 'M-003', 2.1),
(2, 'Lyon', 'France', 'New York', 'USA', TRUE, 0, 'plane', 'M-002', 1.7),
(1, 'Paris', 'France', 'Berlin', 'Germany', TRUE, 0, 'plane', 'M-001', 1.6),
(2, 'Marseille', 'France', 'Berlin', 'Germany', FALSE, 0, 'plane', 'M-002', 2.3),
(2, 'Lyon', 'France', 'Madrid', 'Spain', TRUE, 0, 'plane', 'M-002', 1.7),
(2, 'Nantes', 'France', 'Berlin', 'Germany', TRUE, 0, 'plane', 'M-002', 1.8),
(1, 'Paris', 'France', 'Lyon', 'France', TRUE, 1, 'car', 'M-001', 2.0),
(1, 'Paris', 'France', 'Nancy', 'France', FALSE, 0, 'car', 'M-001', 1.9);

-- 3 Trips between Two Regions of Paris using Car
INSERT INTO Trips (employee, departure_city, departure_country, destination_city, destination_country, is_round_trip, carpooling, transport, mission, carbon_footprint) VALUES
(1, 'Paris', 'France', 'Versailles', 'France', TRUE, 1, 'car', 'M-001', 2.0),
(2, 'Paris', 'France', 'Boulogne-Billancourt', 'France', FALSE, 0, 'car', 'M-001', 1.9);