import React from 'react';
import axios from 'axios';
import '../styles/estheticease.scss';


const FormCargo = () => {
const cargarCliente = async (e) => {
e.preventDefault();
const form = e.target;



const nuevoCliente = {
  nombre: form.Nombre.value,
  contacto: form.Contacto.value,
  correo: form.Correo.value,
  contraseña: form.Contraseña.value,
  genero: form.Genero.value,
  edad: parseInt(form.Edad.value),
};




try {

await axios.post("http://localhost:8000/clientes/", nuevoCliente); // Ruta corregida
     alert("Cliente registrado correctamente");
     form.reset();
    } 
    catch (error) 
    {
        alert("Error al registrar cliente");
        console.error(error);
    }
};



return (

<div className="fondo">

<div className="containerForm">

<h2>Regístrate</h2>

<form onSubmit={cargarCliente}>

<fieldset>

<label htmlFor="Nombre">Nombre</label>

<input type="text" id="Nombre" name="Nombre" required />

</fieldset>

<fieldset>

<label htmlFor="Contacto">Teléfono</label>

<input type="text" id="Contacto" name="Contacto" required />

</fieldset>

<fieldset>

<label htmlFor="Correo">Correo</label>

<input type="email" id="Correo" name="Correo" required />

</fieldset>

<fieldset>

<label htmlFor="Contraseña">Contraseña</label>

<input type="Clave" id="Contraseña" name="Contraseña" required />

</fieldset>

<fieldset>

<label htmlFor="Genero">Género</label>

<input type="text" id="Genero" name="Genero" />

</fieldset>

<fieldset>

<label htmlFor="Edad">Edad</label>

<input type="number" id="Edad" name="Edad" />

</fieldset>

<button type="submit">Registrarse</button>

</form>

</div>

</div>

);

};



export default FormCargo;