import React, { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/dashboard.scss';
import LogoutButton from './LogoutButton';

const Dashboard = () => {
  const navigate = useNavigate();
  const userId = localStorage.getItem('userId');

  useEffect(() => {
    if (!userId) {
      navigate('/login');
    }
  }, [navigate, userId]);

  return (
    <div className="dashboard-container">
      {/* Barra lateral con opciones */}
      <aside className="sidebar">
        <h2 className="sidebar-title">Estheticease</h2>

        <nav className="sidebar-menu">
          <Link to="/catalogo" className="sidebar-item">
            <span className="icon">🛍️</span>
            <span className="label">Catálogo</span>
          </Link>

          <Link to="/calendario" className="sidebar-item">
            <span className="icon">💆‍♀️</span>
            <span className="label">Agendar Cita</span>
          </Link>

          <Link to="/editar-perfil" className="sidebar-item">
            <span className="icon">👤</span>
            <span className="label">Editar Perfil</span>
          </Link>
        </nav>

        <div className="logout-section">
          <LogoutButton />
        </div>
      </aside>

      {/* Contenido principal con bienvenida */}
      <main className="main-content">
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
