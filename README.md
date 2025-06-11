# Estheticease - Sistema de Gestión para Salón de Belleza

## Descripción
Estheticease es un sistema integral de gestión para salones de belleza y estética que permite administrar citas, clientes, empleados, servicios y productos.

## Características Principales
- Gestión de citas y horarios
- Control de inventario
- Gestión de clientes y empleados
- Sistema de ventas
- Panel de administración
- Autenticación y autorización por roles

## Requisitos
- Python 3.8+
- MySQL 8.0+
- Node.js 14+

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd estheticease
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
.\venv\Scripts\activate  # En Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la base de datos:
```bash
mysql -u root -p < ESTHE.sql
```

5. Configurar variables de entorno:
Crear un archivo `.env` en la raíz del proyecto con:
```
DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost/Estheticease
SECRET_KEY=tu_clave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

6. Iniciar el servidor:
```bash
uvicorn app.main:app --reload
```

## Estructura del Proyecto
```
estheticease/
├── app/
│   ├── auth/
│   ├── database/
│   ├── models/
│   ├── routers/
│   └── main.py
├── FrontParaFastApi/
├── requirements.txt
└── ESTHE.sql
```

## Documentación de la API
La documentación de la API está disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contribución
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles. 