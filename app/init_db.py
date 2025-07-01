from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Roles(Base):
    __tablename__ = "roles"
    
    id_rol = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    empleados = relationship("Empleados", back_populates="rol")

class Empleados(Base):
    __tablename__ = "empleados"
    
    id_empleado = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    contacto = Column(String(20), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contraseña = Column(String(200), nullable=False)
    id_rol = Column(Integer, ForeignKey("roles.id_rol"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    rol = relationship("Roles", back_populates="empleados")

class Servicios(Base):
    __tablename__ = "servicios"
    
    id_servicio = Column(Integer, primary_key=True, index=True)
    nombre_servicio = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    precio = Column(Float, nullable=False)
    duracion_minutos = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    
    # Crear roles iniciales
    Session = sessionmaker(bind=engine)
    session = Session()
    
    roles = [
        Roles(nombre_rol="Administrador"),
        Roles(nombre_rol="Recepcionista"),
        Roles(nombre_rol="Empleado"),
        Roles(nombre_rol="Cliente")
    ]
    
    # Agregar roles si no existen
    for rol in roles:
        existing_role = session.query(Roles).filter_by(nombre_rol=rol.nombre_rol).first()
        if not existing_role:
            session.add(rol)
    
    session.commit()
    session.close()
    print("Tablas creadas y roles iniciales insertados")
