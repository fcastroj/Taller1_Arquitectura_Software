from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, func
)
from .database import Base

class ProductModel(Base):
    """
    Modelo ORM de SQLAlchemy que representa la tabla 'products'.
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
    """
    __tablename__ = "chat_memory"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(100), nullable=False, index=True)
    role = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
