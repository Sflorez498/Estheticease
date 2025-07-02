import React, { useState, useEffect } from 'react';
import { Calendar, Views } from 'react-big-calendar';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import axios from 'axios';
import { format, parse, addDays, endOfDay } from 'date-fns';
import es from 'date-fns/locale/es';
import '../styles/Calendario.scss';

// Configurar el localizador de date-fns
const localizer = {
  formats: {
    dateFormat: 'dd/MM/yyyy',
    dayFormat: 'dd',
    weekdayFormat: 'EEEE',
    monthFormat: 'MMMM',
    monthHeaderFormat: 'MMMM yyyy',
    dayHeaderFormat: 'dd',
    dayOfMonthFormat: 'dd',
    timeGutterFormat: 'HH:mm'
  },
  format: (date, formatString, culture, localizer) => {
    return format(date, formatString, { locale: es });
  },
  parse: (dateString, formatString, culture, localizer) => {
    return parse(dateString, formatString, new Date(), { locale: es });
  },
  startOfWeek: () => 0, // Domingo como primer día de la semana
  getDay: date => date.getDay(),
  firstVisibleDay: ({ date }) => date,
  lastVisibleDay: ({ date }) => date,
  navigate: (date, action) => {
    const addFn = {
      PREVIOUS: 'subDays',
      NEXT: 'addDays',
      TODAY: () => new Date(),
    }[action];
    return addFn ? addFn(date, 1) : date;
  },
  range: (start, end) => Array.from({ length: end - start }, (_, i) => addDays(start, i)),
  endOf: (date, unit) => {
    if (unit === 'day') return endOfDay(date);
    return date;
  },
  add: (date, number) => addDays(date, number),
  neq: (date1, date2) => date1.getTime() !== date2.getTime(),
  eq: (date1, date2) => date1.getTime() === date2.getTime(),
  lt: (date1, date2) => date1.getTime() < date2.getTime(),
  lte: (date1, date2) => date1.getTime() <= date2.getTime(),
  gt: (date1, date2) => date1.getTime() > date2.getTime(),
  gte: (date1, date2) => date1.getTime() >= date2.getTime(),
  inRange: (date, min, max) => date.getTime() >= min.getTime() && date.getTime() <= max.getTime(),
  merge: (date1, date2) => new Date(date1.getFullYear(), date1.getMonth(), date1.getDate(),
    date2.getHours(), date2.getMinutes(), date2.getSeconds(), date2.getMilliseconds()),
};

function Calendario({ userId }) {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [selectedDate, setSelectedDate] = useState('');
  const [servicios, setServicios] = useState([]);
  const [empleados, setEmpleados] = useState([]);
  const [disponibilidad, setDisponibilidad] = useState([]);

  // Obtener servicios al cargar
  useEffect(() => {
    axios.get('http://localhost:8000/api/servicios')
      .then(res => {
        setServicios(res.data);
      })
      .catch(err => {
        console.error('Error al obtener servicios:', err);
      });
  }, []);

  // Obtener empleados al cargar
  useEffect(() => {
    axios.get('http://localhost:8000/api/empleado')
      .then(res => {
        setEmpleados(res.data);
      })
      .catch(err => {
        console.error('Error al obtener empleados:', err);
      });
  }, []);

  // Obtener citas del usuario
  useEffect(() => {
    if (userId) {
      axios.get(`http://localhost:8000/api/citas/cliente/${userId}`)
        .then(res => {
          const citas = res.data.map(cita => ({
            title: `${cita.nombre_servicio} - ${cita.nombre_empleado}`,
            start: new Date(`${cita.fecha}T${cita.hora}:00`),
            end: new Date(new Date(`${cita.fecha}T${cita.hora}:00`).getTime() + 30 * 60000),
            allDay: false,
            id: cita.id_cita,
            estado: cita.estado,
            empleado: cita.nombre_empleado,
            servicio: cita.nombre_servicio,
            color: cita.estado === 'Pendiente' ? '#4CAF50' : 
                   cita.estado === 'Confirmada' ? '#2196F3' : 
                   cita.estado === 'Cancelada' ? '#F44336' : 
                   '#8BC34A'
          }));
          setEvents(citas);
          setLoading(false);
        })
        .catch(err => {
          setError('Error al cargar las citas');
          setLoading(false);
          console.error('Error detallado:', err);
        });
    }
  }, [userId]);

  // Manejar selección de slot
  const handleSelectSlot = (slotInfo) => {
    const date = format(slotInfo.start, 'yyyy-MM-dd');
    
    // Verificar si la fecha es válida
    if (new Date(date) < new Date()) {
      alert('No se pueden programar citas en fechas pasadas');
      return;
    }

    // Obtener disponibilidad
    axios.get(`http://localhost:8000/api/citas/disponibilidad?fecha=${date}`)
      .then(res => {
        setDisponibilidad(res.data);
        setSelectedDate(date);
        setShowModal(true);
      })
      .catch(err => {
        setError('Error al obtener disponibilidad');
        console.error('Error detallado:', err);
      });
  };

  // Manejar envío de cita
  const handleSubmitCita = (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const citaData = {
      id_cliente: userId,
      id_servicio: formData.get('servicio'),
      id_empleado: formData.get('empleado'),
      fecha: `${selectedDate}T${formData.get('hora')}:00`,
      estado: 'Pendiente',
      notas: formData.get('notas')
    };

    axios.post('http://localhost:8000/api/citas', citaData)
      .then(res => {
        setShowModal(false);
        // Actualizar citas en el calendario
        axios.get(`http://localhost:8000/api/citas/cliente/${userId}`)
          .then(res => {
            const citas = res.data.map(cita => ({
              title: `${cita.nombre_servicio} - ${cita.nombre_empleado}`,
              start: new Date(`${cita.fecha}T${cita.hora}:00`),
              end: new Date(new Date(`${cita.fecha}T${cita.hora}:00`).getTime() + 30 * 60000),
              allDay: false,
              id: cita.id_cita,
              estado: cita.estado,
              empleado: cita.nombre_empleado,
              servicio: cita.nombre_servicio,
              color: cita.estado === 'Pendiente' ? '#4CAF50' : 
                     cita.estado === 'Confirmada' ? '#2196F3' : 
                     cita.estado === 'Cancelada' ? '#F44336' : 
                     '#8BC34A'
            }));
            setEvents(citas);
          });
        alert('Cita reservada exitosamente');
      })
      .catch(err => {
        setError('Error al reservar la cita');
        console.error('Error detallado:', err);
      });
  };

  // Manejar cierre del modal
  const handleCloseModal = () => {
    setShowModal(false);
    setDisponibilidad([]);
    setSelectedDate('');
  };

  // Mostrar mensaje si no hay userId
  if (!userId) {
    return (
      <div className="calendar-container">
        <div className="error">Por favor, inicia sesión para ver tu calendario</div>
      </div>
    );
  }

  return (
    <div className="calendar-container">
      {loading && <div className="loading">Cargando...</div>}
      {error && <div className="error">{error}</div>}
      
      <Calendar
        localizer={localizer}
        events={events}
        startAccessor="start"
        endAccessor="end"
        views={['month', 'week', 'day']}
        onSelectSlot={handleSelectSlot}
        selectable
        culture="es"
        defaultView={Views.MONTH}
        defaultDate={new Date()}
        style={{ height: 600 }}
        components={{
          event: ({ event }) => (
            <div style={{ backgroundColor: event.color }} className="event">
              {event.title}
            </div>
          )
        }}
      />

      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <h2>Reservar Cita</h2>
            <form onSubmit={handleSubmitCita}>
              <div className="form-group">
                <label>Fecha:</label>
                <input type="text" value={selectedDate} disabled />
              </div>

              <div className="form-group">
                <label>Servicio:</label>
                <select name="servicio" required>
                  <option value="">Selecciona un servicio</option>
                  {servicios.map(servicio => (
                    <option key={servicio.id_servicio} value={servicio.id_servicio}>
                      {servicio.nombre} - {servicio.duracion} min - ${servicio.precio}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Profesional:</label>
                <select name="empleado" required>
                  <option value="">Selecciona un profesional</option>
                  {empleados.map(empleado => (
                    <option key={empleado.id_empleado} value={empleado.id_empleado}>
                      {empleado.nombre} - {empleado.especialidad}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Hora:</label>
                <select name="hora" required>
                  <option value="">Selecciona una hora</option>
                  {disponibilidad.map(hora => (
                    <option key={hora.hora} value={hora.hora}>
                      {hora.hora}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Notas:</label>
                <textarea name="notas" placeholder="Notas opcionales..." rows="3"></textarea>
              </div>

              <div className="form-buttons">
                <button type="submit" className="btn-reservar">Reservar Cita</button>
                <button type="button" onClick={handleCloseModal} className="btn-cancelar">
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Calendario;
