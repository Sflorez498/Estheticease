// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import Login from "./components/Login";
import FormCargo from "./components/FormCargo";
import Catalogo from "./components/Catalogo";
import Calendario from "./components/Calendario";
import "./styles/estheticease.scss";
import "./styles/calendario.scss";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<FormCargo />} />
        <Route path="/catalogo" element={<Catalogo />} />
        <Route path="/calendario" element={<Calendario />} />
      </Routes>
    </Router>
  );
}

export default App;
