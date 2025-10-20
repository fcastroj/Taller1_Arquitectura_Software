from typing import List, Optional, Dict, Any
from src.domain.entities import Product
from src.domain.repositories import IProductRepository
from src.domain.exceptions import ProductNotFoundError, InvalidProductDataError
from src.application.dtos import ProductDTO

class ProductService:
    """
    Servicio de aplicación para gestionar la lógica de negocio de los productos.
    Orquesta las operaciones utilizando el repositorio de productos.
    """
    def __init__(self, product_repository: IProductRepository):
        """
        Inicializa el servicio de productos.

        Args:
            product_repository (IProductRepository): El repositorio de productos
                que se utilizará para acceder a los datos.
        """
        self.product_repository = product_repository

    def get_all_products(self) -> List[ProductDTO]:
        """
        Obtiene todos los productos y los convierte a DTOs.

        Returns:
            List[ProductDTO]: Una lista de todos los productos.
        """
        products = self.product_repository.get_all()
        return [ProductDTO.from_attributes(p) for p in products]

    def get_available_products(self) -> List[ProductDTO]:
        """
        Obtiene todos los productos con stock disponible.

        Returns:
            List[ProductDTO]: Una lista de productos disponibles.
        """
        all_products = self.product_repository.get_all()
        available_products = [p for p in all_products if p.is_available()]
        return [ProductDTO.from_attributes(p) for p in available_products]

    def get_product_by_id(self, product_id: int) -> Optional[ProductDTO]:
        """
        Busca un producto por su ID.

        Args:
            product_id (int): El ID del producto a buscar.

        Returns:
            Optional[ProductDTO]: El DTO del producto si se encuentra.

        Raises:
            ProductNotFoundError: Si no se encuentra ningún producto con ese ID.
        """
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id=product_id)
        return ProductDTO.from_attributes(product)

    def create_product(self, product_dto: ProductDTO) -> ProductDTO:
        """
        Crea un nuevo producto.

        Args:
            product_dto (ProductDTO): El DTO con los datos del nuevo producto.

        Returns:
            ProductDTO: El DTO del producto recién creado.
        
        Raises:
            InvalidProductDataError: Si los datos del producto son inválidos.
        """
        try:
            # El ID debe ser None para la creación
            product_dto.id = None
            product_entity = Product(**product_dto.model_dump())
            
            saved_product = self.product_repository.save(product_entity)
            return ProductDTO.from_attributes(saved_product)
        except ValueError as e:
            raise InvalidProductDataError(str(e))

    def update_product(self, product_id: int, product_dto: ProductDTO) -> ProductDTO:
        """
        Actualiza un producto existente.

        Args:
            product_id (int): El ID del producto a actualizar.
            product_dto (ProductDTO): El DTO con los nuevos datos del producto.

        Returns:
            ProductDTO: El DTO del producto actualizado.

        Raises:
            ProductNotFoundError: Si el producto a actualizar no existe.
            InvalidProductDataError: Si los datos del producto son inválidos.
        """
        existing_product = self.product_repository.get_by_id(product_id)
        if not existing_product:
            raise ProductNotFoundError(product_id=product_id)
        
        try:
            # Actualizamos la entidad existente con los datos del DTO
            update_data = product_dto.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(existing_product, key, value)
            
            # Re-validamos la entidad actualizada
            existing_product.__post_init__()

            updated_product = self.product_repository.save(existing_product)
            return ProductDTO.from_attributes(updated_product)
        except ValueError as e:
            raise InvalidProductDataError(str(e))

    def delete_product(self, product_id: int) -> bool:
        """
        Elimina un producto.

        Args:
            product_id (int): El ID del producto a eliminar.

        Returns:
            bool: True si el producto fue eliminado.

        Raises:
            ProductNotFoundError: Si el producto a eliminar no existe.
        """
        product_to_delete = self.product_repository.get_by_id(product_id)
        if not product_to_delete:
            raise ProductNotFoundError(product_id=product_id)
        
        return self.product_repository.delete(product_id)

    def search_products(self, filters: Dict[str, Any]) -> List[ProductDTO]:
        """
        Busca productos basados en un diccionario de filtros.

        Args:
            filters (Dict[str, Any]): Un diccionario con los filtros a aplicar.
                Ej: {'brand': 'Nike', 'category': 'Running'}

        Returns:
            List[ProductDTO]: Una lista de productos que coinciden con los filtros.
        """
        # Esta es una implementación simple. Una real podría ser más compleja.
        products = self.product_repository.get_all()
        
        if "brand" in filters:
            products = [p for p in products if p.brand.lower() == filters["brand"].lower()]
        
        if "category" in filters:
            products = [p for p in products if p.category.lower() == filters["category"].lower()]
            
        return [ProductDTO.from_attributes(p) for p in products]
