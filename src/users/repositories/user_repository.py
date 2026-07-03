from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import User as UserModel
from db.adapters.sqlalchemy_repository import SQLAlchemyRepository
from db.db import get_async_session

from ..domain.ports import UserRepositoryPort
from ..domain.schemas import UserCreate, UserRead


class UserRepository(
    SQLAlchemyRepository[
        UserCreate,
        UserRead,
        UserModel,
        UUID,
    ],
    UserRepositoryPort,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=UserRead, orm_model=UserModel)

    async def create(self, payload: UserCreate) -> UserRead:
        orm = self._to_orm(payload)

        self.session.add(orm)
        await self.session.commit()
        await self.session.refresh(orm)

        return self._to_entity(orm)

    async def get_user_by_email(self, email: str) -> UserRead | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )

        user_result: UserModel | None = result.scalar_one_or_none()
        return UserRead.from_dict(user_result.to_dict()) if user_result else None

    async def check_email_exists(self, email: str) -> bool:
        return await self.get_user_by_email(email) is not None

    def _to_orm(self, entity: UserCreate) -> UserModel:
        return UserModel(**entity.to_dict())

    def _to_entity(self, model: UserModel) -> UserRead:
        return UserRead.from_dict(model.to_dict())


def get_user_repository(
    session: AsyncSession = Depends(get_async_session),
) -> UserRepositoryPort:
    return UserRepository(session)
