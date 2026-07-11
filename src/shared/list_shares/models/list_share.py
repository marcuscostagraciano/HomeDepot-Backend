import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import BaseModel
from core.models.user import User
from lists.models.list import List


class ListShare(BaseModel):
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey(User.id), nullable=False
    )
    list_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey(List.id), nullable=False
    )

    __table_args__ = (UniqueConstraint("user_id", "list_id", name="uq_user_list"),)
