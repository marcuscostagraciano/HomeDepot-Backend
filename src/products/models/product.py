from sqlalchemy.orm import Mapped

from core.models.auditable import AuditableModel


class Product(AuditableModel):
    name: Mapped[str]
    brand: Mapped[str | None]
    description: Mapped[str | None]
