from typing import Any, Self

from pydantic import BaseModel, ConfigDict


class BasePresentation(BaseModel):
    """Base schema used by the other `schemas` in the project.

    Inherently supports conversion from SQLAlchemy ORM models to Pydantic models, making it easier to work with
    database records in endpoints.

    Also provides immutability to ensure that once an instance is created, it cannot be modified.
    """

    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
        use_enum_values=True,
    )

    def to_dict(self) -> dict[str, Any]:
        """Returns the `dict` representation of said object.

        Returns:
            dict[str, Any]: Dictionary containing the object's information.
        """
        return self.model_dump()

    @classmethod
    def from_dict(cls, dict: dict[str, Any]) -> Self:
        """Returns an instance of the class based in the `dict` provided.

        Args:
            dict (dict[str, Any]): Dictionary containing the object to create the instance.

        Returns:
            Self: Instance of said class with the information of the `dict`.
        """
        return cls(**dict)
