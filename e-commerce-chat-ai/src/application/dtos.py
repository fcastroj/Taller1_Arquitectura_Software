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
        """
        Valida que el precio de un producto sea un número positivo.

        Args:
            v (float): El valor del precio a validar.

        Raises:
            ValueError: Si el precio es menor o igual a cero.

        Returns:
            float: El precio validado.
        """
        if v <= 0:
            raise ValueError('El precio debe ser un número positivo.')
        return v

    @field_validator('stock')
    def stock_must_be_non_negative(cls, v):
        """
        Valida que el stock de un producto no sea un número negativo.

        Args:
            v (int): El valor del stock a validar.

        Raises:
            ValueError: Si el stock es menor que cero.

        Returns:
            int: El stock validado.
        """
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
        """
        Valida que el campo de texto (mensaje o ID de sesión) no esté vacío o solo contenga espacios en blanco.

        Args:
            v (str): El valor del campo a validar.

        Raises:
            ValueError: Si el campo está vacío o solo contiene espacios en blanco.

        Returns:
            str: El valor del campo validado.
        """
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
