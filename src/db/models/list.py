from .base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy import Text
from sqlalchemy.orm import mapped_column
from datetime import date


class List(Base):
    observation: Mapped[str | None] = mapped_column(Text)
    bought: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[str] = mapped_column(default=str(date.today()))
    updated_at: Mapped[str | None] = mapped_column(default=None)
    # user_id_create
    # user_id_update
