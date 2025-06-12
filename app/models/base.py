from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Crear la base declarativa para los modelos
declarative_base = declarative_base()

# Configurar la conexión a la base de datos
DATABASE_URL = "mysql+mysqlconnector://root:110011Sf@localhost:3306/Estheticease"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
