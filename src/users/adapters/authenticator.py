from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_async_session

from ..domain.ports import AuthenticatorPort, PasswordHasherPort, UserRepositoryPort
from ..domain.schemas import UserRead
from ..repositories.user_repository import UserRepository
from .password_hasher import get_password_hasher


class Authenticator(AuthenticatorPort):
    def __init__(
        self,
        repository: UserRepositoryPort,
        password_hasher: PasswordHasherPort,
    ) -> None:
        self.repository = repository
        self.password_hasher = password_hasher

    async def authenticate(self, email: str, password: str) -> UserRead | None:
        user = await self.repository.get_user_by_email(email)

        if not user or not self.password_hasher.verify(password, user.password):
            return None

        return user


def get_authenticator(
    session: AsyncSession = Depends(get_async_session),
    password_hasher: PasswordHasherPort = Depends(get_password_hasher),
) -> AuthenticatorPort:
    return Authenticator(
        repository=UserRepository(session),
        password_hasher=password_hasher,
    )
