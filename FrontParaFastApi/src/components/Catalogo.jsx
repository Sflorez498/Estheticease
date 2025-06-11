// src/components/Catalogo.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FaShoppingCart } from 'react-icons/fa';
import '../styles/Catalogo.scss';

const productos = [
  {
    id: 1,
    nombre: 'Serum Facial Revitalizante',
    descripcion: 'Un serum ligero para una piel radiante.',
    imagen: 'https://http2.mlstatic.com/D_Q_NP_886565-MLU74002890508_012024-O.webp',
    precio: 25000,
  },
  {
    id: 2,
    nombre: 'Mascarilla de Arcilla Purificante',
    descripcion: 'Limpia profundamente los poros y reduce el brillo.',
    imagen: 'https://http2.mlstatic.com/D_NQ_NP_672265-MLU78043970279_072024-O.webp',
    precio: 18000,
  },
  {
    id: 3,
    nombre: 'Aceite Esencial de Lavanda Relajante',
    descripcion: 'Promueve la calma y el bienestar.',
    imagen: 'https://m.media-amazon.com/images/I/7193gkOb8iL._AC_UF1000,1000_QL80_.jpg',
    precio: 12000,
  },
  {
    id: 4,
    nombre: 'Exfoliante Corporal de Café',
    descripcion: 'Suaviza y revitaliza la piel.',
    imagen: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR92KOmDoYAbTE_cTgzF0htDkc8BELtWdi-4Q&s',
    precio: 20000,
  },
  {
    id: 5,
    nombre: 'Crema Hidratante de Rosas',
    descripcion: 'Hidratación profunda con un aroma delicado.',
    imagen: 'https://habibdroguerias.vtexassets.com/arquivos/ids/155849-800-auto?v=638459608786100000&width=800&height=auto&aspect=true',
    precio: 28000,
  },
  {
    id: 6,
    nombre: 'Tónico Facial Refrescante',
    descripcion: 'Equilibra el pH de la piel después de la limpieza.',
    imagen: 'https://habibdroguerias.vtexassets.com/arquivos/ids/163701/7708877993755.jpg?v=638524255998130000',
    precio: 15000,
  },
  {
    id: 7,
    nombre: 'Bálsamo Labial Nutritivo',
    descripcion: 'Hidrata y protege los labios secos.',
    imagen: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQNSKBQjkPFNybi1_jMyJzoVKa3FZevwVhSZQ&s',
    precio: 8000,
  },
  {
    id: 8,
    nombre: 'Mascarilla Capilar Reparadora',
    descripcion: 'Fortalece y da brillo al cabello dañado.',
    imagen: 'https://static.sweetcare.com/img/prd/488/v-638200521557168666/elvive-013686ze_01.jpg',
    precio: 22000,
  },
];

const agregarAlCarrito = (producto) => {
  // Obtener el carrito actual del localStorage
  let carrito = JSON.parse(localStorage.getItem('carrito') || '[]');
  
  // Verificar si el producto ya está en el carrito
  const productoExistente = carrito.find(p => p.id === producto.id);
  
  if (productoExistente) {
    // Si existe, aumentar la cantidad
    productoExistente.cantidad += 1;
  } else {
    // Si no existe, agregar con cantidad 1
    carrito.push({
      ...producto,
      cantidad: 1
    });
  }
  
  // Guardar el carrito actualizado
  localStorage.setItem('carrito', JSON.stringify(carrito));
  
  // Mostrar mensaje de éxito
  alert('Producto agregado al carrito');
};

const Catalogo = () => {
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProductos = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/productos');
        if (!response.ok) {
          const errorData = await response.json().catch(() => null);
          throw new Error(errorData?.detail || 'Error al cargar productos');
        }
        const data = await response.json();
        console.log('Datos recibidos de la API:', data);
        
        // Verificar si data es un array y tiene la estructura correcta
        if (Array.isArray(data)) {
          const productosFormateados = data.map(item => ({
            id_producto: item.id_producto || 0,
            nombre: item.nombre_producto || 'Producto sin nombre',
            precio: item.precio || 0,
            stock: item.stock || 0,
            categoria: item.categoria || 'Sin categoría',
            // Agregar una imagen vacía por defecto
            imagen: item.imagen_url || 'https://via.placeholder.com/200x200?text=No+Image'
          }));
          setProductos(productosFormateados);
        } else {
          throw new Error('Los datos no son un array válido');
        }
      } catch (error) {
        console.error('Error al cargar productos:', error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProductos();
  }, []);

  if (loading) {
    return (
      <div className="catalogo-container">
        <h2>Cargando productos...</h2>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="catalogo-container">
        <h2>Cargando productos...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div className="catalogo-container">
        <h2>Error al cargar productos</h2>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="catalogo-container">
      <h2>Nuestro Catálogo de Belleza</h2>
      <ul className="productos-grid">
        {productos.map(producto => (
          <li key={producto.id_producto} className="producto-item">
            <img src={producto.imagen} alt={producto.nombre} className="producto-imagen" />
            <h3 className="producto-nombre">{producto.nombre}</h3>
            <p className="producto-descripcion">{producto.descripcion}</p>
            <span className="producto-precio">${producto.precio ? producto.precio.toLocaleString() : 'Precio no disponible'}</span>
            <button 
              className="producto-boton" 
              onClick={() => agregarAlCarrito(producto)}
            >
              <FaShoppingCart className="cart-icon" />
              Agregar al Carrito
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Catalogo;