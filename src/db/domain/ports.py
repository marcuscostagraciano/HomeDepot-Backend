from typing import Protocol

from .types import DomainCreateSchemaT, DomainSchemaT, RecordIdT


class RepositoryPort(Protocol[DomainCreateSchemaT, DomainSchemaT, RecordIdT]):
    """Repository protocol for managing record persistence.

    Defines the interface for CRUD operations on records with generic types
    for flexible data and ID representation.

    Type Parameters:
        RecordT: The record data type
        RecordIdT: The record ID type
        ReturnRecordT: The type of the record returned by create and update operations
    """

    async def create(
        self,
        payload: DomainCreateSchemaT,
    ) -> DomainSchemaT: ...
    async def read(
        self,
        id: RecordIdT,
    ) -> DomainSchemaT | None: ...
    async def delete(
        self,
        id: RecordIdT,
    ) -> DomainSchemaT | None: ...

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
