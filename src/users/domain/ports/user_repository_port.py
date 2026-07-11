from typing import Protocol
from uuid import UUID

from db.domain.ports import RepositoryPort

from ..schemas import UserCreate, UserRead


class UserRepositoryPort(
    RepositoryPort[UserCreate, UserRead, UUID, None],
    Protocol,
):
    """Repository protocol for managing user persistence.

    Defines the interface for CRUD operations on users with generic types
    for flexible data and `id` representation.
    """

    async def get_user_by_email(self, email: str) -> UserRead | None:
        """Retrieve a user by their email address.

        Args:
            email (str): The email of the user to retrieve.

        Returns:
            UserRead | None: The user data if found, otherwise None.
        """
        ...

    async def check_email_exists(self, email: str) -> bool:
        """Check if a user with the given email exists.

        Args:
            email (str): The email to check for existence.

        Returns:
            bool: True if a user with the email exists, False otherwise.
        """
        ...
