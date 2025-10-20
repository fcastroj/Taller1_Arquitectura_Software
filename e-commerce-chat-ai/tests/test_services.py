
import pytest
from typing import List, Optional, Dict, Any
from src.domain.entities import Product
from src.domain.repositories import IProductRepository
from src.domain.exceptions import ProductNotFoundError
from src.application.dtos import ProductDTO
from src.application.product_service import ProductService

# Mock Product Repository for testing
class MockProductRepository(IProductRepository):
    def __init__(self, initial_products: List[Product] = None):
        self._products = {p.id: p for p in initial_products} if initial_products else {}
        self._next_id = (max(self._products.keys()) + 1) if self._products else 1

    def get_all(self) -> List[Product]:
        return list(self._products.values())

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self._products.get(product_id)

    def save(self, product: Product) -> Product:
        if product.id is None:
            product.id = self._next_id
            self._next_id += 1
        self._products[product.id] = product
        return product

    def delete(self, product_id: int) -> bool:
        if product_id in self._products:
            del self._products[product_id]
            return True
        return False
    
    def get_by_brand(self, brand: str) -> List[Product]:
        return [p for p in self._products.values() if p.brand == brand]

    def get_by_category(self, category: str) -> List[Product]:
        return [p for p in self._products.values() if p.category == category]

# Fixtures for ProductService tests
@pytest.fixture
def sample_products():
    return [
        Product(id=1, name="Nike Air", brand="Nike", category="Running", size="42", color="Black", price=120.0, stock=10, description="Running shoes"),
        Product(id=2, name="Adidas Ultraboost", brand="Adidas", category="Running", size="43", color="White", price=150.0, stock=5, description="Comfortable shoes"),
        Product(id=3, name="Puma Suede", brand="Puma", category="Casual", size="41", color="Red", price=80.0, stock=0, description="Classic shoes"),
    ]

@pytest.fixture
def mock_product_repo(sample_products):
    return MockProductRepository(initial_products=sample_products)

@pytest.fixture
def product_service(mock_product_repo):
    return ProductService(product_repository=mock_product_repo)

# Tests for ProductService
def test_get_all_products(product_service: ProductService):
    """Test retrieving all products."""
    products = product_service.get_all_products()
    assert len(products) == 3
    assert isinstance(products[0], ProductDTO)

def test_get_available_products(product_service: ProductService):
    """Test retrieving only available products."""
    products = product_service.get_available_products()
    assert len(products) == 2
    assert all(p.stock > 0 for p in products)

def test_get_product_by_id(product_service: ProductService):
    """Test retrieving a product by its ID."""
    product = product_service.get_product_by_id(1)
    assert product is not None
    assert product.id == 1
    assert product.name == "Nike Air"

def test_get_product_by_id_not_found(product_service: ProductService):
    """Test that ProductNotFoundError is raised for a non-existent ID."""
    with pytest.raises(ProductNotFoundError):
        product_service.get_product_by_id(999)

def test_create_product(product_service: ProductService):
    """Test creating a new product."""
    new_product_dto = ProductDTO(
        name="New Balance 574", brand="New Balance", category="Casual", 
        size="42", color="Grey", price=90.0, stock=20, description="A new shoe"
    )
    created_product = product_service.create_product(new_product_dto)
    assert created_product.id is not None
    assert created_product.name == "New Balance 574"
    
    # Verify it was actually added
    all_products = product_service.get_all_products()
    assert len(all_products) == 4

def test_update_product(product_service: ProductService):
    """Test updating an existing product."""
    update_dto = ProductDTO(
        id=1, name="Nike Air Max", brand="Nike", category="Lifestyle", 
        size="42", color="Black", price=130.0, stock=8, description="Updated shoes"
    )
    updated_product = product_service.update_product(1, update_dto)
    assert updated_product.name == "Nike Air Max"
    assert updated_product.price == 130.0
    assert updated_product.stock == 8

def test_update_product_not_found(product_service: ProductService):
    """Test that updating a non-existent product raises an error."""
    update_dto = ProductDTO(
        id=999, name="Ghost Shoe", brand="None", category="None", 
        size="0", color="None", price=1.0, stock=1, description="Does not exist"
    )
    with pytest.raises(ProductNotFoundError):
        product_service.update_product(999, update_dto)

def test_delete_product(product_service: ProductService):
    """Test deleting a product."""
    result = product_service.delete_product(1)
    assert result is True
    
    with pytest.raises(ProductNotFoundError):
        product_service.get_product_by_id(1)
    
    all_products = product_service.get_all_products()
    assert len(all_products) == 2

def test_delete_product_not_found(product_service: ProductService):
    """Test that deleting a non-existent product raises an error."""
    with pytest.raises(ProductNotFoundError):
        product_service.delete_product(999)

def test_search_products(product_service: ProductService):
    """Test searching for products with filters."""
    # Search by brand
    nike_products = product_service.search_products(filters={"brand": "Nike"})
    assert len(nike_products) == 1
    assert nike_products[0].brand == "Nike"

    # Search by category
    running_products = product_service.search_products(filters={"category": "Running"})
    assert len(running_products) == 2

    # Search by brand and category
    adidas_running = product_service.search_products(filters={"brand": "Adidas", "category": "Running"})
    assert len(adidas_running) == 1
    assert adidas_running[0].name == "Adidas Ultraboost"


# Mocks and fixtures for ChatService tests
from src.domain.entities import ChatMessage, ChatContext
from src.domain.repositories import IChatRepository
from src.application.services import IAIService
from src.application.chat_service import ChatService
from src.application.dtos import ChatMessageRequestDTO
from src.domain.exceptions import ChatServiceError

class MockChatRepository(IChatRepository):
    def __init__(self):
        self._messages: Dict[str, List[ChatMessage]] = {}
        self._next_id = 1

    def save_message(self, message: ChatMessage) -> ChatMessage:
        message.id = self._next_id
        self._next_id += 1
        if message.session_id not in self._messages:
            self._messages[message.session_id] = []
        self._messages[message.session_id].append(message)
        return message

    def get_session_history(self, session_id: str, limit: Optional[int] = None) -> List[ChatMessage]:
        history = self._messages.get(session_id, [])
        if limit:
            return history[-limit:]
        return history

    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        return self.get_session_history(session_id, limit=count)

    def delete_session_history(self, session_id: str) -> int:
        if session_id in self._messages:
            count = len(self._messages[session_id])
            del self._messages[session_id]
            return count
        return 0

class MockAIService(IAIService):
    async def generate_response(self, user_message: str, products: List[Product], context: ChatContext) -> str:
        if "error" in user_message:
            raise Exception("AI service error")
        return f"AI response to: {user_message}"

@pytest.fixture
def mock_chat_repo():
    return MockChatRepository()

@pytest.fixture
def mock_ai_service():
    return MockAIService()

@pytest.fixture
def chat_service(mock_chat_repo, mock_product_repo, mock_ai_service):
    return ChatService(
        chat_repository=mock_chat_repo,
        product_repository=mock_product_repo,
        ai_service=mock_ai_service
    )

# Tests for ChatService
@pytest.mark.asyncio
async def test_process_message(chat_service: ChatService, mock_chat_repo: MockChatRepository):
    """Test successful processing of a user message."""
    request = ChatMessageRequestDTO(session_id="session1", message="Hello")
    response = await chat_service.process_message(request)

    assert response.session_id == "session1"
    assert response.user_message == "Hello"
    assert response.assistant_message == "AI response to: Hello"
    
    history = mock_chat_repo.get_session_history("session1")
    assert len(history) == 2
    assert history[0].role == "user"
    assert history[1].role == "assistant"

@pytest.mark.asyncio
async def test_process_message_error(chat_service: ChatService):
    """Test that ChatServiceError is raised when the AI service fails."""
    request = ChatMessageRequestDTO(session_id="session1", message="trigger error")
    with pytest.raises(ChatServiceError):
        await chat_service.process_message(request)

def test_get_session_history(chat_service: ChatService, mock_chat_repo: MockChatRepository):
    """Test retrieving session history."""
    # Add some messages to the history
    mock_chat_repo.save_message(ChatMessage(session_id="session2", role="user", message="First message", id=None))
    mock_chat_repo.save_message(ChatMessage(session_id="session2", role="assistant", message="First response", id=None))

    history_dtos = chat_service.get_session_history("session2")
    assert len(history_dtos) == 2
    assert history_dtos[0].role == "user"
    assert history_dtos[1].message == "First response"

def test_clear_session_history(chat_service: ChatService, mock_chat_repo: MockChatRepository):
    """Test clearing a session's history."""
    mock_chat_repo.save_message(ChatMessage(session_id="session3", role="user", message="A message", id=None))
    
    deleted_count = chat_service.clear_session_history("session3")
    assert deleted_count == 1
    
    history = mock_chat_repo.get_session_history("session3")
    assert len(history) == 0
