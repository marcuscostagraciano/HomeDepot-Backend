from datetime import datetime, timedelta
from typing import Any, Dict
from zoneinfo import ZoneInfo

from jwt import decode, encode

from core.config.settings import Settings

from ..domain.ports import JWTServicePort
from ..domain.schemas import TokenSchema


class JWTService:
    def __init__(
        self,
        settings: Settings,
    ):
        self.settings = settings

    def generate(
        self,
        payload: Dict[str, Any],
    ) -> TokenSchema:
        return_payload: Dict[str, Any] = payload.copy()
        return_payload.update(
            {
                "exp": datetime.now(tz=ZoneInfo("UTC"))
                + timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            }
        )

        return TokenSchema(
            token_type="Bearer",
            access_token=encode(
                payload=return_payload,
                key=self.settings.JWT_SECRET,
                algorithm=self.settings.JWT_ALGORITHM,
            ),
        )

    def decode(
        self,
        token: str,
    ) -> Dict[str, Any]:
        return decode(
            token,
            self.settings.JWT_SECRET,
            algorithms=[self.settings.JWT_ALGORITHM],
        )


def get_jwt_service() -> JWTServicePort:
    """Get a new instance of JWTService.

    Returns:
        JWTServicePort: New instance of JWTService.
    """
    settings = Settings()

    return JWTService(settings)
