import React from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/estheticease.scss';

const FormCargo = () => {
  const navigate = useNavigate();

  const cargarCliente = async (e) => {
    e.preventDefault();
    const form = e.target;

    const nuevoCliente = {
      nombre: form.Nombre.value,
      contacto: form.Contacto.value,
      correo: form.Correo.value,
      contraseña: form.Contraseña.value,
      genero: form.Genero.value,
      edad: parseInt(form.Edad.value),
    };

    try {
      const response = await axios.post("http://localhost:8000/clientes", nuevoCliente);
      console.log("Respuesta del servidor:", response.data);
      alert("Cliente registrado correctamente");
      form.reset();
    } catch (error) {
      console.error("Error completo:", error);
      const errorMessage = error.response?.data?.detail || "Error al registrar cliente";
      alert(errorMessage);
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
      {/* Barra de navegación */}
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
          <button type="submit">Registrarse</button>
        </form>
      </div>
    </div>
  );
};

export default FormCargo;