import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';
import '../styles/mis-compras.scss';

const MisCompras = () => {
  const [ordenes, setOrdenes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const userId = localStorage.getItem('userId');
    if (!userId) {
      navigate('/login');
      return;
    }

    const cargarOrdenes = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/ordenes/cliente/${userId}`);
        setOrdenes(response.data);
      } catch (error) {
        console.error('Error al cargar órdenes:', error);
      } finally {
        setLoading(false);
      }
    };

    cargarOrdenes();
  }, []);

  const formatearFecha = (fecha) => {
    return format(new Date(fecha), "d 'de' MMMM, yyyy", { locale: es });
  };

  if (loading) {
    return <div className="loading">Cargando historial de compras...</div>;
  }

  return (
    <div className="mis-compras-container">
      <h2>Mi Historial de Compras</h2>

      {ordenes.length === 0 ? (
        <p className="no-ordenes">No tienes compras realizadas</p>
      ) : (
        <div className="ordenes-lista">
          {ordenes.map((orden) => (
            <div key={orden.id_orden} className="orden-card">
              <div className="orden-header">
                <div className="orden-info">
                  <h3>Orden #{orden.id_orden}</h3>
                  <p className="fecha">{formatearFecha(orden.fecha)}</p>
                </div>
                <div className="orden-estado">
                  <span className={`estado ${orden.estado.toLowerCase()}`}>
                    {orden.estado}
                  </span>
                </div>
              </div>

              <div className="productos-lista">
                {orden.productos.map((producto, index) => (
                  <div key={index} className="producto-item">
                    <div className="producto-info">
                      <p className="nombre">{producto.nombre}</p>
                      <p className="cantidad">Cantidad: {producto.cantidad}</p>
                    </div>
                    <p className="precio">
                      ${(producto.precio_unitario * producto.cantidad).toFixed(2)}
                    </p>
                  </div>
                ))}
              </div>

              <div className="orden-footer">
                <div className="total">
                  <span>Total</span>
                  <span className="monto">${orden.total.toFixed(2)}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MisCompras; 