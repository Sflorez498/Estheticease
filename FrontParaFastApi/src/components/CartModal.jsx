import React from 'react';
import { FaShoppingCart } from 'react-icons/fa';
import '../styles/CartModal.scss';

const CartModal = ({ isOpen, onClose }) => {
  const carrito = JSON.parse(localStorage.getItem('carrito') || '[]');
  const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);

  if (!isOpen) return null;

  return (
    <div className="cart-modal-overlay">
      <div className="cart-modal">
        <div className="cart-header">
          <h3>Carrito de Compras</h3>
          <button onClick={onClose} className="close-button">×</button>
        </div>
        {carrito.length === 0 ? (
          <p className="empty-cart">El carrito está vacío</p>
        ) : (
          <div className="cart-items">
            {carrito.map((item, index) => (
              <div key={`cart-item-${item.id}-${index}`} className="cart-item">
                <img 
                  src={item.imagen || 'https://via.placeholder.com/80x80?text=No+Image'} 
                  alt={item.nombre} 
                  className="cart-item-image"
                  onError={(e) => {
                    e.target.src = 'https://via.placeholder.com/80x80?text=No+Image';
                  }}
                />
                <div className="cart-item-details">
                  <h4>{item.nombre}</h4>
                  <p>Cantidad: {item.cantidad}</p>
                  <p>Precio: ${item.precio.toLocaleString()}</p>
                </div>
                <div className="cart-item-total">
                  <p>Total: ${item.precio * item.cantidad}</p>
                </div>
              </div>
            ))}
            <div className="cart-total">
              <h4>Total: ${total.toLocaleString()}</h4>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CartModal;
