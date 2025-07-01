// Componente para editar el perfil de usuario
// Permite actualizar los datos personales del usuario
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/editProfile.scss';

const EditProfile = () => {
  const navigate = useNavigate();
  // Estados para manejar el formulario y el estado de carga
  const [formData, setFormData] = useState(null);  // Datos del formulario
  const [loading, setLoading] = useState(true);    // Estado de carga
  const [error, setError] = useState('');         // Manejo de errores

  // Efecto que se ejecuta al montar el componente
  useEffect(() => {
    // Verificar si hay un usuario logueado
    const userId = localStorage.getItem('userId');
    if (!userId) {
      navigate('/login');
      return;
    }

    // Obtener datos del usuario actual desde la API
    fetch(`http://localhost:8000/api/clientes/${userId}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('No se pudo obtener los datos del usuario');
        }
        return response.json();
      })
      .then(data => {
        // Inicializar el formulario con los datos del usuario
        setFormData({
          nombre: data.Nombre,
          contacto: data.Contacto,
          correo: data.Correo,
          contraseña: '', // No mostramos la contraseña actual
          genero: data.Genero,
          edad: data.Edad
        });
        setLoading(false);
      })
      .catch(error => {
        setError('Error al cargar los datos del perfil');
        setLoading(false);
        console.error('Error:', error);
      });
  }, [navigate]);

  // Maneja los cambios en los campos del formulario
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Maneja el envío del formulario
  const handleSubmit = async (e) => {
    e.preventDefault();
    const userId = localStorage.getItem('userId');
    
    try {
      // Enviar datos actualizados al backend
      const response = await fetch(`http://localhost:8000/api/clientes/${userId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        alert('Perfil actualizado exitosamente');
        navigate('/dashboard');
      } else {
        throw new Error('Error al actualizar el perfil');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error al actualizar el perfil. Por favor, inténtalo de nuevo.');
    }
  };

  // Manejo de estados de carga y errores
  if (loading) {
    return <div className="edit-profile-container">Cargando...</div>;
  }

  if (error) {
    return <div className="edit-profile-container">{error}</div>;
  }

  if (!formData) {
    return <div className="edit-profile-container">No se pudieron cargar los datos</div>;
  }

  return (
    <div className="edit-profile-container">
      <h1>Editar Perfil</h1>
      <form onSubmit={handleSubmit} className="edit-profile-form">
        {/* Campo para el nombre */}
        <div className="form-group">
          <label htmlFor="nombre">Nombre:</label>
          <input
            type="text"
            id="nombre"
            name="nombre"
            value={formData.nombre}
            onChange={handleChange}
            required
          />
        </div>
        {/* Campo para el contacto */}
        <div className="form-group">
          <label htmlFor="contacto">Contacto:</label>
          <input
            type="text"
            id="contacto"
            name="contacto"
            value={formData.contacto}
            onChange={handleChange}
            required
          />
        </div>
        {/* Campo para el correo */}
        <div className="form-group">
          <label htmlFor="correo">Correo:</label>
          <input
            type="email"
            id="correo"
            name="correo"
            value={formData.correo}
            onChange={handleChange}
            required
          />
        </div>
        {/* Campo para la contraseña */}
        <div className="form-group">
          <label htmlFor="contraseña">Contraseña:</label>
          <input
            type="password"
            id="contraseña"
            name="contraseña"
            value={formData.contraseña}
            onChange={handleChange}
            required
          />
        </div>
        {/* Campo para el género */}
        <div className="form-group">
          <label htmlFor="genero">Género:</label>
          <select
            id="genero"
            name="genero"
            value={formData.genero}
            onChange={handleChange}
            required
          >
            <option value="">Selecciona tu género</option>
            <option value="Masculino">Masculino</option>
            <option value="Femenino">Femenino</option>
            <option value="Otro">Otro</option>
          </select>
        </div>
        {/* Campo para la edad */}
        <div className="form-group">
          <label htmlFor="edad">Edad:</label>
          <input
            type="number"
            id="edad"
            name="edad"
            value={formData.edad}
            onChange={handleChange}
            required
          />
        </div>
        {/* Botón para enviar el formulario */}
        <button type="submit">Guardar Cambios</button>
      </form>
    </div>
  );
};

export default EditProfile;
