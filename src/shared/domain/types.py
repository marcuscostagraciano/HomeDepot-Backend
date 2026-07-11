from dataclasses import dataclass
from typing import Self
from uuid import UUID

AssociationId = tuple[UUID, UUID]


@dataclass(frozen=True)
class AssociationIdVO:
    first_id: UUID
    second_id: UUID

    def __iter__(self):
        yield self.first_id
        yield self.second_id

    def __str__(self) -> str:
        return f"{self.first_id}/{self.second_id}"

    @classmethod
    def from_tuple(cls, value: AssociationId) -> Self:
        return cls(value[0], value[1])

    def to_tuple(self) -> AssociationId:
        return (self.first_id, self.second_id)
