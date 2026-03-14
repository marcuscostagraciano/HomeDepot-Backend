from datetime import date

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models import BaseModel


class List(BaseModel):
    observation: Mapped[str | None] = mapped_column(Text)
    bought: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[str] = mapped_column(default=str(date.today()))
    updated_at: Mapped[str | None] = mapped_column(default=None)
    # user_id_create
    # user_id_update
