from typing import Protocol

from users.schemas.user import UserRead


class AuthRepositoryPort(Protocol):
    async def authenticate(self, email: str, password: str) -> UserRead | None: ...
