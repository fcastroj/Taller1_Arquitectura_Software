import google.generativeai as genai
from typing import List

from src.application.services import IAIService
from src.config import GEMINI_API_KEY
from src.domain.entities import Product, ChatContext
from src.domain.exceptions import ChatServiceError

class GeminiService(IAIService):
    """
    Implementación del servicio de IA utilizando la API de Google Gemini.
    """
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("La API key de Gemini no está configurada en las variables de entorno.")
        
        genai.configure(api_key=GEMINI_API_KEY)
        # Usamos un modelo moderno y rápido como gemini-1.5-flash
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def _format_products_info(self, products: List[Product]) -> str:
        """Formatea la lista de productos en un string legible para el prompt."""
        if not products:
            return "No hay productos disponibles en este momento."
        
        product_lines = [
            f"- {p.name} (Marca: {p.brand}, Categoría: {p.category}, Talla: {p.size}, Precio: ${p.price:.2f}, Stock: {p.stock})"
            for p in products
        ]
        return "\n".join(product_lines)

    async def generate_response(
        self, user_message: str, products: List[Product], context: ChatContext
    ) -> str:
        """
        Genera una respuesta de la IA construyendo un prompt detallado y llamando a la API de Gemini.
        """
        products_info = self._format_products_info(products)
        conversation_history = context.format_for_prompt()

        system_prompt = f"""
Eres un asistente virtual experto en ventas de zapatos para un e-commerce.
Tu objetivo es ayudar a los clientes a encontrar los zapatos perfectos de una manera amigable y profesional.

INSTRUCCIONES:
- Sé amable, servicial y conversacional.
- Utiliza la información de los productos disponibles para responder a las preguntas de los clientes.
- Si un cliente pregunta por un tipo de zapato, recomienda modelos específicos de la lista.
- Menciona siempre el nombre, la marca, el precio y el stock si es relevante.
- Utiliza el historial de la conversación para entender el contexto y dar respuestas coherentes. No repitas información que ya has dado a menos que te lo pidan.
- Si no sabes la respuesta o un producto no está en la lista, sé honesto y dilo. No inventes productos o características.
- Responde en español.

--- 
AQUÍ ESTÁ LA LISTA DE PRODUCTOS DISPONIBLES EN LA TIENDA:
{products_info}
---

HISTORIAL DE LA CONVERSACIÓN RECIENTE:
{conversation_history}

--- 
MENSAJE ACTUAL DEL USUARIO:
\"{user_message}\"

Asistente:
"""
        
        try:
            response = await self.model.generate_content_async(system_prompt)
            
            # Validación básica de la respuesta
            if not response.parts:
                 return "Lo siento, no pude generar una respuesta en este momento. Por favor, intenta de nuevo."
            return response.text
        except Exception as e:
            # En una aplicación real, aquí se registraría el error detalladamente
            print(f"Error al llamar a la API de Gemini: {e}")
            raise ChatServiceError(f"Hubo un error al comunicarse con el servicio de IA.")