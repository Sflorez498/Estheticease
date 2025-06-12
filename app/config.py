"""
Configuración de la aplicación

Este archivo contiene la configuración general de la aplicación,
incluyendo variables de entorno y configuraciones específicas.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    """Clase de configuración"""
    
    # Base de datos
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '110011Sf')
    DB_NAME = os.getenv('DB_NAME', 'Estheticease')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'tu_clave_secreta_muy_segura_aqui')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', 30))
    
    # Sistema de puntos
    PUNTOS_POR_SERVICIO = int(os.getenv('PUNTOS_POR_SERVICIO', 100))
    MIN_PUNTOS_CANJE = int(os.getenv('MIN_PUNTOS_CANJE', 500))
    
    # Configuración general
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    @classmethod
    def get_db_url(cls):
        """Obtener URL de conexión a la base de datos"""
        return f"mysql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"

# Crear instancia de configuración
config = Config()
