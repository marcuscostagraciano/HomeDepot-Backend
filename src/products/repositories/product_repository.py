from sqlalchemy.ext.asyncio import AsyncSession

from db.adapters.sqlalchemy_repository import SQLAlchemyRepository
from products.domain.ports import ProductRepositoryPort
from products.models import Product
from products.schemas.product import ProductCreate, ProductRead


class ProductRepository(
    SQLAlchemyRepository[ProductCreate, Product, ProductRead],
    ProductRepositoryPort,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=Product, schema=ProductRead)
