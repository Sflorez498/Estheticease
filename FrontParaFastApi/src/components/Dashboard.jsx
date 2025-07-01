// Componente principal del Dashboard
// Muestra las opciones principales disponibles para el usuario
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/dashboard.scss';
import LogoutButton from './LogoutButton';

const Dashboard = () => {
  const navigate = useNavigate();
  // Obtener el ID del usuario desde localStorage
  const userId = localStorage.getItem('userId');

  // Verificar si hay sesión activa
  React.useEffect(() => {
    if (!userId) {
      navigate('/login');
    }
  }, [navigate, userId]);

  return (
    <div className="dashboard-container">
      {/* Encabezado del dashboard */}
      <div className="dashboard-header">
        <h1>Bienvenido a Estheticease</h1>
        <LogoutButton />  {/* Botón para cerrar sesión */}
      </div>
      {/* Contenedor de opciones */}
      <div className="dashboard-options">
        {/* Opción de Catálogo */}
        <Link to="/catalogo" className="dashboard-card">
          <div className="dashboard-icon">🛒</div>
          <h2>Catálogo de Productos</h2>
          <p>Explora y compra nuestros productos de belleza</p>
        </Link>
        {/* Opción de Calendario */}
        <Link to="/calendario" className="dashboard-card">
          <div className="dashboard-icon">📅</div>
          <h2>Agendar Cita</h2>
          <p>Reserva tu cita con nuestros servicios</p>
        </Link>
        {/* Opción de Editar Perfil */}
        <Link to="/editar-perfil" className="dashboard-card">
          <div className="dashboard-icon">👤</div>
          <h2>Editar Perfil</h2>
          <p>Actualiza tus datos personales</p>
        </Link>
      </div>
    </div>
  );
};

export default Dashboard;
