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
        self.db = db

    def _model_to_entity(self, model: ChatMemoryModel) -> ChatMessage:
        """Convierte un modelo SQLAlchemy a una entidad de dominio."""
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=model.timestamp
        )

    def _entity_to_model(self, entity: ChatMessage) -> ChatMemoryModel:
        """Convierte una entidad de dominio a un modelo SQLAlchemy."""
        return ChatMemoryModel(
            id=entity.id,
            session_id=entity.session_id,
            role=entity.role,
            message=entity.message,
            timestamp=entity.timestamp
        )

    def save_message(self, message: ChatMessage) -> ChatMessage:
        model = self._entity_to_model(message)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def get_session_history(self, session_id: str, limit: Optional[int] = None) -> List[ChatMessage]:
        query = self.db.query(ChatMemoryModel).filter(ChatMemoryModel.session_id == session_id).order_by(ChatMemoryModel.timestamp.asc())
        if limit:
            query = query.limit(limit)
        models = query.all()
        return [self._model_to_entity(m) for m in models]

    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
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
        num_deleted = self.db.query(ChatMemoryModel).filter(ChatMemoryModel.session_id == session_id).delete()
        self.db.commit()
        return num_deleted
