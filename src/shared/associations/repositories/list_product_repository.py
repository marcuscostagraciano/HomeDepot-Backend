from typing import Tuple
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.adapters.sqlalchemy_repository import SQLAlchemyRepository

from ..domain.ports import ListProductRepositoryPort
from ..domain.schemas import ListProductCreate, ListProductRead, ListProductUpdate
from ..models.list_product import ListProduct as ListProductModel


class ListProductRepository(
    SQLAlchemyRepository[
        ListProductCreate,
        ListProductRead,
        ListProductModel,
        Tuple[UUID, UUID],
    ],
    ListProductRepositoryPort,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            session=session, model=ListProductRead, orm_model=ListProductModel
        )

    async def read(
        self,
        id: Tuple[UUID, UUID],
    ) -> ListProductRead | None:
        list_id, product_id = id
        query = select(ListProductModel).where(
            ListProductModel.list_id == list_id,
            ListProductModel.product_id == product_id,
        )

        result = await self.session.execute(query)
        orm = result.scalar_one_or_none()

        if orm is None:
            return None

        return self._to_entity(orm)

    async def read_all_by_list(self, list_id: UUID) -> list[ListProductRead]:
        query = select(ListProductModel).where(ListProductModel.list_id == list_id)
        result = await self.session.execute(query)

        return [self._to_entity(obj) for obj in result.scalars().all()]

    async def create(self, payload: ListProductCreate) -> ListProductRead:
        db_obj = self._to_orm(payload)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)

        return self._to_entity(db_obj)

    async def update(
        self,
        id: Tuple[UUID, UUID],
        payload: ListProductUpdate,
    ) -> ListProductRead | None:
        list_id, product_id = id
        query = select(ListProductModel).where(
            ListProductModel.list_id == list_id,
            ListProductModel.product_id == product_id,
        )

        result = await self.session.execute(query)
        orm = result.scalar_one_or_none()

        if orm is None:
            return None

        if payload.quantity is not None:
            orm.quantity = payload.quantity
        if payload.bought is not None:
            orm.bought = payload.bought
        if payload.notes is not None:
            orm.notes = payload.notes

        await self.session.commit()
        await self.session.refresh(orm)

        return self._to_entity(orm)

    async def delete(self, id: Tuple[UUID, UUID]) -> ListProductRead | None:
        list_id, product_id = id
        query = select(ListProductModel).where(
            ListProductModel.list_id == list_id,
            ListProductModel.product_id == product_id,
        )

        result = await self.session.execute(query)
        orm = result.scalar_one_or_none()

        if orm is None:
            return None

        await self.session.delete(orm)
        await self.session.commit()

        return self._to_entity(orm)

    def _to_orm(self, entity: ListProductCreate) -> ListProductModel:
        return ListProductModel(**entity.to_dict())

    def _to_entity(self, model: ListProductModel) -> ListProductRead:
        return ListProductRead.from_dict(model.to_dict())
