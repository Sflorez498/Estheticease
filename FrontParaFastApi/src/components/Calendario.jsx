import React, { useState } from "react";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import "../styles/Calendario.scss";

// Imágenes de profesionales
import avatarProfesional1 from "../assets/images/profesional2.avif";
import avatarProfesional2 from "../assets/images/profesional1.webp";
import avatarProfesional3 from "../assets/images/profesional3.avif";

// Imágenes de servicios
import servicioMasaje from "../assets/images/masaje.jpg";
import servicioLimpieza from "../assets/images/limpieza.jpeg";
import servicioCorporal from "../assets/images/corporal.jpg";

// Datos simulados
const profesionales = {
  "2025-05-28": [
    { nombre: "Ana López", imagen: avatarProfesional1 },
    { nombre: "Carlos Ruiz", imagen: avatarProfesional2 },
  ],
  "2025-05-29": [{ nombre: "Lucía Méndez", imagen: avatarProfesional3 }],
};

const servicios = {
  "2025-05-28": [
    { nombre: "Masaje relajante", imagen: servicioMasaje },
    { nombre: "Limpieza facial", imagen: servicioLimpieza },
  ],
  "2025-05-29": [{ nombre: "Tratamiento corporal", imagen: servicioCorporal }],
};

const Calendario = () => {
  const [fechaSeleccionada, setFechaSeleccionada] = useState(null);

  const handleDateChange = (date) => {
    const fecha = date.toISOString().split("T")[0];
    setFechaSeleccionada(fecha);
  };

  const tileClassName = ({ date, view }) => {
    if (view === "month") {
      const fecha = date.toISOString().split("T")[0];
      if (profesionales[fecha] && profesionales[fecha].length > 0) {
        return "available-day";
      }
      return "unavailable-day";
    }
    return null;
  };

  return (
    <div className="calendario-container">
      <h2>Agendar Cita</h2>
      <Calendar onChange={handleDateChange} tileClassName={tileClassName} />
      {fechaSeleccionada && (
        <div className="info-cita">
          <h3>Fecha: {fechaSeleccionada}</h3>

          <h4>Profesionales disponibles:</h4>
          <div className="profesionales-grid">
            {(profesionales[fechaSeleccionada] || []).length > 0 ? (
              profesionales[fechaSeleccionada].map((prof, idx) => (
                <div key={idx} className="profesional-card">
                  <img src={prof.imagen} alt={prof.nombre} className="profesional-img" />
                  <p>{prof.nombre}</p>
                </div>
              ))
            ) : (
              <p>No hay profesionales disponibles.</p>
            )}
          </div>

          <h4>Servicios disponibles:</h4>
          <div className="servicios-grid">
            {(servicios[fechaSeleccionada] || []).length > 0 ? (
              servicios[fechaSeleccionada].map((serv, idx) => (
                <div key={idx} className="servicio-card">
                  <img src={serv.imagen} alt={serv.nombre} className="servicio-img" />
                  <p>{serv.nombre}</p>
                </div>
              ))
            ) : (
              <p>No hay servicios disponibles.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Calendario;
