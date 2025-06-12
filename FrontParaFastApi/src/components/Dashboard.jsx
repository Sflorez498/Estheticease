import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/dashboard.scss';
import LogoutButton from './LogoutButton';

const Dashboard = () => {
  const navigate = useNavigate();
  const userId = localStorage.getItem('userId');

  // Redirigir a login si no hay sesión
  React.useEffect(() => {
    if (!userId) {
      navigate('/login');
    }
  }, [navigate, userId]);

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Bienvenido a Estheticease</h1>
        <LogoutButton />
      </div>
      <div className="dashboard-options">
        <Link to="/catalogo" className="dashboard-card">
          <div className="dashboard-icon">🛒</div>
          <h2>Catálogo de Productos</h2>
          <p>Explora y compra nuestros productos de belleza</p>
        </Link>
        <Link to="/calendario" className="dashboard-card">
          <div className="dashboard-icon">📅</div>
          <h2>Agendar Cita</h2>
          <p>Reserva tu cita con nuestros servicios</p>
        </Link>
      </div>
    </div>
  );
};

export default Dashboard;
