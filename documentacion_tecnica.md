# Documentación Técnica Estheticease

---

## 1. Introducción

### 1.1 Contexto del Proyecto
Estheticease es una aplicación web que busca digitalizar y optimizar la gestión de citas y servicios en centros de cosmetología. El proyecto surge como respuesta a la necesidad de modernizar los procesos administrativos y de atención al cliente en este sector.

### 1.2 Objetivo General
Desarrollar una plataforma web que permita a los centros de cosmetología gestionar eficientemente sus citas, servicios y productos, mejorando la experiencia tanto para clientes como para profesionales.

---

## 2. Formulación del Proyecto

### 2.1 Análisis del Problema
- Gestión manual de citas
- Falta de sistema de agendamiento en línea
- Dificultad en la gestión de horarios
- Proceso de registro de clientes ineficiente
- Falta de seguimiento de tratamientos
- Limitaciones en la comunicación cliente-profesional

### 2.2 Solución Propuesta
Desarrollar una aplicación web que:
- Permita la gestión en línea de citas
- Proporcione un catálogo interactivo de servicios
- Facilite la comunicación entre clientes y profesionales
- Ofrezca un sistema de seguimiento de tratamientos
- Proporcione análisis y reportes en tiempo real

---

## 3. Metas de Negocio

### 3.1 Requisitos Funcionales

#### 3.1.1 Gestión de Citas
- Agendamiento en línea de citas
- Gestión de horarios de profesionales
- Sistema de recordatorios
- Historial de citas
- Cancelación y reprogramación

#### 3.1.2 Catálogo de Servicios
- Visualización de servicios disponibles
- Filtros y búsqueda avanzada
- Descripciones detalladas
- Precios y promociones
- Galería de imágenes

#### 3.1.3 Gestión de Clientes
- Registro y perfil de clientes
- Historial de tratamientos
- Preferencias y alergias
- Sistema de puntos/lealtad
- Comunicación directa

#### 3.1.4 Sistema de Profesionales
- Perfiles de profesionales
- Especialidades y horarios
- Evaluaciones y calificaciones
- Gestión de disponibilidad
- Reportes de rendimiento

### 3.2 Reglas de Negocio

1. **Citología**
   - Un cliente no puede agendar más de 3 citas por día
   - Las citas deben ser agendadas con mínimo 24 horas de antelación
   - Los recordatorios se envían 24 horas antes de la cita
   - Las cancelaciones deben realizarse con mínimo 12 horas de antelación

2. **Gestión de Servicios**
   - Un servicio debe tener al menos una imagen representativa
   - Los servicios deben estar categorizados
   - Los precios deben ser actualizados mensualmente
   - Los servicios inactivos deben ser archivados, no eliminados

3. **Gestión de Clientes**
   - Los datos personales deben ser validados
   - Los clientes pueden modificar su perfil
   - Los historiales de tratamiento son permanentes
   - Las preferencias son personalizables

4. **Gestión de Profesionales**
   - Los profesionales deben tener al menos una especialidad
   - Los horarios deben ser definidos por día
   - Las evaluaciones son anónimas
   - El sistema de puntos se actualiza mensualmente

---

## 4. Diseño del Proyecto

### 4.1 Casos de Uso

#### 4.1.1 Cliente
- Registrar cuenta
- Ver servicios disponibles
- Agendar cita
- Ver perfil
- Cancelar cita
- Ver historial

#### 4.1.2 Administrador
- Gestionar servicios
- Gestionar profesionales
- Gestionar citas
- Gestionar clientes
- Ver reportes

### 4.2 Diagrama de Clases

```
+-----------------+
|     Cliente     |
+-----------------+
| - id            |
| - nombre        |
| - email         |
| - telefono      |
| - preferencias  |
| - alergias      |
+-----------------+

+-----------------+
|     Servicio    |
+-----------------+
| - id            |
| - nombre        |
| - descripcion   |
| - precio        |
| - categoria     |
| - imagen        |
+-----------------+

+-----------------+
|    Profesional  |
+-----------------+
| - id            |
| - nombre        |
| - especialidad  |
| - horario       |
| - calificacion  |
+-----------------+

+-----------------+
|      Cita       |
+-----------------+
| - id            |
| - fecha         |
| - hora          |
| - cliente_id    |
| - servicio_id   |
| - profesional_id|
| - estado        |
+-----------------+
```

### 4.3 Modelo de Base de Datos

```
CREATE TABLE clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    preferencias TEXT,
    alergias TEXT,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE servicios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    categoria VARCHAR(50),
    imagen_url VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE profesionales (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100) NOT NULL,
    calificacion DECIMAL(3,2) DEFAULT 0.0,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE citas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    cliente_id INT,
    servicio_id INT,
    profesional_id INT,
    estado VARCHAR(20) DEFAULT 'pendiente',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (servicio_id) REFERENCES servicios(id),
    FOREIGN KEY (profesional_id) REFERENCES profesionales(id)
);
```

### 4.4 Wireframes

#### 4.4.1 Página Principal
- Header con logo y menú de navegación
- Hero section con llamado a acción
- Sección de servicios destacados
- Sección de profesionales
- Sección de testimonios
- Footer con información de contacto

#### 4.4.2 Catálogo de Servicios
- Filtros y búsqueda
- Grid de servicios
- Detalles de servicio
- Sistema de reservas

#### 4.4.3 Agenda de Citas
- Calendario interactivo
- Formulario de reserva
- Lista de citas
- Historial de citas

#### 4.4.4 Perfil de Cliente
- Información personal
- Preferencias
- Historial de tratamientos
- Sistema de puntos

---

## 5. Consideraciones Técnicas

### 5.1 Seguridad
- Autenticación JWT
- Validación de datos
- Protección contra inyección SQL
- Encriptación de datos sensibles
- Control de acceso por roles

### 5.2 Optimización
- Caching de datos
- Optimización de consultas
- Lazy loading
- Compresión de imágenes
- Minificación de assets

### 5.3 Mantenibilidad
- Código modular
- Documentación completa
- Pruebas unitarias
- Sistema de logs
- Monitoreo de errores

---

## 6. Plan de Implementación

### 6.1 Fases del Proyecto
1. **Fase 1 - Configuración**
   - Setup del entorno
   - Configuración de base de datos
   - Estructura inicial del proyecto

2. **Fase 2 - Backend**
   - API REST
   - Modelos de datos
   - Autenticación
   - Endpoints principales

3. **Fase 3 - Frontend**
   - Componentes básicos
   - Sistema de rutas
   - Interfaz principal
   - Catálogo de servicios

4. **Fase 4 - Integración**
   - Conexión API
   - Pruebas de integración
   - Optimización
   - Despliegue inicial

5. **Fase 5 - Mantenimiento**
   - Monitoreo
   - Actualizaciones
   - Soporte
   - Mejoras continuas

---

## 7. Conclusiones

Estheticease representa una solución moderna y eficiente para la gestión de centros de cosmetología. La combinación de tecnologías modernas y un diseño centrado en el usuario proporciona una experiencia superior tanto para clientes como para profesionales, optimizando procesos y mejorando la rentabilidad de los centros.
