import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/carrito.scss';

const Carrito = () => {
  const navigate = useNavigate();
  const [productos, setProductos] = useState([]);
  const [total, setTotal] = useState(0);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [paymentInfo, setPaymentInfo] = useState({
    cardNumber: '',
    expiryDate: '',
    cvv: '',
    name: ''
  });

  useEffect(() => {
    const carrito = JSON.parse(localStorage.getItem('carrito') || '[]');
    setProductos(carrito);
    calcularTotal(carrito);
  }, []);

  const calcularTotal = (items) => {
    const suma = items.reduce((acc, item) => acc + (item.precio * item.cantidad), 0);
    setTotal(suma);
  };

  const actualizarCantidad = (index, nuevaCantidad) => {
    if (nuevaCantidad < 1) return;
    
    const nuevosProductos = [...productos];
    nuevosProductos[index].cantidad = nuevaCantidad;
    setProductos(nuevosProductos);
    localStorage.setItem('carrito', JSON.stringify(nuevosProductos));
    calcularTotal(nuevosProductos);
  };

  const eliminarProducto = (index) => {
    const nuevosProductos = productos.filter((_, i) => i !== index);
    setProductos(nuevosProductos);
    localStorage.setItem('carrito', JSON.stringify(nuevosProductos));
    calcularTotal(nuevosProductos);
  };

  const handlePaymentSubmit = async (e) => {
    e.preventDefault();
    try {
      // Simulación de procesamiento de pago
      const paymentResult = await procesarPago();
      
      if (paymentResult.success) {
        // Actualizar stock de productos
        for (const producto of productos) {
          await axios.put(`http://localhost:8000/productos/stock/${producto.id_producto}`, {
            cantidad: producto.cantidad
          });
        }

        // Crear orden en la base de datos
        await axios.post('http://localhost:8000/ordenes', {
          id_cliente: localStorage.getItem('userId'),
          productos: productos,
          total: total,
          estado: 'completado'
        });

        // Limpiar carrito
        localStorage.removeItem('carrito');
        setProductos([]);
        setTotal(0);
        setShowPaymentModal(false);

        alert('¡Pago procesado exitosamente!');
        navigate('/mis-compras');
      }
    } catch (error) {
      console.error('Error al procesar el pago:', error);
      alert('Error al procesar el pago. Por favor intente nuevamente.');
    }
  };

  const procesarPago = () => {
    // Simulación de procesamiento de pago
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ success: true, message: 'Pago procesado exitosamente' });
      }, 2000);
    });
  };

  return (
    <div className="carrito-container">
      <h2>Mi Carrito</h2>
      
      {productos.length === 0 ? (
        <p>No hay productos en el carrito</p>
      ) : (
        <>
          <div className="productos-lista">
            {productos.map((producto, index) => (
              <div key={index} className="producto-item">
                <img src={producto.imagen_url} alt={producto.nombre} />
                <div className="producto-info">
                  <h3>{producto.nombre}</h3>
                  <p>{producto.descripcion}</p>
                  <p className="precio">${producto.precio}</p>
                </div>
                <div className="cantidad-control">
                  <button onClick={() => actualizarCantidad(index, producto.cantidad - 1)}>-</button>
                  <span>{producto.cantidad}</span>
                  <button onClick={() => actualizarCantidad(index, producto.cantidad + 1)}>+</button>
                </div>
                <button className="eliminar" onClick={() => eliminarProducto(index)}>Eliminar</button>
              </div>
            ))}
          </div>
          
          <div className="carrito-resumen">
            <h3>Resumen de la Compra</h3>
            <p>Total: ${total}</p>
            <button className="pagar" onClick={() => setShowPaymentModal(true)}>
              Proceder al Pago
            </button>
          </div>
        </>
      )}

      {showPaymentModal && (
        <div className="modal-payment">
          <div className="modal-content">
            <h3>Información de Pago</h3>
            <form onSubmit={handlePaymentSubmit}>
              <input
                type="text"
                placeholder="Número de Tarjeta"
                value={paymentInfo.cardNumber}
                onChange={(e) => setPaymentInfo({...paymentInfo, cardNumber: e.target.value})}
                required
              />
              <div className="card-details">
                <input
                  type="text"
                  placeholder="MM/YY"
                  value={paymentInfo.expiryDate}
                  onChange={(e) => setPaymentInfo({...paymentInfo, expiryDate: e.target.value})}
                  required
                />
                <input
                  type="text"
                  placeholder="CVV"
                  value={paymentInfo.cvv}
                  onChange={(e) => setPaymentInfo({...paymentInfo, cvv: e.target.value})}
                  required
                />
              </div>
              <input
                type="text"
                placeholder="Nombre en la Tarjeta"
                value={paymentInfo.name}
                onChange={(e) => setPaymentInfo({...paymentInfo, name: e.target.value})}
                required
              />
              <div className="modal-buttons">
                <button type="submit">Confirmar Pago</button>
                <button type="button" onClick={() => setShowPaymentModal(false)}>Cancelar</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Carrito; 