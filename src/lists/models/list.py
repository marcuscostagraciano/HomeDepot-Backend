from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models import BaseModel


class List(BaseModel):
    observation: Mapped[str | None] = mapped_column(Text)
    bought: Mapped[bool] = mapped_column(default=False)
    # user_id_create
    # user_id_update
