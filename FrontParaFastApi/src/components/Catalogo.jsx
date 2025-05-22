// src/components/Catalogo.jsx
import React from 'react';
import '../styles/Catalogo.scss'; // Importa el archivo SCSS

const productos = [
  {
    id: 1,
    nombre: 'Serum Facial Revitalizante',
    descripcion: 'Un serum ligero para una piel radiante.',
    imagen: 'https://http2.mlstatic.com/D_Q_NP_886565-MLU74002890508_012024-O.webp',
    precio: '$25.000',
  },
  {
    id: 2,
    nombre: 'Mascarilla de Arcilla Purificante',
    descripcion: 'Limpia profundamente los poros y reduce el brillo.',
    imagen: 'https://http2.mlstatic.com/D_NQ_NP_672265-MLU78043970279_072024-O.webp',
    precio: '$18.000',
  },
  {
    id: 3,
    nombre: 'Aceite Esencial de Lavanda Relajante',
    descripcion: 'Promueve la calma y el bienestar.',
    imagen: 'https://m.media-amazon.com/images/I/7193gkOb8iL._AC_UF1000,1000_QL80_.jpg',
    precio: '$12.000',
  },
  {
    id: 4,
    nombre: 'Exfoliante Corporal de Café',
    descripcion: 'Suaviza y revitaliza la piel.',
    imagen: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR92KOmDoYAbTE_cTgzF0htDkc8BELtWdi-4Q&s',
    precio: '$20.000',
  },
  {
    id: 5,
    nombre: 'Crema Hidratante de Rosas',
    descripcion: 'Hidratación profunda con un aroma delicado.',
    imagen: 'https://habibdroguerias.vtexassets.com/arquivos/ids/155849-800-auto?v=638459608786100000&width=800&height=auto&aspect=true',
    precio: '$28.000',
  },
  {
    id: 6,
    nombre: 'Tónico Facial Refrescante',
    descripcion: 'Equilibra el pH de la piel después de la limpieza.',
    imagen: 'https://habibdroguerias.vtexassets.com/arquivos/ids/163701/7708877993755.jpg?v=638524255998130000',
    precio: '$15.000',
  },
  {
    id: 7,
    nombre: 'Bálsamo Labial Nutritivo',
    descripcion: 'Hidrata y protege los labios secos.',
    imagen: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQNSKBQjkPFNybi1_jMyJzoVKa3FZevwVhSZQ&s',
    precio: '$8.000',
  },
  {
    id: 8,
    nombre: 'Mascarilla Capilar Reparadora',
    descripcion: 'Fortalece y da brillo al cabello dañado.',
    imagen: 'https://static.sweetcare.com/img/prd/488/v-638200521557168666/elvive-013686ze_01.jpg',
    precio: '$22.000',
  },
];

const Catalogo = () => {
  return (
    <div className="catalogo-container">
      <h2>Nuestro Catálogo de Belleza</h2>
      <ul className="productos-grid">
        {productos.map(producto => (
          <li key={producto.id} className="producto-item">
            <img src={producto.imagen} alt={producto.nombre} className="producto-imagen" />
            <h3 className="producto-nombre">{producto.nombre}</h3>
            <p className="producto-descripcion">{producto.descripcion}</p>
            <span className="producto-precio">{producto.precio}</span>
            <button className="producto-boton">Ver más</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Catalogo;