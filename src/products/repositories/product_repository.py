from typing import Tuple
from uuid import UUID

from sqlalchemy import Select, and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import BinaryExpression, ColumnElement

from core.domain.enums import SortFieldEnum
from db.adapters.sqlalchemy_repository import SQLAlchemyRepository
from db.adapters.types import SortFieldMapping

from ..domain.filters import ProductFilters
from ..domain.ports import ProductRepositoryPort
from ..domain.schemas import ProductCreate, ProductRead
from ..models.product import Product as ProductModel

type Query = Select[Tuple[ProductModel]]


class ProductRepository(
    SQLAlchemyRepository[
        ProductCreate,
        ProductRead,
        ProductModel,
        UUID,
        UUID,
    ],
    ProductRepositoryPort,
):
    SORT_FIELDS: SortFieldMapping = {
        SortFieldEnum.ID: ProductModel.id,
        SortFieldEnum.CREATED_DATE: ProductModel.created_date,
        SortFieldEnum.UPDATED_DATE: ProductModel.updated_date,
    }

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=ProductRead, orm_model=ProductModel)

    async def read_all(self, filters: ProductFilters) -> list[ProductRead]:
        query: Query = select(ProductModel)

        query = self._apply_filters(query, filters)
        query = self._apply_sort(query, filters.sort, filters.order)
        query = self._apply_pagination(query, filters.page, filters.limit)

        query_result: list[ProductModel] = await self._execute(query)
        return [self._to_entity(r) for r in query_result]

    def _apply_filters(self, query: Query, filters: ProductFilters) -> Query:
        conditions: list[BinaryExpression[bool] | ColumnElement[bool]] = []

        if filters.name:
            conditions.append(ProductModel.name.ilike(f"%{filters.name}%"))

        if filters.brand:
            conditions.append(ProductModel.brand == filters.brand)

        if conditions:
            query = query.where(and_(*conditions))

        return query

    def _to_orm(self, entity: ProductCreate) -> ProductModel:
        return ProductModel(**entity.to_dict())

    def _to_entity(self, model: ProductModel) -> ProductRead:
        return ProductRead.from_dict(model.to_dict())
