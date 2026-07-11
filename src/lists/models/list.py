from sqlalchemy.orm import Mapped, mapped_column

from core.models.auditable import AuditableModel


class List(AuditableModel):
    name: Mapped[str]
    observation: Mapped[str | None]
    bought: Mapped[bool] = mapped_column(default=False)
