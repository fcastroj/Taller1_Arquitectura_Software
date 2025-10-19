from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

@dataclass
class Product:
    """
    Entidad que representa un producto en el e-commerce.
    Contiene la lógica de negocio relacionada con productos.

    Attributes:
        id (Optional[int]): Identificador único del producto.
        name (str): Nombre del producto.
        brand (str): Marca del producto.
        category (str): Categoría del producto.
        size (str): Talla del producto.
        color (str): Color del producto.
        price (float): Precio del producto.
        stock (int): Cantidad de producto en inventario.
        description (str): Descripción del producto.
    """
    id: Optional[int]
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    def __post_init__(self):
        """
        Validaciones que se ejecutan después de crear el objeto.
        Lanza ValueError si alguna validación falla.
        """
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        if self.price <= 0:
            raise ValueError("El precio debe ser mayor a 0.")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo.")

    def is_available(self) -> bool:
        """
        Verifica si el producto tiene stock disponible.

        Returns:
            bool: True si el stock es mayor a 0, False en caso contrario.
        """
        return self.stock > 0

    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce el stock del producto.

        Args:
            quantity (int): La cantidad a reducir.

        Raises:
            ValueError: Si la cantidad es negativa o si no hay suficiente stock.
        """
        if quantity <= 0:
            raise ValueError("La cantidad a reducir debe ser positiva.")
        if self.stock < quantity:
            raise ValueError(f"Stock insuficiente. Stock actual: {self.stock}, se intentó reducir: {quantity}")
        self.stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        """
        Aumenta el stock del producto.

        Args:
            quantity (int): La cantidad a aumentar.

        Raises:
            ValueError: Si la cantidad es negativa.
        """
        if quantity <= 0:
            raise ValueError("La cantidad a aumentar debe ser positiva.")
        self.stock += quantity


@dataclass
class ChatMessage:
    """
    Entidad que representa un mensaje en el chat.

    Attributes:
        id (Optional[int]): Identificador único del mensaje.
        session_id (str): Identificador de la sesión de chat.
        role (str): Rol del autor del mensaje ('user' o 'assistant').
        message (str): Contenido del mensaje.
        timestamp (datetime): Fecha y hora del mensaje.
    """
    id: Optional[int]
    session_id: str
    role: str
    message: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        """
        Validaciones que se ejecutan después de crear el objeto.
        """
        if not self.session_id or not self.session_id.strip():
            raise ValueError("El session_id no puede estar vacío.")
        if self.role not in ['user', 'assistant']:
            raise ValueError("El rol debe ser 'user' o 'assistant'.")
        if not self.message or not self.message.strip():
            raise ValueError("El mensaje no puede estar vacío.")

    def is_from_user(self) -> bool:
        """Retorna True si el mensaje es del usuario."""
        return self.role == 'user'

    def is_from_assistant(self) -> bool:
        """Retorna True si el mensaje es del asistente."""
        return self.role == 'assistant'


@dataclass
class ChatContext:
    """
    Value Object que encapsula el contexto de una conversación.
    Mantiene los mensajes recientes para dar coherencia al chat.

    Attributes:
        messages (List[ChatMessage]): Lista de mensajes en la conversación.
        max_messages (int): Número máximo de mensajes a mantener en el contexto.
    """
    messages: List[ChatMessage]
    max_messages: int = 6

    def get_recent_messages(self) -> List[ChatMessage]:
        """
        Retorna los últimos N mensajes (definido por max_messages).

        Returns:
            List[ChatMessage]: Una lista con los mensajes más recientes.
        """
        return self.messages[-self.max_messages:]

    def format_for_prompt(self) -> str:
        """
        Formatea los mensajes para incluirlos en el prompt de la IA.
        Formato:
        "Usuario: mensaje del usuario
        Asistente: respuesta del asistente"

        Returns:
            str: Una cadena de texto con el historial formateado.
        """
        formatted_history = []
        for msg in self.get_recent_messages():
            role_spanish = "Usuario" if msg.is_from_user() else "Asistente"
            formatted_history.append(f"{role_spanish}: {msg.message}")
        return "\n".join(formatted_history)
