from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.adapters.sqlalchemy_repository import SQLAlchemyRepository

from ...domain.types import AssociationIdVO
from ..domain.ports import ListShareRepositoryPort
from ..domain.schemas import UserListCreate, UserListRead
from ..models.list_share import ListShare as ListShareModel


class ListShareRepository(
    SQLAlchemyRepository[
        UserListCreate,
        UserListRead,
        ListShareModel,
        AssociationIdVO,
        None,
    ],
    ListShareRepositoryPort,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=UserListRead, orm_model=ListShareModel)

    async def read(
        self,
        id: AssociationIdVO,
    ) -> UserListRead | None:
        orm = await self._find_share(id)
        return self._to_entity(orm) if orm else None

    async def read_by_user_and_list(
        self,
        user_id: UUID,
        list_id: UUID,
    ) -> UserListRead | None:
        query = select(ListShareModel).where(
            ListShareModel.user_id == user_id,
            ListShareModel.list_id == list_id,
        )
        result = await self.session.execute(query)
        orm = result.scalar_one_or_none()

        return self._to_entity(orm) if orm else None

    async def read_all_by_user(self, user_id: UUID) -> list[UserListRead]:
        query = select(ListShareModel).where(ListShareModel.user_id == user_id)
        result = await self.session.execute(query)

        return [self._to_entity(obj) for obj in result.scalars().all()]

    async def delete(
        self,
        id: AssociationIdVO,
    ) -> UserListRead | None:
        orm = await self._find_share(id)
        if orm is None:
            return None

        await self.session.delete(orm)
        await self.session.commit()

        return self._to_entity(orm)

    def _build_share_query(self, id: AssociationIdVO):
        user_id, list_id = id

        return select(ListShareModel).where(
            ListShareModel.user_id == user_id,
            ListShareModel.list_id == list_id,
        )

    async def _find_share(
        self,
        id: AssociationIdVO,
    ) -> ListShareModel | None:
        result = await self.session.execute(self._build_share_query(id))
        return result.scalar_one_or_none()

    def _to_orm(self, entity: UserListCreate) -> ListShareModel:
        return ListShareModel(**entity.to_dict())

    def _to_entity(self, model: ListShareModel) -> UserListRead:
        return UserListRead.from_dict(model.to_dict())
