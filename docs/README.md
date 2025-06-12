# Sistema de gestión de salas de stheitease-beauty

## explicación
SthetaSe es una aplicación web que promueve la gestión diaria de salas de belleza y estética. Desde el servicio al cliente hasta la gestión de inventario, todo está diseñado para facilitar su vida.

## Características principales
-D es la gestión de la fecha y el horario
- Gestión de inversiones a través de notificaciones de acciones
- Gestión completa de clientes y empleados
- Sistema de ventas con monitoreo de productos
- Comité de Gestión Intuitiva
- Un sistema seguro con roles y autoridad

## Requisitos
-Python 3.8+
-Mysql 8.0+
-Node.js 14+

## instalar

# 1. Primer clon del repositorio.
"Intento"
git -klon [url_del_repositorio]
Estética de CD
`` `` ``

# 2. Cree y active un entorno virtual.
"Intento"
python -m -venv -venv
source venv/bin/activate # En Linux/Mac
＃O
.\venv\Scripts\activate # En Windows
`` `` ``

# 3. Instalación de la unidad:
"Intento"
Repormations.txt de PIP Install-R.txt
`` `` ``

# 4. Configure la base de datos:
"Intento"
mysql -u root -p 
`` `` ``

# 5. Construcción de variables circundantes:
Cree un archivo ".sv" para los activos regulares del proyecto.
`` `` ``
database_url = mysql+pymysql: // usuario: contraseña@localhost/sthexase
secry_key = tu_clave_secreta
Algoritmo = HS256
Access_token_expire_minutes = 30
`` `` ``

# 6. Inicie el servidor:
"Intento"
Aplicación de Uvicorn. Mayor: App -Reelgroad
`` `` ``

## Estructura del proyecto
`` `` ``
Belleza/estética/
├── app/ # Backend FastAPI
│ ├── auth/ # Autenticación
│ ├── database/ # Conexiones DB
│ ├── models/ # Modelos de datos
│ ├── routers/ # Rutas API
│ └── main.py # Punto de entrada
├── FrontParaFastApi/ # Frontend React
├── requirements.txt # Dependencias Python
└── ESTHE.sql # Estructura DB
`` `` ``

## Documentación de  API
Puede consultar la documentación de la API.
-Swagger ui: http ： // localhost: 8000/documentos
-Redoc: http ： // localhost ： 8000/redoc

¡Ambas interfaces son interactivas y puede probar la API directamente!

## contribución
1. Bifurca el proyecto
2. 
3 .. Commit Cambios ("git commit -m" agrega algunas características sorprendentes ")
4. Push Ararama (`Git Push Origen Feature/AmazingFeature")))
5。

## licencia
Este proyecto está bajo la licencia: se puede encontrar más información en el archivo [licencia] (licencia).