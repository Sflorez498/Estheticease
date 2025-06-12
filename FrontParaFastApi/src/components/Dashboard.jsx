import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Dashboard.scss';

const Dashboard = () => {
  const navigate = useNavigate();
  const userId = localStorage.getItem('userId');

  // Simular datos del usuario
  const userData = {
    nombre: 'Cliente', // Esto debería venir de la API
    imagen: 'https://images.unsplash.com/photo-1560400688-677466a25d04?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
  };

  return (
    <div className="dashboard-container">
      {/* Sección de Bienvenida */}
      <div className="welcome-section">
        <div className="welcome-content">
          <h2>Bienvenido/a, {userData.nombre}</h2>
          <p>¡Disfruta de nuestros servicios de belleza y estética!</p>
        </div>
        <div className="welcome-image">
          <img src="https://images.unsplash.com/photo-1550439062-609e1531270e?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60" 
               alt="Bienvenida" 
               className="welcome-img" />
        </div>
      </div>

      {/* Sección de Opciones */}
      <div className="options-section">
        <h3>Tus Opciones</h3>
        <div className="options-grid">
          {/* Agendar Cita */}
          <div className="option-card" onClick={() => navigate('/calendario')}>
            <img src="https://images.unsplash.com/photo-1560439062-609e1531270e?ixlib=rb-1.2.1&auto=format&fit=crop&w=200&q=60" 
                 alt="Agendar Cita" 
                 className="option-img" />
            <h4>Agendar Cita</h4>
            <p>Reserva tu cita con nuestros especialistas</p>
          </div>

          {/* Comprar Productos */}
          <div className="option-card" onClick={() => navigate('/catalogo')}>
            <img src="https://images.unsplash.com/photo-1557862954-9e64453f842f?ixlib=rb-1.2.1&auto=format&fit=crop&w=200&q=60" 
                 alt="Productos" 
                 className="option-img" />
            <h4>Comprar Productos</h4>
            <p>Explora nuestra tienda de productos</p>
          </div>

          {/* Ver Citas */}
          <div className="option-card" onClick={() => navigate('/mis-citas')}>
            <img src="https://images.unsplash.com/photo-1557862954-9e64453f842f?ixlib=rb-1.2.1&auto=format&fit=crop&w=200&q=60" 
                 alt="Mis Citas" 
                 className="option-img" />
            <h4>Mis Citas</h4>
            <p>Ver y gestionar tus citas</p>
          </div>
        </div>
      </div>

      {/* Información del Usuario */}
      <div className="user-info">
        <img src={userData.imagen} alt="Perfil" className="user-image" />
        <div className="user-details">
          <h4>ID: {userId}</h4>
          {/* Aquí podríamos mostrar más información del usuario */}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
