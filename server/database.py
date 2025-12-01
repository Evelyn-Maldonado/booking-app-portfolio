import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Tomamos la URL de las variables de entorno (definida en docker-compose)
# Si no existe, usa una por defecto para local (útil para testing fuera de docker)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/booking_system")

# Creamos el motor de conexión
engine = create_engine(DATABASE_URL)

# Creamos la sesión (la "herramienta" para hacer consultas)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para nuestros modelos
Base = declarative_base()

# Dependencia para obtener la DB en cada petición (Patrón de FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()