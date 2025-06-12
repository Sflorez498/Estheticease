import React, { useState, useEffect } from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import { format, parse, startOfWeek, getDay } from 'date-fns';
import es from 'date-fns/locale/es';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/calendario.scss';

// ✅ localizer válido para react-big-calendar
const locales = {
  es: es,
};

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek: () => startOfWeek(new Date(), { weekStartsOn: 1 }),
  getDay,
  locales,
});

const Calendario = () => {
  const navigate = useNavigate();
  const [events, setEvents] = useState([]);
  const [selectedDate, setSelectedDate] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [modalContent, setModalContent] = useState('');
  const [servicios, setServicios] = useState([]);
  const [empleados, setEmpleados] = useState([]);
  const [disponibilidad, setDisponibilidad] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/servicios')
      .then(res => setServicios(res.data))
      .catch(err => console.error('Error al obtener servicios:', err));

    axios.get('http://localhost:8000/api/empleados')
      .then(res => setEmpleados(res.data))
      .catch(err => console.error('Error al obtener empleados:', err));

    const userId = localStorage.getItem('userId');
    if (userId) {
      axios.get(`http://localhost:8000/api/citas/cliente/${userId}`)
        .then(res => {
          const citas = res.data.map(cita => ({
            title: cita.nombre_servicio,
            start: new Date(`${format(new Date(cita.Fecha), 'yyyy-MM-dd')}T${format(new Date(cita.Hora), 'HH:mm')}`),
            end: new Date(new Date(`${format(new Date(cita.Fecha), 'yyyy-MM-dd')}T${format(new Date(cita.Hora), 'HH:mm')}`).getTime() + 30 * 60000),
            allDay: false,
            id: cita.Id_Cita
          }));
          setEvents(citas);
        })
        .catch(err => console.error('Error al obtener citas:', err));
    }
  }, []);

  const handleSelectSlot = (slotInfo) => {
    const date = format(slotInfo.start, 'yyyy-MM-dd');
    axios.get(`http://localhost:8000/api/citas/disponibilidad?fecha=${date}`)
      .then(res => {
        setDisponibilidad(res.data);
        setSelectedDate(date);
        setShowModal(true);

        const modalHTML = `
          <form id="citaForm">
            <label>Servicio:
              <select name="servicio" required>
                <option value="">Selecciona</option>
                ${servicios.map(s => `<option value="${s.id_servicio}">${s.nombre}</option>`).join('')}
              </select>
            </label>
            <label>Profesional:
              <select name="empleado" required>
                <option value="">Selecciona</option>
                ${empleados.map(e => `<option value="${e.id_empleado}">${e.nombre} (${e.especialidad})</option>`).join('')}
              </select>
            </label>
            <label>Hora:
              <select name="hora" required>
                <option value="">Selecciona</option>
                ${res.data.map(d => `<option value="${format(new Date(d.hora), 'HH:mm')}">${format(new Date(d.hora), 'HH:mm')}</option>`).join('')}
              </select>
            </label>
            <label>Notas:
              <textarea name="notas" placeholder="Notas opcionales..."></textarea>
            </label>
            <button type="submit">Reservar</button>
          </form>`;
        setModalContent(modalHTML);
      })
      .catch(err => console.error('Error al obtener disponibilidad:', err));
  };

  const handleModalSubmit = (e) => {
    e.preventDefault();
    const form = e.target;
    const servicio = form.servicio.value;
    const empleado = form.empleado.value;
    const hora = form.hora.value;
    const notas = form.notas.value;

    if (!servicio || !empleado || !hora) {
      alert('Completa todos los campos');
      return;
    }

    axios.post('http://localhost:8000/api/citas', {
      id_cliente: localStorage.getItem('userId'),
      id_empleado: parseInt(empleado),
      id_servicio: parseInt(servicio),
      fecha: format(new Date(selectedDate), 'yyyy-MM-dd'),
      hora: format(new Date(hora), 'HH:mm'),
      notas
    })
    .then(() => {
      setShowModal(false);
      const servicioNombre = servicios.find(s => s.id_servicio === parseInt(servicio))?.nombre || 'Cita';
      setEvents([...events, {
        title: servicioNombre,
        start: new Date(`${format(new Date(selectedDate), 'yyyy-MM-dd')}T${format(new Date(hora), 'HH:mm')}`),
        end: new Date(new Date(`${format(new Date(selectedDate), 'yyyy-MM-dd')}T${format(new Date(hora), 'HH:mm')}`).getTime() + 30 * 60000),
        allDay: false
      }]);
      alert('Cita reservada');
    })
    .catch(err => {
      console.error('Error al reservar:', err);
      alert('Error al reservar la cita');
    });
  };

  const handleLogout = () => {
    localStorage.removeItem('userId');
    navigate('/');
  };

  return (
    <div className="calendario-container">
      <div className="header-container">
        <h2>Agenda de Citas</h2>
        <button className="btn-cerrar-sesion" onClick={handleLogout}>Cerrar Sesión</button>
      </div>

      <Calendar
        localizer={localizer}
        events={events}
        startAccessor="start"
        endAccessor="end"
        selectable
        style={{ height: 500 }}
        onSelectSlot={handleSelectSlot}
        views={['month', 'week', 'day', 'agenda']}
        defaultView="month"
        defaultDate={new Date()}
        messages={{
          next: 'Siguiente',
          previous: 'Anterior',
          today: 'Hoy',
          month: 'Mes',
          week: 'Semana',
          day: 'Día',
          agenda: 'Agenda'
        }}
      />

      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <h3>Nueva Cita</h3>
            <div onSubmit={handleModalSubmit} dangerouslySetInnerHTML={{ __html: modalContent }} />
          </div>
        </div>
      )}
    </div>
  );
};

export default Calendario;
