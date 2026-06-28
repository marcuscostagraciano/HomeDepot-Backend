from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class Settings:
    """
    Central configuration for the application.
    This is the ONLY place that reads environment variables.
    """

    # Enviroment
    DEBUG: bool = getenv("DEBUG", "false") == "true"
    """Check if the application is running in debug mode. Defaults to False."""

    # JWT
    JWT_SECRET: str = getenv("JWT_SECRET", "test-secret")
    """Secret key used for signing JWT tokens"""
    JWT_ALGORITHM: str = getenv("JWT_ALGORITHM", "HS256")
    """Algorithm used for signing JWT tokens. Defaults to HS256."""

    # Token
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "5"))
    """Expiration time for access tokens in minutes. Defaults to 5 minutes."""

    # Database
    DATABASE_URL: str = getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    """Database connection URL. Defaults to a local SQLite database."""
