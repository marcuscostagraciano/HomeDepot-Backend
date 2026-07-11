from typing import TypeVar

from core.domain.schemas import DomainCreateSchema, DomainSchema

DomainCreateSchemaT = TypeVar(
    "DomainCreateSchemaT",
    contravariant=True,
    bound=DomainCreateSchema,
)
DomainSchemaT = TypeVar(
    "DomainSchemaT",
    covariant=True,
    bound=DomainSchema,
)
RecordIdT = TypeVar(
    "RecordIdT",
    contravariant=True,
)
CreatorIdT = TypeVar(
    "CreatorIdT",
    contravariant=True,
)
