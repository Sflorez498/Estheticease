// src/components/Login.jsx
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/estheticease.scss';

const Login = () => {
  const navigate = useNavigate();
  const [error, setError] = useState('');

  const manejarLogin = async (e) => {
    e.preventDefault();
    const form = e.target;

    const correo = form.Correo.value;
    const contraseña = form.Contraseña.value;

    try {
      const response = await axios.post('http://localhost:8000/api/clientes/login', {
        correo: correo,
        contraseña: contraseña
      });

      console.log('Respuesta del backend:', response.data);
      console.log('Status:', response.status);

      // Verificar si la respuesta es exitosa
      if (response.status === 200) {
        console.log('Inicio de sesión exitoso');
        
        // Generar un token simple
        const token = 'Bearer ' + Math.random().toString(36).substring(2, 15);
        
        // Guardar el token y el ID del cliente
        localStorage.setItem('token', token);
        localStorage.setItem('userId', response.data.Id_Cliente);
        
        // Forzar la actualización del componente antes de redirigir
        window.location.href = '/dashboard';
      } else {
        setError('Error al iniciar sesión');
      }
    } catch (error) {
      setError(error.response?.data?.detail || 'Error al iniciar sesión');
      console.error('Error de inicio de sesión:', error);
    }
  };

  const irARegistro = () => {
    navigate("/registro");
  };

  const irAHome = () => {
    navigate("/");
  };

  return (
    <div className="fondo">
      {/* Barra de navegación */}
      <div className="navbar">
        <div className="navbar-logo" onClick={irAHome}>
          Estheticease
        </div>
        <ul className="navbar-links">
          <li onClick={irAHome}>Inicio</li>
          <li onClick={irARegistro}>Registrarse</li>
        </ul>
      </div>

      <div className="containerForm">
        <h2>Iniciar Sesión</h2>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <form onSubmit={manejarLogin}>
          <fieldset>
            <label htmlFor="Correo">Correo</label>
            <input type="email" id="Correo" name="Correo" required />
          </fieldset>
          <fieldset>
            <label htmlFor="Contraseña">Contraseña</label>
            <input type="password" id="Contraseña" name="Contraseña" required />
          </fieldset>
          <button type="submit">Entrar</button>
        </form>
      </div>
    </div>
  );
};

export default Login;