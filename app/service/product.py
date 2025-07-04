from app.models.product import Product
from app.schema.product import ProductCreate, ProductUpdate
from app.service.base import Service


class ProductService(Service[Product, ProductCreate, ProductUpdate]):
    def __init__(self):
        super().__init__(Product)


productService = ProductService()

__all__ = ["productService"]
