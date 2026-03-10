import uuid

from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
