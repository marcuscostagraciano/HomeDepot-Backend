from typing import Tuple
from uuid import UUID

from sqlalchemy import Select, and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import BinaryExpression, ColumnElement

from core.domain.enums import SortFieldEnum
from db.adapters.sqlalchemy_repository import SQLAlchemyRepository
from db.adapters.types import SortFieldMapping
from shared.list_shares.models.list_share import ListShare as ListShareModel

from ..domain.filters import ListFilters
from ..domain.ports import ListRepositoryPort
from ..domain.schemas import List, ListCreate, ListRead
from ..models.list import List as ListModel

type Query = Select[Tuple[ListModel]]


class ListRepository(
    SQLAlchemyRepository[
        ListCreate,
        ListRead,
        ListModel,
        UUID,
        UUID,
    ],
    ListRepositoryPort,
):
    SORT_FIELDS: SortFieldMapping = {
        SortFieldEnum.ID: ListModel.id,
        SortFieldEnum.CREATED_DATE: ListModel.created_date,
        SortFieldEnum.UPDATED_DATE: ListModel.updated_date,
    }

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=ListRead, orm_model=ListModel)

    async def create(
        self,
        payload: ListCreate,
    ) -> ListRead:
        db_obj = self._to_orm(payload)

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)

        return self._to_entity(db_obj)

    async def read_all(
        self,
        filters: ListFilters,
    ) -> list[List]:
        query: Query = select(ListModel)

        query = self._apply_filters(query, filters)
        query = self._apply_sort(query, filters.sort, filters.order)
        query = self._apply_pagination(query, filters.page, filters.limit)

        return await self._execute(query)

    async def read_all_accessible(
        self,
        filters: ListFilters,
        user_id: UUID,
    ) -> list[List]:
        query: Query = select(ListModel)

        accessible_ids = select(ListShareModel.list_id).where(
            ListShareModel.user_id == user_id
        )

        query = query.where(
            or_(
                ListModel.created_by_id == user_id,
                ListModel.id.in_(accessible_ids),
            )
        )

        query = self._apply_filters(query, filters)
        query = self._apply_sort(query, filters.sort, filters.order)
        query = self._apply_pagination(query, filters.page, filters.limit)

        return await self._execute(query)

    def _apply_filters(
        self,
        query: Query,
        filters: ListFilters,
    ) -> Query:
        conditions: list[BinaryExpression[bool] | ColumnElement[bool]] = []

        if filters.name:
            conditions.append(ListModel.name.ilike(f"%{filters.name}%"))

        if filters.observation:
            conditions.append(ListModel.observation.ilike(f"%{filters.observation}%"))

        if filters.bought is not None:
            conditions.append(ListModel.bought == filters.bought)

        if conditions:
            query = query.where(and_(*conditions))

        return query

    def _to_orm(self, entity: ListCreate) -> ListModel:
        return ListModel(**entity.to_dict())

    def _to_entity(self, model: ListModel) -> ListRead:
        return ListRead.from_dict(model.to_dict())
