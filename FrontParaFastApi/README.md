# Estheticease 🧖‍♀️💅

**Estheticease** es una aplicación web moderna para centros de cosmetología tipo spa. Permite a los clientes navegar por el portafolio de servicios y productos, agendar citas con profesionales y consultar horarios disponibles. Está diseñada para ofrecer una experiencia digital moderna, optimizando procesos y mejorando la atención al cliente.

---

## 🚀 Funcionalidades Principales

- 🧴 Catálogo de servicios y productos
- 📅 Sistema de agendamiento en línea
- 👩‍⚕️ Gestión de profesionales y horarios
- 💰 Sistema de pagos integrado
- 📊 Dashboard de administración
- 🔐 Autenticación y control de roles
- 📱 Interfaz responsive

---

## 🛠️ Tecnologías Utilizadas

### Frontend
- **React** - Biblioteca para interfaces dinámicas
- **TailwindCSS** - Framework CSS para diseño estilizado
- **React Router** - Navegación entre páginas
- **Axios** - Manejo de peticiones HTTP
- **React Icons** - Iconos para la interfaz
- **React Modal** - Componentes modales

### Componentes Principales
- **Home.jsx** - Página principal
- **Catalogo.jsx** - Visualización de servicios y productos
- **Calendario.jsx** - Sistema de agendamiento
- **Dashboard.jsx** - Panel de administración
- **Login.jsx** - Sistema de autenticación
- **FormCargo.jsx** - Gestión de roles
- **PagoModal.jsx** - Sistema de pagos
- **Navbar.jsx** - Barra de navegación
- **Protegida.jsx** - Componente de rutas protegidas

---

## 📁 Estructura del Proyecto

```bash
FrontParaFastApi/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── Calendario.jsx
│   │   ├── Catalogo.jsx
│   │   ├── Dashboard.jsx
│   │   ├── FormCargo.jsx
│   │   ├── Home.jsx
│   │   ├── Login.jsx
│   │   ├── LogoutButton.jsx
│   │   ├── Navbar.jsx
│   │   ├── PagoModal.jsx
│   │   └── Protegida.jsx
│   ├── App.jsx
│   ├── index.js
│   └── routes.jsx
├── package.json
├── .gitignore
└── README.md
```

## ⚙️ Instalación y Ejecución

### Requisitos Previos

- Node.js + npm
- Git

### Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd FrontParaFastApi
```

2. Instalar dependencias:
```bash
npm install
```

3. Configurar variables de entorno:
```bash
# Crear archivo .env en la raíz del proyecto
VITE_API_URL=http://localhost:8000
```

4. Iniciar la aplicación:
```bash
npm run dev
```

## 🧪 Estado del Proyecto
- 🚀 Versión 1.0.0
- 📋 Documentación completa disponible en la carpeta docs/
- 🛠️ Sistema de autenticación implementado
- 🎨 Interfaz de usuario responsive
- 🔄 Integración con backend FastAPI

## 📫 Contacto
- Autor: GeralSilva, CristianFlorez
- 📧 Email: geraldine_basto@gmail.com, cristian_sflorez@soy.sena.edu.co
- 🌐 Documentación técnica: [docs/documentacion_tecnica.md](../docs/documentacion_tecnica.md)
- 📚 API Reference: [docs/api.md](../docs/api.md)

