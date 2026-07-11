from uuid import UUID

from core.domain.errors import NotFoundError, RequiredFieldMissingError

from ..domain.filters import ProductFilters
from ..domain.ports import ProductRepositoryPort
from ..domain.schemas import Product, ProductCreate


async def create_product(
    repository: ProductRepositoryPort,
    product: ProductCreate,
    creator_id: UUID,
) -> Product:
    if not product.name:
        raise RequiredFieldMissingError("name")

    return await repository.create(product, creator_id=creator_id)


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
