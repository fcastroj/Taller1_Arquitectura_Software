"""
Este módulo contiene la función para cargar datos iniciales en la base de datos.
Es útil para poblar la base de datos con información de ejemplo al inicio de la aplicación.
"""

from sqlalchemy.orm import Session
from .models import ProductModel

def load_initial_data(db: Session):
    """
    Carga datos iniciales de productos en la base de datos si la tabla está vacía.

    Args:
        db (Session): La sesión de la base de datos para realizar la operación.
    """
    # Verificar si ya hay productos en la base de datos
    if db.query(ProductModel).count() == 0:
        print("Base de datos vacía, cargando datos iniciales de productos...")
        
        initial_products = [
            ProductModel(name="Air Zoom Pegasus 40", brand="Nike", category="Running", size="42", color="Negro", price=129.99, stock=15, description="Zapatillas de running neutras para entrenamiento diario."),
            ProductModel(name="Ultraboost Light", brand="Adidas", category="Running", size="41", color="Blanco", price=189.95, stock=10, description="Amortiguación BOOST para un retorno de energía increíble."),
            ProductModel(name="Suede Classic XXI", brand="Puma", category="Casual", size="43", color="Rojo", price=75.00, stock=25, description="Un clásico atemporal con exterior de ante de primera calidad."),
            ProductModel(name="GEL-Kayano 30", brand="ASICS", category="Running", size="42.5", color="Azul", price=160.00, stock=8, description="Máxima estabilidad y comodidad para corredores pronadores."),
            ProductModel(name="Chuck Taylor All Star", brand="Converse", category="Casual", size="40", color="Negro", price=60.00, stock=30, description="El icónico modelo de lona que nunca pasa de moda."),
            ProductModel(name="Club C 85", brand="Reebok", category="Casual", size="44", color="Blanco", price=85.00, stock=18, description="Estilo retro de tenis con una parte superior de cuero suave."),
            ProductModel(name="Clifton 9", brand="Hoka", category="Running", size="43", color="Naranja", price=145.00, stock=12, description="Amortiguación y ligereza para tus carreras diarias."),
            ProductModel(name="574 Core", brand="New Balance", category="Casual", size="41.5", color="Gris", price=90.00, stock=22, description="Silueta clásica con amortiguación ENCAP en la mediasuela."),
            ProductModel(name="Oxford Impermeable", brand="Timberland", category="Formal", size="44", color="Marrón", price=130.00, stock=7, description="Elegancia y protección contra el agua para un look formal."),
            ProductModel(name="Vaporfly 3", brand="Nike", category="Running", size="42", color="Verde", price=250.00, stock=5, description="Diseñadas para la competición, con placa de fibra de carbono para máxima propulsión.")
        ]
        
        db.add_all(initial_products)
        db.commit()
        print(f"{len(initial_products)} productos cargados en la base de datos.")
    else:
        print("La base de datos ya contiene datos. No se cargaron datos iniciales.")
