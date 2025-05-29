// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "./components/Home";
import FormCargo from "./components/FormCargo";
import Login from "./components/Login";
import Catalogo from "./components/Catalogo";
import Calendario from "./components/Calendario"; // <-- Importa tu componente Calendario

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/registro" element={<FormCargo />} />
        <Route path="/login" element={<Login />} />
        <Route path="/catalogo" element={<Catalogo />} />
        <Route path="/calendario" element={<Calendario />} /> {/* Añade la ruta */}
      </Routes>
    </Router>
  );
}

export default App;
