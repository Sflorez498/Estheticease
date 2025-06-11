-- Crear la tabla productos
CREATE TABLE IF NOT EXISTS productos (
    Id_Producto INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion TEXT,
    Precio DECIMAL(10,2) NOT NULL,
    Stock INT NOT NULL DEFAULT 0,
    Imagen_URL VARCHAR(255),
    Categoria VARCHAR(50) NOT NULL,
    Fecha_Creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Fecha_Actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insertar datos de prueba
INSERT INTO productos (Nombre, Descripcion, Precio, Stock, Imagen_URL, Categoria) VALUES
('Serum Facial Revitalizante', 'Un serum ligero para una piel radiante.', 25000, 50, 'https://http2.mlstatic.com/D_Q_NP_886565-MLU74002890508_012024-O.webp', 'Cuidado Facial'),
('Mascarilla de Arcilla Purificante', 'Limpia profundamente los poros y reduce el brillo.', 18000, 30, 'https://http2.mlstatic.com/D_NQ_NP_672265-MLU78043970279_072024-O.webp', 'Cuidado Facial'),
('Aceite Esencial de Lavanda Relajante', 'Promueve la calma y el bienestar.', 12000, 40, 'https://m.media-amazon.com/images/I/7193gkOb8iL._AC_UF1000,1000_QL80_.jpg', 'Cuidado Corporal'),
('Exfoliante Corporal de Café', 'Suaviza y revitaliza la piel.', 20000, 25, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR92KOmDoYAbTE_cTgzF0htDkc8BELtWdi-4Q&s', 'Cuidado Corporal'),
('Crema Hidratante de Rosas', 'Hidratación profunda con un aroma delicado.', 28000, 45, 'https://habibdroguerias.vtexassets.com/arquivos/ids/155849-800-auto?v=638459608786100000&width=800&height=auto&aspect=true', 'Cuidado Facial'),
('Tónico Facial Refrescante', 'Equilibra el pH de la piel después de la limpieza.', 15000, 60, 'https://habibdroguerias.vtexassets.com/arquivos/ids/163701/7708877993755.jpg?v=638524255998130000', 'Cuidado Facial'),
('Bálsamo Labial Nutritivo', 'Hidrata y protege los labios secos.', 8000, 70, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQNSKBQjkPFNybi1_jMyJzoVKa3FZevwVhSZQ&s', 'Cuidado Labial'),
('Mascarilla Capilar Reparadora', 'Fortalece y da brillo al cabello dañado.', 22000, 35, 'https://static.sweetcare.com/img/prd/488/v-638200521557168666/elvive-013686ze_01.jpg', 'Cuidado Capilar');
