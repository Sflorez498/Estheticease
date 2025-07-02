import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/estheticease.scss';

const FormCargo = () => {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const cargarCliente = async (e) => {
    e.preventDefault();
    const form = e.target;

    if (!form.Nombre.value.trim()) {
      setError('Por favor, ingrese un nombre');
      return;
    }
    if (!form.Contacto.value.trim()) {
      setError('Por favor, ingrese un teléfono');
      return;
    }
    if (!form.Correo.value.trim() || !form.Correo.value.includes('@')) {
      setError('Por favor, ingrese un correo válido');
      return;
    }
    if (!form.Contraseña.value.trim()) {
      setError('Por favor, ingrese una contraseña');
      return;
    }

    const nuevoCliente = {
      nombre: form.Nombre.value.trim(),
      contacto: form.Contacto.value.trim(),
      correo: form.Correo.value.trim(),
      contraseña: form.Contraseña.value,
      genero: form.Genero.value.trim(),
      edad: parseInt(form.Edad.value) || null,
    };

    try {
      setLoading(true);
      setError('');

      const config = {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        withCredentials: true
      };

      const response = await axios.post("http://localhost:8000/api/clientes", nuevoCliente, config);
      console.log("Respuesta del servidor:", response.data);

      navigate('/login', { 
        state: { message: 'Registro exitoso. Por favor, inicia sesión.' }
      });
    } catch (error) {
      console.error("Error completo:", error);
      const errorMessage = error.response?.data?.detail || 
        error.message || 
        "No se pudo conectar con el servidor. Por favor, verifique que:\n" +
        "1. El servidor FastAPI está corriendo\n" +
        "2. El puerto 8000 está abierto\n" +
        "3. La URL es correcta";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const irALogin = () => {
    navigate("/login");
  };

  const irAHome = () => {
    navigate("/");
  };

  return (
    <div className="fondo">
      <div className="navbar">
        <div className="navbar-logo" onClick={irAHome}>
          Estheticease
        </div>
        <ul className="navbar-links">
          <li onClick={irAHome}>Inicio</li>
          <li onClick={irALogin}>Iniciar Sesión</li>
        </ul>
      </div>

      <div className="containerForm">
        <h2>Regístrate</h2>
        {error && <div className="error-message">{error}</div>}
        {loading && <div className="loading-message">Registrando...</div>}

        <form onSubmit={cargarCliente}>
          <fieldset>
            <label htmlFor="Nombre">Nombre</label>
            <input type="text" id="Nombre" name="Nombre" required />
          </fieldset>

          <fieldset>
            <label htmlFor="Contacto">Teléfono</label>
            <input type="text" id="Contacto" name="Contacto" required />
          </fieldset>

          <fieldset>
            <label htmlFor="Correo">Correo</label>
            <input type="email" id="Correo" name="Correo" required />
          </fieldset>

          <fieldset>
            <label htmlFor="Contraseña">Contraseña</label>
            <input type="password" id="Contraseña" name="Contraseña" required />
          </fieldset>

          <fieldset>
            <label htmlFor="Genero">Género</label>
            <input type="text" id="Genero" name="Genero" />
          </fieldset>

          <fieldset>
            <label htmlFor="Edad">Edad</label>
            <input type="number" id="Edad" name="Edad" />
          </fieldset>

          <button type="submit" disabled={loading}>
            {loading ? 'Registrando...' : 'Registrarse'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default FormCargo;
