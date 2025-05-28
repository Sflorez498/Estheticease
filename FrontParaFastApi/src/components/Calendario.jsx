import React, { useState } from "react";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import "../styles/components"; // Asegúrate de tener estilos aquí

const profesionales = {
  "2025-05-28": ["Ana López", "Carlos Ruiz"],
  "2025-05-29": ["Lucía Méndez"],
};


const servicios = {
  "2025-05-28": ["Masaje relajante", "Limpieza facial"],
  "2025-05-29": ["Tratamiento corporal"],
};

const Calendario = () => {
  const [fechaSeleccionada, setFechaSeleccionada] = useState(null);

  const handleDateChange = (date) => {
    setFechaSeleccionada(date.toISOString().split("T")[0]); // Formato YYYY-MM-DD
  };

  return (
    <div className="calendario-container">
      <h2>Agendar Cita</h2>
      <Calendar onChange={handleDateChange} />
      {fechaSeleccionada && (
        <div className="info-cita">
          <h3>Fecha: {fechaSeleccionada}</h3>

          <h4>Profesionales disponibles:</h4>
          <ul>
            {(profesionales[fechaSeleccionada] || ["Ninguno disponible"]).map((prof, idx) => (
              <li key={idx}>{prof}</li>
            ))}
          </ul>

          <h4>Procesos disponibles:</h4>
          <ul>
            {(servicios[fechaSeleccionada] || ["Sin servicios disponibles"]).map((serv, idx) => (
              <li key={idx}>{serv}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Calendario;
