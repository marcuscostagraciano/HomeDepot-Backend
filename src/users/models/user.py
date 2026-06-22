from sqlalchemy.orm import Mapped

from core.models import BaseModel


class User(BaseModel):
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
