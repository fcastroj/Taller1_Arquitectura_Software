from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional
from datetime import datetime

class ProductDTO(BaseModel):
    """
    DTO para transferir datos de productos.
    Pydantic valida automáticamente los tipos y las reglas.
    """
    id: Optional[int] = None
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    @field_validator('price')
    def price_must_be_positive(cls, v):
        """Valida que el precio sea mayor a 0."""
        if v <= 0:
            raise ValueError('El precio debe ser un número positivo.')
        return v

    @field_validator('stock')
    def stock_must_be_non_negative(cls, v):
        """Valida que el stock no sea negativo."""
        if v < 0:
            raise ValueError('El stock no puede ser un número negativo.')
        return v

    model_config = ConfigDict(from_attributes=True)

class ChatMessageRequestDTO(BaseModel):
    """DTO para recibir un nuevo mensaje de chat del usuario."""
    session_id: str
    message: str

    @field_validator('message', 'session_id')
    def not_empty(cls, v):
        """Valida que el campo no esté vacío."""
        if not v or not v.strip():
            raise ValueError('El campo no puede estar vacío.')
        return v

class ChatMessageResponseDTO(BaseModel):
    """DTO para enviar la respuesta del chat al usuario."""
    session_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime

class ChatHistoryDTO(BaseModel):
    """DTO para representar un único mensaje en el historial de chat."""
    id: int
    role: str
    message: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
