from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.entities import Product
from src.domain.repositories import IProductRepository
from src.infrastructure.db.models import ProductModel

class SQLProductRepository(IProductRepository):
    """
    Implementación del repositorio de productos utilizando SQLAlchemy con una base de datos SQL.
    """
    def __init__(self, db: Session):
        """
        Inicializa el repositorio de productos con una sesión de base de datos.

        Args:
            db (Session): La sesión de SQLAlchemy para interactuar con la base de datos.
        """
        self.db = db

    def _model_to_entity(self, model: ProductModel) -> Product:
        """
        Convierte un objeto `ProductModel` de SQLAlchemy a una entidad de dominio `Product`.

        Args:
            model (ProductModel): El modelo de base de datos a convertir.

        Returns:
            Product: La entidad de dominio `Product` resultante.
        """
        return Product(
            id=model.id,
            name=model.name,
            brand=model.brand,
            category=model.category,
            size=model.size,
            color=model.color,
            price=model.price,
            stock=model.stock,
            description=model.description
        )

    def _entity_to_model(self, entity: Product) -> ProductModel:
        """
        Convierte una entidad de dominio `Product` a un objeto `ProductModel` de SQLAlchemy.
        Si la entidad tiene un ID, intenta actualizar un modelo existente; de lo contrario, crea uno nuevo.

        Args:
            entity (Product): La entidad de dominio a convertir.

        Returns:
            ProductModel: El modelo de base de datos `ProductModel` resultante.
        """
        if entity.id:
            model = self.db.query(ProductModel).filter(ProductModel.id == entity.id).first()
            if model:
                # Actualiza el modelo existente
                model.name = entity.name
                model.brand = entity.brand
                model.category = entity.category
                model.size = entity.size
                model.color = entity.color
                model.price = entity.price
                model.stock = entity.stock
                model.description = entity.description
                return model
        
        # Crea un nuevo modelo si no tiene ID o no se encontró uno existente
        return ProductModel(
            id=entity.id,
            name=entity.name,
            brand=entity.brand,
            category=entity.category,
            size=entity.size,
            color=entity.color,
            price=entity.price,
            stock=entity.stock,
            description=entity.description
        )

    def get_all(self) -> List[Product]:
        """
        Recupera todos los productos de la base de datos.

        Returns:
            List[Product]: Una lista de todas las entidades `Product`.
        """
        models = self.db.query(ProductModel).all()
        return [self._model_to_entity(m) for m in models]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Busca un producto por su identificador único.

        Args:
            product_id (int): El ID del producto a buscar.

        Returns:
            Optional[Product]: La entidad `Product` si se encuentra, de lo contrario None.
        """
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        return self._model_to_entity(model) if model else None

    def get_by_brand(self, brand: str) -> List[Product]:
        """
        Busca productos por su marca.

        Args:
            brand (str): La marca de los productos a buscar.

        Returns:
            List[Product]: Una lista de entidades `Product` que coinciden con la marca.
        """
        models = self.db.query(ProductModel).filter(ProductModel.brand == brand).all()
        return [self._model_to_entity(m) for m in models]

    def get_by_category(self, category: str) -> List[Product]:
        """
        Busca productos por su categoría.

        Args:
            category (str): La categoría de los productos a buscar.

        Returns:
            List[Product]: Una lista de entidades `Product` que coinciden con la categoría.
        """
        models = self.db.query(ProductModel).filter(ProductModel.category == category).all()
        return [self._model_to_entity(m) for m in models]

    def save(self, product: Product) -> Product:
        """
        Guarda un producto en la base de datos. Si el producto tiene un ID, intenta actualizarlo;
        de lo contrario, lo inserta como un nuevo producto.

        Args:
            product (Product): La entidad `Product` a guardar.

        Returns:
            Product: La entidad `Product` guardada, con su ID actualizado si fue una inserción.
        """
        model = self._entity_to_model(product)
        if not model.id: # Si es un producto nuevo, lo añade a la sesión
            self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto de la base de datos por su ID.

        Args:
            product_id (int): El ID del producto a eliminar.

        Returns:
            bool: True si el producto fue eliminado exitosamente, False si no se encontró.
        """
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return True
        return False
