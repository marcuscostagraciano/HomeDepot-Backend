from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class User(BaseModel):
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str]
