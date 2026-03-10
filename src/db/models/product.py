from .base import Base
from sqlalchemy.orm import Mapped


class Product(Base):
    name: Mapped[str]
    brand: Mapped[str | None]
    description: Mapped[str | None]
    price: Mapped[float | None]
