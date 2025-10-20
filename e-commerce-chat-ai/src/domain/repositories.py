from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Product, ChatMessage

class IProductRepository(ABC):
    """
    Interface que define el contrato para el repositorio de productos.
    Las implementaciones concretas estarán en la capa de infraestructura.
    """

    @abstractmethod
    def get_all(self) -> List[Product]:
        """Obtiene todos los productos."""
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Obtiene un producto por su ID.

        Args:
            product_id (int): El ID del producto a buscar.

        Returns:
            Optional[Product]: El producto si se encuentra, de lo contrario None.
        """
        pass

    @abstractmethod
    def get_by_brand(self, brand: str) -> List[Product]:
        """
        Obtiene una lista de productos de una marca específica.

        Args:
            brand (str): La marca a filtrar.

        Returns:
            List[Product]: Lista de productos de la marca especificada.
        """
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> List[Product]:
        """
        Obtiene una lista de productos de una categoría específica.

        Args:
            category (str): La categoría a filtrar.

        Returns:
            List[Product]: Lista de productos de la categoría especificada.
        """
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        """
        Guarda o actualiza un producto en el repositorio.
        Si el producto tiene un ID, se actualiza. Si no, se crea.

        Args:
            product (Product): La entidad del producto a guardar.

        Returns:
            Product: El producto guardado (con el ID asignado si es nuevo).
        """
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto por su ID.

        Args:
            product_id (int): El ID del producto a eliminar.

        Returns:
            bool: True si el producto fue eliminado, False si no se encontró.
        """
        pass

class IChatRepository(ABC):
    """
    Interface que define el contrato para gestionar el historial de conversaciones.
    """

    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje de chat en el historial.

        Args:
            message (ChatMessage): El mensaje a guardar.

        Returns:
            ChatMessage: El mensaje guardado con su ID asignado.
        """
        pass

    @abstractmethod
    def get_session_history(self, session_id: str, limit: Optional[int] = None) -> List[ChatMessage]:
        """
        Obtiene el historial de una sesión de chat.

        Args:
            session_id (str): El ID de la sesión.
            limit (Optional[int]): El número máximo de mensajes a retornar.

        Returns:
            List[ChatMessage]: Lista de mensajes en orden cronológico.
        """
        pass
        
    @abstractmethod
    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        Obtiene los N mensajes más recientes de una sesión.

        Args:
            session_id (str): El ID de la sesión.
            count (int): El número de mensajes recientes a obtener.

        Returns:
            List[ChatMessage]: Lista de los mensajes más recientes en orden cronológico.
        """
        pass

    @abstractmethod
    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de una sesión de chat.

        Args:
            session_id (str): El ID de la sesión a eliminar.

        Returns:
            int: El número de mensajes que fueron eliminados.
        """
        pass
