// Componente Dashboard: Panel principal de la aplicación
// Este componente proporciona la interfaz principal de navegación y bienvenida

// Importaciones necesarias
import React, { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/dashboard.scss';
import LogoutButton from './LogoutButton';

const Dashboard = () => {
  // Hook para manejar la navegación entre rutas
  const navigate = useNavigate();
  // Obtención del ID del usuario actual
  const userId = localStorage.getItem('userId');

  // Efecto que verifica la sesión al cargar el componente
  useEffect(() => {
    // Si no hay sesión, redirige al login
    if (!userId) {
      navigate('/login');
    }
  }, [navigate, userId]);

  return (
    <div className="dashboard-container">
      {/* Barra lateral de navegación */}
      <aside className="sidebar">
        {/* Título de la aplicación */}
        <h2 className="sidebar-title">Estheticease</h2>

        {/* Menú de navegación */}
        <nav className="sidebar-menu">
          {/* Enlace al catálogo de productos */}
          <Link to="/catalogo" className="sidebar-item">
            <span className="icon">🛍️</span>
            <span className="label">Catálogo</span>
          </Link>

          {/* Enlace para agendar citas */}
          <Link to="/calendario" className="sidebar-item">
            <span className="icon">💆‍♀️</span>
            <span className="label">Agendar Cita</span>
          </Link>

          {/* Enlace para editar perfil */}
          <Link to="/editar-perfil" className="sidebar-item">
            <span className="icon">👤</span>
            <span className="label">Editar Perfil</span>
          </Link>
        </nav>

        {/* Sección para el botón de cierre de sesión */}
        <div className="logout-section">
          <LogoutButton />
        </div>
      </aside>

      {/* Área principal del dashboard */}
      <main className="main-content">
        {/* Sección de bienvenida */}
        <section className="welcome-box">
          <h1>¡Bienvenida a Estheticease!</h1>
          <p>
            Hoy es un buen día para consentirte 🌸 <br />
            Disfruta de nuestros productos y servicios pensados para tu bienestar.
          </p>
        </section>
      </main>
    </div>
  );
};

export default Dashboard;
