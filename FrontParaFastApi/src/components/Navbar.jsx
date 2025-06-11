import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../styles/Navbar.scss';

const Navbar = () => {
  const [carritoCount, setCarritoCount] = useState(0);
  const [showCartPreview, setShowCartPreview] = useState(false);

  useEffect(() => {
    const carrito = JSON.parse(localStorage.getItem('carrito') || '[]');
    let count = 0;
    carrito.forEach(item => {
      count += item.cantidad || 0;
    });
    setCarritoCount(count);
  }, []);

  const handleCartClick = () => {
    setShowCartPreview(!showCartPreview);
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/">EstheticEase</Link>
      </div>
      <div className="navbar-links">
        <Link to="/catalogo">Catálogo</Link>
        <div className="cart-container" onClick={handleCartClick}>
          <i className="cart-icon fas fa-shopping-cart"></i>
          {carritoCount > 0 && (
            <span className="carrito-count">{carritoCount}</span>
          )}
          <div className={`cart-preview ${showCartPreview ? 'active' : ''}`}>
            <div className="cart-preview-header">
              <h3>Carrito de compras</h3>
              <button>Ver carrito</button>
            </div>
            <div className="cart-preview-items">
              {/* Aquí se renderizarán los items del carrito */}
            </div>
            <div className="cart-preview-footer">
              <p>Total: $0.00</p>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
