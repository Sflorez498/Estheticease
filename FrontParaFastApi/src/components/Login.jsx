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
      const response = await axios.post('http://localhost:8000/login/', {
        Correo: correo,
        Contraseña: contraseña,
      });

      // Si la respuesta es exitosa (status code 2xx)
      if (response.status >= 200 && response.status < 300) {
        alert('Inicio de sesión exitoso');
        // Aquí podrías guardar el token de autenticación que el backend debería devolver
        // Por ejemplo: localStorage.setItem('authToken', response.data.token);
        navigate('/catalogo');
      } else {
        setError(response.data?.detail || 'Error al iniciar sesión');
      }
    } catch (error) {
      setError(error.response?.data?.detail || 'Error al iniciar sesión');
      console.error('Error de inicio de sesión:', error);
    }
  };

  return (
    <div className="fondo">
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