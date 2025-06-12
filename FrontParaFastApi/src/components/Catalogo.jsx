// src/components/Catalogo.jsx
import React, { useState, useEffect } from 'react';
import { FaShoppingCart } from 'react-icons/fa';
import { FaTimes } from 'react-icons/fa';
import { Modal, Button, Form, Alert } from 'react-bootstrap';
import '../styles/Catalogo.scss';
import { productos } from '../data/productos';

const obtenerTotalCarrito = (carrito) => {
  return carrito.reduce((total, item) => total + (item.precio * item.cantidad), 0);
};

const Catalogo = () => {
  const [loading, setLoading] = useState(true);
  const [mostrarCarrito, setMostrarCarrito] = useState(false);
  const [mostrarPago, setMostrarPago] = useState(false);
  const [numeroTarjeta, setNumeroTarjeta] = useState('');
  const [clave, setClave] = useState('');
  const [errorPago, setErrorPago] = useState('');
  const [exitoPago, setExitoPago] = useState(false);

  // Obtener carrito del localStorage
  const carrito = JSON.parse(localStorage.getItem('carrito') || '[]');
  const totalItems = carrito.reduce((total, item) => total + item.cantidad, 0);

  const agregarAlCarrito = (producto) => {
    // Obtener el carrito actual del localStorage
    let carrito = JSON.parse(localStorage.getItem('carrito') || '[]');
    
    // Verificar si el producto ya está en el carrito
    const productoExistente = carrito.find(p => p.id_producto === producto.id_producto);
    
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

  const eliminarDelCarrito = (id) => {
    const nuevoCarrito = carrito.filter(item => item.id_producto !== id);
    localStorage.setItem('carrito', JSON.stringify(nuevoCarrito));
    setMostrarCarrito(true); // Actualizar la vista del carrito
  };

  const limpiarCarrito = () => {
    localStorage.removeItem('carrito');
    setMostrarCarrito(true); // Actualizar la vista del carrito
  };

  const realizarPago = () => {
    // Validar número de tarjeta (10 dígitos)
    if (!/^[0-9]{10}$/.test(numeroTarjeta)) {
      setErrorPago('El número de tarjeta debe tener exactamente 10 dígitos');
      return;
    }

    // Validar clave (al menos 4 caracteres)
    if (clave.length < 4) {
      setErrorPago('La clave debe tener al menos 4 caracteres');
      return;
    }

    // Simular proceso de pago
    setExitoPago(true);
    setTimeout(() => {
      // Limpiar el carrito
      limpiarCarrito();
      // Cerrar el modal de pago
      setMostrarPago(false);
      // Limpiar los campos
      setNumeroTarjeta('');
      setClave('');
      setErrorPago('');
      setExitoPago(false);
      // Cerrar el carrito
      setMostrarCarrito(false);
    }, 1500);
  };

  useEffect(() => {
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="catalogo-container">
        <h2>Cargando productos...</h2>
      </div>
    );
  }

  return (
    <div className="catalogo-container">
      {/* Carrito */}
      <div className="carrito-header">
        <FaShoppingCart 
          className="cart-icon-header" 
          onClick={() => setMostrarCarrito(!mostrarCarrito)}
          style={{ cursor: 'pointer' }}
        />
        {totalItems > 0 && (
          <span className="cart-count">{totalItems}</span>
        )}
      </div>

      {mostrarCarrito && (
        <div className="carrito-modal">
          <div className="carrito-modal-content">
            <div className="carrito-header-modal">
              <h3>Carrito de Compras</h3>
              <FaTimes 
                className="close-icon" 
                onClick={() => setMostrarCarrito(false)}
              />
            </div>
            {carrito.length > 0 ? (
              <div className="carrito-items">
                {carrito.map(item => (
                  <div key={item.id_producto} className="carrito-item">
                    <img 
                      src={item.imagen_url} 
                      alt={item.nombre_producto} 
                      className="carrito-item-image"
                    />
                    <div className="carrito-item-details">
                      <h4>{item.nombre_producto}</h4>
                      <p>Cantidad: {item.cantidad}</p>
                      <p>Precio: ${item.precio.toLocaleString()}</p>
                      <button 
                        className="carrito-item-remove" 
                        onClick={() => eliminarDelCarrito(item.id_producto)}
                      >
                        Eliminar
                      </button>
                    </div>
                  </div>
                ))}
                <div className="carrito-total">
                  <h4>Total: ${obtenerTotalCarrito(carrito).toLocaleString()}</h4>
                  <div className="carrito-actions">
                    <button 
                      className="carrito-pagar" 
                      onClick={() => setMostrarPago(true)}
                    >
                      Realizar Pago
                    </button>
                    <button className="carrito-limpiar" onClick={limpiarCarrito}>
                      Limpiar Carrito
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <p className="carrito-vacio">El carrito está vacío</p>
            )}
          </div>
        </div>
      )}

      {/* Modal de Pago */}
      <Modal show={mostrarPago} onHide={() => setMostrarPago(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Pago</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {exitoPago ? (
            <Alert variant="success">
              ¡Compra exitosa! Los productos han sido eliminados del carrito.
            </Alert>
          ) : (
            <Form onSubmit={(e) => {
              e.preventDefault();
              realizarPago();
            }}>
              <Form.Group className="mb-3">
                <Form.Label>Número de tarjeta</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="1234567890"
                  value={numeroTarjeta}
                  onChange={(e) => setNumeroTarjeta(e.target.value)}
                />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Clave</Form.Label>
                <Form.Control
                  type="password"
                  placeholder="Clave"
                  value={clave}
                  onChange={(e) => setClave(e.target.value)}
                />
              </Form.Group>
              {errorPago && <Alert variant="danger">{errorPago}</Alert>}
              <Button variant="primary" type="submit" className="w-100">
                Pagar
              </Button>
            </Form>
          )}
        </Modal.Body>
      </Modal>

      {/* Catálogo */}
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