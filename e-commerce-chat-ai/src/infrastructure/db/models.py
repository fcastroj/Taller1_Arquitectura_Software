"""
Este módulo define los modelos de base de datos (ORM) utilizando SQLAlchemy.
Cada clase representa una tabla en la base de datos y sus respectivas columnas.
"""

from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, func
)
from .database import Base

class ProductModel(Base):
    """
    Modelo ORM de SQLAlchemy que representa la tabla 'products'.
    Almacena la información detallada de cada producto disponible en el e-commerce.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False, index=True)
    brand = Column(String(100), index=True)
    category = Column(String(100), index=True)
    size = Column(String(20))
    color = Column(String(50))
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    description = Column(Text)

class ChatMemoryModel(Base):
    """
    Modelo ORM de SQLAlchemy que representa la tabla 'chat_memory'.
    Almacena el historial de mensajes de las conversaciones del chat, incluyendo
    el ID de sesión, el rol (usuario/asistente), el mensaje y la marca de tiempo.
    """
    __tablename__ = "chat_memory"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(100), nullable=False, index=True)
    role = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
