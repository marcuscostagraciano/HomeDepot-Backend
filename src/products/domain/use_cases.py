from uuid import UUID

from core.domain.errors import (
    NotFoundError,
    NotNegativeNumberError,
    RequiredFieldMissingError,
)

from ..domain.filters import ProductFilters
from ..domain.ports import ProductRepositoryPort
from ..domain.schemas import Product, ProductCreate


async def create_product(
    repository: ProductRepositoryPort,
    product: ProductCreate,
    user_id: UUID,
) -> Product:
    if not product.name:
        raise RequiredFieldMissingError("name")

    if product.price is not None and product.price < 0:
        raise NotNegativeNumberError("price", product.price)

    return await repository.create(product)


async def read_product(
    repository: ProductRepositoryPort,
    product_id: UUID,
) -> Product:
    product = await repository.read(product_id)

    if not product:
        raise NotFoundError("Product", str(product_id))

    return product


async def read_products(
    repository: ProductRepositoryPort,
    filters: ProductFilters,
) -> list[Product]:
    return await repository.read_all(filters)
