from dataclasses import asdict, dataclass, replace
from datetime import datetime
from typing import Any, Self
from uuid import UUID


@dataclass(frozen=True)
class DomainSchema:
    def to_dict(self) -> dict[str, Any]:
        """Returns the `dict` representation of said object.

        Returns:
            dict[str, Any]: Dictionary containing the object's information.
        """
        return asdict(self)

    def copy(self, *, update: dict[str, Any] | None = None) -> Self:
        """Returns a copy of said object, optionally updating its attributes.

        Args:
            update (dict[str, Any] | None, optional): Dictionary containing the
                attributes to update in the copied object. Defaults to `None`.

        Returns:
            Self: Copy of said object with the specified updates applied.
        """
        return replace(self, **(update or {}))

    @classmethod
    def from_dict(cls, dict: dict[str, Any]) -> Self:
        """Returns an instance of the class based in the `dict` provided.

        Args:
            dict (dict[str, Any]): Dictionary containing the object to create the instance.

        Returns:
            Self: Instance of said class with the information of the `dict`.
        """
        return cls(**dict)


@dataclass(frozen=True)
class DomainCreateSchema(DomainSchema): ...


@dataclass(frozen=True)
class DomainReadSchema(DomainSchema):
    id: UUID
    created_date: datetime
    updated_date: datetime | None
