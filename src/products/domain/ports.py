from typing import List, Protocol
from uuid import UUID

from db.domain import RepositoryPort

from ..domain import ProductFilters
from ..models import Product
from ..schemas import ProductCreate, ProductRead


class ProductRepositoryPort(
    RepositoryPort[ProductCreate, ProductRead, UUID],
    Protocol,
):
    """Repository protocol for managing product persistence.

    Defines the interface for CRUD operations on products with generic types
    for flexible data and `id` representation.

    In another words, this protocol supplies the interface for the product repository,
    while also defining the types of the data it will handle.
    """
