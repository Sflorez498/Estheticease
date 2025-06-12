// Muestra el calendario de citas y permite agendar nuevas
import React, { useState, useEffect } from 'react';
import { Calendar, dateFnsLocalizer } from 'react-big-calendar';
import { format, parse, startOfWeek, getDay } from 'date-fns';
import es from 'date-fns/locale/es';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../styles/calendario.scss';

const locales = { es };
const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek: () => startOfWeek(new Date(), { weekStartsOn: 1 }),
  getDay,
  locales,
});

const Calendario = () => {
  const navigate = useNavigate();
  const [events, setEvents] = useState([]);               // Citas en el calendario
  const [selectedDate, setSelectedDate] = useState(null); // Fecha seleccionada
  const [showModal, setShowModal] = useState(false);      // Estado del modal
  const [servicios, setServicios] = useState([]);         // Servicios disponibles
  const [empleados, setEmpleados] = useState([]);         // Profesionales disponibles
  const [disponibilidad, setDisponibilidad] = useState([]); // Horas disponibles
  const [loading, setLoading] = useState(false);          // Estado de carga
  const [error, setError] = useState('');               // Mensaje de error
  const [status, setStatus] = useState('');               // Estado de la operación

  // Carga inicial: servicios, empleados y citas del cliente
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        setStatus('Cargando datos...');
        
        // Cargar servicios
        try {
          const serviciosRes = await axios.get('http://localhost:8000/api/servicios/'); // Corregir la URL de la API de servicios para eliminar la barra final
          if (serviciosRes.data) {
            setServicios(serviciosRes.data);
            console.log('Servicios cargados:', serviciosRes.data);
          } else {
            console.error('Respuesta vacía de servicios:', serviciosRes);
            throw new Error('Respuesta vacía de servicios');
          }
        } catch (serviciosErr) {
          console.error('Error al cargar servicios:', serviciosErr.response?.data || serviciosErr);
          const serviciosMessage = serviciosErr.response?.data?.detail || 
                                serviciosErr.response?.data?.message || 
                                serviciosErr.message || 
                                'Error al cargar los servicios';
          setError(serviciosMessage || 'Error al cargar los servicios');
          setStatus('Error al cargar servicios');
          throw serviciosErr;
        }

        // Cargar empleados
        try {
          const empleadosRes = await axios.get('http://localhost:8000/api/citas/empleados');
          if (empleadosRes.data) {
            setEmpleados(empleadosRes.data);
            console.log('Empleados cargados:', empleadosRes.data);
          } else {
            console.error('Respuesta vacía de empleados:', empleadosRes);
            throw new Error('Respuesta vacía de empleados');
          }
        } catch (empleadosErr) {
          console.error('Error al cargar empleados:', empleadosErr.response?.data || empleadosErr);
          const empleadosMessage = empleadosErr.response?.data?.detail || 
                                empleadosErr.response?.data?.message || 
                                empleadosErr.message || 
                                'Error al cargar los empleados';
          setError(empleadosMessage || 'Error al cargar los empleados');
          setStatus('Error al cargar empleados');
          throw empleadosErr;
        }

        // Cargar citas del usuario
        try {
          const userId = localStorage.getItem('userId');
          if (userId) {
            const citasRes = await axios.get(`http://localhost:8000/api/citas/cliente/${userId}`);
            if (citasRes.data) {
              const citas = citasRes.data.map(cita => {
                const start = new Date(`${format(new Date(cita.Fecha), 'yyyy-MM-dd')}T${format(new Date(cita.Hora), 'HH:mm')}`);
                const end = new Date(start.getTime() + 30 * 60000);
                return {
                  title: cita.nombre_servicio,
                  start,
                  end,
                  allDay: false,
                  id: cita.Id_Cita
                };
              });
              setEvents(citas);
              console.log('Citas cargadas:', citas);
            } else {
              console.error('Respuesta vacía de citas:', citasRes);
              throw new Error('Respuesta vacía de citas');
            }
          }
        } catch (citasErr) {
          console.error('Error al cargar citas:', citasErr.response?.data || citasErr);
          const citasMessage = citasErr.response?.data?.detail || 
                             citasErr.response?.data?.message || 
                             citasErr.message || 
                             'Error al cargar las citas';
            setError(citasMessage || 'Error al cargar las citas');
          setStatus('Error al cargar citas');
          throw citasErr;
        }

        setStatus('Datos cargados');
      } catch (err) {
        console.error('Error general al cargar datos:', err.response?.data || err);
        const errorMessage = err.response?.data?.detail || 
                           err.response?.data?.message || 
                           err.message || 
                           'Error al cargar los datos. Por favor, intenta nuevamente.';
            setError(errorMessage || 'Error al cargar los datos');
        setStatus('Error al cargar datos');
      }
    };

    loadInitialData();
  }, []);

  // Al seleccionar una fecha del calendario
  const handleSelectSlot = async (slotInfo) => {
    const date = format(slotInfo.start, 'yyyy-MM-dd');
    setSelectedDate(date);
    try {
      setStatus('Cargando disponibilidad...');
      const res = await axios.get(`http://localhost:8000/api/citas/disponibilidad?fecha=${date}`);
      setDisponibilidad(res.data);
      setShowModal(true);
      setStatus('');
    } catch (err) {
      console.error('Error al cargar disponibilidad:', err);
      setError('Error al cargar la disponibilidad. Por favor, intenta nuevamente.');
      setStatus('Error al cargar disponibilidad');
    }
  };

  // Enviar formulario de nueva cita
  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const form = e.target;
    const formData = new FormData(form);

    try {
      const response = await axios.post('http://localhost:8000/api/citas', {
        fecha: selectedDate,
        hora: formData.get('hora'),
        id_servicio: formData.get('servicio'),
        id_empleado: formData.get('empleado'),
        notas: formData.get('notas')
      });

      const nuevoEvento = {
        title: servicios.find(s => s.id_servicio === Number(formData.get('servicio')))?.nombre || 'Nuevo servicio',
        start: new Date(`${selectedDate}T${formData.get('hora')}`),
        end: new Date(new Date(`${selectedDate}T${formData.get('hora')}`).getTime() + 30 * 60000),
        allDay: false,
        id: response.data.id
      };
      setEvents([...events, nuevoEvento]);
      setShowModal(false);
    } catch (err) {
      console.error('Error al reservar cita:', err);
      alert('Error al reservar la cita');
    } finally {
      setLoading(false);
    }
  };

  // Cerrar sesión
  const handleLogout = () => {
    localStorage.removeItem('userId');
    navigate('/');
  };

  return (
    <div className="calendario-container">
      {status && <div className="status-message">{status}</div>}
      {error && <div className="error-message">{error}</div>}
      <div className="header-container">
        <h2>Agenda de Citas</h2>
        {status && <p className="status">{status}</p>}
        {error && <p className="error">{error}</p>}
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

      {/* Modal de reserva */}
      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <h3>Reservar Cita</h3>
            <form onSubmit={handleFormSubmit}>
              <label>Servicio:
                <select name="servicio" required>
                  <option value="">Selecciona</option>
                  {servicios.map(s => (
                    <option key={s.id_servicio} value={s.id_servicio}>{s.nombre}</option>
                  ))}
                </select>
              </label>
              <label>Profesional:
                <select name="empleado" required>
                  <option value="">Selecciona</option>
                  {empleados.map(e => (
                    <option key={e.id_empleado} value={e.id_empleado}>{e.nombre} ({e.especialidad})</option>
                  ))}
                </select>
              </label>
              <label>Hora:
                <select name="hora" required>
                  <option value="">Selecciona</option>
                  {disponibilidad.map(d => {
                    const hora = format(new Date(d.hora), 'HH:mm');
                    return <option key={hora} value={hora}>{hora}</option>;
                  })}
                </select>
              </label>
              <label>Notas:
                <textarea name="notas" placeholder="Notas opcionales..." />
              </label>
              <button type="submit" disabled={loading}>{loading ? 'Reservando...' : 'Reservar'}</button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Calendario;
