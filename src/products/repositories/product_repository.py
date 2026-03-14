from sqlalchemy.ext.asyncio import AsyncSession

from db.adapters.sqlalchemy_repository import SQLAlchemyRepository
from products.domain.ports import ProductRepositoryPort
from products.models import Product


class ProductRepository(
    SQLAlchemyRepository,
    ProductRepositoryPort,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=Product)
