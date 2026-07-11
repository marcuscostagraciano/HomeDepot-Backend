from abc import ABC, abstractmethod
from typing import Generic, Tuple, Type

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.enums import SortFieldEnum, SortOrderEnum

from ..domain.types import CreatorIdT, DomainCreateSchemaT, DomainSchemaT, RecordIdT
from .types import ORMModelT, SortFieldMapping


class SQLAlchemyRepository(
    ABC,
    Generic[
        DomainCreateSchemaT,
        DomainSchemaT,
        ORMModelT,
        RecordIdT,
        CreatorIdT,
    ],
):
    SORT_FIELDS: SortFieldMapping = {}

    def __init__(
        self,
        session: AsyncSession,
        model: Type[DomainSchemaT],
        orm_model: Type[ORMModelT],
    ) -> None:
        self.session = session
        self.model = model
        self.orm_model = orm_model

    @abstractmethod
    def _to_orm(self, entity: DomainCreateSchemaT) -> ORMModelT:
        """Converts from the `domain` to the `model`. `Domain` > `Adapter`.

        Args:
            entity (DomainCreateSchemaT): `Domain` implementation of the resource.

        Returns:
            ORMModelT: `Adapter` implementation  of the resource.
        """
        ...

    @abstractmethod
    def _to_entity(self, model: ORMModelT) -> DomainSchemaT:
        """Converts from the `model` to the domain``. `Adapter` > `Domain`.

        Args:
            model (ORMModelT): `Adapter` implementation  of the resource.

        Returns:
            DomainSchemaT: `Domain` implementation of the resource.
        """
        ...

    async def create(
        self,
        payload: DomainCreateSchemaT,
        creator_id: CreatorIdT | None = None,
    ) -> DomainSchemaT:
        if creator_id is not None:
            payload = payload.copy(update={"created_by_id": creator_id})

        orm = self._to_orm(payload)

        self.session.add(orm)
        await self.session.commit()
        await self.session.refresh(orm)

        return self._to_entity(orm)

    async def read(
        self,
        id: RecordIdT,
    ) -> DomainSchemaT | None:
        orm = await self.session.get(self.orm_model, id)

        if orm is None:
            return None

        return self._to_entity(orm)

    async def delete(self, id: RecordIdT) -> DomainSchemaT | None:
        orm = await self.session.get(self.orm_model, id)

        if orm is None:
            return None

        await self.session.delete(orm)
        await self.session.commit()

        return self._to_entity(orm)

    async def _execute(self, query: Select[Tuple[ORMModelT]]) -> list[ORMModelT]:
        result = await self.session.execute(query)

        return [obj for obj in result.scalars().all()]

    def _apply_sort(
        self,
        query: Select[Tuple[ORMModelT]],
        sort: SortFieldEnum,
        order: SortOrderEnum,
    ) -> Select[Tuple[ORMModelT]]:
        column = self.SORT_FIELDS[sort]

        if order is SortOrderEnum.DESC:
            return query.order_by(column.desc())

        return query.order_by(column.asc())

    def _apply_pagination(
        self,
        query: Select[Tuple[ORMModelT]],
        page: int,
        limit: int,
    ) -> Select[Tuple[ORMModelT]]:
        return query.offset((page - 1) * limit).limit(limit)
