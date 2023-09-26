-- Create the ESCUELA database if it doesn't exist
CREATE DATABASE IF NOT EXISTS ESCUELA;

-- Switch to using the ESCUELA database
USE ESCUELA;

-- Create the Carreras table
CREATE TABLE IF NOT EXISTS Carreras (
    IDCARRERA INT PRIMARY KEY AUTO_INCREMENT,
    NOMBRE VARCHAR(255) NOT NULL,
    DURACION INT
);

-- Insert sample data into the Carreras table
INSERT INTO Carreras (NOMBRE, DURACION)
VALUES
('Software', 3),
('Enfermeria', 3),
('Turismo', 3);


-- Create the EstadoAlumno table
CREATE TABLE IF NOT EXISTS EstadoAlumno (
    IDESTADOALUMNO INT PRIMARY KEY AUTO_INCREMENT,
    NOMBRE VARCHAR(255) NOT NULL
);

-- Insert sample data into the estadoalumno table
INSERT INTO EstadoAlumno (NOMBRE)
VALUES
('Libre'),
('Promocionado'),
('Regular');


-- Create the Alumnos table with foreign key constraints
CREATE TABLE IF NOT EXISTS Alumnos (
    IDALUMNO INT PRIMARY KEY AUTO_INCREMENT,
    NOMBRE VARCHAR(255) NOT NULL,
    APELLIDO VARCHAR(255) NOT NULL,
    DNI VARCHAR(20) NOT NULL,
    IDCARRERA INT NOT NULL,
    IDESTADOALUMNO INT NOT NULL,
    FOREIGN KEY (IDCARRERA) REFERENCES Carreras(IDCARRERA),
    FOREIGN KEY (IDESTADOALUMNO) REFERENCES EstadoAlumno(IDESTADOALUMNO)
);

-- Insert data into the Alumnos table
INSERT INTO Alumnos (nombre, apellido, dni, idcarrera, idestadoalumno)
VALUES
('Carlos', 'Juarez', '33.589.560', 2, 1),
('Luis', 'González', '44.123.789', 1, 2),
('Ana', 'Perez', '22.456.890', 3, 3),
('María', 'Lopez', '12.345.678', 2, 1),
('Diego', 'Martinez', '89.765.432', 1, 2),
('Laura', 'Rodriguez', '55.678.901', 2, 3),
('Pedro', 'Hernandez', '44.567.890', 3, 1),
('Sofía', 'García', '11.234.567', 2, 2),
('Juan', 'Diaz', '09.876.543', 1, 3),
('Mónica', 'Fernandez', '66.789.012', 3, 1);
