from typing import Any, Dict, Protocol

from users.schemas.user import UserRead

from ..schemas.token import TokenSchema


class AuthRepositoryPort(Protocol):
    async def authenticate(self, email: str, password: str) -> UserRead | None: ...
