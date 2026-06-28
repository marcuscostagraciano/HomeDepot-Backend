from typing import Generic, Type

from sqlalchemy.ext.asyncio import AsyncSession

from core.domain import SortField, SortFieldMapping, SortOrder

from ..domain import CreateSchema, Model, QuerySelect, RecordIdT, ReturnSchema


class SQLAlchemyRepository(Generic[CreateSchema, Model, ReturnSchema, RecordIdT]):
    SORT_FIELDS: SortFieldMapping = {}

    def __init__(
        self,
        session: AsyncSession,
        model: Type[Model],
        schema: Type[ReturnSchema],
    ) -> None:
        self.session = session
        self.model = model
        self.schema = schema

    async def create(self, payload: CreateSchema) -> ReturnSchema:
        db_obj = self.model(**payload.model_dump())

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)

        return self.schema.model_validate(db_obj)

    async def read(self, id: RecordIdT) -> ReturnSchema | None:
        db_obj = await self.session.get(self.model, id)

        if db_obj is None:
            return None

        return self.schema.model_validate(db_obj)

    async def delete(self, id: RecordIdT) -> ReturnSchema | None:
        obj = await self.session.get(self.model, id)

        if obj is None:
            return None

        await self.session.delete(obj)
        await self.session.commit()

        return self.schema.model_validate(obj)

    async def execute(self, query: QuerySelect[Model]) -> list[ReturnSchema]:
        result = await self.session.execute(query)

        return [self.schema.model_validate(obj) for obj in result.scalars().all()]

    def apply_sort(
        self,
        query: QuerySelect[Model],
        sort: SortField,
        order: SortOrder,
    ) -> QuerySelect[Model]:
        column = self.SORT_FIELDS[sort]

        if order is SortOrder.DESC:
            return query.order_by(column.desc())

        return query.order_by(column.asc())

    def apply_pagination(
        self,
        query: QuerySelect[Model],
        page: int,
        limit: int,
    ) -> QuerySelect[Model]:
        return query.offset((page - 1) * limit).limit(limit)
