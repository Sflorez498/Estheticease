import React, { useState, useEffect } from 'react';
import { FaUser, FaCalendar, FaShoppingCart } from 'react-icons/fa';
import '../styles/App.scss';
import Calendario from './Calendario';
import Catalogo from './Catalogo';

const App = () => {
  const [usuario, setUsuario] = useState(null);
  const [seccionActual, setSeccionActual] = useState('inicio');

  useEffect(() => {
    // Verificar si hay un usuario en localStorage
    const usuarioGuardado = localStorage.getItem('usuario');
    if (usuarioGuardado) {
      setUsuario(JSON.parse(usuarioGuardado));
      setSeccionActual('bienvenida');
    }
  }, []);

  const iniciarSesion = (nombre) => {
    const nuevoUsuario = { nombre };
    localStorage.setItem('usuario', JSON.stringify(nuevoUsuario));
    setUsuario(nuevoUsuario);
    setSeccionActual('bienvenida');
  };

  const cerrarSesion = () => {
    localStorage.removeItem('usuario');
    setUsuario(null);
    setSeccionActual('inicio');
  };

  return (
    <div className="app-container">
      {seccionActual === 'inicio' ? (
        <div className="inicio-container">
          <h1>Bienvenido a Estheticease</h1>
          <div className="inicio-form">
            <h2>Iniciar Sesión</h2>
            <input
              type="text"
              placeholder="Nombre de usuario"
              onChange={(e) => setUsuario({ nombre: e.target.value })}
            />
            <button onClick={() => iniciarSesion(usuario?.nombre)}>
              <FaUser /> Iniciar Sesión
            </button>
          </div>
        </div>
      ) : (
        <>
          <div className="bienvenida-container">
            {seccionActual === 'bienvenida' && (
              <div className="bienvenida">
                <h2>Bienvenido, {usuario.nombre}</h2>
                <div className="opciones">
                  <button 
                    onClick={() => setSeccionActual('citas')}
                    className="opcion-btn"
                  >
                    <FaCalendar />
                    Agendar Citas
                  </button>
                  <button 
                    onClick={() => setSeccionActual('compras')}
                    className="opcion-btn"
                  >
                    <FaShoppingCart />
                    Compras
                  </button>
                </div>
              </div>
            )}
          </div>

          {seccionActual === 'citas' && (
            <div className="seccion-container">
              <Calendario />
            </div>
          )}

          {seccionActual === 'compras' && (
            <div className="seccion-container">
              <Catalogo />
            </div>
          )}

          {seccionActual !== 'inicio' && (
            <button 
              className="cerrar-sesion-btn"
              onClick={cerrarSesion}
            >
              <FaUser /> Cerrar Sesión
            </button>
          )}
        </>
      )}
    </div>
  );
};

export default App;
