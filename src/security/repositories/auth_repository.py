from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_async_session
from security.adapters import get_password_hasher
from security.domain import AuthRepositoryPort, PasswordHasherPort
from users.models.user import User
from users.schemas.user import UserRead


class AuthRepository(AuthRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def authenticate(self, email: str, password: str) -> UserRead | None:
        result = await self.session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user or not validate_hash(password, user.password):
            return None

        return UserRead.model_validate(user)


def get_auth_repository(
    session: AsyncSession = Depends(get_async_session),
) -> AuthRepositoryPort:
    return AuthRepository(session)
