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
    SQLAlchemyRepository[ProductCreate, Product, ProductRead, UUID],
    ProductRepositoryPort,
):
    SORT_FIELDS: SortFieldMapping = {
        SortField.ID: Product.id,
        SortField.CREATED_DATE: Product.created_date,
        SortField.UPDATED_DATE: Product.updated_date,
    }

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=Product, schema=ProductRead)

    async def read_all(self, filters: ProductFilters) -> list[ProductRead]:
        query: QuerySelect[Product] = select(Product)

        query = self._apply_filters(query, filters)
        query = self.apply_sort(query, filters.sort, filters.order)
        query = self.apply_pagination(query, filters.page, filters.limit)

        return await self.execute(query)

    def _apply_filters(
        self, query: QuerySelect[Product], filters: ProductFilters
    ) -> QuerySelect[Product]:
        conditions: list[BinaryExpression[bool] | ColumnElement[bool]] = []

        if filters.search:
            conditions.append(Product.name.ilike(f"%{filters.search}%"))

        if filters.brand:
            conditions.append(Product.brand == filters.brand)

        if filters.min_price is not None:
            conditions.append(Product.price >= filters.min_price)

        if filters.max_price is not None:
            conditions.append(Product.price <= filters.max_price)

        if conditions:
            query = query.where(and_(*conditions))

        return query
