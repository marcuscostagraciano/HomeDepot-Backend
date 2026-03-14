from sqlalchemy.orm import Mapped

from core.models import BaseModel


class Product(BaseModel):
    name: Mapped[str]
    brand: Mapped[str | None]
    description: Mapped[str | None]
    price: Mapped[float | None]
