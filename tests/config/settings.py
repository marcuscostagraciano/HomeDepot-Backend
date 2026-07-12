from dataclasses import dataclass

from src.core.config import Settings as CoreSettings


@dataclass(frozen=True)
class Settings(CoreSettings):
    """Central configuration for the application testing."""

    JWT_SECRET: str = "mocked-jwt-test-secret-0123456789"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
