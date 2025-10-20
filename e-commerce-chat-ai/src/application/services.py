from abc import ABC, abstractmethod
from typing import List
from src.domain.entities import Product, ChatContext

class IAIService(ABC):
    """
    Interface que define el contrato para un servicio de IA generativa.
    Esto permite que la capa de aplicación sea independiente del proveedor de IA (Gemini, OpenAI, etc.).
    """
    @abstractmethod
    async def generate_response(
        self, user_message: str, products: List[Product], context: ChatContext
    ) -> str:
        """
        Genera una respuesta de la IA basada en el mensaje del usuario,
        el catálogo de productos y el contexto de la conversación.

        Args:
            user_message (str): El mensaje enviado por el usuario.
            products (List[Product]): La lista de productos disponibles para informar a la IA.
            context (ChatContext): El historial de la conversación reciente.

        Returns:
            str: La respuesta de texto generada por la IA.
        """
        pass
