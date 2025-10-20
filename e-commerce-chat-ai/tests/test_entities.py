
import pytest
from datetime import datetime
from src.domain.entities import Product, ChatMessage, ChatContext

# Pruebas para la entidad Product

def test_product_creation():
    """Prueba la creación exitosa de un producto."""
    product = Product(id=1, name="Zapatos Nike", brand="Nike", category="Running", size="42", color="Negro", price=120.0, stock=10, description="Zapatos para correr.")
    assert product.name == "Zapatos Nike"
    assert product.price == 120.0
    assert product.stock == 10

def test_product_invalid_price():
    """Prueba que el precio no puede ser cero o negativo."""
    with pytest.raises(ValueError, match="El precio debe ser mayor a 0."):
        Product(id=1, name="Zapatos Nike", brand="Nike", category="Running", size="42", color="Negro", price=0, stock=10, description="Zapatos para correr.")
    with pytest.raises(ValueError, match="El precio debe ser mayor a 0."):
        Product(id=1, name="Zapatos Nike", brand="Nike", category="Running", size="42", color="Negro", price=-10, stock=10, description="Zapatos para correr.")

def test_product_invalid_stock():
    """Prueba que el stock no puede ser negativo."""
    with pytest.raises(ValueError, match="El stock no puede ser negativo."):
        Product(id=1, name="Zapatos Nike", brand="Nike", category="Running", size="42", color="Negro", price=120.0, stock=-1, description="Zapatos para correr.")

def test_product_empty_name():
    """Prueba que el nombre del producto no puede estar vacío."""
    with pytest.raises(ValueError, match="El nombre no puede estar vacío."):
        Product(id=1, name="", brand="Nike", category="Running", size="42", color="Negro", price=120.0, stock=10, description="Zapatos para correr.")

def test_product_is_available():
    """Prueba la lógica de disponibilidad de stock."""
    product = Product(id=1, name="Zapatos Nike", brand="Nike", category="Running", size="42", color="Negro", price=120.0, stock=1, description="Zapatos para correr.")
    assert product.is_available()
    product.stock = 0
    assert not product.is_available()

def test_product_reduce_stock():
    """Prueba la reducción de stock."""
    product = Product(id=1, name="Zapatos Nike", brand="Nike", category="Running", size="42", color="Negro", price=120.0, stock=10, description="Zapatos para correr.")
    product.reduce_stock(3)
    assert product.stock == 7

def test_product_reduce_stock_insufficient():
    """Prueba que no se puede reducir más stock del disponible."""
    product = Product(id=1, name="Zapatos Nike", brand="Nike", category="Running", size="42", color="Negro", price=120.0, stock=5, description="Zapatos para correr.")
    with pytest.raises(ValueError, match="Stock insuficiente para reducir en 6 unidades."):
        product.reduce_stock(6)

def test_product_reduce_stock_negative_quantity():
    """Prueba que no se puede reducir el stock en una cantidad negativa."""
    product = Product(id=1, name="Zapatos Nike", brand="Nike", category="Running", size="42", color="Negro", price=120.0, stock=10, description="Zapatos para correr.")
    with pytest.raises(ValueError, match="La cantidad a reducir debe ser positiva."):
        product.reduce_stock(-2)

def test_product_increase_stock():
    """Prueba el aumento de stock."""
    product = Product(id=1, name="Zapatos Nike", brand="Nike", category="Running", size="42", color="Negro", price=120.0, stock=10, description="Zapatos para correr.")
    product.increase_stock(5)
    assert product.stock == 15

def test_product_increase_stock_negative_quantity():
    """Prueba que no se puede aumentar el stock en una cantidad negativa."""
    product = Product(id=1, name="Zapatos Nike", brand="Nike", category="Running", size="42", color="Negro", price=120.0, stock=10, description="Zapatos para correr.")
    with pytest.raises(ValueError, match="La cantidad a aumentar debe ser positiva."):
        product.increase_stock(-5)

# Pruebas para la entidad ChatMessage

def test_chat_message_creation():
    """Prueba la creación exitosa de un mensaje de chat."""
    now = datetime.now()
    message = ChatMessage(id=1, session_id="session123", role="user", message="Hola", timestamp=now)
    assert message.session_id == "session123"
    assert message.role == "user"
    assert message.message == "Hola"
    assert message.timestamp == now

def test_chat_message_invalid_role():
    """Prueba que el rol debe ser 'user' o 'assistant'."""
    with pytest.raises(ValueError, match="El rol debe ser 'user' o 'assistant'."):
        ChatMessage(id=1, session_id="session123", role="admin", message="Hola", timestamp=datetime.now())

def test_chat_message_empty_message():
    """Prueba que el mensaje no puede estar vacío."""
    with pytest.raises(ValueError, match="El mensaje no puede estar vacío."):
        ChatMessage(id=1, session_id="session123", role="user", message="", timestamp=datetime.now())

def test_chat_message_empty_session_id():
    """Prueba que el session_id no puede estar vacío."""
    with pytest.raises(ValueError, match="El session_id no puede estar vacío."):
        ChatMessage(id=1, session_id="", role="user", message="Hola", timestamp=datetime.now())

def test_chat_message_is_from_user():
    """Prueba la verificación de si el mensaje es del usuario."""
    message = ChatMessage(id=1, session_id="session123", role="user", message="Hola", timestamp=datetime.now())
    assert message.is_from_user()
    assert not message.is_from_assistant()

def test_chat_message_is_from_assistant():
    """Prueba la verificación de si el mensaje es del asistente."""
    message = ChatMessage(id=1, session_id="session123", role="assistant", message="Hola", timestamp=datetime.now())
    assert message.is_from_assistant()
    assert not message.is_from_user()

# Pruebas para el Value Object ChatContext

def test_chat_context_get_recent_messages():
    """Prueba que se obtienen los N mensajes más recientes."""
    messages = [
        ChatMessage(id=i, session_id="s1", role="user", message=f"Msg {i}", timestamp=datetime.now())
        for i in range(10)
    ]
    context = ChatContext(messages=messages, max_messages=5)
    recent = context.get_recent_messages()
    assert len(recent) == 5
    assert recent[0].id == 5
    assert recent[-1].id == 9

def test_chat_context_format_for_prompt():
    """Prueba el formato del historial para el prompt de la IA."""
    now = datetime.now()
    messages = [
        ChatMessage(id=1, session_id="s1", role="user", message="Hola, busco zapatos.", timestamp=now),
        ChatMessage(id=2, session_id="s1", role="assistant", message="¡Hola! ¿Qué tipo de zapatos buscas?", timestamp=now),
        ChatMessage(id=3, session_id="s1", role="user", message="Para correr.", timestamp=now),
    ]
    context = ChatContext(messages=messages)
    prompt = context.format_for_prompt()
    expected_prompt = (
        "Usuario: Hola, busco zapatos.\n"
        "Asistente: ¡Hola! ¿Qué tipo de zapatos buscas?\n"
        "Usuario: Para correr."
    )
    assert prompt == expected_prompt

def test_chat_context_format_for_prompt_empty():
    """Prueba el formato con un historial vacío."""
    context = ChatContext(messages=[])
    prompt = context.format_for_prompt()
    assert prompt == ""
