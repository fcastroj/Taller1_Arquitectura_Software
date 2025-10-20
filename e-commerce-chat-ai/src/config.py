"""
Este módulo gestiona la configuración de la aplicación, cargando variables de entorno.
Define constantes para la clave de la API de Gemini, la URL de la base de datos y el entorno.
"""

import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/ecommerce_chat.db")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
