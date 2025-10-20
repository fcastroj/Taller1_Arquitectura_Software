from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from src.domain.entities import ChatMessage
from src.domain.repositories import IChatRepository
from src.infrastructure.db.models import ChatMemoryModel

class SQLChatRepository(IChatRepository):
    """
    Implementación del repositorio de historial de chat utilizando SQLAlchemy.
    """
    def __init__(self, db: Session):
        """
        Inicializa el repositorio de chat con una sesión de base de datos.

        Args:
            db (Session): La sesión de SQLAlchemy para interactuar con la base de datos.
        """
        self.db = db

    def _model_to_entity(self, model: ChatMemoryModel) -> ChatMessage:
        """
        Convierte un objeto `ChatMemoryModel` de SQLAlchemy a una entidad de dominio `ChatMessage`.

        Args:
            model (ChatMemoryModel): El modelo de base de datos a convertir.

        Returns:
            ChatMessage: La entidad de dominio `ChatMessage` resultante.
        """
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=model.timestamp
        )

    def _entity_to_model(self, entity: ChatMessage) -> ChatMemoryModel:
        """
        Convierte una entidad de dominio `ChatMessage` a un objeto `ChatMemoryModel` de SQLAlchemy.

        Args:
            entity (ChatMessage): La entidad de dominio a convertir.

        Returns:
            ChatMemoryModel: El modelo de base de datos `ChatMemoryModel` resultante.
        """
        return ChatMemoryModel(
            id=entity.id,
            session_id=entity.session_id,
            role=entity.role,
            message=entity.message,
            timestamp=entity.timestamp
        )

    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un nuevo mensaje de chat en la base de datos o actualiza uno existente.

        Args:
            message (ChatMessage): El mensaje de chat a guardar.

        Returns:
            ChatMessage: El mensaje de chat guardado, incluyendo su ID si fue recién creado.
        """
        model = self._entity_to_model(message)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def get_session_history(self, session_id: str, limit: Optional[int] = None) -> List[ChatMessage]:
        """
        Recupera el historial de mensajes para una sesión de chat específica.

        Args:
            session_id (str): El ID de la sesión de chat.
            limit (Optional[int]): El número máximo de mensajes a recuperar. Si es None, recupera todos.

        Returns:
            List[ChatMessage]: Una lista de entidades `ChatMessage` ordenadas cronológicamente.
        """
        query = self.db.query(ChatMemoryModel).filter(ChatMemoryModel.session_id == session_id).order_by(ChatMemoryModel.timestamp.asc())
        if limit:
            query = query.limit(limit)
        models = query.all()
        return [self._model_to_entity(m) for m in models]

    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        Recupera los 'count' mensajes más recientes de una sesión de chat específica.

        Los mensajes se devuelven en orden cronológico ascendente (el más antiguo primero).

        Args:
            session_id (str): El ID de la sesión de chat.
            count (int): El número de mensajes más recientes a recuperar.

        Returns:
            List[ChatMessage]: Una lista de entidades `ChatMessage` ordenadas cronológicamente.
        """
        # Obtiene los 'count' más recientes (ordenados descendente por tiempo)
        # y luego los invierte para que queden en orden cronológico (el más antiguo primero).
        models = (self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp.desc())
            .limit(count)
            .all())
        
        # Invertir la lista para que el orden sea cronológico ascendente
        models.reverse()
        return [self._model_to_entity(m) for m in models]

    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina todos los mensajes del historial para una sesión de chat específica.

        Args:
            session_id (str): El ID de la sesión de chat de la cual eliminar el historial.

        Returns:
            int: El número de registros (mensajes) eliminados de la base de datos.
        """
        num_deleted = self.db.query(ChatMemoryModel).filter(ChatMemoryModel.session_id == session_id).delete()
        self.db.commit()
        return num_deleted
