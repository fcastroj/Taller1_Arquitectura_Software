from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

# Importaciones de nuestro proyecto
from src.infrastructure.db.database import init_db, get_db
from src.infrastructure.repositories.product_repository import SQLProductRepository
from src.infrastructure.repositories.chat_repository import SQLChatRepository
from src.infrastructure.llm_providers.gemini_service import GeminiService

from src.application.product_service import ProductService
from src.application.chat_service import ChatService
from src.application.dtos import ProductDTO, ChatMessageRequestDTO, ChatMessageResponseDTO, ChatHistoryDTO

from src.domain.exceptions import ProductNotFoundError, ChatServiceError

# --- Configuración de la App ---
app = FastAPI(
    title="E-commerce Chat API",
    description="API para un e-commerce de zapatos con un asistente de chat inteligente.",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, deberías restringir esto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Evento de Inicio ---
@app.on_event("startup")
def on_startup():
    """
    Se ejecuta cuando la aplicación se inicia.
    Crea las tablas de la base de datos y carga los datos iniciales.
    """
    init_db()

# --- Inyección de Dependencias ---
def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    repo = SQLProductRepository(db)
    return ProductService(repo)

def get_chat_service(db: Session = Depends(get_db)) -> ChatService:
    chat_repo = SQLChatRepository(db)
    product_repo = SQLProductRepository(db)
    ai_service = GeminiService()
    return ChatService(chat_repo, product_repo, ai_service)

# --- Endpoints de la API ---

@app.get("/", tags=["General"])
def read_root():
    """Endpoint raíz que muestra información básica de la API."""
    return {
        "message": "Bienvenido a la API del E-commerce con Chat Inteligente",
        "version": app.version,
        "docs_url": "/docs"
    }

@app.get("/health", tags=["General"])
def health_check():
    """Endpoint de health check para verificar que la API está funcionando."""
    return {"status": "ok"}

# --- Endpoints de Productos ---

@app.get("/products", response_model=List[ProductDTO], tags=["Products"])
def get_all_products(product_service: ProductService = Depends(get_product_service)):
    """Obtiene la lista completa de todos los productos."""
    return product_service.get_all_products()

@app.get("/products/{product_id}", response_model=ProductDTO, tags=["Products"])
def get_product_by_id(product_id: int, product_service: ProductService = Depends(get_product_service)):
    """Obtiene un producto específico por su ID."""
    try:
        product = product_service.get_product_by_id(product_id)
        return product
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

# --- Endpoints del Chat ---

@app.post("/chat", response_model=ChatMessageResponseDTO, tags=["Chat"])
async def process_chat_message(
    request: ChatMessageRequestDTO,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Procesa un mensaje del usuario a través del chat y obtiene una respuesta de la IA.
    """
    try:
        response = await chat_service.process_message(request)
        return response
    except ChatServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Un error inesperado ocurrió: {str(e)}")

@app.get("/chat/history/{session_id}", response_model=List[ChatHistoryDTO], tags=["Chat"])
def get_chat_history(session_id: str, chat_service: ChatService = Depends(get_chat_service)):
    """Obtiene el historial de conversación para una sesión específica."""
    return chat_service.get_session_history(session_id)

@app.delete("/chat/history/{session_id}", tags=["Chat"])
def delete_chat_history(session_id: str, chat_service: ChatService = Depends(get_chat_service)):
    """Elimina todo el historial de una sesión de chat."""
    deleted_count = chat_service.clear_session_history(session_id)
    return {"message": f"Historial de la sesión '{session_id}' eliminado. Se borraron {deleted_count} mensajes."}
