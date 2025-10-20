import asyncio
from datetime import datetime
from typing import List

from src.application.dtos import (ChatMessageRequestDTO, ChatMessageResponseDTO,
                                  ChatHistoryDTO)
from src.application.services import IAIService
from src.domain.entities import ChatContext, ChatMessage
from src.domain.exceptions import ChatServiceError
from src.domain.repositories import IChatRepository, IProductRepository


class ChatService:
    """
    Servicio de aplicación para gestionar la lógica de negocio del chat.
    """

    def __init__(
        self,
        chat_repository: IChatRepository,
        product_repository: IProductRepository,
        ai_service: IAIService,
    ):
        """
        Inicializa el servicio de chat.

        Args:
            chat_repository: Repositorio para el historial del chat.
            product_repository: Repositorio para los productos.
            ai_service: Servicio de IA para generar respuestas.
        """
        self.chat_repository = chat_repository
        self.product_repository = product_repository
        self.ai_service = ai_service

    async def process_message(
        self, request: ChatMessageRequestDTO
    ) -> ChatMessageResponseDTO:
        """
        Procesa un mensaje de chat del usuario y retorna la respuesta de la IA.

        Este es el flujo principal del caso de uso del chat.
        """
        try:
            # 1. Guardar el mensaje del usuario
            user_message = ChatMessage(
                session_id=request.session_id,
                role="user",
                message=request.message,
                id=None
            )
            self.chat_repository.save_message(user_message)

            # 2. Obtener contexto (productos e historial)
            # Usamos asyncio.gather para correr estas dos tareas en paralelo
            products_task = asyncio.to_thread(self.product_repository.get_all)
            history_task = asyncio.to_thread(
                self.chat_repository.get_recent_messages, request.session_id, 6
            )
            products, recent_history = await asyncio.gather(products_task, history_task)

            chat_context = ChatContext(messages=recent_history)

            # 3. Generar respuesta de la IA
            assistant_text = await self.ai_service.generate_response(
                user_message=request.message,
                products=products,
                context=chat_context,
            )

            # 4. Guardar la respuesta del asistente
            assistant_message = ChatMessage(
                session_id=request.session_id,
                role="assistant",
                message=assistant_text,
                id=None
            )
            self.chat_repository.save_message(assistant_message)

            # 5. Retornar la respuesta
            return ChatMessageResponseDTO(
                session_id=request.session_id,
                user_message=user_message.message,
                assistant_message=assistant_message.message,
                timestamp=assistant_message.timestamp,
            )
        except Exception as e:
            # En un caso real, aquí habría un logging más detallado
            raise ChatServiceError(f"Error procesando el mensaje: {e}")

    def get_session_history(self, session_id: str) -> List[ChatHistoryDTO]:
        """
        Obtiene el historial completo de mensajes para una sesión de chat específica.

        Args:
            session_id: El identificador único de la sesión de chat.

        Returns:
            Una lista de DTOs que representan el historial de mensajes de la sesión.
        """
        history = self.chat_repository.get_session_history(session_id)
        return [ChatHistoryDTO.model_validate(msg, from_attributes=True) for msg in history]

    def clear_session_history(self, session_id: str) -> int:
        """
        Elimina todos los mensajes del historial para una sesión de chat específica.

        Args:
            session_id: El identificador único de la sesión de chat.

        Returns:
            El número de mensajes eliminados.
        """
        return self.chat_repository.delete_session_history(session_id)
