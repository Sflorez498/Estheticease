// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import Login from "./components/Login";
import FormCargo from "./components/FormCargo";
import Catalogo from "./components/Catalogo";
import Calendario from "./components/Calendario";
import Dashboard from "./components/Dashboard";
import Protegida from "./components/Protegida";
import "./styles/estheticease.scss";
import "./styles/calendario.scss";
import "./styles/dashboard.scss";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/registro" element={<FormCargo />} />
        <Route
          path="/dashboard"
          element={
            <Protegida>
              <Dashboard />
            </Protegida>
          }
        />
        <Route
          path="/catalogo"
          element={
            <Protegida>
              <Catalogo />
            </Protegida>
          }
        />
        <Route
          path="/calendario"
          element={
            <Protegida>
              <Calendario />
            </Protegida>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
