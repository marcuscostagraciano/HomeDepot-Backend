from typing import Protocol

from ..schemas import UserRead


class AuthenticatorPort(Protocol):
    async def authenticate(self, email: str, password: str) -> UserRead | None: ...
