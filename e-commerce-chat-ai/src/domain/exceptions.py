"""
Excepciones específicas del dominio.
Representan errores de negocio, no errores técnicos.
"""

class ProductNotFoundError(Exception):
    """Se lanza cuando se busca un producto que no existe."""
    def __init__(self, product_id: int = None):
        """
        Inicializa la excepción `ProductNotFoundError`.

        Args:
            product_id (int, optional): El ID del producto que no se encontró. Por defecto es None.
        """
        if product_id:
            self.message = f"Producto con ID {product_id} no encontrado"
        else:
            self.message = "Producto no encontrado"
        super().__init__(self.message)

class InvalidProductDataError(Exception):
    """Se lanza cuando los datos de un producto son inválidos (ej: precio negativo)."""
    def __init__(self, message: str = "Datos de producto inválidos"):
        """
        Inicializa la excepción `InvalidProductDataError`.

        Args:
            message (str, optional): Mensaje de error detallado. Por defecto es "Datos de producto inválidos".
        """
        self.message = message
        super().__init__(self.message)

class ChatServiceError(Exception):
    """Se lanza cuando hay un error en el servicio de chat, como un fallo en la IA."""
    def __init__(self, message: str = "Error en el servicio de chat"):
        """
        Inicializa la excepción `ChatServiceError`.

        Args:
            message (str, optional): Mensaje de error detallado. Por defecto es "Error en el servicio de chat".
        """
        self.message = message
        super().__init__(self.message)
