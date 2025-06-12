import React from 'react';
import { useNavigate } from 'react-router-dom';

const LogoutButton = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Eliminar el token y el userId del localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    
    // Redirigir a la página de inicio
    navigate('/');
  };

  return (
    <button
      onClick={handleLogout}
      className="logout-button"
      style={{
        backgroundColor: '#e74c3c',
        color: 'white',
        border: 'none',
        padding: '8px 16px',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '1rem',
        transition: 'background-color 0.2s',
        marginRight: '1rem'
      }}
    >
      Cerrar Sesión
    </button>
  );
};

export default LogoutButton;
