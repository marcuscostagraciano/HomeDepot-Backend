from uuid import UUID

from core.errors import NotFoundError, NotNegativeNumberError, RequiredFieldMissingError
from products.domain import ProductRepositoryPort
from products.schemas import ProductCreate, ProductRead


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


async def read_products(repository: ProductRepositoryPort) -> list[ProductRead]:
    products = await repository.read_all()

    return products
