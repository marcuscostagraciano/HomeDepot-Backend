import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class BaseModel(DeclarativeBase):
    """Base model used by the other `models` in the project.

    It provides a common `UUID` id field and automatically generates the `__tablename__` based on the class name.
    """

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
