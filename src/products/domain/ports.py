from typing import List, Protocol
from uuid import UUID

from db.domain.ports import RepositoryPort

from ..domain.filters import ProductFilters
from ..domain.schemas import Product, ProductCreate


class ProductRepositoryPort(
    RepositoryPort[
        ProductCreate,
        Product,
        UUID,
    ],
    Protocol,
):
    """Repository protocol for managing product persistence.

    Defines the interface for CRUD operations on products with generic types
    for flexible data and `id` representation.

    In another words, this protocol supplies the interface for the product repository,
    while also defining the types of the data it will handle.
    """

    async def read_all(self, filters: ProductFilters) -> List[Product]: ...
