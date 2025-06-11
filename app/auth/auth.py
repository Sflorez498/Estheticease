# Importamos las librerías necesarias para la autenticación
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.models.empleado import Empleado

# Configuración de seguridad para los tokens JWT
# La clave secreta se usa para encriptar los tokens
# El algoritmo HS256 es el método de encriptación
# Los tokens expiran después de 30 minutos
SECRET_KEY = "tu_clave_secreta_muy_segura_aqui"  # Deberías mover esto a variables de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para crear tokens JWT
# Recibe datos del usuario y crea un token de acceso
# El token expira después del tiempo especificado
# Si no se especifica tiempo, expira después de 15 minutos
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para obtener el usuario actual
# Verifica el token y retorna los datos del usuario
# Si el token es inválido, retorna un error 401
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(Empleado).filter(Empleado.correo == email).first()
    if user is None:
        raise credentials_exception
    return user

# Función para verificar si el usuario es administrador
# Solo los usuarios con rol de administrador pueden acceder
# Si no es administrador, retorna un error 403
async def get_current_admin_user(current_user: Empleado = Depends(get_current_user)):
    if current_user.id_rol != 1:  # Asumiendo que 1 es el ID del rol de administrador
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario no tiene permisos de administrador"
        )
    return current_user 