from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.adapters.sqlalchemy_repository import SQLAlchemyRepository
from db.db import get_async_session

from ..domain.ports import UserRepositoryPort
from ..models.user import User
from ..schemas.user import UserCreate, UserRead


class UserRepository(
    SQLAlchemyRepository[UserCreate, User, UserRead],
    UserRepositoryPort,
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=User, schema=UserRead)

    async def get_user_by_email(self, email: str) -> UserRead | None:
        result = await self.session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        return UserRead.model_validate(user) if user else None

    async def check_email_exists(self, email: str) -> bool:
        return await self.get_user_by_email(email) is not None


def get_user_repository(
    session: AsyncSession = Depends(get_async_session),
) -> UserRepositoryPort:
    return UserRepository(session)
