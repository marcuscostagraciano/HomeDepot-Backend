from typing import Protocol, Type

from sqlalchemy.ext.asyncio import AsyncSession

from core.domain import SortField, SortOrder

from .types import CreateSchema, Model, QuerySelect, RecordIdT, ReturnSchema


class RepositoryPort(Protocol[CreateSchema, Model, ReturnSchema, RecordIdT]):
    """Repository protocol for managing record persistence.

    Defines the interface for CRUD operations on records with generic types
    for flexible data and ID representation.

    Type Parameters:
        RecordT: The record data type
        RecordIdT: The record ID type
        ReturnRecordT: The type of the record returned by create and update operations
    """

    def __init__(
        self, session: AsyncSession, model: Type[Model], schema: Type[ReturnSchema]
    ) -> None: ...

    async def create(self, payload: CreateSchema) -> ReturnSchema: ...
    async def read(self, id: RecordIdT) -> ReturnSchema | None: ...
    async def delete(self, id: RecordIdT) -> ReturnSchema | None: ...
    async def execute(self, query: QuerySelect[Model]) -> list[ReturnSchema]: ...
    def apply_sort(
        self,
        query: QuerySelect[Model],
        sort: SortField,
        order: SortOrder,
    ) -> QuerySelect[Model]: ...

    def apply_pagination(
        self,
        query: QuerySelect[Model],
        page: int,
        limit: int,
    ) -> QuerySelect[Model]: ...

    # async def get_record(self, record_id: RecordIdT) -> ReturnRecordT | None:
    #     """Retrieve a record by ID.

    #     Args:
    #         record_id: The ID of the record to retrieve

    #     Returns:
    #         The record if found, None otherwise
    #     """
    #     ...

    # async def update_record(
    #     self, record_id: RecordIdT, payload: RecordT
    # ) -> ReturnRecordT | None:
    #     """Update an existing record.

    #     Args:
    #         record_id: The ID of the record to update
    #         payload: The updated record data

    #     Returns:
    #         The updated record if found, None otherwise
    #     """
    #     ...

    # async def delete_record(self, record_id: RecordIdT) -> ReturnRecordT:
    #     """Delete a record by ID.

    #     Args:
    #         record_id: The ID of the record to delete

    #     Returns:
    #         True if the record was deleted, False if not found
    #     """
    #     ...

    # async def list_records(self) -> List[ReturnRecordT]:
    #     """List all records.

    #     Returns:
    #         A list of all records
    #     """
    #     ...

    # async def record_exists(self, record_id: RecordIdT) -> bool:
    #     """Check if a record exists by ID.

    #     Args:
    #         record_id: The ID of the record to check
    #     """
    #     ...
