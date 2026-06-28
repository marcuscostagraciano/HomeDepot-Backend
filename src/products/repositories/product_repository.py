from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import BinaryExpression, ColumnElement

from core.domain import SortField, SortFieldMapping
from db.adapters.sqlalchemy_repository import SQLAlchemyRepository
from db.domain import QuerySelect

from ..domain import ProductFilters, ProductRepositoryPort
from ..models import Product
from ..schemas import ProductCreate, ProductRead


class ProductRepository(
    SQLAlchemyRepository[ProductCreate, Product, ProductRead],
    ProductRepositoryPort,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=Product, schema=ProductRead)
