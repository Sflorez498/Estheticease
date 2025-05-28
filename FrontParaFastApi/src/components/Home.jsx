import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/home.scss";

const Home = () => {
  const navigate = useNavigate();

  const irARegistro = () => {
    navigate("/registro");
  };

  const irALogin = () => {
    navigate("/login");
  };

  return (
    <div className="home">
      <div className="navbar">
        <div className="navbar-logo" onClick={() => navigate("/")}>
          Estheticease
        </div>
        <ul className="navbar-links">
          <li onClick={irARegistro}>Registrarse</li>
          <li onClick={irALogin}>Iniciar Sesión</li>
          <li onClick={() => navigate("/catalogo")}>Catálogo</li>
          <li onClick={() => navigate("/contacto")}>Contacto</li>
          <li onClick={() => navigate("/nosotros")}>Nosotros</li>
          <li onClick={() => navigate("/ayuda")}>Ayuda</li>
          <li onClick={() => navigate("/terminos")}>Términos y Condiciones</li>
          <li onClick={() => navigate("/calendario")}>Calendario</li>



        </ul>
        <div className="navbar-calendar">
  <input
    type="date"
    onChange={(e) => alert(`Fecha seleccionada: ${e.target.value}`)}
  />
</div>

      </div>

      <header className="home-header">
        <h1>Bienvenido a Estheticease</h1>

        <div className="calendario-boton">
  <label htmlFor="fecha">Agendar una cita:</label>
  <input
    type="date"
    id="fecha"
    name="fecha"
    onChange={(e) => alert(`Fecha seleccionada: ${e.target.value}`)}
  />
</div>
        

      </header>

      <section className="servicios">
        <h2>Servicios</h2>
        <div className="cards">
          <div className="card">
            <img
              src="https://dulcefiguraspa.com/wp-content/uploads/2024/01/img-5-tipos-de-masajes-relajante-1.webp"
              alt="Masaje relajante"
            />
            <h3>Masajes Relajantes</h3>
            <p>Alivia el estrés y mejora tu bienestar.</p>
          </div>
          <div className="card">
            <img
              src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQB-QFGPa82ZddLOwn7fsL0PaTyICe8_HfjCQ&s"
              alt="Faciales"
            />  
            <h3>Faciales</h3>
            <p>Restaura la frescura y vitalidad de tu rostro.</p>
          </div>
          <div className="card">
            <img
              src="https://aromaticosdeoccidente.com/wp-content/uploads/2021/09/Cuidado-corporal.jpg" 
              alt="Cuidado corporal" 
            /> 
            <h3>Cuidado Corporal</h3>
            <p>Tratamientos integrales para una piel radiante.</p>
          </div>
        </div>
      </section>

      <footer className="home-footer">
        <p>&copy; 2025 Estheticease - Todos los derechos reservados</p>
      </footer>
    </div>
  );
};

export default Home;