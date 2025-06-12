import React from 'react';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const isAuthenticated = !!localStorage.getItem('token');
  const from = location.state?.from?.pathname || '/dashboard';

  // Intentar obtener el token del localStorage
  const token = localStorage.getItem('token');
  
  // Si no hay token, redirigir a login
  if (!token) {
    navigate('/login', { replace: true, state: { from: location.pathname } });
    return null;
  }

  // Si el token existe, continuar con el componente
  return children;
};

export default ProtectedRoute;
