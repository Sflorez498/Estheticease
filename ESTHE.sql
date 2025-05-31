CREATE DATABASE Estheticease;
USE Estheticease;

-- Tabla de Roles de usuario (admin, recepcionista, cliente, etc.)
CREATE TABLE Roles (
    id_rol INT PRIMARY KEY AUTO_INCREMENT,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO Roles (nombre_rol)
VALUES ('Administrador'), ('Recepcionista'), ('Empleado'), ('Cliente');

-- Tabla de Empleados
CREATE TABLE Empleados (
    id_empleado INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    contacto VARCHAR(20),
    correo VARCHAR(100) UNIQUE,
    contraseña VARCHAR(200) NOT NULL,
    id_rol INT,
    FOREIGN KEY (id_rol) REFERENCES Roles(id_rol) ON DELETE SET NULL
);

-- Tabla de Clientes
CREATE TABLE Clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(40) NOT NULL,
    contacto VARCHAR(20) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    contraseña VARCHAR(200) NOT NULL,
    genero VARCHAR(20),
    edad INT
);

-- Tabla de Servicios
CREATE TABLE Servicios (
    id_servicio INT PRIMARY KEY AUTO_INCREMENT,
    nombre_servicio VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL
);

-- Tabla de Productos
CREATE TABLE Productos (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre_producto VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    inventario INT, 
    precio DECIMAL(10,2) NOT NULL
);

-- Tabla de Horarios
CREATE TABLE Horarios (
    id_horario INT PRIMARY KEY AUTO_INCREMENT,
    id_empleado INT,
    dia_semana ENUM('Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo') NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado) ON DELETE CASCADE
);

-- Tabla de Citas
CREATE TABLE Citas (
    id_cita INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT,
    id_servicio INT,
    id_empleado INT,
    fecha_hora DATETIME NOT NULL,
    estado ENUM('Pendiente', 'Confirmada', 'Cancelada') DEFAULT 'Pendiente',
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_servicio) REFERENCES Servicios(id_servicio) ON DELETE SET NULL,
    FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado) ON DELETE SET NULL
);

-- Tabla de Ventas
CREATE TABLE Ventas (
    id_venta INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT,
    id_producto INT,
    cantidad INT NOT NULL,
    total DECIMAL(10,2),
    fecha_venta DATE NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto) ON DELETE SET NULL
);

-- Tabla de Historial de cambios en citas
CREATE TABLE Historial_Citas (
    id_historial INT PRIMARY KEY AUTO_INCREMENT,
    id_cita INT,
    estado_anterior ENUM('Pendiente', 'Confirmada', 'Cancelada'),
    estado_nuevo ENUM('Pendiente', 'Confirmada', 'Cancelada'),
    fecha_cambio DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cita) REFERENCES Citas(id_cita) ON DELETE CASCADE
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_cliente_correo ON Clientes(correo);
CREATE INDEX idx_empleado_correo ON Empleados(correo);
CREATE INDEX idx_servicio_nombre ON Servicios(nombre_servicio);
CREATE INDEX idx_producto_categoria ON Productos(categoria);

-- Datos de ejemplo (Clientes, Empleados, Servicios, Productos)

INSERT INTO Clientes (nombre, contacto, correo, contraseña, genero, edad)
VALUES 
    ('Diego Cubides', '3120124521', 'Diego_9822@hotmail.com', '158754Dc-', 'masculino', 27),
    ('Steven Florez', '3507718249', 'sflorez498@gmail.com', '110011Sf-', 'masculino', 30);

INSERT INTO Empleados (nombre, contacto, correo, contraseña, id_rol)
VALUES 
    ('Laura Pérez', '3001234567', 'laura@estheticease.com', '123Laura-', 3),
    ('Carlos Gómez', '3019876543', 'carlos@estheticease.com', '456Carlos-', 3);

INSERT INTO Servicios (nombre_servicio, descripcion, precio) 
VALUES 
    ('Corte de cabello', 'Corte profesional para mujeres y hombres', 200.00),
    ('Manicure', 'Manicure con esmaltado semipermanente', 300.00);

INSERT INTO Productos (nombre_producto, categoria, inventario, precio) 
VALUES 
    ('Shampoo hidratante', 'Cuidado del cabello', 20, 150.00),
    ('Crema facial', 'Cuidado de la piel', 15, 250.00);

INSERT INTO Horarios (id_empleado, dia_semana, hora_inicio, hora_fin)
VALUES 
    (1, 'Lunes', '09:00:00', '17:00:00'),
    (2, 'Martes', '10:00:00', '18:00:00');

INSERT INTO Citas (id_cliente, id_servicio, id_empleado, fecha_hora, estado) 
VALUES 
    (1, 1, 1, '2025-03-15 10:00:00', 'Cancelada'),
    (2, 2, 2, '2025-03-16 14:30:00', 'Pendiente');

INSERT INTO Ventas (id_cliente, id_producto, cantidad, total, fecha_venta) 
VALUES 
    (1, 1, 2, 300.00, '2025-04-11'),
    (2, 2, 1, 250.00, '2025-03-11');

INSERT INTO Historial_Citas (id_cita, estado_anterior, estado_nuevo)
VALUES 
    (1, 'Pendiente', 'Cancelada');
