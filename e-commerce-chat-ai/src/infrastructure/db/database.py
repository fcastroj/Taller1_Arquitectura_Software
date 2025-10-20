from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.config import DATABASE_URL

# El argumento connect_args es necesario solo para SQLite
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Función de dependencia de FastAPI para obtener una sesión de base de datos.
    Asegura que la sesión de la base de datos se cierre siempre después de una solicitud.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Inicializa la base de datos creando todas las tablas definidas en los modelos
    y carga los datos iniciales.
    Esta función debe ser llamada al iniciar la aplicación.
    """
    # Importa todos los modelos aquí antes de llamar a create_all
    # para que se registren correctamente en los metadatos de la Base.
    from . import models
    from .init_data import load_initial_data

    print("Creando todas las tablas de la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas.")

    # Cargar datos iniciales
    db = SessionLocal()
    try:
        load_initial_data(db)
    finally:
        db.close()
