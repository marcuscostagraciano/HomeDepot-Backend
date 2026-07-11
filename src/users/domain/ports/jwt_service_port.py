from typing import Any, Dict, Protocol

from ..schemas import TokenSchema


class JWTServicePort(Protocol):
    def generate(self, payload: Dict[str, Any]) -> TokenSchema: ...

    def decode(self, token: str) -> Dict[str, Any]: ...
