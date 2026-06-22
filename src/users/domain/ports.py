from typing import Protocol
from uuid import UUID

from db.domain import RepositoryPort
from users.schemas.user import UserCreate, UserRead


class UserRepositoryPort(
    RepositoryPort[UserCreate, UserRead, UUID],
    Protocol,
):
    """Repository protocol for managing user persistence.

    Defines the interface for CRUD operations on users with generic types
    for flexible data and `id` representation.
    """
