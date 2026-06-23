from typing import Protocol
from uuid import UUID

from db.domain import RepositoryPort
from lists.schemas import ListCreate, ListRead


class ListRepositoryPort(
    RepositoryPort[ListCreate, ListRead, UUID],
    Protocol,
):
    """Repository protocol for managing list persistence."""
