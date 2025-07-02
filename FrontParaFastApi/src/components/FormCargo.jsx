// Importa React y las herramientas necesarias
import React from 'react';
import axios from 'axios'; // Para hacer solicitudes HTTP
import { useNavigate } from 'react-router-dom'; // Para navegación entre rutas
import '../styles/estheticease.scss'; // Estilos personalizados

const FormCargo = () => {
  const navigate = useNavigate(); // Hook para redirigir a otras páginas

  // Función que se ejecuta al enviar el formulario
  const cargarCliente = async (e) => {
    e.preventDefault(); // Previene el comportamiento por defecto del formulario
    const form = e.target; // Referencia al formulario

    // Objeto con los datos ingresados por el usuario
    const nuevoCliente = {
      nombre: form.Nombre.value,
      contacto: form.Contacto.value,
      correo: form.Correo.value,
      contraseña: form.Contraseña.value,
      genero: form.Genero.value,
      edad: parseInt(form.Edad.value), // Convierte edad a número
    };

    try {
      // Envia los datos al backend con POST
      const response = await axios.post("http://localhost:8000/api/clientes", nuevoCliente);
      console.log("Respuesta del servidor:", response.data);
      alert("Cliente registrado correctamente");
      form.reset(); // Limpia el formulario
    } catch (error) {
      // Muestra un mensaje de error si la solicitud falla
      console.error("Error completo:", error);
      const errorMessage = error.response?.data?.detail || "Error al registrar cliente";
      alert(errorMessage);
    }
  };

  // Redirige al login
  const irALogin = () => {
    navigate("/login");
  };

  // Redirige al home
  const irAHome = () => {
    navigate("/");
  };

  return (
    <div className="fondo">
      {/* Barra de navegación superior */}
      <div className="navbar">
        <div className="navbar-logo" onClick={irAHome}>
          Estheticease
        </div>
        <ul className="navbar-links">
          <li onClick={irAHome}>Inicio</li>
          <li onClick={irALogin}>Iniciar Sesión</li>
        </ul>
      </div>

      {/* Contenedor del formulario */}
      <div className="containerForm">
        <h2>Regístrate</h2>
        <form onSubmit={cargarCliente}>
          {/* Campo: Nombre */}
          <fieldset>
            <label htmlFor="Nombre">Nombre</label>
            <input type="text" id="Nombre" name="Nombre" required />
          </fieldset>

          {/* Campo: Teléfono */}
          <fieldset>
            <label htmlFor="Contacto">Teléfono</label>
            <input type="text" id="Contacto" name="Contacto" required />
          </fieldset>

          {/* Campo: Correo */}
          <fieldset>
            <label htmlFor="Correo">Correo</label>
            <input type="email" id="Correo" name="Correo" required />
          </fieldset>

          {/* Campo: Contraseña */}
          <fieldset>
            <label htmlFor="Contraseña">Contraseña</label>
            <input type="password" id="Contraseña" name="Contraseña" required />
          </fieldset>

          {/* Campo: Género */}
          <fieldset>
            <label htmlFor="Genero">Género</label>
            <input type="text" id="Genero" name="Genero" />
          </fieldset>

          {/* Campo: Edad */}
          <fieldset>
            <label htmlFor="Edad">Edad</label>
            <input type="number" id="Edad" name="Edad" />
          </fieldset>

          {/* Botón de envío */}
          <button type="submit">Registrarse</button>
        </form>
      </div>
    </div>
  );
};

export default FormCargo;
