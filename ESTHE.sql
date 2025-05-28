-- Crear y usar la base de datos
CREATE DATABASE IF NOT EXISTS Estheticease1;
USE Estheticease1;

-- Tabla de Clientes
DROP TABLE IF EXISTS Clientes;

CREATE TABLE Clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(40),
    Contacto VARCHAR(20),
    Correo VARCHAR(100),
    Contraseña varchar(200),
    Genero VARCHAR(20),
    Edad INT
);

INSERT INTO Clientes (Nombre, Contacto, Correo, Contraseña, Genero, Edad)
VALUES 
    ("Diego Cubides", "3120124521", "Diego_9822@hotmail.com","158754Dc-", "masculino", 27),
    ("Steven Florez", "3507718249", "sflorez498@gmail.com","110011Sf-", "masculino", 30);

SELECT * FROM Clientes;

-- Tabla de Servicios
DROP TABLE IF EXISTS Servicios;

CREATE TABLE Servicios (
    id_servicio INT PRIMARY KEY AUTO_INCREMENT,
    nombre_servicio VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2)
);

INSERT INTO Servicios (id_servicio, nombre_servicio, descripcion, precio) 
VALUES 
    (24, 'Corte de cabello', 'Corte profesional para mujeres y hombres', 200.00),
    (15, 'Manicure', 'Manicure con esmaltado semipermanente', 300.00);

SELECT * FROM Servicios;

-- Tabla de Citas
DROP TABLE IF EXISTS Citas;

CREATE TABLE Citas (
    id_cita INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT,
    id_servicio INT,
    fecha_hora DATETIME,
    estado ENUM('Pendiente', 'Confirmada', 'Cancelada') DEFAULT 'Pendiente'
);

INSERT INTO Citas (id_cliente, id_servicio, fecha_hora, estado) 
VALUES 
    (1, 1, '2025-03-15 10:00:00', "Cancelada"),
    (2, 2, '2025-03-16 14:30:00', "Pendiente");

SELECT * FROM Citas;

-- Tabla de Productos
DROP TABLE IF EXISTS Productos;

CREATE TABLE Productos (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre_producto VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    inventario INT, 
    precio DECIMAL(10,2)
);

INSERT INTO Productos (id_producto, nombre_producto, categoria, precio, inventario) 
VALUES 
    (30, 'Shampoo hidratante', 'Cuidado del cabello', 150.00, 20),
    (45, 'Crema facial', 'Cuidado de la piel', 250.00, 15);

SELECT * FROM Productos;

-- Tabla de Ventas
DROP TABLE IF EXISTS Ventas;

CREATE TABLE Ventas (
    id_venta INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT,
    id_producto INT,
    cantidad INT NOT NULL,
    total DECIMAL(10,2),
    fecha_venta DATE
);

INSERT INTO Ventas (id_venta, id_cliente, id_producto, cantidad, total, fecha_venta) 
VALUES 
    (2, 102, 4, 150.75, 20000.00, '2025-04-11'),
    (1, 101, 3, 150.75, 30000.00, '2025-03-11');

SELECT * FROM Ventas;
