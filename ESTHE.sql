CREATE DATABASE Estheticease;
USE Estheticease;

-- Tabla de Productos
CREATE TABLE Productos (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    imagen_url VARCHAR(255),
    categoria VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de Roles de usuario (admin, recepcionista, cliente, etc.)
CREATE TABLE Roles (
    id_rol INT PRIMARY KEY AUTO_INCREMENT,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO Roles (nombre_rol)
VALUES ('Administrador'), ('Recepcionista'), ('Empleado'), ('Cliente');

-- Tabla de Empleados
CREATE TABLE Empleados (
    id_empleado INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    contacto VARCHAR(20) CHECK (contacto REGEXP '^[0-9]{10}$'),
    correo VARCHAR(100) UNIQUE CHECK (correo REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    contraseña VARCHAR(200) NOT NULL,
    id_rol INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_rol) REFERENCES Roles(id_rol) ON DELETE SET NULL
);

-- Tabla de Clientes
CREATE TABLE Clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(40) NOT NULL,
    contacto VARCHAR(20) NOT NULL CHECK (contacto REGEXP '^[0-9]{10}$'),
    correo VARCHAR(100) NOT NULL UNIQUE CHECK (correo REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    contraseña VARCHAR(200) NOT NULL,
    genero VARCHAR(20) CHECK (genero IN ('masculino', 'femenino', 'otro')),
    edad INT CHECK (edad >= 18),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de Servicios
CREATE TABLE Servicios (
    id_servicio INT PRIMARY KEY AUTO_INCREMENT,
    nombre_servicio VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL CHECK (precio > 0),
    duracion_minutos INT NOT NULL CHECK (duracion_minutos > 0),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de Productos
CREATE TABLE Productos (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre_producto VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    inventario INT CHECK (inventario >= 0),
    precio DECIMAL(10,2) NOT NULL CHECK (precio > 0),
    stock_minimo INT DEFAULT 5 CHECK (stock_minimo >= 0),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de Disponibilidad
CREATE TABLE Disponibilidad (
    id_disponibilidad INT PRIMARY KEY AUTO_INCREMENT,
    id_empleado INT,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado) ON DELETE CASCADE
);

-- Tabla de Citas
CREATE TABLE Citas (
    id_cita INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT,
    id_servicio INT,
    id_empleado INT,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado ENUM('Pendiente', 'Confirmada', 'Cancelada', 'Completada') DEFAULT 'Pendiente',
    notas TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_servicio) REFERENCES Servicios(id_servicio) ON DELETE SET NULL,
    FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado) ON DELETE SET NULL
);

-- Tabla de Reservas
CREATE TABLE Reservas (
    id_reserva INT PRIMARY KEY AUTO_INCREMENT,
    id_cita INT NOT NULL,
    id_disponibilidad INT NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cita) REFERENCES Citas(id_cita),
    FOREIGN KEY (id_disponibilidad) REFERENCES Disponibilidad(id_disponibilidad)
);

-- Tabla de Ventas
CREATE TABLE Ventas (
    id_venta INT PRIMARY KEY AUTO_INCREMENT,
    id_cliente INT,
    id_producto INT,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    total DECIMAL(10,2) CHECK (total > 0),
    fecha_venta DATE NOT NULL,
    metodo_pago ENUM('Efectivo', 'Tarjeta', 'Transferencia') NOT NULL,
    estado ENUM('Completada', 'Cancelada', 'Pendiente') DEFAULT 'Completada',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES Productos(id_producto) ON DELETE SET NULL
);

-- Tabla de Historial de cambios en citas
CREATE TABLE Historial_Citas (
    id_historial INT PRIMARY KEY AUTO_INCREMENT,
    id_cita INT,
    estado_anterior ENUM('Pendiente', 'Confirmada', 'Cancelada', 'Completada'),
    estado_nuevo ENUM('Pendiente', 'Confirmada', 'Cancelada', 'Completada'),
    fecha_cambio DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cita) REFERENCES Citas(id_cita) ON DELETE CASCADE
);

-- Tabla de Notificaciones
CREATE TABLE Notificaciones (
    id_notificacion INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT,
    tipo_usuario ENUM('Cliente', 'Empleado') NOT NULL,
    mensaje TEXT NOT NULL,
    leido BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES Clientes(id_cliente) ON DELETE CASCADE
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_cliente_correo ON Clientes(correo);
CREATE INDEX idx_empleado_correo ON Empleados(correo);
CREATE INDEX idx_servicio_nombre ON Servicios(nombre_servicio);
CREATE INDEX idx_producto_categoria ON Productos(categoria);
CREATE INDEX idx_citas_fecha ON Citas(fecha_hora);
CREATE INDEX idx_ventas_fecha ON Ventas(fecha_venta);

-- Trigger para actualizar inventario después de una venta
DELIMITER //
CREATE TRIGGER after_venta_insert
AFTER INSERT ON Ventas
FOR EACH ROW
BEGIN
    UPDATE Productos 
    SET inventario = inventario - NEW.cantidad
    WHERE id_producto = NEW.id_producto;
END//
DELIMITER ;

-- Trigger para registrar cambios en citas
DELIMITER //
CREATE TRIGGER before_cita_update
BEFORE UPDATE ON Citas
FOR EACH ROW
BEGIN
    IF OLD.estado != NEW.estado THEN
        INSERT INTO Historial_Citas (id_cita, estado_anterior, estado_nuevo)
        VALUES (OLD.id_cita, OLD.estado, NEW.estado);
    END IF;
END//
DELIMITER ;

-- Datos de ejemplo (Clientes, Empleados, Servicios, Productos)
INSERT INTO Clientes (nombre, contacto, correo, contraseña, genero, edad)
VALUES 
    ('Diego Cubides', '3120124521', 'Diego_9822@hotmail.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBAQNQxQxJ5K8i', 'masculino', 27),
    ('Steven Florez', '3507718249', 'sflorez498@gmail.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBAQNQxQxJ5K8i', 'masculino', 30);

INSERT INTO Empleados (nombre, contacto, correo, contraseña, id_rol)
VALUES 
    ('Laura Pérez', '3001234567', 'laura@estheticease.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBAQNQxQxJ5K8i', 3),
    ('Carlos Gómez', '3019876543', 'carlos@estheticease.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBAQNQxQxJ5K8i', 3);

INSERT INTO Servicios (nombre_servicio, descripcion, precio, duracion_minutos) 
VALUES 
    ('Corte de cabello', 'Corte profesional para mujeres y hombres', 200.00, 60),
    ('Manicure', 'Manicure con esmaltado semipermanente', 300.00, 90);

INSERT INTO Productos (nombre_producto, categoria, inventario, precio, stock_minimo) 
VALUES 
    ('Shampoo hidratante', 'Cuidado del cabello', 20, 150.00, 5),
    ('Crema facial', 'Cuidado de la piel', 15, 250.00, 3);

INSERT INTO Horarios (id_empleado, dia_semana, hora_inicio, hora_fin)
VALUES 
    (1, 'Lunes', '09:00:00', '17:00:00'),
    (2, 'Martes', '10:00:00', '18:00:00');

INSERT INTO Citas (id_cliente, id_servicio, id_empleado, fecha_hora, estado) 
VALUES 
    (1, 1, 1, '2025-03-15 10:00:00', 'Cancelada'),
    (2, 2, 2, '2025-03-16 14:30:00', 'Pendiente');

INSERT INTO Ventas (id_cliente, id_producto, cantidad, total, fecha_venta, metodo_pago) 
VALUES 
    (1, 1, 2, 300.00, '2025-04-11', 'Efectivo'),
    (2, 2, 1, 250.00, '2025-03-11', 'Tarjeta');
