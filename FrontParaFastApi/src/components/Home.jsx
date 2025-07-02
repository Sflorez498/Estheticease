import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/home.scss";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="home">

      {/* Navbar (igual que antes) */}
      <div className="navbar">
        <div className="navbar-logo" onClick={() => navigate("/")}>
          Estheticease
        </div>
        <ul className="navbar-links">
          <li onClick={() => navigate("/registro")}>Registrarse</li>
          <li onClick={() => navigate("/login")}>Login</li>
        </ul>
      </div>
{/* Hero */}
<section
  className="hero"
  style={{
    position: "relative",
    backgroundImage: "url('https://i.pinimg.com/736x/4f/ac/6a/4fac6a5b2f1d11667644f8d99b498d6a.jpg')",
    backgroundSize: "cover",
    backgroundPosition: "center",
    height: "70vh",
    color: "#fff",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    textAlign: "center",
    padding: "0 20px",
    zIndex: 1,
    overflow: "hidden"
  }}
>
  {/* Overlay semitransparente */}
  <div
    style={{
      position: "absolute",
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: "rgba(0, 0, 0, 0.4)", // Cambia a rgba(255, 255, 255, 0.4) si prefieres blanquear
      zIndex: 0
    }}
  />

  {/* Contenido encima del overlay */}
  <div style={{ zIndex: 1 }}>
    <h1 style={{ fontSize: "4rem", marginBottom: "1.5rem" }}>
      Relájate y Renueva Tu Belleza
    </h1>
    <p
      style={{
        fontSize: "1.5rem",
        maxWidth: "800px",
        marginBottom: "2.5rem"
      }}
    >
      Descubre nuestros tratamientos personalizados para cuidar tu cuerpo y mente.
    </p>
  </div>
</section>


      {/* Servicios */}
      <section className="servicios" style={{ padding: "40px 20px", backgroundColor: "#f9f9f9" }}>
        <h2 style={{ textAlign: "center", marginBottom: "4rem" }}>Nuestros Servicios</h2>
        <div className="cards" style={{
          display: "flex",
          justifyContent: "center",
          gap: "60px",
          flexWrap: "wrap"
        }}>
          {/* Card 1 */}
          <div className="card" style={{
            backgroundColor: "#fff",
            borderRadius: "20px",
            boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
            maxWidth: "300px",
            padding: "50px",
            textAlign: "center"
          }}>
            <img
              src="https://dulcefiguraspa.com/wp-content/uploads/2024/01/img-5-tipos-de-masajes-relajante-1.webp"
              alt="Masaje relajante"
              style={{ borderRadius: "20px", width: "110%", height: "190px", objectFit: "cover" }}
            />
            <h3 style={{ marginTop: "30px" }}>Masajes Relajantes</h3>
            <p>Alivia el estrés y mejora tu bienestar.</p>
          </div>

          {/* Card 2 */}
          <div className="card" style={{
            backgroundColor: "#fff",
            borderRadius: "20px",
            boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
            maxWidth: "300px",
            padding: "50px",
            textAlign: "center"
          }}>
            <img
              src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQB-QFGPa82ZddLOwn7fsL0PaTyICe8_HfjCQ&s"
              alt="Faciales"
              style={{ borderRadius: "20px", width: "110%", height: "190px", objectFit: "cover" }}
            />
            <h3 style={{ marginTop: "30px" }}>Faciales</h3>
            <p>Restaura la frescura y vitalidad de tu rostro.</p>
          </div>

          {/* Card 3 */}
          <div className="card" style={{
            backgroundColor: "#fff",
            borderRadius: "20px",
            boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
            maxWidth: "300px",
            padding: "50px",
            textAlign: "center"
          }}>
            <img
              src="https://aromaticosdeoccidente.com/wp-content/uploads/2021/09/Cuidado-corporal.jpg"
              alt="Cuidado corporal"
              style={{ borderRadius: "20px", width: "110%", height: "190px", objectFit: "cover" }}
            />
            <h3 style={{ marginTop: "30px" }}>Cuidado Corporal</h3>
            <p>Tratamientos integrales para una piel radiante.</p>
          </div>
        </div>
      </section>

      {/* Sobre Nosotros */}
      <section className="sobre-nosotros" style={{ padding: "40px 20px", maxWidth: "900px", margin: "auto", textAlign: "center" }}>
        <h2>Sobre Nosotros</h2>
        <p style={{ fontSize: "1.1rem", lineHeight: "1.6", marginTop: "15px" }}>
          En Estheticease nos dedicamos a ofrecer experiencias únicas de relajación y cuidado personal, combinando tecnología y técnicas tradicionales para tu bienestar integral.
        </p>
      </section>

      {/* Testimonios */}
      <section className="testimonios" style={{ backgroundColor: "#f9f9f9", padding: "40px 20px" }}>
        <h2 style={{ textAlign: "center", marginBottom: "2rem" }}>Lo que dicen nuestros clientes</h2>
        <div style={{ maxWidth: "800px", margin: "auto", display: "flex", gap: "20px", flexWrap: "wrap", justifyContent: "center" }}>
          <div style={{
            backgroundColor: "#fff",
            padding: "20px",
            borderRadius: "10px",
            boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
            maxWidth: "350px"
          }}>
            <p>"Excelente servicio, el masaje me dejó renovada y con mucha energía."</p>
            <p style={{ fontWeight: "bold", marginTop: "10px" }}>— María G.</p>
          </div>
          <div style={{
            backgroundColor: "#fff",
            padding: "20px",
            borderRadius: "10px",
            boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
            maxWidth: "350px"
          }}>
            <p>"Muy profesionales y ambiente muy relajante. Volveré pronto."</p>
            <p style={{ fontWeight: "bold", marginTop: "10px" }}>— Juan P.</p>
          </div>
        </div>
      </section>

      <section
  style={{
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "40px 20px",
    backgroundColor: "#fff",
    textAlign: "left"
  }}
>
  {/* Imagen a la izquierda */}
  <div style={{ flex: 1 }}>
    <img
      src="https://bethelspa.com/inicio/wp-content/uploads/2023/11/WEB_IMAGENES_amigas-02.jpg" // Reemplaza con tu imagen real
      alt="Promoción spa"
      style={{ width: "100%", borderRadius: "10px" }}
    />
  </div>

  {/* Formulario a la derecha */}
  <div style={{ flex: 2, paddingLeft: "200px" }}>
    <h2>Suscríbete a nuestro boletín</h2>
    <p>Recibe promociones exclusivas y consejos de belleza directamente en tu correo.</p>

    <form style={{ marginTop: "60px", display: "flex", alignItems: "center" }}>
      <input
        type="email"
        placeholder="Tu correo electrónico"
        style={{
          padding: "10px",
          borderRadius: "5px",
          border: "1px solid #ccc",
          width: "300px",
          marginRight: "10px"
        }}
      />
      <button
        style={{
          padding: "10px 20px", /*boton de suscribirse*/
          backgroundColor: "#ff7e5f",
          color: "#fff",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer"
        }}
      >
        Suscribirme
      </button>
    </form>
  </div>
</section>
    


      {/* Footer con links */}
      <footer className="home-footer" style={{ textAlign: "center", padding: "20px", backgroundColor: "#333", color: "#fff" }}>
        <p>&copy; 2025 Estheticease - Todos los derechos reservados</p>
        <ul className="footer-links" style={{ listStyle: "none", padding: 0, marginTop: "1rem", display: "flex", gap: "1.5rem", justifyContent: "center" }}>
          <li style={{ cursor: "pointer" }} onClick={() => navigate("/contacto")}>Contacto</li>
          <li style={{ cursor: "pointer" }} onClick={() => navigate("/nosotros")}>Nosotros</li>
          <li style={{ cursor: "pointer" }} onClick={() => navigate("/ayuda")}>Ayuda</li>
          <li style={{ cursor: "pointer" }} onClick={() => navigate("/terminos")}>Términos y Condiciones</li>
        </ul>
      </footer>

    </div>

  
  );
};



export default Home;
