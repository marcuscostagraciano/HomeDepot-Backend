import uuid

from sqlalchemy import ForeignKey, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import BaseModel
from lists.models.list import List
from products.models.product import Product


class ListProduct(BaseModel):
    list_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey(List.id), nullable=False
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey(Product.id), nullable=False
    )
    quantity: Mapped[int] = mapped_column(nullable=False)
    bought: Mapped[bool] = mapped_column(default=False, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, default=None)

    __table_args__ = (
        UniqueConstraint("list_id", "product_id", name="uq_list_product"),
    )
