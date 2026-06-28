from uuid import UUID

from core.domain import NotFoundError, NotNegativeNumberError, RequiredFieldMissingError

from ..domain import ProductFilters, ProductRepositoryPort
from ..schemas import ProductCreate, ProductRead


async def create_product(
    product: ProductCreate, repository: ProductRepositoryPort
) -> ProductRead:
    if not product.name:
        raise RequiredFieldMissingError("name")

    if product.price is not None and product.price < 0:
        raise NotNegativeNumberError("price", product.price)

    return await repository.create(product)


async def read_product(
    product_id: UUID, repository: ProductRepositoryPort
) -> ProductRead:
    product = await repository.read(product_id)

    if not product:
        raise NotFoundError("Product", str(product_id))

    return product


async def read_products(
    repository: ProductRepositoryPort,
    filters: ProductFilters,
) -> list[ProductRead]:
    return await repository.read_all(filters)
