import React, { useState, useEffect } from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import format from 'date-fns/format';
import parse from 'date-fns/parse';
import startOfWeek from 'date-fns/startOfWeek';
import getDay from 'date-fns/getDay';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import es from 'date-fns/locale/es';

const locales = {
  'es': es,
};

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

const Calendario = () => {
  const navigate = useNavigate();
  const [citas, setCitas] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedService, setSelectedService] = useState('');
  const [servicios, setServicios] = useState([]);

  const handleLogout = () => {
    localStorage.removeItem('userId');
    navigate('/');
  };

  useEffect(() => {
    const userId = localStorage.getItem('userId');
    if (!userId) {
      navigate('/login');
      return;
    }

    const fetchCitas = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/citas/cliente/${userId}`);
        console.log('Citas obtenidas:', response.data);
        const citasFormateadas = response.data.map(cita => ({
          title: `Cita: ${cita.servicio_nombre}`,
          start: new Date(cita.Fecha_Cita),
          end: new Date(cita.Fecha_Cita),
          id: cita.Id_Cita,
        }));
        setCitas(citasFormateadas);
      } catch (error) {
        console.error('Error al cargar citas:', error);
      }
    };

    const fetchServicios = async () => {
      try {
        const response = await axios.get('http://localhost:8000/servicios');
        console.log('Servicios obtenidos:', response.data);
        setServicios(response.data);
      } catch (error) {
        console.error('Error al cargar servicios:', error);
      }
    };

    fetchCitas();
    fetchServicios();
  }, [navigate]);

  const handleSelectSlot = (slotInfo) => {
    setSelectedDate(slotInfo.start);
    setShowModal(true);
  };

  const handleSubmitCita = async () => {
    try {
      const userId = localStorage.getItem('userId');
      if (!userId || !selectedService || !selectedDate) {
        alert('Por favor seleccione un servicio y una fecha');
        return;
      }

      const nuevaCita = {
        id_clientes: parseInt(userId),
        id_servicio: parseInt(selectedService),
        fecha_cita: format(selectedDate, 'yyyy-MM-dd'),
        estado: 'Pendiente'
      };

      console.log('Enviando cita:', nuevaCita);
      const response = await axios.post('http://localhost:8000/citas', nuevaCita);
      console.log('Respuesta:', response.data);
      
      alert('Cita agendada exitosamente');
      setShowModal(false);
      
      // Recargar citas
      const citasResponse = await axios.get(`http://localhost:8000/citas/cliente/${userId}`);
      const citasFormateadas = citasResponse.data.map(cita => ({
        title: `Cita: ${cita.servicio_nombre}`,
        start: new Date(cita.Fecha_Cita),
        end: new Date(cita.Fecha_Cita),
        id: cita.Id_Cita,
      }));
      setCitas(citasFormateadas);
    } catch (error) {
      console.error('Error al agendar cita:', error);
      const mensaje = error.response?.data?.detail || 'Error al agendar la cita';
      alert(mensaje);
    }
  };

  return (
    <div className="calendario-container">
      <div className="header-container">
        <h2>Agenda de Citas</h2>
        <button className="btn-cerrar-sesion" onClick={handleLogout}>
          Cerrar Sesión
        </button>
      </div>
      <Calendar
        localizer={localizer}
        events={citas}
        startAccessor="start"
        endAccessor="end"
        style={{ height: 500 }}
        onSelectSlot={handleSelectSlot}
        selectable
        messages={{
          next: "Siguiente",
          previous: "Anterior",
          today: "Hoy",
          month: "Mes",
          week: "Semana",
          day: "Día"
        }}
      />

      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <h3>Agendar Nueva Cita</h3>
            <p>Fecha seleccionada: {format(selectedDate, 'dd/MM/yyyy')}</p>
            <select 
              value={selectedService} 
              onChange={(e) => setSelectedService(e.target.value)}
            >
              <option value="">Seleccione un servicio</option>
              {servicios.map(servicio => (
                <option key={servicio.Id_Servicio} value={servicio.Id_Servicio}>
                  {servicio.Nombre} - ${servicio.Precio}
                </option>
              ))}
            </select>
            <div className="modal-buttons">
              <button onClick={handleSubmitCita}>Confirmar</button>
              <button onClick={() => setShowModal(false)}>Cancelar</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Calendario;
