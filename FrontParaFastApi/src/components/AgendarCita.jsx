import React, { useState, useEffect } from 'react';
import axios from '../api/axioInstance';
import '../styles/AgendarCita.scss';

const AgendarCita = () => {
    const [servicios, setServicios] = useState([]);
    const [empleados, setEmpleados] = useState([]);
    const [fechaSeleccionada, setFechaSeleccionada] = useState(new Date().toISOString().split('T')[0]);
    const [horaSeleccionada, setHoraSeleccionada] = useState('');
    const [disponibilidad, setDisponibilidad] = useState([]);
    const [cita, setCita] = useState({
        id_cliente: localStorage.getItem('id_usuario'),
        id_empleado: '',
        id_servicio: '',
        fecha: '',
        hora: '',
        notas: ''
    });

    useEffect(() => {
        cargarServicios();
        cargarEmpleados();
    }, []);

    const cargarServicios = async () => {
        try {
            const response = await axios.get('/cita/servicios');
            const servicios = response.data.map(servicio => ({
                id_servicio: servicio[0],
                nombre: servicio[1],
                duracion: servicio[2],
                precio: servicio[3],
                estado: servicio[4]
            }));
            setServicios(servicios);
        } catch (error) {
            console.error('Error al cargar servicios:', error);
            alert('Error al cargar los servicios. Por favor, inténtalo de nuevo.');
        }
    };

    const cargarEmpleados = async () => {
        try {
            const response = await axios.get('/cita/empleados');
            const empleados = response.data.map(empleado => ({
                id_empleado: empleado[0],
                nombre: empleado[1],
                correo: empleado[2],
                id_rol: empleado[3]
            }));
            setEmpleados(empleados);
        } catch (error) {
            console.error('Error al cargar empleados:', error);
            alert('Error al cargar los empleados. Por favor, inténtalo de nuevo.');
        }
    };

    const cargarDisponibilidad = async (fecha) => {
        try {
            const response = await axios.get(`/cita/disponibilidad?fecha=${fecha}`);
            setDisponibilidad(response.data);
        } catch (error) {
            console.error('Error al cargar disponibilidad:', error);
        }
    };

    const manejarCambio = (e) => {
        const { name, value } = e.target;
        setCita(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const manejarFecha = (e) => {
        const fecha = e.target.value;
        setFechaSeleccionada(fecha);
        cargarDisponibilidad(fecha);
    };

    const manejarHora = (e) => {
        setHoraSeleccionada(e.target.value);
    };

    const crearCita = async (e) => {
        e.preventDefault();
        try {
            // Formatear los datos antes de enviar
            const citaFormateada = {
                id_cliente: localStorage.getItem('id_usuario'),
                id_empleado: cita.id_empleado,
                id_servicio: cita.id_servicio,
                fecha: cita.fecha,
                hora: cita.hora,
                estado: 'Pendiente',
                notas: cita.notas
            };
            
            const response = await axios.post('/cita', citaFormateada);
            alert('Cita agendada exitosamente!');
            // Limpiar formulario
            setCita({
                id_cliente: localStorage.getItem('id_usuario'),
                id_empleado: '',
                id_servicio: '',
                fecha: '',
                hora: '',
                notas: ''
            });
            // Recargar la página para mostrar la nueva cita
            window.location.reload();
        } catch (error) {
            console.error('Error al crear cita:', error);
            alert('Error al agendar cita. Por favor, inténtalo de nuevo.');
        }
    };

    return (
        <div className="agendar-cita">
            <h2>Agendar Cita</h2>
            <form onSubmit={crearCita}>
                <div className="form-group">
                    <label>Servicio</label>
                    <select name="id_servicio" value={cita.id_servicio} onChange={manejarCambio} required>
                        <option value="">Selecciona un servicio</option>
                        {servicios.map(servicio => (
                            <option key={servicio.id_servicio} value={servicio.id_servicio}>
                                {servicio.nombre}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="form-group">
                    <label>Empleado</label>
                    <select name="id_empleado" value={cita.id_empleado} onChange={manejarCambio} required>
                        <option value="">Selecciona un empleado</option>
                        {empleados.map(empleado => (
                            <option key={empleado.id_empleado} value={empleado.id_empleado}>
                                {empleado.nombre}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="form-group">
                    <label>Fecha</label>
                    <input
                        type="date"
                        value={fechaSeleccionada}
                        onChange={manejarFecha}
                        required
                        min={new Date().toISOString().split('T')[0]}
                    />
                </div>

                <div className="form-group">
                    <label>Hora</label>
                    <select name="hora" value={horaSeleccionada} onChange={manejarHora} required>
                        <option value="">Selecciona una hora</option>
                        {disponibilidad.map(hora => (
                            <option key={hora} value={hora}>
                                {hora}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="form-group">
                    <label>Notas</label>
                    <textarea
                        name="notas"
                        value={cita.notas}
                        onChange={manejarCambio}
                        placeholder="Notas adicionales..."
                    />
                </div>

                <button type="submit" className="btn-primary">Agendar Cita</button>
            </form>
        </div>
    );
};

export default AgendarCita;
