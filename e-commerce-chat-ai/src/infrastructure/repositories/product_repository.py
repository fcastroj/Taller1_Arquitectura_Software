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
        self.db = db

    def _model_to_entity(self, model: ProductModel) -> Product:
        """Convierte un modelo SQLAlchemy a una entidad de dominio."""
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
        Convierte una entidad de dominio a un modelo SQLAlchemy.
        Si el producto ya tiene un ID, busca el modelo existente para actualizarlo.
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
        models = self.db.query(ProductModel).all()
        return [self._model_to_entity(m) for m in models]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        return self._model_to_entity(model) if model else None

    def get_by_brand(self, brand: str) -> List[Product]:
        models = self.db.query(ProductModel).filter(ProductModel.brand == brand).all()
        return [self._model_to_entity(m) for m in models]

    def get_by_category(self, category: str) -> List[Product]:
        models = self.db.query(ProductModel).filter(ProductModel.category == category).all()
        return [self._model_to_entity(m) for m in models]

    def save(self, product: Product) -> Product:
        model = self._entity_to_model(product)
        if not model.id: # Si es un producto nuevo, lo añade a la sesión
            self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def delete(self, product_id: int) -> bool:
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return True
        return False
